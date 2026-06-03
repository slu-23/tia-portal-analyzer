"""TIA Portal Analyzer - AI-powered program detection and analysis."""

__version__ = "0.1.0"
__author__ = "slu-23"
__description__ = "Intelligent TIA Portal program analyzer using AI Agent"

from .detector import PortalProgramDetector
from .agent import PortalAnalyzerAgent
from .analyzer import ProgramAnalyzer
from .models import AnalysisResult, ProgramMetadata

__all__ = [
    "PortalProgramDetector",
    "PortalAnalyzerAgent",
    "ProgramAnalyzer",
    "AnalysisResult",
    "ProgramMetadata",
]
