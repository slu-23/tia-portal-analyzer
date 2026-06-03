"""Data models for TIA Portal analysis."""

from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ProgramType(str, Enum):
    """TIA Portal program block types."""
    OB = "OB"  # Organization Block
    FC = "FC"  # Function
    FB = "FB"  # Function Block
    DB = "DB"  # Data Block
    UDT = "UDT"  # User Defined Type
    UNKNOWN = "UNKNOWN"


class LanguageType(str, Enum):
    """Programming languages supported."""
    AWL = "AWL"  # Statement List
    SCL = "SCL"  # Structured Control Language
    XML = "XML"  # TIA Portal XML format
    LD = "LD"  # Ladder Diagram (梯形图)
    GRAPH = "GRAPH"  # Sequential function chart
    UNKNOWN = "UNKNOWN"


class ConfidenceLevel(str, Enum):
    """Confidence levels for detection."""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    UNCERTAIN = "UNCERTAIN"


class ProgramMetadata(BaseModel):
    """Metadata about a detected program."""
    name: str = Field(..., description="Program name")
    program_type: ProgramType = Field(..., description="Type of program block")
    language: LanguageType = Field(..., description="Programming language")
    file_path: str = Field(..., description="Path to the program file")
    file_size: int = Field(..., description="File size in bytes")
    created_date: Optional[datetime] = Field(None, description="Program creation date")
    modified_date: Optional[datetime] = Field(None, description="Last modification date")
    version: Optional[str] = Field(None, description="Program version")


class DetectionResult(BaseModel):
    """Result of program detection."""
    is_tia_portal: bool = Field(..., description="Whether file is TIA Portal program")
    confidence: ConfidenceLevel = Field(..., description="Confidence of detection")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score 0-1")
    program_metadata: Optional[ProgramMetadata] = Field(None, description="Detected program metadata")
    detected_features: List[str] = Field(default_factory=list, description="Detected features")
    warnings: List[str] = Field(default_factory=list, description="Detection warnings")


class CodeMetrics(BaseModel):
    """Code quality and complexity metrics."""
    lines_of_code: int = Field(default=0)
    cyclomatic_complexity: float = Field(default=1.0)
    nesting_depth: int = Field(default=0)
    functions_count: int = Field(default=0)
    variables_count: int = Field(default=0)
    comments_ratio: float = Field(default=0.0)
    code_coverage: float = Field(default=0.0)
    rung_count: int = Field(default=0, description="Number of rungs (for ladder diagrams)")
    contact_count: int = Field(default=0, description="Number of contacts (for ladder diagrams)")
    coil_count: int = Field(default=0, description="Number of coils (for ladder diagrams)")


class DependencyInfo(BaseModel):
    """Information about program dependencies."""
    name: str
    type: str
    line_number: Optional[int] = None
    description: Optional[str] = None


class AnalysisResult(BaseModel):
    """Complete analysis result for a program."""
    file_path: str = Field(..., description="Analyzed file path")
    detection_result: DetectionResult = Field(..., description="Detection results")
    metadata: Optional[ProgramMetadata] = Field(None, description="Program metadata")
    metrics: CodeMetrics = Field(default_factory=CodeMetrics, description="Code metrics")
    dependencies: List[DependencyInfo] = Field(default_factory=list, description="Program dependencies")
    risk_assessment: Dict[str, Any] = Field(default_factory=dict, description="Risk assessment")
    recommendations: List[str] = Field(default_factory=list, description="Analysis recommendations")
    analysis_timestamp: datetime = Field(default_factory=datetime.now)
    agent_reasoning: str = Field(default="", description="AI agent reasoning process")
    
    def report(self) -> str:
        """Generate human-readable report."""
        report_lines = [
            "=" * 60,
            "TIA PORTAL PROGRAM ANALYSIS REPORT",
            "=" * 60,
            f"\nFile: {self.file_path}",
            f"Analysis Time: {self.analysis_timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            f"\n--- DETECTION RESULTS ---",
            f"Is TIA Portal Program: {self.detection_result.is_tia_portal}",
            f"Confidence Level: {self.detection_result.confidence.value}",
            f"Confidence Score: {self.detection_result.confidence_score:.2%}",
        ]
        
        if self.metadata:
            report_lines.extend([
                f"\n--- PROGRAM METADATA ---",
                f"Name: {self.metadata.name}",
                f"Type: {self.metadata.program_type.value}",
                f"Language: {self.metadata.language.value}",
                f"File Size: {self.metadata.file_size} bytes",
            ])
        
        report_lines.extend([
            f"\n--- CODE METRICS ---",
            f"Lines of Code: {self.metrics.lines_of_code}",
            f"Cyclomatic Complexity: {self.metrics.cyclomatic_complexity:.2f}",
            f"Nesting Depth: {self.metrics.nesting_depth}",
            f"Functions: {self.metrics.functions_count}",
            f"Variables: {self.metrics.variables_count}",
        ])
        
        # Add ladder diagram specific metrics
        if self.metadata and self.metadata.language == LanguageType.LD:
            report_lines.extend([
                f"\n--- LADDER DIAGRAM METRICS ---",
                f"Rungs: {self.metrics.rung_count}",
                f"Contacts: {self.metrics.contact_count}",
                f"Coils: {self.metrics.coil_count}",
            ])
        
        if self.recommendations:
            report_lines.append(f"\n--- RECOMMENDATIONS ---")
            for i, rec in enumerate(self.recommendations, 1):
                report_lines.append(f"{i}. {rec}")
        
        if self.agent_reasoning:
            report_lines.append(f"\n--- AGENT ANALYSIS ---")
            report_lines.append(self.agent_reasoning)
        
        report_lines.append("\n" + "=" * 60)
        return "\n".join(report_lines)
