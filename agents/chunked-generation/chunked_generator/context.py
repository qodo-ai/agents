"""
Context Manager - Maintains consistency and context across chunks
"""

import json
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class ProjectContext:
    """Global project context shared across all chunks"""
    architecture_decisions: Dict[str, str]
    global_dependencies: List[str]
    primary_language: str
    primary_framework: str
    coding_standards: Dict[str, str]
    naming_conventions: Dict[str, str]
    project_patterns: Dict[str, str]
    created_at: str
    last_updated: str


@dataclass
class ChunkInterface:
    """Interface definition for a chunk"""
    chunk_id: str
    interface_name: str
    interface_type: str  # "class", "function", "api", "module"
    description: str
    parameters: Dict[str, str]
    return_type: str
    dependencies: List[str]
    file_location: str


@dataclass
class ComponentRegistry:
    """Registry of generated components and their interfaces"""
    chunk_id: str
    chunk_name: str
    files_generated: List[str]
    interfaces_provided: List[ChunkInterface]
    interfaces_required: List[str]
    completion_time: str
    status: str


class ContextManager:
    """Manages global context and ensures consistency across chunks"""
    
    def __init__(self, context_file: str = ".project_context.json"):
        self.context_file = context_file
        self.project_context: Optional[ProjectContext] = None
        self.component_registry: Dict[str, ComponentRegistry] = {}
        self.interface_registry: Dict[str, ChunkInterface] = {}
        self.pattern_library: Dict[str, str] = {}
        
    def initialize_project_context(self, architecture_decisions: Dict[str, str],
                                 global_dependencies: List[str],
                                 primary_language: str,
                                 primary_framework: str):
        """Initialize the global project context"""
        
        # Determine coding standards based on language
        coding_standards = self._get_coding_standards(primary_language)
        
        # Determine naming conventions
        naming_conventions = self._get_naming_conventions(primary_language)
        
        # Determine project patterns
        project_patterns = self._get_project_patterns(primary_language, primary_framework)
        
        self.project_context = ProjectContext(
            architecture_decisions=architecture_decisions,
            global_dependencies=global_dependencies,
            primary_language=primary_language,
            primary_framework=primary_framework,
            coding_standards=coding_standards,
            naming_conventions=naming_conventions,
            project_patterns=project_patterns,
            created_at=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat()
        )
        
        self._save_context()
    
    def get_project_context(self) -> Dict[str, Any]:
        """Get the current project context"""
        if not self.project_context:
            return {}
        
        return asdict(self.project_context)
    
    def register_chunk_completion(self, chunk_id: str, interfaces: Dict[str, str],
                                files_generated: List[str]):
        """Register a completed chunk and its interfaces"""
        
        # Create interface objects
        chunk_interfaces = []
        for interface_name, description in interfaces.items():
            interface = ChunkInterface(
                chunk_id=chunk_id,
                interface_name=interface_name,
                interface_type=self._infer_interface_type(interface_name, description),
                description=description,
                parameters={},  # Would be populated by analyzing generated code
                return_type="",  # Would be populated by analyzing generated code
                dependencies=[],  # Would be populated by analyzing generated code
                file_location=""  # Would be populated by analyzing generated files
            )
            chunk_interfaces.append(interface)
            self.interface_registry[f"{chunk_id}.{interface_name}"] = interface
        
        # Register component
        component = ComponentRegistry(
            chunk_id=chunk_id,
            chunk_name=chunk_id.replace('_', ' ').title(),
            files_generated=files_generated,
            interfaces_provided=chunk_interfaces,
            interfaces_required=[],  # Would be populated by analyzing dependencies
            completion_time=datetime.now().isoformat(),
            status="completed"
        )
        
        self.component_registry[chunk_id] = component
        
        # Update project context
        if self.project_context:
            self.project_context.last_updated = datetime.now().isoformat()
        
        self._save_context()
    
    def get_chunk_interfaces(self, chunk_id: str) -> Dict[str, str]:
        """Get interfaces provided by a specific chunk"""
        if chunk_id not in self.component_registry:
            return {}
        
        component = self.component_registry[chunk_id]
        return {
            interface.interface_name: interface.description
            for interface in component.interfaces_provided
        }
    
    def get_available_interfaces(self) -> Dict[str, ChunkInterface]:
        """Get all available interfaces from completed chunks"""
        return self.interface_registry.copy()
    
    def get_coding_standards_for_chunk(self, chunk_id: str) -> Dict[str, str]:
        """Get coding standards that should be applied to a specific chunk"""
        if not self.project_context:
            return {}
        
        standards = self.project_context.coding_standards.copy()
        
        # Add chunk-specific standards if needed
        if chunk_id.startswith("api_"):
            standards.update({
                "api_versioning": "Use semantic versioning",
                "error_handling": "Return structured error responses",
                "documentation": "Include OpenAPI/Swagger documentation"
            })
        elif chunk_id.startswith("database_"):
            standards.update({
                "migrations": "Use database migrations for schema changes",
                "indexing": "Add appropriate database indexes",
                "constraints": "Use database constraints for data integrity"
            })
        elif chunk_id.startswith("frontend_"):
            standards.update({
                "accessibility": "Follow WCAG 2.1 guidelines",
                "responsive": "Implement responsive design",
                "performance": "Optimize for Core Web Vitals"
            })
        
        return standards
    
    def get_naming_conventions_for_chunk(self, chunk_id: str) -> Dict[str, str]:
        """Get naming conventions for a specific chunk"""
        if not self.project_context:
            return {}
        
        return self.project_context.naming_conventions.copy()
    
    def get_integration_requirements(self, chunk_id: str, 
                                   dependencies: List[str]) -> Dict[str, Any]:
        """Get integration requirements for a chunk based on its dependencies"""
        requirements = {
            "required_interfaces": [],
            "configuration_needed": [],
            "initialization_order": [],
            "error_handling": []
        }
        
        for dep_id in dependencies:
            if dep_id in self.component_registry:
                component = self.component_registry[dep_id]
                
                # Add required interfaces
                for interface in component.interfaces_provided:
                    requirements["required_interfaces"].append({
                        "interface": f"{dep_id}.{interface.interface_name}",
                        "description": interface.description,
                        "type": interface.interface_type
                    })
                
                # Add configuration requirements
                requirements["configuration_needed"].append(f"Configure {dep_id} connection")
                
                # Add to initialization order
                requirements["initialization_order"].append(dep_id)
        
        return requirements
    
    def validate_chunk_consistency(self, chunk_id: str, 
                                 generated_files: List[str]) -> List[str]:
        """Validate that a chunk follows project consistency rules"""
        issues = []
        
        if not self.project_context:
            return ["Project context not initialized"]
        
        # Check file naming conventions
        naming_issues = self._validate_file_naming(generated_files)
        issues.extend(naming_issues)
        
        # Check coding standards (would require code analysis)
        # This is a placeholder for more sophisticated analysis
        
        return issues
    
    def get_chunk_template_context(self, chunk_id: str) -> Dict[str, Any]:
        """Get template context for generating a specific chunk"""
        if not self.project_context:
            return {}
        
        context = {
            "project_context": asdict(self.project_context),
            "available_interfaces": {
                name: asdict(interface) 
                for name, interface in self.interface_registry.items()
            },
            "coding_standards": self.get_coding_standards_for_chunk(chunk_id),
            "naming_conventions": self.get_naming_conventions_for_chunk(chunk_id),
            "patterns": self._get_relevant_patterns(chunk_id)
        }
        
        return context
    
    def add_pattern(self, pattern_name: str, pattern_code: str, 
                   description: str = ""):
        """Add a reusable pattern to the pattern library"""
        self.pattern_library[pattern_name] = {
            "code": pattern_code,
            "description": description,
            "added_at": datetime.now().isoformat()
        }
        self._save_context()
    
    def get_pattern(self, pattern_name: str) -> Optional[Dict[str, str]]:
        """Get a specific pattern from the library"""
        return self.pattern_library.get(pattern_name)
    
    def _get_coding_standards(self, language: str) -> Dict[str, str]:
        """Get coding standards for a specific language"""
        standards = {
            "python": {
                "style_guide": "PEP 8",
                "docstring_format": "Google style docstrings",
                "type_hints": "Use type hints for all functions",
                "imports": "Use absolute imports, group imports",
                "line_length": "88 characters (Black formatter)",
                "error_handling": "Use specific exception types",
                "logging": "Use structured logging with appropriate levels"
            },
            "javascript": {
                "style_guide": "Airbnb JavaScript Style Guide",
                "documentation": "JSDoc comments for functions",
                "modules": "Use ES6 modules",
                "async": "Use async/await over promises",
                "error_handling": "Use try/catch blocks",
                "naming": "camelCase for variables, PascalCase for classes"
            },
            "java": {
                "style_guide": "Google Java Style Guide",
                "documentation": "Javadoc for public methods",
                "packages": "Use reverse domain naming",
                "exceptions": "Use checked exceptions appropriately",
                "generics": "Use generics for type safety",
                "naming": "camelCase for methods, PascalCase for classes"
            }
        }
        
        return standards.get(language, {
            "style_guide": "Follow language best practices",
            "documentation": "Document all public interfaces",
            "error_handling": "Handle errors gracefully",
            "testing": "Include unit tests"
        })
    
    def _get_naming_conventions(self, language: str) -> Dict[str, str]:
        """Get naming conventions for a specific language"""
        conventions = {
            "python": {
                "variables": "snake_case",
                "functions": "snake_case",
                "classes": "PascalCase",
                "constants": "UPPER_SNAKE_CASE",
                "modules": "snake_case",
                "packages": "lowercase"
            },
            "javascript": {
                "variables": "camelCase",
                "functions": "camelCase",
                "classes": "PascalCase",
                "constants": "UPPER_SNAKE_CASE",
                "files": "camelCase or kebab-case"
            },
            "java": {
                "variables": "camelCase",
                "methods": "camelCase",
                "classes": "PascalCase",
                "constants": "UPPER_SNAKE_CASE",
                "packages": "lowercase.with.dots"
            }
        }
        
        return conventions.get(language, {
            "variables": "Follow language conventions",
            "functions": "Follow language conventions",
            "classes": "Follow language conventions"
        })
    
    def _get_project_patterns(self, language: str, framework: str) -> Dict[str, str]:
        """Get common project patterns for language/framework combination"""
        patterns = {}
        
        if language == "python":
            patterns.update({
                "error_handling": "Use custom exception classes",
                "configuration": "Use environment variables with defaults",
                "logging": "Use structured logging with correlation IDs",
                "testing": "Use pytest with fixtures"
            })
            
            if framework == "flask":
                patterns.update({
                    "app_structure": "Use application factory pattern",
                    "blueprints": "Organize routes with blueprints",
                    "database": "Use SQLAlchemy with migrations"
                })
            elif framework == "django":
                patterns.update({
                    "apps": "Create focused Django apps",
                    "models": "Use Django ORM best practices",
                    "views": "Use class-based views"
                })
        
        elif language == "javascript":
            patterns.update({
                "modules": "Use ES6 modules",
                "async": "Use async/await",
                "error_handling": "Use Error objects with stack traces"
            })
            
            if framework == "react":
                patterns.update({
                    "components": "Use functional components with hooks",
                    "state": "Use Context API or Redux for global state",
                    "styling": "Use CSS modules or styled-components"
                })
            elif framework == "express":
                patterns.update({
                    "middleware": "Use middleware for cross-cutting concerns",
                    "routes": "Organize routes in separate modules",
                    "validation": "Use schema validation middleware"
                })
        
        return patterns
    
    def _infer_interface_type(self, interface_name: str, description: str) -> str:
        """Infer the type of interface based on name and description"""
        name_lower = interface_name.lower()
        desc_lower = description.lower()
        
        if "api" in name_lower or "endpoint" in desc_lower:
            return "api"
        elif "class" in desc_lower or name_lower.endswith("class"):
            return "class"
        elif "function" in desc_lower or "method" in desc_lower:
            return "function"
        elif "module" in desc_lower or "package" in desc_lower:
            return "module"
        else:
            return "interface"
    
    def _validate_file_naming(self, files: List[str]) -> List[str]:
        """Validate file naming conventions"""
        issues = []
        
        if not self.project_context:
            return issues
        
        conventions = self.project_context.naming_conventions
        language = self.project_context.primary_language
        
        for file_path in files:
            filename = os.path.basename(file_path)
            name_without_ext = os.path.splitext(filename)[0]
            
            # Check based on language conventions
            if language == "python":
                if not self._is_snake_case(name_without_ext) and not filename.startswith('.'):
                    issues.append(f"File {filename} should use snake_case naming")
            elif language == "javascript":
                if not (self._is_camel_case(name_without_ext) or self._is_kebab_case(name_without_ext)):
                    issues.append(f"File {filename} should use camelCase or kebab-case naming")
        
        return issues
    
    def _is_snake_case(self, name: str) -> bool:
        """Check if name follows snake_case convention"""
        return name.islower() and '_' in name or name.islower()
    
    def _is_camel_case(self, name: str) -> bool:
        """Check if name follows camelCase convention"""
        return name[0].islower() and any(c.isupper() for c in name[1:])
    
    def _is_kebab_case(self, name: str) -> bool:
        """Check if name follows kebab-case convention"""
        return name.islower() and '-' in name
    
    def _get_relevant_patterns(self, chunk_id: str) -> Dict[str, Any]:
        """Get patterns relevant to a specific chunk"""
        relevant_patterns = {}
        
        # Filter patterns based on chunk type
        for pattern_name, pattern_data in self.pattern_library.items():
            if self._is_pattern_relevant(pattern_name, chunk_id):
                relevant_patterns[pattern_name] = pattern_data
        
        return relevant_patterns
    
    def _is_pattern_relevant(self, pattern_name: str, chunk_id: str) -> bool:
        """Check if a pattern is relevant to a specific chunk"""
        pattern_lower = pattern_name.lower()
        chunk_lower = chunk_id.lower()
        
        # Simple relevance matching - could be more sophisticated
        if "api" in pattern_lower and "api" in chunk_lower:
            return True
        elif "database" in pattern_lower and "database" in chunk_lower:
            return True
        elif "frontend" in pattern_lower and "frontend" in chunk_lower:
            return True
        elif "test" in pattern_lower and "test" in chunk_lower:
            return True
        
        return False
    
    def _save_context(self):
        """Save context to file"""
        try:
            context_data = {
                "project_context": asdict(self.project_context) if self.project_context else None,
                "component_registry": {
                    k: asdict(v) for k, v in self.component_registry.items()
                },
                "interface_registry": {
                    k: asdict(v) for k, v in self.interface_registry.items()
                },
                "pattern_library": self.pattern_library
            }
            
            with open(self.context_file, 'w') as f:
                json.dump(context_data, f, indent=2)
                
        except Exception as e:
            print(f"Failed to save context: {e}")
    
    def load_context(self):
        """Load context from file"""
        try:
            if os.path.exists(self.context_file):
                with open(self.context_file, 'r') as f:
                    context_data = json.load(f)
                
                # Reconstruct objects
                if context_data.get("project_context"):
                    self.project_context = ProjectContext(**context_data["project_context"])
                
                # Reconstruct component registry
                for chunk_id, component_data in context_data.get("component_registry", {}).items():
                    # Convert interfaces back to objects
                    interfaces = [ChunkInterface(**iface) for iface in component_data["interfaces_provided"]]
                    component_data["interfaces_provided"] = interfaces
                    self.component_registry[chunk_id] = ComponentRegistry(**component_data)
                
                # Reconstruct interface registry
                for interface_name, interface_data in context_data.get("interface_registry", {}).items():
                    self.interface_registry[interface_name] = ChunkInterface(**interface_data)
                
                # Load pattern library
                self.pattern_library = context_data.get("pattern_library", {})
                
        except Exception as e:
            print(f"Failed to load context: {e}")
    
    def get_context_summary(self) -> Dict[str, Any]:
        """Get a summary of the current context"""
        return {
            "project_initialized": self.project_context is not None,
            "completed_chunks": len(self.component_registry),
            "available_interfaces": len(self.interface_registry),
            "patterns_available": len(self.pattern_library),
            "primary_language": self.project_context.primary_language if self.project_context else None,
            "primary_framework": self.project_context.primary_framework if self.project_context else None
        }