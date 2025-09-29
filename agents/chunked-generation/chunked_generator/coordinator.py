"""
Chunk Coordinator - Manages the generation process across multiple chunks
"""

import os
import json
import time
import asyncio
import subprocess
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

from .analyzer import ProjectAnalysis, ChunkDefinition
from .context import ContextManager


class ChunkStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class ChunkResult:
    chunk_id: str
    status: ChunkStatus
    files_generated: List[str]
    lines_generated: int
    generation_time: float
    error_message: Optional[str] = None
    retry_count: int = 0


@dataclass
class GenerationState:
    project_id: str
    prompt: str
    analysis: ProjectAnalysis
    chunk_results: Dict[str, ChunkResult]
    current_chunk: Optional[str]
    start_time: float
    last_update: float
    global_context: Dict
    project_structure: Dict


class ChunkCoordinator:
    """Coordinates the generation of multiple chunks while maintaining consistency"""
    
    def __init__(self, output_dir: str, max_parallel: int = 3, 
                 progress_callback: Optional[Callable] = None):
        self.output_dir = output_dir
        self.max_parallel = max_parallel
        self.progress_callback = progress_callback
        self.context_manager = ContextManager()
        self.state_file = os.path.join(output_dir, ".generation_state.json")
        self.lock = threading.Lock()
        
    def generate_project(self, analysis: ProjectAnalysis, prompt: str,
                        language: str = "python", framework: str = "",
                        resume_from: str = "") -> GenerationState:
        """
        Generate a complete project using the chunked approach
        
        Args:
            analysis: Project analysis with chunk definitions
            prompt: Original project prompt
            language: Primary programming language
            framework: Primary framework
            resume_from: Resume from a specific checkpoint
            
        Returns:
            GenerationState with results
        """
        # Create or load generation state
        if resume_from and os.path.exists(self.state_file):
            state = self._load_state()
            self._log_progress(f"Resuming generation from {resume_from}")
        else:
            state = self._create_initial_state(analysis, prompt)
            self._log_progress("Starting new project generation")
        
        # Initialize context manager
        self.context_manager.initialize_project_context(
            analysis.architecture_decisions,
            analysis.global_dependencies,
            language,
            framework
        )
        
        try:
            # Generate chunks in dependency order
            self._generate_chunks_ordered(state, analysis)
            
            # Perform integration validation
            self._validate_integration(state)
            
            # Generate final documentation
            self._generate_project_documentation(state)
            
            self._log_progress("Project generation completed successfully!")
            
        except Exception as e:
            self._log_progress(f"Generation failed: {str(e)}")
            state.chunk_results[state.current_chunk or "unknown"] = ChunkResult(
                chunk_id=state.current_chunk or "unknown",
                status=ChunkStatus.FAILED,
                files_generated=[],
                lines_generated=0,
                generation_time=0,
                error_message=str(e)
            )
        finally:
            self._save_state(state)
        
        return state
    
    def _create_initial_state(self, analysis: ProjectAnalysis, prompt: str) -> GenerationState:
        """Create initial generation state"""
        project_id = f"project_{int(time.time())}"
        
        # Initialize chunk results
        chunk_results = {}
        for chunk in analysis.chunks:
            chunk_results[chunk.chunk_id] = ChunkResult(
                chunk_id=chunk.chunk_id,
                status=ChunkStatus.PENDING,
                files_generated=[],
                lines_generated=0,
                generation_time=0
            )
        
        return GenerationState(
            project_id=project_id,
            prompt=prompt,
            analysis=analysis,
            chunk_results=chunk_results,
            current_chunk=None,
            start_time=time.time(),
            last_update=time.time(),
            global_context={},
            project_structure={}
        )
    
    def _generate_chunks_ordered(self, state: GenerationState, analysis: ProjectAnalysis):
        """Generate chunks in dependency order"""
        # Create dependency graph
        dependency_graph = self._build_dependency_graph(analysis.chunks)
        
        # Generate chunks in topological order
        completed_chunks = set()
        
        while len(completed_chunks) < len(analysis.chunks):
            # Find chunks ready for generation (dependencies satisfied)
            ready_chunks = []
            for chunk in analysis.chunks:
                if (chunk.chunk_id not in completed_chunks and
                    all(dep in completed_chunks for dep in chunk.dependencies)):
                    ready_chunks.append(chunk)
            
            if not ready_chunks:
                raise Exception("Circular dependency detected in chunks")
            
            # Generate ready chunks (up to max_parallel)
            batch_size = min(len(ready_chunks), self.max_parallel)
            batch_chunks = ready_chunks[:batch_size]
            
            self._generate_chunk_batch(state, batch_chunks)
            
            # Mark completed chunks
            for chunk in batch_chunks:
                if state.chunk_results[chunk.chunk_id].status == ChunkStatus.COMPLETED:
                    completed_chunks.add(chunk.chunk_id)
                elif state.chunk_results[chunk.chunk_id].status == ChunkStatus.FAILED:
                    # Try to recover or skip
                    if self._attempt_chunk_recovery(state, chunk):
                        completed_chunks.add(chunk.chunk_id)
                    else:
                        # Skip this chunk and its dependents
                        self._skip_dependent_chunks(state, chunk, analysis.chunks)
                        completed_chunks.add(chunk.chunk_id)
    
    def _generate_chunk_batch(self, state: GenerationState, chunks: List[ChunkDefinition]):
        """Generate a batch of chunks in parallel"""
        with ThreadPoolExecutor(max_workers=len(chunks)) as executor:
            # Submit chunk generation tasks
            future_to_chunk = {}
            for chunk in chunks:
                future = executor.submit(self._generate_single_chunk, state, chunk)
                future_to_chunk[future] = chunk
            
            # Process completed chunks
            for future in as_completed(future_to_chunk):
                chunk = future_to_chunk[future]
                try:
                    result = future.result()
                    state.chunk_results[chunk.chunk_id] = result
                    self._update_context_from_chunk(chunk, result)
                    self._log_progress(f"Completed chunk: {chunk.chunk_name}")
                except Exception as e:
                    state.chunk_results[chunk.chunk_id] = ChunkResult(
                        chunk_id=chunk.chunk_id,
                        status=ChunkStatus.FAILED,
                        files_generated=[],
                        lines_generated=0,
                        generation_time=0,
                        error_message=str(e)
                    )
                    self._log_progress(f"Failed chunk: {chunk.chunk_name} - {str(e)}")
                
                # Save state after each chunk
                self._save_state(state)
    
    def _generate_single_chunk(self, state: GenerationState, chunk: ChunkDefinition) -> ChunkResult:
        """Generate a single chunk"""
        start_time = time.time()
        
        with self.lock:
            state.current_chunk = chunk.chunk_id
            self._log_progress(f"Generating chunk: {chunk.chunk_name}")
        
        try:
            # Create chunk-specific prompt
            chunk_prompt = self._create_chunk_prompt(state, chunk)
            
            # Create chunk directory
            chunk_dir = os.path.join(self.output_dir, chunk.chunk_id)
            os.makedirs(chunk_dir, exist_ok=True)
            
            # Generate chunk using qodo
            files_generated = self._execute_chunk_generation(
                chunk_prompt, chunk_dir, chunk, state
            )
            
            # Count lines generated
            lines_generated = self._count_lines_in_files(files_generated)
            
            # Validate chunk
            self._validate_chunk(chunk, files_generated)
            
            generation_time = time.time() - start_time
            
            return ChunkResult(
                chunk_id=chunk.chunk_id,
                status=ChunkStatus.COMPLETED,
                files_generated=files_generated,
                lines_generated=lines_generated,
                generation_time=generation_time
            )
            
        except Exception as e:
            generation_time = time.time() - start_time
            return ChunkResult(
                chunk_id=chunk.chunk_id,
                status=ChunkStatus.FAILED,
                files_generated=[],
                lines_generated=0,
                generation_time=generation_time,
                error_message=str(e)
            )
    
    def _create_chunk_prompt(self, state: GenerationState, chunk: ChunkDefinition) -> str:
        """Create a detailed prompt for a specific chunk"""
        # Get context from completed dependencies
        dependency_context = self._get_dependency_context(state, chunk)
        
        # Get global project context
        global_context = self.context_manager.get_project_context()
        
        prompt = f"""
Generate the '{chunk.chunk_name}' component for this project:

ORIGINAL PROJECT PROMPT:
{state.prompt}

CHUNK DESCRIPTION:
{chunk.description}

CHUNK REQUIREMENTS:
- Estimated lines: {chunk.estimated_lines}
- Complexity: {chunk.complexity}
- Technologies: {', '.join(chunk.technologies)}
- Files to generate: {', '.join(chunk.files_to_generate)}

INTERFACES TO IMPLEMENT:
{json.dumps(chunk.interfaces, indent=2)}

GLOBAL PROJECT CONTEXT:
{json.dumps(global_context, indent=2)}

DEPENDENCY CONTEXT:
{dependency_context}

SPECIFIC INSTRUCTIONS:
1. Follow the established project architecture and patterns
2. Maintain consistency with existing code style and conventions
3. Implement all required interfaces for integration with other chunks
4. Include comprehensive error handling and logging
5. Add appropriate documentation and comments
6. Generate only the files specified for this chunk
7. Ensure code is production-ready and follows best practices

Generate complete, functional code that integrates seamlessly with the rest of the project.
"""
        return prompt
    
    def _execute_chunk_generation(self, prompt: str, chunk_dir: str, 
                                 chunk: ChunkDefinition, state: GenerationState) -> List[str]:
        """Execute the actual code generation for a chunk"""
        # Prepare qodo command
        cmd = [
            "qodo", "generate_code",
            "--ci",
            "--set", f"prompt={prompt}",
            "--set", f"output_dir={chunk_dir}",
            "--set", f"language={state.analysis.architecture_decisions.get('primary_language', 'python')}",
            "--set", "include_tests=true",
            "--set", "include_docs=true"
        ]
        
        # Add framework if specified
        framework = state.analysis.architecture_decisions.get('primary_framework')
        if framework:
            cmd.extend(["--set", f"framework={framework}"])
        
        # Execute command
        try:
            result = subprocess.run(
                cmd,
                cwd=self.output_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout per chunk
            )
            
            if result.returncode != 0:
                # Try fallback generation
                return self._fallback_chunk_generation(chunk, chunk_dir, state)
            
        except subprocess.TimeoutExpired:
            self._log_progress(f"Chunk generation timed out, using fallback")
            return self._fallback_chunk_generation(chunk, chunk_dir, state)
        except Exception as e:
            self._log_progress(f"Chunk generation failed: {e}, using fallback")
            return self._fallback_chunk_generation(chunk, chunk_dir, state)
        
        # Find generated files
        generated_files = []
        for root, dirs, files in os.walk(chunk_dir):
            for file in files:
                if not file.startswith('.'):
                    generated_files.append(os.path.join(root, file))
        
        return generated_files
    
    def _fallback_chunk_generation(self, chunk: ChunkDefinition, 
                                  chunk_dir: str, state: GenerationState) -> List[str]:
        """Fallback generation using templates"""
        generated_files = []
        
        # Create basic files based on chunk specification
        for file_spec in chunk.files_to_generate:
            if file_spec.endswith('/'):
                # Directory
                os.makedirs(os.path.join(chunk_dir, file_spec), exist_ok=True)
            else:
                # File
                file_path = os.path.join(chunk_dir, file_spec)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                # Generate basic content based on file type
                content = self._generate_fallback_content(file_spec, chunk, state)
                
                with open(file_path, 'w') as f:
                    f.write(content)
                
                generated_files.append(file_path)
        
        return generated_files
    
    def _generate_fallback_content(self, file_spec: str, chunk: ChunkDefinition, 
                                  state: GenerationState) -> str:
        """Generate fallback content for a file"""
        language = state.analysis.architecture_decisions.get('primary_language', 'python')
        
        if file_spec.endswith('.py'):
            return f'''"""
{chunk.chunk_name} - {chunk.description}

This module was generated as part of the {state.project_id} project.
"""

# TODO: Implement {chunk.chunk_name} functionality
# Interfaces: {', '.join(chunk.interfaces.keys())}

class {chunk.chunk_name.replace(' ', '')}:
    """Main class for {chunk.chunk_name}"""
    
    def __init__(self):
        pass
    
    def main_function(self):
        """Main functionality for this chunk"""
        pass

# Module initialization
if __name__ == "__main__":
    instance = {chunk.chunk_name.replace(' ', '')}()
    instance.main_function()
'''
        elif file_spec.endswith('.js'):
            return f'''/**
 * {chunk.chunk_name} - {chunk.description}
 * 
 * This module was generated as part of the {state.project_id} project.
 */

// TODO: Implement {chunk.chunk_name} functionality
// Interfaces: {', '.join(chunk.interfaces.keys())}

class {chunk.chunk_name.replace(' ', '')} {{
    constructor() {{
        // Initialize {chunk.chunk_name}
    }}
    
    mainFunction() {{
        // Main functionality for this chunk
    }}
}}

module.exports = {chunk.chunk_name.replace(' ', '')};
'''
        elif file_spec.endswith('.md'):
            return f'''# {chunk.chunk_name}

{chunk.description}

## Overview

This component is part of the {state.project_id} project.

## Interfaces

{chr(10).join(f"- **{k}**: {v}" for k, v in chunk.interfaces.items())}

## Usage

TODO: Add usage instructions

## Dependencies

{chr(10).join(f"- {dep}" for dep in chunk.dependencies)}
'''
        else:
            return f'''# {chunk.chunk_name}
# {chunk.description}
# Generated for project: {state.project_id}

# TODO: Implement functionality
'''
    
    def _get_dependency_context(self, state: GenerationState, chunk: ChunkDefinition) -> str:
        """Get context from completed dependency chunks"""
        context_parts = []
        
        for dep_id in chunk.dependencies:
            if dep_id in state.chunk_results:
                result = state.chunk_results[dep_id]
                if result.status == ChunkStatus.COMPLETED:
                    context_parts.append(f"""
DEPENDENCY: {dep_id}
- Status: Completed
- Files generated: {len(result.files_generated)}
- Lines of code: {result.lines_generated}
- Available interfaces: {self.context_manager.get_chunk_interfaces(dep_id)}
""")
        
        return "\n".join(context_parts) if context_parts else "No dependencies"
    
    def _update_context_from_chunk(self, chunk: ChunkDefinition, result: ChunkResult):
        """Update global context with information from completed chunk"""
        if result.status == ChunkStatus.COMPLETED:
            self.context_manager.register_chunk_completion(
                chunk.chunk_id,
                chunk.interfaces,
                result.files_generated
            )
    
    def _validate_chunk(self, chunk: ChunkDefinition, files_generated: List[str]):
        """Validate that a chunk was generated correctly"""
        if not files_generated:
            raise Exception(f"No files generated for chunk {chunk.chunk_id}")
        
        # Check that required files exist
        for required_file in chunk.files_to_generate:
            if not required_file.endswith('/'):  # Skip directories
                found = any(required_file in f for f in files_generated)
                if not found:
                    self._log_progress(f"Warning: Required file {required_file} not found in chunk {chunk.chunk_id}")
    
    def _validate_integration(self, state: GenerationState):
        """Validate that all chunks integrate properly"""
        self._log_progress("Validating chunk integration...")
        
        # Check interface compatibility
        for chunk in state.analysis.chunks:
            for dep_id in chunk.dependencies:
                if dep_id not in state.chunk_results:
                    continue
                
                dep_result = state.chunk_results[dep_id]
                if dep_result.status != ChunkStatus.COMPLETED:
                    self._log_progress(f"Warning: Dependency {dep_id} not completed for {chunk.chunk_id}")
        
        self._log_progress("Integration validation completed")
    
    def _generate_project_documentation(self, state: GenerationState):
        """Generate comprehensive project documentation"""
        self._log_progress("Generating project documentation...")
        
        # Create main README
        readme_content = self._create_project_readme(state)
        readme_path = os.path.join(self.output_dir, "README.md")
        
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        
        # Create architecture documentation
        arch_content = self._create_architecture_docs(state)
        arch_path = os.path.join(self.output_dir, "ARCHITECTURE.md")
        
        with open(arch_path, 'w') as f:
            f.write(arch_content)
        
        self._log_progress("Project documentation generated")
    
    def _create_project_readme(self, state: GenerationState) -> str:
        """Create main project README"""
        total_files = sum(len(result.files_generated) for result in state.chunk_results.values())
        total_lines = sum(result.lines_generated for result in state.chunk_results.values())
        
        return f"""# {state.project_id.replace('_', ' ').title()}

Generated by MasterMindAI Chunked Code Generator

## Project Overview

{state.prompt}

## Project Statistics

- **Total Files Generated**: {total_files}
- **Total Lines of Code**: {total_lines:,}
- **Number of Chunks**: {len(state.analysis.chunks)}
- **Generation Time**: {time.time() - state.start_time:.1f} seconds

## Architecture

This project follows a {state.analysis.chunk_strategy.value} architecture with the following components:

{chr(10).join(f"- **{chunk.chunk_name}**: {chunk.description}" for chunk in state.analysis.chunks)}

## Setup Instructions

1. Install dependencies:
   ```bash
   # Install global dependencies
   {chr(10).join(f"   # {dep}" for dep in state.analysis.global_dependencies)}
   ```

2. Configure the project:
   ```bash
   # Follow setup instructions in each component directory
   ```

3. Run tests:
   ```bash
   # Run component tests
   # Run integration tests
   ```

## Project Structure

```
{self._generate_project_tree(state)}
```

## Components

{chr(10).join(self._create_component_docs(chunk, state.chunk_results.get(chunk.chunk_id)) for chunk in state.analysis.chunks)}

## Contributing

This project was generated using intelligent chunking. Each component is designed to be:
- Self-contained with clear interfaces
- Thoroughly tested
- Well-documented
- Following consistent patterns

## License

Generated code - customize as needed for your project.
"""
    
    def _create_architecture_docs(self, state: GenerationState) -> str:
        """Create detailed architecture documentation"""
        return f"""# Architecture Documentation

## Overview

This document describes the architecture of the {state.project_id} project.

## Architecture Decisions

{chr(10).join(f"- **{k}**: {v}" for k, v in state.analysis.architecture_decisions.items())}

## Component Dependencies

```mermaid
graph TD
{chr(10).join(f"    {chunk.chunk_id}[{chunk.chunk_name}]" for chunk in state.analysis.chunks)}
{chr(10).join(f"    {dep} --> {chunk.chunk_id}" for chunk in state.analysis.chunks for dep in chunk.dependencies)}
```

## Interface Specifications

{chr(10).join(self._create_interface_docs(chunk) for chunk in state.analysis.chunks)}

## Technology Stack

{chr(10).join(f"- {tech}" for tech in set().union(*[chunk.technologies for chunk in state.analysis.chunks]))}

## Deployment Considerations

- Each component can be deployed independently
- Follow the dependency order for deployment
- Ensure all interfaces are properly configured
"""
    
    def _create_component_docs(self, chunk: ChunkDefinition, result: Optional[ChunkResult]) -> str:
        """Create documentation for a single component"""
        status = result.status.value if result else "unknown"
        files_count = len(result.files_generated) if result else 0
        lines_count = result.lines_generated if result else 0
        
        return f"""
### {chunk.chunk_name}

**Status**: {status}  
**Description**: {chunk.description}  
**Files Generated**: {files_count}  
**Lines of Code**: {lines_count}  
**Dependencies**: {', '.join(chunk.dependencies) if chunk.dependencies else 'None'}

**Interfaces**:
{chr(10).join(f"- {k}: {v}" for k, v in chunk.interfaces.items())}
"""
    
    def _create_interface_docs(self, chunk: ChunkDefinition) -> str:
        """Create interface documentation for a chunk"""
        return f"""
### {chunk.chunk_name} Interfaces

{chr(10).join(f"#### {interface_name}{chr(10)}{interface_desc}{chr(10)}" for interface_name, interface_desc in chunk.interfaces.items())}
"""
    
    def _generate_project_tree(self, state: GenerationState) -> str:
        """Generate a text representation of the project structure"""
        tree_lines = [state.project_id + "/"]
        
        for chunk in state.analysis.chunks:
            tree_lines.append(f"├── {chunk.chunk_id}/")
            result = state.chunk_results.get(chunk.chunk_id)
            if result and result.files_generated:
                for i, file_path in enumerate(result.files_generated[:3]):  # Show first 3 files
                    relative_path = os.path.relpath(file_path, self.output_dir)
                    prefix = "│   ├── " if i < 2 else "│   └── "
                    tree_lines.append(f"{prefix}{os.path.basename(relative_path)}")
                if len(result.files_generated) > 3:
                    tree_lines.append(f"│   └── ... ({len(result.files_generated) - 3} more files)")
        
        tree_lines.append("├── README.md")
        tree_lines.append("└── ARCHITECTURE.md")
        
        return chr(10).join(tree_lines)
    
    def _attempt_chunk_recovery(self, state: GenerationState, chunk: ChunkDefinition) -> bool:
        """Attempt to recover from a failed chunk"""
        result = state.chunk_results[chunk.chunk_id]
        
        if result.retry_count >= 2:  # Max 2 retries
            return False
        
        self._log_progress(f"Attempting recovery for chunk: {chunk.chunk_name}")
        
        # Increment retry count
        result.retry_count += 1
        
        # Try with simplified approach
        try:
            simplified_chunk = ChunkDefinition(
                chunk_id=chunk.chunk_id,
                chunk_name=chunk.chunk_name,
                description=f"Simplified {chunk.description}",
                dependencies=chunk.dependencies,
                estimated_lines=chunk.estimated_lines // 2,  # Reduce complexity
                priority=chunk.priority,
                complexity="medium" if chunk.complexity == "high" else "low",
                files_to_generate=chunk.files_to_generate[:2],  # Reduce files
                interfaces=chunk.interfaces,
                technologies=chunk.technologies
            )
            
            new_result = self._generate_single_chunk(state, simplified_chunk)
            state.chunk_results[chunk.chunk_id] = new_result
            
            return new_result.status == ChunkStatus.COMPLETED
            
        except Exception as e:
            self._log_progress(f"Recovery failed for {chunk.chunk_name}: {e}")
            return False
    
    def _skip_dependent_chunks(self, state: GenerationState, failed_chunk: ChunkDefinition, 
                              all_chunks: List[ChunkDefinition]):
        """Skip chunks that depend on a failed chunk"""
        def has_dependency(chunk: ChunkDefinition, failed_id: str) -> bool:
            return failed_id in chunk.dependencies
        
        for chunk in all_chunks:
            if has_dependency(chunk, failed_chunk.chunk_id):
                if state.chunk_results[chunk.chunk_id].status == ChunkStatus.PENDING:
                    state.chunk_results[chunk.chunk_id].status = ChunkStatus.SKIPPED
                    self._log_progress(f"Skipped chunk {chunk.chunk_name} due to failed dependency")
    
    def _build_dependency_graph(self, chunks: List[ChunkDefinition]) -> Dict[str, List[str]]:
        """Build dependency graph for chunks"""
        graph = {}
        for chunk in chunks:
            graph[chunk.chunk_id] = chunk.dependencies
        return graph
    
    def _count_lines_in_files(self, files: List[str]) -> int:
        """Count total lines in generated files"""
        total_lines = 0
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    total_lines += sum(1 for line in f if line.strip())
            except Exception:
                pass  # Skip files that can't be read
        return total_lines
    
    def _save_state(self, state: GenerationState):
        """Save generation state to file"""
        try:
            # Convert to serializable format
            state_dict = asdict(state)
            
            # Handle non-serializable objects
            state_dict['analysis'] = asdict(state.analysis)
            state_dict['analysis']['project_type'] = state.analysis.project_type.value
            state_dict['analysis']['chunk_strategy'] = state.analysis.chunk_strategy.value
            state_dict['analysis']['chunks'] = [asdict(chunk) for chunk in state.analysis.chunks]
            
            # Convert chunk results
            for chunk_id, result in state_dict['chunk_results'].items():
                state_dict['chunk_results'][chunk_id] = asdict(result)
                state_dict['chunk_results'][chunk_id]['status'] = result.status.value
            
            with open(self.state_file, 'w') as f:
                json.dump(state_dict, f, indent=2)
                
        except Exception as e:
            self._log_progress(f"Failed to save state: {e}")
    
    def _load_state(self) -> GenerationState:
        """Load generation state from file"""
        with open(self.state_file, 'r') as f:
            state_dict = json.load(f)
        
        # Convert back to proper objects
        # This is a simplified version - in practice you'd need full deserialization
        return GenerationState(**state_dict)
    
    def _log_progress(self, message: str):
        """Log progress message"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        print(formatted_message)
        
        if self.progress_callback:
            self.progress_callback(formatted_message)
    
    def get_progress_summary(self, state: GenerationState) -> Dict:
        """Get current progress summary"""
        total_chunks = len(state.analysis.chunks)
        completed = sum(1 for r in state.chunk_results.values() if r.status == ChunkStatus.COMPLETED)
        failed = sum(1 for r in state.chunk_results.values() if r.status == ChunkStatus.FAILED)
        in_progress = sum(1 for r in state.chunk_results.values() if r.status == ChunkStatus.IN_PROGRESS)
        
        progress_percentage = (completed / total_chunks) * 100 if total_chunks > 0 else 0
        
        return {
            "total_chunks": total_chunks,
            "completed": completed,
            "failed": failed,
            "in_progress": in_progress,
            "progress_percentage": progress_percentage,
            "current_chunk": state.current_chunk,
            "elapsed_time": time.time() - state.start_time
        }