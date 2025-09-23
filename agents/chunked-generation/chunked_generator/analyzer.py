"""
Project Analyzer - Intelligent analysis and chunking of large-scale project requirements
"""

import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class ProjectType(Enum):
    WEB_APPLICATION = "web_application"
    MACHINE_LEARNING = "machine_learning"
    ENTERPRISE_SOFTWARE = "enterprise_software"
    GAME_DEVELOPMENT = "game_development"
    MICROSERVICES = "microservices"
    DATA_PLATFORM = "data_platform"
    MOBILE_APPLICATION = "mobile_application"
    DESKTOP_APPLICATION = "desktop_application"


class ChunkStrategy(Enum):
    MODULAR = "modular"      # By functional modules
    LAYERED = "layered"      # By architectural layers
    FEATURE = "feature"      # By user features
    DOMAIN = "domain"        # By business domains


@dataclass
class ChunkDefinition:
    chunk_id: str
    chunk_name: str
    description: str
    dependencies: List[str]
    estimated_lines: int
    priority: int
    complexity: str
    files_to_generate: List[str]
    interfaces: Dict[str, str]
    technologies: List[str]


@dataclass
class ProjectAnalysis:
    project_type: ProjectType
    estimated_total_lines: int
    complexity_score: int
    chunk_strategy: ChunkStrategy
    chunks: List[ChunkDefinition]
    global_dependencies: List[str]
    architecture_decisions: Dict[str, str]
    estimated_duration: str


class ProjectAnalyzer:
    """Analyzes project requirements and creates intelligent chunking strategies"""
    
    def __init__(self):
        self.project_patterns = self._load_project_patterns()
        self.technology_mappings = self._load_technology_mappings()
        
    def analyze_project(self, prompt: str, language: str = "python", 
                       framework: str = "", max_chunk_size: int = 2000,
                       chunk_strategy: str = "modular") -> ProjectAnalysis:
        """
        Analyze a project prompt and create a chunking strategy
        
        Args:
            prompt: The project description
            language: Primary programming language
            framework: Primary framework
            max_chunk_size: Maximum lines per chunk
            chunk_strategy: Strategy for chunking
            
        Returns:
            ProjectAnalysis with detailed chunking plan
        """
        # Determine project type
        project_type = self._identify_project_type(prompt)
        
        # Estimate complexity and size
        complexity_score = self._estimate_complexity(prompt)
        estimated_lines = self._estimate_total_lines(prompt, complexity_score)
        
        # Create chunking strategy
        strategy = ChunkStrategy(chunk_strategy)
        chunks = self._create_chunks(prompt, project_type, strategy, language, 
                                   framework, max_chunk_size, estimated_lines)
        
        # Identify global dependencies
        global_deps = self._identify_global_dependencies(prompt, language, framework)
        
        # Make architecture decisions
        arch_decisions = self._make_architecture_decisions(prompt, project_type, 
                                                         language, framework)
        
        # Estimate duration
        duration = self._estimate_duration(estimated_lines, complexity_score, len(chunks))
        
        return ProjectAnalysis(
            project_type=project_type,
            estimated_total_lines=estimated_lines,
            complexity_score=complexity_score,
            chunk_strategy=strategy,
            chunks=chunks,
            global_dependencies=global_deps,
            architecture_decisions=arch_decisions,
            estimated_duration=duration
        )
    
    def _identify_project_type(self, prompt: str) -> ProjectType:
        """Identify the type of project based on the prompt"""
        prompt_lower = prompt.lower()
        
        # Web application indicators
        if any(term in prompt_lower for term in [
            'web app', 'website', 'web application', 'api', 'rest', 'graphql',
            'frontend', 'backend', 'full stack', 'web service', 'web platform'
        ]):
            return ProjectType.WEB_APPLICATION
            
        # Machine learning indicators
        if any(term in prompt_lower for term in [
            'machine learning', 'ml', 'ai', 'neural network', 'deep learning',
            'data science', 'model', 'training', 'prediction', 'classification',
            'regression', 'nlp', 'computer vision', 'tensorflow', 'pytorch'
        ]):
            return ProjectType.MACHINE_LEARNING
            
        # Game development indicators
        if any(term in prompt_lower for term in [
            'game', 'gaming', 'unity', 'unreal', 'pygame', 'game engine',
            'graphics', 'rendering', 'physics', 'gameplay', '2d', '3d'
        ]):
            return ProjectType.GAME_DEVELOPMENT
            
        # Microservices indicators
        if any(term in prompt_lower for term in [
            'microservice', 'microservices', 'distributed', 'service mesh',
            'kubernetes', 'docker', 'containerized', 'scalable architecture'
        ]):
            return ProjectType.MICROSERVICES
            
        # Data platform indicators
        if any(term in prompt_lower for term in [
            'data platform', 'data pipeline', 'etl', 'data warehouse',
            'analytics', 'big data', 'data processing', 'streaming'
        ]):
            return ProjectType.DATA_PLATFORM
            
        # Mobile application indicators
        if any(term in prompt_lower for term in [
            'mobile app', 'android', 'ios', 'react native', 'flutter',
            'mobile application', 'smartphone', 'tablet'
        ]):
            return ProjectType.MOBILE_APPLICATION
            
        # Desktop application indicators
        if any(term in prompt_lower for term in [
            'desktop app', 'desktop application', 'gui', 'tkinter',
            'qt', 'electron', 'native app', 'windows app', 'mac app'
        ]):
            return ProjectType.DESKTOP_APPLICATION
            
        # Default to enterprise software
        return ProjectType.ENTERPRISE_SOFTWARE
    
    def _estimate_complexity(self, prompt: str) -> int:
        """Estimate project complexity on a scale of 1-10"""
        complexity_indicators = {
            'simple': ['simple', 'basic', 'minimal', 'quick', 'small'],
            'medium': ['medium', 'standard', 'typical', 'moderate'],
            'complex': ['complex', 'advanced', 'enterprise', 'large', 'comprehensive'],
            'very_complex': ['massive', 'huge', 'extensive', 'full-featured', 'complete']
        }
        
        prompt_lower = prompt.lower()
        score = 5  # Default medium complexity
        
        # Check for complexity indicators
        if any(term in prompt_lower for term in complexity_indicators['simple']):
            score = max(score - 2, 1)
        elif any(term in prompt_lower for term in complexity_indicators['complex']):
            score = min(score + 2, 8)
        elif any(term in prompt_lower for term in complexity_indicators['very_complex']):
            score = min(score + 4, 10)
            
        # Adjust based on feature count
        feature_count = len(re.findall(r'\b(?:feature|function|capability|module|component)\b', prompt_lower))
        if feature_count > 10:
            score = min(score + 2, 10)
        elif feature_count > 5:
            score = min(score + 1, 10)
            
        # Adjust based on technology stack complexity
        complex_tech = ['kubernetes', 'microservices', 'machine learning', 'blockchain', 'ai']
        if any(tech in prompt_lower for tech in complex_tech):
            score = min(score + 1, 10)
            
        return score
    
    def _estimate_total_lines(self, prompt: str, complexity_score: int) -> int:
        """Estimate total lines of code for the project"""
        base_lines = {
            1: 500,      # Very simple
            2: 1000,     # Simple
            3: 2500,     # Simple-medium
            4: 5000,     # Medium-low
            5: 10000,    # Medium
            6: 20000,    # Medium-high
            7: 40000,    # Complex
            8: 80000,    # Very complex
            9: 150000,   # Extremely complex
            10: 300000   # Massive
        }
        
        return base_lines.get(complexity_score, 10000)
    
    def _create_chunks(self, prompt: str, project_type: ProjectType, 
                      strategy: ChunkStrategy, language: str, framework: str,
                      max_chunk_size: int, estimated_lines: int) -> List[ChunkDefinition]:
        """Create chunk definitions based on project type and strategy"""
        
        if project_type == ProjectType.WEB_APPLICATION:
            return self._create_web_app_chunks(prompt, strategy, language, framework, max_chunk_size)
        elif project_type == ProjectType.MACHINE_LEARNING:
            return self._create_ml_chunks(prompt, strategy, language, framework, max_chunk_size)
        elif project_type == ProjectType.GAME_DEVELOPMENT:
            return self._create_game_chunks(prompt, strategy, language, framework, max_chunk_size)
        elif project_type == ProjectType.MICROSERVICES:
            return self._create_microservices_chunks(prompt, strategy, language, framework, max_chunk_size)
        elif project_type == ProjectType.DATA_PLATFORM:
            return self._create_data_platform_chunks(prompt, strategy, language, framework, max_chunk_size)
        else:
            return self._create_generic_chunks(prompt, strategy, language, framework, max_chunk_size, estimated_lines)
    
    def _create_web_app_chunks(self, prompt: str, strategy: ChunkStrategy, 
                              language: str, framework: str, max_chunk_size: int) -> List[ChunkDefinition]:
        """Create chunks for web applications"""
        chunks = []
        
        # Core infrastructure chunk
        chunks.append(ChunkDefinition(
            chunk_id="core_infrastructure",
            chunk_name="Core Infrastructure",
            description="Project setup, configuration, and core utilities",
            dependencies=[],
            estimated_lines=min(1500, max_chunk_size),
            priority=1,
            complexity="medium",
            files_to_generate=[
                "requirements.txt", "setup.py", "config.py", "utils.py",
                "constants.py", "exceptions.py", "logging_config.py"
            ],
            interfaces={"config": "Configuration management", "utils": "Utility functions"},
            technologies=[language, framework]
        ))
        
        # Database models chunk
        chunks.append(ChunkDefinition(
            chunk_id="database_models",
            chunk_name="Database Models",
            description="Data models, schemas, and database configuration",
            dependencies=["core_infrastructure"],
            estimated_lines=min(2000, max_chunk_size),
            priority=2,
            complexity="medium",
            files_to_generate=[
                "models.py", "database.py", "migrations/", "schemas.py"
            ],
            interfaces={"models": "Data models", "database": "Database connection"},
            technologies=[language, "database"]
        ))
        
        # API/Backend chunk
        chunks.append(ChunkDefinition(
            chunk_id="api_backend",
            chunk_name="API Backend",
            description="REST API endpoints, business logic, and services",
            dependencies=["core_infrastructure", "database_models"],
            estimated_lines=min(3000, max_chunk_size),
            priority=3,
            complexity="high",
            files_to_generate=[
                "api/", "services/", "controllers/", "middleware/", "auth.py"
            ],
            interfaces={"api": "REST endpoints", "services": "Business logic"},
            technologies=[language, framework, "api"]
        ))
        
        # Frontend chunk (if applicable)
        if any(term in prompt.lower() for term in ['frontend', 'ui', 'interface', 'web interface']):
            chunks.append(ChunkDefinition(
                chunk_id="frontend_ui",
                chunk_name="Frontend UI",
                description="User interface components and frontend logic",
                dependencies=["api_backend"],
                estimated_lines=min(2500, max_chunk_size),
                priority=4,
                complexity="medium",
                files_to_generate=[
                    "templates/", "static/", "components/", "pages/"
                ],
                interfaces={"ui": "User interface", "components": "Reusable components"},
                technologies=["html", "css", "javascript"]
            ))
        
        # Authentication & Security chunk
        chunks.append(ChunkDefinition(
            chunk_id="auth_security",
            chunk_name="Authentication & Security",
            description="User authentication, authorization, and security features",
            dependencies=["database_models"],
            estimated_lines=min(1800, max_chunk_size),
            priority=5,
            complexity="high",
            files_to_generate=[
                "auth/", "security/", "permissions.py", "jwt_handler.py"
            ],
            interfaces={"auth": "Authentication", "security": "Security utilities"},
            technologies=[language, "security"]
        ))
        
        # Testing chunk
        chunks.append(ChunkDefinition(
            chunk_id="testing_suite",
            chunk_name="Testing Suite",
            description="Comprehensive test suite for all components",
            dependencies=["api_backend", "auth_security"],
            estimated_lines=min(2000, max_chunk_size),
            priority=6,
            complexity="medium",
            files_to_generate=[
                "tests/", "test_config.py", "fixtures/", "test_utils.py"
            ],
            interfaces={"tests": "Test utilities"},
            technologies=[language, "testing"]
        ))
        
        return chunks
    
    def _create_ml_chunks(self, prompt: str, strategy: ChunkStrategy, 
                         language: str, framework: str, max_chunk_size: int) -> List[ChunkDefinition]:
        """Create chunks for machine learning projects"""
        chunks = []
        
        # Data preprocessing chunk
        chunks.append(ChunkDefinition(
            chunk_id="data_preprocessing",
            chunk_name="Data Preprocessing",
            description="Data loading, cleaning, and preprocessing pipelines",
            dependencies=[],
            estimated_lines=min(2000, max_chunk_size),
            priority=1,
            complexity="medium",
            files_to_generate=[
                "data/", "preprocessing.py", "data_loader.py", "feature_engineering.py"
            ],
            interfaces={"data": "Data loading", "preprocessing": "Data preprocessing"},
            technologies=[language, "pandas", "numpy"]
        ))
        
        # Model architecture chunk
        chunks.append(ChunkDefinition(
            chunk_id="model_architecture",
            chunk_name="Model Architecture",
            description="Neural network architectures and model definitions",
            dependencies=["data_preprocessing"],
            estimated_lines=min(2500, max_chunk_size),
            priority=2,
            complexity="high",
            files_to_generate=[
                "models/", "architectures.py", "layers.py", "model_utils.py"
            ],
            interfaces={"models": "Model definitions", "architectures": "Network architectures"},
            technologies=[language, framework, "ml"]
        ))
        
        # Training pipeline chunk
        chunks.append(ChunkDefinition(
            chunk_id="training_pipeline",
            chunk_name="Training Pipeline",
            description="Model training, validation, and optimization",
            dependencies=["model_architecture"],
            estimated_lines=min(2200, max_chunk_size),
            priority=3,
            complexity="high",
            files_to_generate=[
                "training/", "trainer.py", "optimizer.py", "scheduler.py"
            ],
            interfaces={"training": "Training pipeline", "trainer": "Model trainer"},
            technologies=[language, framework, "training"]
        ))
        
        # Evaluation and metrics chunk
        chunks.append(ChunkDefinition(
            chunk_id="evaluation_metrics",
            chunk_name="Evaluation & Metrics",
            description="Model evaluation, metrics, and performance analysis",
            dependencies=["training_pipeline"],
            estimated_lines=min(1500, max_chunk_size),
            priority=4,
            complexity="medium",
            files_to_generate=[
                "evaluation/", "metrics.py", "visualizations.py", "reports.py"
            ],
            interfaces={"evaluation": "Model evaluation", "metrics": "Performance metrics"},
            technologies=[language, "visualization"]
        ))
        
        # Inference service chunk
        chunks.append(ChunkDefinition(
            chunk_id="inference_service",
            chunk_name="Inference Service",
            description="Model serving and inference API",
            dependencies=["model_architecture"],
            estimated_lines=min(1800, max_chunk_size),
            priority=5,
            complexity="medium",
            files_to_generate=[
                "inference/", "api.py", "model_server.py", "prediction.py"
            ],
            interfaces={"inference": "Model inference", "api": "Inference API"},
            technologies=[language, "api", "serving"]
        ))
        
        return chunks
    
    def _create_game_chunks(self, prompt: str, strategy: ChunkStrategy, 
                           language: str, framework: str, max_chunk_size: int) -> List[ChunkDefinition]:
        """Create chunks for game development projects"""
        chunks = []
        
        # Game engine core
        chunks.append(ChunkDefinition(
            chunk_id="game_engine_core",
            chunk_name="Game Engine Core",
            description="Core game engine systems and utilities",
            dependencies=[],
            estimated_lines=min(2500, max_chunk_size),
            priority=1,
            complexity="high",
            files_to_generate=[
                "engine/", "core.py", "game_loop.py", "time_manager.py"
            ],
            interfaces={"engine": "Game engine", "core": "Core systems"},
            technologies=[language, framework]
        ))
        
        # Graphics and rendering
        chunks.append(ChunkDefinition(
            chunk_id="graphics_rendering",
            chunk_name="Graphics & Rendering",
            description="Graphics rendering, sprites, and visual effects",
            dependencies=["game_engine_core"],
            estimated_lines=min(2200, max_chunk_size),
            priority=2,
            complexity="high",
            files_to_generate=[
                "graphics/", "renderer.py", "sprites.py", "effects.py"
            ],
            interfaces={"graphics": "Graphics system", "renderer": "Rendering engine"},
            technologies=[language, "graphics"]
        ))
        
        # Game mechanics
        chunks.append(ChunkDefinition(
            chunk_id="game_mechanics",
            chunk_name="Game Mechanics",
            description="Core gameplay mechanics and systems",
            dependencies=["game_engine_core"],
            estimated_lines=min(2000, max_chunk_size),
            priority=3,
            complexity="medium",
            files_to_generate=[
                "mechanics/", "player.py", "entities.py", "physics.py"
            ],
            interfaces={"mechanics": "Game mechanics", "entities": "Game entities"},
            technologies=[language, "physics"]
        ))
        
        return chunks
    
    def _create_microservices_chunks(self, prompt: str, strategy: ChunkStrategy, 
                                   language: str, framework: str, max_chunk_size: int) -> List[ChunkDefinition]:
        """Create chunks for microservices architecture"""
        chunks = []
        
        # Service discovery and configuration
        chunks.append(ChunkDefinition(
            chunk_id="service_discovery",
            chunk_name="Service Discovery",
            description="Service registry, discovery, and configuration management",
            dependencies=[],
            estimated_lines=min(1500, max_chunk_size),
            priority=1,
            complexity="medium",
            files_to_generate=[
                "discovery/", "registry.py", "config_service.py", "health_check.py"
            ],
            interfaces={"discovery": "Service discovery", "config": "Configuration"},
            technologies=[language, "microservices"]
        ))
        
        # API Gateway
        chunks.append(ChunkDefinition(
            chunk_id="api_gateway",
            chunk_name="API Gateway",
            description="API gateway for routing and load balancing",
            dependencies=["service_discovery"],
            estimated_lines=min(2000, max_chunk_size),
            priority=2,
            complexity="high",
            files_to_generate=[
                "gateway/", "router.py", "load_balancer.py", "middleware.py"
            ],
            interfaces={"gateway": "API gateway", "router": "Request routing"},
            technologies=[language, "gateway"]
        ))
        
        # Individual services (create multiple based on prompt)
        service_count = self._estimate_service_count(prompt)
        for i in range(min(service_count, 5)):  # Limit to 5 services for manageability
            chunks.append(ChunkDefinition(
                chunk_id=f"service_{i+1}",
                chunk_name=f"Service {i+1}",
                description=f"Microservice {i+1} implementation",
                dependencies=["service_discovery"],
                estimated_lines=min(1800, max_chunk_size),
                priority=3 + i,
                complexity="medium",
                files_to_generate=[
                    f"services/service_{i+1}/", f"service_{i+1}_api.py"
                ],
                interfaces={f"service_{i+1}": f"Service {i+1} API"},
                technologies=[language, framework]
            ))
        
        return chunks
    
    def _create_data_platform_chunks(self, prompt: str, strategy: ChunkStrategy, 
                                   language: str, framework: str, max_chunk_size: int) -> List[ChunkDefinition]:
        """Create chunks for data platform projects"""
        chunks = []
        
        # Data ingestion
        chunks.append(ChunkDefinition(
            chunk_id="data_ingestion",
            chunk_name="Data Ingestion",
            description="Data ingestion pipelines and connectors",
            dependencies=[],
            estimated_lines=min(2000, max_chunk_size),
            priority=1,
            complexity="medium",
            files_to_generate=[
                "ingestion/", "connectors.py", "pipelines.py", "streaming.py"
            ],
            interfaces={"ingestion": "Data ingestion", "connectors": "Data connectors"},
            technologies=[language, "data"]
        ))
        
        # Data processing
        chunks.append(ChunkDefinition(
            chunk_id="data_processing",
            chunk_name="Data Processing",
            description="ETL pipelines and data transformation",
            dependencies=["data_ingestion"],
            estimated_lines=min(2500, max_chunk_size),
            priority=2,
            complexity="high",
            files_to_generate=[
                "processing/", "etl.py", "transformations.py", "validators.py"
            ],
            interfaces={"processing": "Data processing", "etl": "ETL pipelines"},
            technologies=[language, "etl"]
        ))
        
        # Data storage
        chunks.append(ChunkDefinition(
            chunk_id="data_storage",
            chunk_name="Data Storage",
            description="Data warehouse and storage management",
            dependencies=["data_processing"],
            estimated_lines=min(1800, max_chunk_size),
            priority=3,
            complexity="medium",
            files_to_generate=[
                "storage/", "warehouse.py", "partitioning.py", "indexing.py"
            ],
            interfaces={"storage": "Data storage", "warehouse": "Data warehouse"},
            technologies=[language, "database"]
        ))
        
        return chunks
    
    def _create_generic_chunks(self, prompt: str, strategy: ChunkStrategy, 
                             language: str, framework: str, max_chunk_size: int,
                             estimated_lines: int) -> List[ChunkDefinition]:
        """Create generic chunks for unknown project types"""
        chunks = []
        
        # Calculate number of chunks needed
        num_chunks = max(2, min(10, estimated_lines // max_chunk_size + 1))
        
        for i in range(num_chunks):
            chunks.append(ChunkDefinition(
                chunk_id=f"module_{i+1}",
                chunk_name=f"Module {i+1}",
                description=f"Project module {i+1}",
                dependencies=[] if i == 0 else [f"module_{i}"],
                estimated_lines=min(estimated_lines // num_chunks, max_chunk_size),
                priority=i + 1,
                complexity="medium",
                files_to_generate=[f"module_{i+1}.py"],
                interfaces={f"module_{i+1}": f"Module {i+1} interface"},
                technologies=[language]
            ))
        
        return chunks
    
    def _estimate_service_count(self, prompt: str) -> int:
        """Estimate number of microservices needed"""
        # Look for explicit mentions of services or domains
        service_indicators = re.findall(r'\b(?:service|microservice|domain|module)\b', prompt.lower())
        return max(2, min(len(service_indicators), 8))
    
    def _identify_global_dependencies(self, prompt: str, language: str, framework: str) -> List[str]:
        """Identify global dependencies for the project"""
        deps = []
        
        # Language-specific dependencies
        if language == "python":
            deps.extend(["python>=3.8", "pip", "virtualenv"])
        elif language == "javascript":
            deps.extend(["node.js", "npm"])
        elif language == "java":
            deps.extend(["java", "maven"])
        
        # Framework-specific dependencies
        if framework:
            deps.append(framework)
        
        # Common dependencies based on prompt
        prompt_lower = prompt.lower()
        if "database" in prompt_lower or "sql" in prompt_lower:
            deps.append("database")
        if "api" in prompt_lower or "rest" in prompt_lower:
            deps.append("api_framework")
        if "test" in prompt_lower:
            deps.append("testing_framework")
        
        return deps
    
    def _make_architecture_decisions(self, prompt: str, project_type: ProjectType, 
                                   language: str, framework: str) -> Dict[str, str]:
        """Make key architecture decisions for the project"""
        decisions = {}
        
        # Language and framework decisions
        decisions["primary_language"] = language
        if framework:
            decisions["primary_framework"] = framework
        
        # Architecture pattern decisions
        if project_type == ProjectType.WEB_APPLICATION:
            decisions["architecture_pattern"] = "MVC" if not framework else "Framework-specific"
            decisions["api_style"] = "REST"
        elif project_type == ProjectType.MICROSERVICES:
            decisions["architecture_pattern"] = "Microservices"
            decisions["communication"] = "HTTP/gRPC"
        elif project_type == ProjectType.MACHINE_LEARNING:
            decisions["architecture_pattern"] = "Pipeline"
            decisions["model_serving"] = "API"
        
        # Database decisions
        if "database" in prompt.lower():
            if "nosql" in prompt.lower():
                decisions["database_type"] = "NoSQL"
            else:
                decisions["database_type"] = "SQL"
        
        # Deployment decisions
        if "cloud" in prompt.lower() or "aws" in prompt.lower():
            decisions["deployment_target"] = "Cloud"
        elif "docker" in prompt.lower():
            decisions["containerization"] = "Docker"
        
        return decisions
    
    def _estimate_duration(self, estimated_lines: int, complexity_score: int, chunk_count: int) -> str:
        """Estimate project generation duration"""
        # Base time per line of code (in seconds)
        base_time_per_line = 0.1
        
        # Complexity multiplier
        complexity_multiplier = 1 + (complexity_score - 5) * 0.2
        
        # Chunk overhead (coordination time)
        chunk_overhead = chunk_count * 30  # 30 seconds per chunk for coordination
        
        total_seconds = (estimated_lines * base_time_per_line * complexity_multiplier) + chunk_overhead
        
        if total_seconds < 60:
            return f"{int(total_seconds)} seconds"
        elif total_seconds < 3600:
            return f"{int(total_seconds / 60)} minutes"
        else:
            hours = int(total_seconds / 3600)
            minutes = int((total_seconds % 3600) / 60)
            return f"{hours}h {minutes}m"
    
    def _load_project_patterns(self) -> Dict:
        """Load project patterns for analysis"""
        # This would typically load from a configuration file
        return {
            "web_patterns": ["api", "frontend", "backend", "database"],
            "ml_patterns": ["data", "model", "training", "inference"],
            "game_patterns": ["engine", "graphics", "mechanics", "audio"]
        }
    
    def _load_technology_mappings(self) -> Dict:
        """Load technology mappings"""
        return {
            "python": ["flask", "django", "fastapi", "pytorch", "tensorflow"],
            "javascript": ["react", "vue", "angular", "express", "node"],
            "java": ["spring", "hibernate", "maven", "gradle"]
        }
    
    def save_analysis(self, analysis: ProjectAnalysis, filepath: str):
        """Save analysis to file"""
        with open(filepath, 'w') as f:
            json.dump(asdict(analysis), f, indent=2, default=str)
    
    def load_analysis(self, filepath: str) -> ProjectAnalysis:
        """Load analysis from file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Convert back to proper types
        data['project_type'] = ProjectType(data['project_type'])
        data['chunk_strategy'] = ChunkStrategy(data['chunk_strategy'])
        data['chunks'] = [ChunkDefinition(**chunk) for chunk in data['chunks']]
        
        return ProjectAnalysis(**data)