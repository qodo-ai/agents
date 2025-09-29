"""
Template Manager - Provides templates and scaffolding for large-scale projects
"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ProjectTemplate:
    """Template for a specific type of project"""
    name: str
    description: str
    language: str
    framework: str
    base_structure: Dict[str, str]  # directory -> description
    required_files: List[str]
    dependencies: List[str]
    setup_commands: List[str]


class TemplateManager:
    """Manages project templates for different types of large-scale projects"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def get_template(self, project_type: str, language: str, framework: str = "") -> Optional[ProjectTemplate]:
        """Get a template for a specific project type"""
        template_key = f"{project_type}_{language}_{framework}".lower()
        return self.templates.get(template_key)
    
    def create_project_structure(self, template: ProjectTemplate, output_dir: str):
        """Create the basic project structure from a template"""
        for directory, description in template.base_structure.items():
            dir_path = os.path.join(output_dir, directory)
            os.makedirs(dir_path, exist_ok=True)
            
            # Create a README in each directory explaining its purpose
            readme_path = os.path.join(dir_path, "README.md")
            if not os.path.exists(readme_path):
                with open(readme_path, 'w') as f:
                    f.write(f"# {directory.replace('/', ' ').title()}\n\n{description}\n")
    
    def generate_base_files(self, template: ProjectTemplate, output_dir: str, 
                           project_name: str, prompt: str):
        """Generate base files for the project"""
        for file_path in template.required_files:
            full_path = os.path.join(output_dir, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            content = self._generate_file_content(file_path, template, project_name, prompt)
            
            with open(full_path, 'w') as f:
                f.write(content)
    
    def _load_templates(self) -> Dict[str, ProjectTemplate]:
        """Load all available project templates"""
        templates = {}
        
        # Web Application Templates
        templates["web_application_python_flask"] = ProjectTemplate(
            name="Flask Web Application",
            description="Large-scale Flask web application with modular architecture",
            language="python",
            framework="flask",
            base_structure={
                "app": "Main application package",
                "app/api": "REST API endpoints",
                "app/models": "Database models",
                "app/services": "Business logic services",
                "app/utils": "Utility functions",
                "app/auth": "Authentication and authorization",
                "app/static": "Static files (CSS, JS, images)",
                "app/templates": "Jinja2 templates",
                "migrations": "Database migrations",
                "tests": "Test suite",
                "tests/unit": "Unit tests",
                "tests/integration": "Integration tests",
                "config": "Configuration files",
                "docs": "Documentation",
                "scripts": "Utility scripts"
            },
            required_files=[
                "requirements.txt",
                "app/__init__.py",
                "app/config.py",
                "app/models/__init__.py",
                "app/api/__init__.py",
                "app/services/__init__.py",
                "run.py",
                "wsgi.py",
                "Dockerfile",
                "docker-compose.yml",
                ".env.example",
                ".gitignore",
                "README.md",
                "pytest.ini",
                "setup.py"
            ],
            dependencies=[
                "flask>=2.0.0",
                "flask-sqlalchemy",
                "flask-migrate",
                "flask-jwt-extended",
                "flask-cors",
                "python-dotenv",
                "gunicorn",
                "pytest",
                "pytest-cov"
            ],
            setup_commands=[
                "pip install -r requirements.txt",
                "flask db init",
                "flask db migrate",
                "flask db upgrade"
            ]
        )
        
        templates["web_application_python_django"] = ProjectTemplate(
            name="Django Web Application",
            description="Large-scale Django web application with app-based architecture",
            language="python",
            framework="django",
            base_structure={
                "project": "Main Django project",
                "apps": "Django applications",
                "apps/core": "Core functionality",
                "apps/users": "User management",
                "apps/api": "API endpoints",
                "static": "Static files",
                "media": "User uploaded files",
                "templates": "Django templates",
                "tests": "Test suite",
                "docs": "Documentation",
                "scripts": "Management scripts",
                "config": "Configuration files"
            },
            required_files=[
                "requirements.txt",
                "manage.py",
                "project/__init__.py",
                "project/settings.py",
                "project/urls.py",
                "project/wsgi.py",
                "apps/__init__.py",
                "apps/core/__init__.py",
                "apps/core/models.py",
                "apps/core/views.py",
                "apps/core/urls.py",
                "Dockerfile",
                "docker-compose.yml",
                ".env.example",
                ".gitignore",
                "README.md",
                "pytest.ini"
            ],
            dependencies=[
                "django>=4.0.0",
                "djangorestframework",
                "django-cors-headers",
                "python-decouple",
                "gunicorn",
                "pytest-django",
                "pytest-cov"
            ],
            setup_commands=[
                "pip install -r requirements.txt",
                "python manage.py migrate",
                "python manage.py collectstatic"
            ]
        )
        
        templates["web_application_javascript_react"] = ProjectTemplate(
            name="React Web Application",
            description="Large-scale React application with component-based architecture",
            language="javascript",
            framework="react",
            base_structure={
                "src": "Source code",
                "src/components": "Reusable components",
                "src/pages": "Page components",
                "src/hooks": "Custom React hooks",
                "src/services": "API services",
                "src/utils": "Utility functions",
                "src/context": "React context providers",
                "src/styles": "CSS and styling",
                "public": "Public assets",
                "tests": "Test files",
                "docs": "Documentation",
                "build": "Build output"
            },
            required_files=[
                "package.json",
                "src/index.js",
                "src/App.js",
                "src/App.css",
                "public/index.html",
                "public/manifest.json",
                ".gitignore",
                "README.md",
                "Dockerfile",
                ".env.example",
                "jest.config.js"
            ],
            dependencies=[
                "react",
                "react-dom",
                "react-router-dom",
                "axios",
                "@testing-library/react",
                "@testing-library/jest-dom",
                "jest"
            ],
            setup_commands=[
                "npm install",
                "npm run build"
            ]
        )
        
        # Machine Learning Templates
        templates["machine_learning_python_pytorch"] = ProjectTemplate(
            name="PyTorch ML Project",
            description="Large-scale machine learning project with PyTorch",
            language="python",
            framework="pytorch",
            base_structure={
                "src": "Source code",
                "src/data": "Data loading and preprocessing",
                "src/models": "Model architectures",
                "src/training": "Training scripts",
                "src/evaluation": "Evaluation and metrics",
                "src/inference": "Inference and serving",
                "src/utils": "Utility functions",
                "data": "Dataset storage",
                "data/raw": "Raw data",
                "data/processed": "Processed data",
                "models": "Saved models",
                "experiments": "Experiment tracking",
                "notebooks": "Jupyter notebooks",
                "tests": "Test suite",
                "docs": "Documentation",
                "scripts": "Utility scripts"
            },
            required_files=[
                "requirements.txt",
                "src/__init__.py",
                "src/data/__init__.py",
                "src/models/__init__.py",
                "src/training/__init__.py",
                "src/config.py",
                "train.py",
                "evaluate.py",
                "inference.py",
                "Dockerfile",
                ".gitignore",
                "README.md",
                "setup.py",
                "pytest.ini"
            ],
            dependencies=[
                "torch",
                "torchvision",
                "numpy",
                "pandas",
                "scikit-learn",
                "matplotlib",
                "seaborn",
                "jupyter",
                "tensorboard",
                "pytest"
            ],
            setup_commands=[
                "pip install -r requirements.txt",
                "python -m pytest tests/"
            ]
        )
        
        # Microservices Templates
        templates["microservices_python_fastapi"] = ProjectTemplate(
            name="FastAPI Microservices",
            description="Microservices architecture with FastAPI",
            language="python",
            framework="fastapi",
            base_structure={
                "services": "Individual microservices",
                "services/gateway": "API Gateway service",
                "services/auth": "Authentication service",
                "services/user": "User management service",
                "services/shared": "Shared utilities",
                "infrastructure": "Infrastructure code",
                "infrastructure/docker": "Docker configurations",
                "infrastructure/k8s": "Kubernetes manifests",
                "tests": "Test suite",
                "docs": "Documentation",
                "scripts": "Deployment scripts"
            },
            required_files=[
                "docker-compose.yml",
                "services/gateway/main.py",
                "services/gateway/requirements.txt",
                "services/auth/main.py",
                "services/auth/requirements.txt",
                "services/user/main.py",
                "services/user/requirements.txt",
                "services/shared/__init__.py",
                "infrastructure/docker/Dockerfile.base",
                ".gitignore",
                "README.md",
                "Makefile"
            ],
            dependencies=[
                "fastapi",
                "uvicorn",
                "pydantic",
                "sqlalchemy",
                "alembic",
                "redis",
                "pytest",
                "httpx"
            ],
            setup_commands=[
                "docker-compose up -d",
                "make test"
            ]
        )
        
        # Game Development Templates
        templates["game_development_python_pygame"] = ProjectTemplate(
            name="Pygame Game Project",
            description="Large-scale game development project with Pygame",
            language="python",
            framework="pygame",
            base_structure={
                "src": "Source code",
                "src/engine": "Game engine components",
                "src/entities": "Game entities",
                "src/systems": "Game systems",
                "src/scenes": "Game scenes",
                "src/ui": "User interface",
                "src/audio": "Audio management",
                "src/graphics": "Graphics and rendering",
                "assets": "Game assets",
                "assets/images": "Image assets",
                "assets/sounds": "Audio assets",
                "assets/fonts": "Font assets",
                "levels": "Level data",
                "tests": "Test suite",
                "docs": "Documentation",
                "tools": "Development tools"
            },
            required_files=[
                "requirements.txt",
                "main.py",
                "src/__init__.py",
                "src/engine/__init__.py",
                "src/engine/game.py",
                "src/engine/scene_manager.py",
                "src/config.py",
                "src/constants.py",
                ".gitignore",
                "README.md",
                "setup.py"
            ],
            dependencies=[
                "pygame",
                "numpy",
                "pytest"
            ],
            setup_commands=[
                "pip install -r requirements.txt",
                "python main.py"
            ]
        )
        
        return templates
    
    def _generate_file_content(self, file_path: str, template: ProjectTemplate, 
                              project_name: str, prompt: str) -> str:
        """Generate content for a specific file based on template"""
        
        if file_path == "requirements.txt":
            return "\n".join(template.dependencies) + "\n"
        
        elif file_path == "README.md":
            return self._generate_readme(template, project_name, prompt)
        
        elif file_path == ".gitignore":
            return self._generate_gitignore(template.language)
        
        elif file_path == "Dockerfile":
            return self._generate_dockerfile(template)
        
        elif file_path == "docker-compose.yml":
            return self._generate_docker_compose(template, project_name)
        
        elif file_path.endswith("__init__.py"):
            return self._generate_python_init(file_path, template)
        
        elif file_path == "setup.py":
            return self._generate_setup_py(template, project_name)
        
        elif file_path == "package.json":
            return self._generate_package_json(template, project_name)
        
        else:
            return self._generate_generic_file(file_path, template, project_name)
    
    def _generate_readme(self, template: ProjectTemplate, project_name: str, prompt: str) -> str:
        """Generate README.md content"""
        return f"""# {project_name}

{template.description}

## Project Description

{prompt}

## Architecture

This project follows a {template.framework} architecture with the following structure:

{chr(10).join(f"- **{dir_name}**: {desc}" for dir_name, desc in template.base_structure.items())}

## Setup

1. Install dependencies:
   ```bash
   {chr(10).join(f"   {cmd}" for cmd in template.setup_commands)}
   ```

2. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Run the application:
   ```bash
   # Add specific run commands here
   ```

## Development

### Project Structure

```
{project_name}/
{chr(10).join(f"├── {dir_name}/" for dir_name in template.base_structure.keys())}
```

### Dependencies

{chr(10).join(f"- {dep}" for dep in template.dependencies)}

### Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src
```

## Deployment

This project includes Docker configuration for easy deployment:

```bash
docker-compose up -d
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

Add your license information here.
"""
    
    def _generate_gitignore(self, language: str) -> str:
        """Generate .gitignore content based on language"""
        common = """# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local
.env.*.local

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build outputs
build/
dist/
target/
"""
        
        if language == "python":
            return common + """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
develop-eggs/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# Jupyter
.ipynb_checkpoints/

# pytest
.pytest_cache/
.coverage
htmlcov/

# mypy
.mypy_cache/
.dmypy.json
dmypy.json
"""
        
        elif language == "javascript":
            return common + """
# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Next.js
.next/
out/

# React
build/

# Coverage
coverage/
.nyc_output/
"""
        
        else:
            return common
    
    def _generate_dockerfile(self, template: ProjectTemplate) -> str:
        """Generate Dockerfile content"""
        if template.language == "python":
            return f"""FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \\
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "main.py"]
"""
        
        elif template.language == "javascript":
            return f"""FROM node:16-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Build application
RUN npm run build

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# Change ownership
RUN chown -R nextjs:nodejs /app
USER nextjs

# Expose port
EXPOSE 3000

# Run application
CMD ["npm", "start"]
"""
        
        else:
            return """FROM alpine:latest

WORKDIR /app

# Copy application
COPY . .

# Expose port
EXPOSE 8080

# Run application
CMD ["./app"]
"""
    
    def _generate_docker_compose(self, template: ProjectTemplate, project_name: str) -> str:
        """Generate docker-compose.yml content"""
        return f"""version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV=development
    volumes:
      - .:/app
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: {project_name}
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
"""
    
    def _generate_python_init(self, file_path: str, template: ProjectTemplate) -> str:
        """Generate Python __init__.py content"""
        module_name = os.path.dirname(file_path).replace('/', '.').replace('src.', '')
        
        return f'''"""
{module_name.replace('.', ' ').title()} module

Part of the {template.name} project.
"""

__version__ = "1.0.0"
'''
    
    def _generate_setup_py(self, template: ProjectTemplate, project_name: str) -> str:
        """Generate setup.py content"""
        return f'''from setuptools import setup, find_packages

setup(
    name="{project_name}",
    version="1.0.0",
    description="{template.description}",
    packages=find_packages(),
    install_requires=[
        {chr(10).join(f'        "{dep}",' for dep in template.dependencies)}
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
'''
    
    def _generate_package_json(self, template: ProjectTemplate, project_name: str) -> str:
        """Generate package.json content"""
        return f'''{{
  "name": "{project_name}",
  "version": "1.0.0",
  "description": "{template.description}",
  "main": "src/index.js",
  "scripts": {{
    "start": "node src/index.js",
    "dev": "nodemon src/index.js",
    "build": "webpack --mode production",
    "test": "jest",
    "test:watch": "jest --watch",
    "lint": "eslint src/",
    "lint:fix": "eslint src/ --fix"
  }},
  "dependencies": {{
    {chr(10).join(f'    "{dep}": "latest",' for dep in template.dependencies)}
  }},
  "devDependencies": {{
    "nodemon": "^2.0.0",
    "jest": "^27.0.0",
    "eslint": "^8.0.0"
  }},
  "keywords": [
    "{template.framework}",
    "{template.language}"
  ],
  "author": "",
  "license": "MIT"
}}
'''
    
    def _generate_generic_file(self, file_path: str, template: ProjectTemplate, 
                              project_name: str) -> str:
        """Generate generic file content"""
        file_ext = os.path.splitext(file_path)[1]
        
        if file_ext == ".py":
            return f'''"""
{os.path.basename(file_path)} - Part of {project_name}

Generated as part of the {template.name} template.
"""

# TODO: Implement functionality for {os.path.basename(file_path)}

def main():
    """Main function"""
    pass

if __name__ == "__main__":
    main()
'''
        
        elif file_ext == ".js":
            return f'''/**
 * {os.path.basename(file_path)} - Part of {project_name}
 * 
 * Generated as part of the {template.name} template.
 */

// TODO: Implement functionality for {os.path.basename(file_path)}

function main() {{
    // Main function
}}

if (require.main === module) {{
    main();
}}

module.exports = {{ main }};
'''
        
        elif file_ext in [".yml", ".yaml"]:
            return f"""# {os.path.basename(file_path)}
# Configuration file for {project_name}

# TODO: Add configuration options
"""
        
        else:
            return f"""# {os.path.basename(file_path)}
# Generated for {project_name}

# TODO: Add content
"""
    
    def list_available_templates(self) -> List[Dict[str, str]]:
        """List all available templates"""
        return [
            {
                "key": key,
                "name": template.name,
                "description": template.description,
                "language": template.language,
                "framework": template.framework
            }
            for key, template in self.templates.items()
        ]