"""
MasterMindAI Chunked Code Generator

A sophisticated system for generating massive code projects by intelligently
breaking them down into manageable chunks and coordinating their generation.
"""

__version__ = "1.0.0"
__author__ = "MasterMindAI Team"

from .analyzer import ProjectAnalyzer
from .coordinator import ChunkCoordinator
from .context import ContextManager
from .templates import TemplateManager

__all__ = [
    "ProjectAnalyzer",
    "ChunkCoordinator", 
    "ContextManager",
    "TemplateManager"
]