"""TIA Portal program detection engine."""

import re
from pathlib import Path
from typing import Dict, List, Set, Optional
from loguru import logger

from .models import (
    DetectionResult,
    ProgramMetadata,
    ProgramType,
    LanguageType,
    ConfidenceLevel,
)


class PortalProgramDetector:
    """Detects and identifies TIA Portal programs."""

    # Patterns for different program types
    PATTERNS = {
        ProgramType.OB: [
            r"ORGANIZATION_BLOCK",
            r"\bOB\s*\d+",
            r"BEGIN_ORGANIZATION_BLOCK",
        ],
        ProgramType.FC: [
            r"FUNCTION",
            r"\bFC\s*\d+",
            r"BEGIN_FUNCTION",
            r"FUNCTION_BLOCK\s*FC",
        ],
        ProgramType.FB: [
            r"FUNCTION_BLOCK",
            r"\bFB\s*\d+",
            r"BEGIN_FUNCTION_BLOCK",
            r"UDT\s*FB",
        ],
        ProgramType.DB: [
            r"DATA_BLOCK",
            r"\bDB\s*\d+",
            r"BEGIN_DATA_BLOCK",
            r"STRUCT",
        ],
        ProgramType.UDT: [
            r"USER_DEFINED_TYPE",
            r"\bUDT\s*\d+",
            r"TYPE\s*",
        ],
    }

    # Ladder Diagram patterns
    LADDER_PATTERNS = [
        r"NETWORK\s+\d+",  # Network definition
        r"-\|\|-",  # Contact symbol
        r"-/\|-",  # Negated contact
        r"-(\s*)-",  # Coil
        r"-(/)- ",  # Negated coil
        r"\(\s*\)",  # Coil in parentheses
        r"\bLD\b",  # Load operation
        r"\bAND\b",  # AND operation
        r"\bOR\b",  # OR operation
        r"\bXOR\b",  # XOR operation
        r"\bNOT\b",  # NOT operation
        r"\bS\b",  # Set coil
        r"\bR\b",  # Reset coil
        r"END_NETWORK",  # End of network
    ]

    # XML and AWL/SCL signatures
    SIEMENS_SIGNATURES = {
        "siemens": ["siemens", "automation", "tia", "portal"],
        "plc": ["plc", "automation", "control", "scada"],
        "s7": ["s7-1200", "s7-1500", "s7-300", "s7-400"],
    }

    # Common TIA Portal XML namespaces
    XML_NAMESPACES = {
        "http://siemens.com/",
        "www.siemens.com",
        "automation",
    }

    def __init__(self, verbose: bool = False):
        """Initialize detector.
        
        Args:
            verbose: Enable verbose logging
        """
        self.verbose = verbose
        if verbose:
            logger.enable("portal_analyzer")

    def detect_file(self, file_path: str) -> DetectionResult:
        """Detect if a file is a TIA Portal program.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            DetectionResult with detection information
        """
        try:
            path = Path(file_path)
            if not path.exists():
                logger.error(f"File not found: {file_path}")
                return self._create_negative_result(file_path)

            file_content = self._read_file_safe(file_path)
            return self._analyze_content(file_content, file_path)

        except Exception as e:
            logger.error(f"Error detecting file {file_path}: {e}")
            return self._create_negative_result(file_path)

    def analyze_file(self, file_path: str) -> Dict:
        """Analyze a file (alias for detect_file).
        
        Args:
            file_path: Path to the file
            
        Returns:
            Detection result as dictionary
        """
        result = self.detect_file(file_path)
        return result.model_dump()

    def _read_file_safe(self, file_path: str) -> str:
        """Safely read file with encoding detection.
        
        Args:
            file_path: Path to file
            
        Returns:
            File content as string
        """
        encodings = ["utf-8", "utf-16", "latin-1", "cp1252"]
        
        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    return f.read()
            except (UnicodeDecodeError, UnicodeError):
                continue
        
        # Fallback: read as binary
        with open(file_path, "rb") as f:
            return f.read().decode("utf-8", errors="ignore")

    def _analyze_content(self, content: str, file_path: str) -> DetectionResult:
        """Analyze file content for TIA Portal signatures.
        
        Args:
            content: File content
            file_path: Original file path
            
        Returns:
            DetectionResult
        """
        features = []
        confidence_score = 0.0
        
        # Check file extension
        ext_score = self._check_file_extension(file_path)
        confidence_score += ext_score * 0.2
        if ext_score > 0:
            features.append(f"TIA Portal file extension")
        
        # Check for XML signatures
        xml_score = self._check_xml_signatures(content)
        confidence_score += xml_score * 0.25
        if xml_score > 0:
            features.append(f"XML structure detected")
        
        # Check for Ladder Diagram patterns
        ld_score = self._check_ladder_patterns(content)
        confidence_score += ld_score * 0.2
        if ld_score > 0:
            features.append(f"Ladder diagram patterns detected")
        
        # Check for AWL/SCL patterns
        awl_score = self._check_awl_patterns(content)
        confidence_score += awl_score * 0.25
        if awl_score > 0:
            features.append(f"AWL/SCL patterns detected")
        
        # Check for program type patterns
        type_score, prog_type = self._detect_program_type(content)
        confidence_score += type_score * 0.2
        if type_score > 0:
            features.append(f"Program type: {prog_type.value}")
        
        # Check for Siemens signatures
        siemens_score = self._check_siemens_signatures(content)
        confidence_score += siemens_score * 0.1
        if siemens_score > 0:
            features.append(f"Siemens/TIA signature detected")
        
        # Normalize confidence score
        confidence_score = min(1.0, confidence_score)
        
        # Determine if it's a TIA Portal program
        is_tia_portal = confidence_score > 0.5
        confidence_level = self._get_confidence_level(confidence_score)
        
        # Extract metadata
        metadata = None
        if is_tia_portal:
            metadata = self._extract_metadata(content, file_path, prog_type)
        
        return DetectionResult(
            is_tia_portal=is_tia_portal,
            confidence=confidence_level,
            confidence_score=confidence_score,
            program_metadata=metadata,
            detected_features=features,
        )

    def _check_file_extension(self, file_path: str) -> float:
        """Check file extension for TIA Portal indicators.
        
        Args:
            file_path: File path
            
        Returns:
            Score 0.0-1.0
        """
        valid_extensions = {
            ".xml": 1.0,
            ".awl": 0.9,
            ".stl": 0.9,
            ".scl": 0.8,
            ".sce": 0.8,
            ".ld": 0.9,  # 梯形图
            ".lad": 0.9,  # Ladder Diagram
            ".graph": 0.7,
            ".s7p": 0.9,
            ".s7pt": 0.9,
        }
        
        ext = Path(file_path).suffix.lower()
        return valid_extensions.get(ext, 0.0)

    def _check_xml_signatures(self, content: str) -> float:
        """Check for TIA Portal XML signatures.
        
        Args:
            content: File content
            
        Returns:
            Score 0.0-1.0
        """
        if "<?xml" not in content:
            return 0.0
        
        score = 0.1  # Base score for XML
        
        # Check for Siemens namespaces
        if any(ns in content.lower() for ns in self.XML_NAMESPACES):
            score += 0.3
        
        # Check for specific TIA elements
        tia_elements = [
            "Project", "Device", "PlcProgram", "ProgramSection",
            "Network", "Block", "Function", "FunctionBlock",
            "Contact", "Coil",
        ]
        tia_count = sum(1 for elem in tia_elements if elem in content)
        score += min(0.5, tia_count * 0.1)
        
        return min(1.0, score)

    def _check_ladder_patterns(self, content: str) -> float:
        """Check for Ladder Diagram patterns.
        
        Args:
            content: File content
            
        Returns:
            Score 0.0-1.0
        """
        score = 0.0
        
        # Count ladder diagram patterns
        pattern_count = 0
        for pattern in self.LADDER_PATTERNS:
            matches = len(re.findall(pattern, content, re.IGNORECASE | re.MULTILINE))
            if matches > 0:
                pattern_count += matches
        
        # Calculate score based on pattern matches
        if pattern_count > 0:
            score = min(1.0, pattern_count * 0.1)
        
        # Check for common ladder keywords
        ladder_keywords = [
            r"\bNETWORK\b",
            r"\bLD\b",
            r"\bAND\b",
            r"\bOR\b",
            r"\bNOT\b",
            r"\bSET\b",
            r"\bRESET\b",
        ]
        
        keyword_count = sum(1 for kw in ladder_keywords if re.search(kw, content, re.IGNORECASE))
        if keyword_count > 0:
            score = max(score, min(1.0, keyword_count * 0.15))
        
        return score

    def _check_awl_patterns(self, content: str) -> float:
        """Check for AWL/SCL programming patterns.
        
        Args:
            content: File content
            
        Returns:
            Score 0.0-1.0
        """
        score = 0.0
        
        # AWL/STL keywords
        awl_keywords = [
            r"\bAWL\b", r"\bSTL\b", r"\bSCAL\b", r"\bSCL\b",
            r"\bNETWORK\b", r"\bSEGMENT\b", r"\bTITLE\b",
            r"\bAUTHOR\b", r"\bCREATE\b", r"\bREQUEST\b",
        ]
        
        for pattern in awl_keywords:
            if re.search(pattern, content, re.IGNORECASE):
                score += 0.15
        
        # Common AWL instructions
        instructions = [
            r"\bLD\b", r"\bST\b", r"\bAND\b", r"\bOR\b",
            r"\bXOR\b", r"\bADD\b", r"\bSUB\b", r"\bMOV\b",
            r"\bCALL\b", r"\bRET\b", r"\bJMP\b",
        ]
        
        instr_count = sum(1 for instr in instructions if re.search(instr, content, re.IGNORECASE))
        score += min(0.5, instr_count * 0.05)
        
        return min(1.0, score)

    def _detect_program_type(self, content: str) -> tuple:
        """Detect program type.
        
        Args:
            content: File content
            
        Returns:
            Tuple of (score, program_type)
        """
        best_score = 0.0
        best_type = ProgramType.UNKNOWN
        
        for prog_type, patterns in self.PATTERNS.items():
            score = 0.0
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    score += 1.0 / len(patterns)
            
            if score > best_score:
                best_score = score
                best_type = prog_type
        
        return min(1.0, best_score), best_type

    def _check_siemens_signatures(self, content: str) -> float:
        """Check for Siemens/Automation signatures.
        
        Args:
            content: File content
            
        Returns:
            Score 0.0-1.0
        """
        score = 0.0
        content_lower = content.lower()
        
        for category, keywords in self.SIEMENS_SIGNATURES.items():
            for keyword in keywords:
                if keyword in content_lower:
                    score += 0.2 / len(self.SIEMENS_SIGNATURES)
        
        return min(1.0, score)

    def _extract_metadata(self, content: str, file_path: str, prog_type: ProgramType) -> ProgramMetadata:
        """Extract metadata from program.
        
        Args:
            content: File content
            file_path: File path
            prog_type: Detected program type
            
        Returns:
            ProgramMetadata
        """
        path = Path(file_path)
        name = path.stem
        
        # Try to extract language
        language = self._detect_language(file_path, content)
        
        return ProgramMetadata(
            name=name,
            program_type=prog_type,
            language=language,
            file_path=file_path,
            file_size=len(content.encode()),
        )

    def _detect_language(self, file_path: str, content: str) -> LanguageType:
        """Detect programming language.
        
        Args:
            file_path: File path
            content: File content
            
        Returns:
            LanguageType
        """
        ext = Path(file_path).suffix.lower()
        
        if ext == ".xml":
            return LanguageType.XML
        elif ext in [".ld", ".lad"]:
            return LanguageType.LD
        elif ext in [".awl", ".stl"]:
            return LanguageType.AWL
        elif ext in [".scl", ".sce"]:
            return LanguageType.SCL
        elif ext == ".graph":
            return LanguageType.GRAPH
        else:
            # Analyze content
            if "<?xml" in content:
                return LanguageType.XML
            elif self._check_ladder_patterns(content) > 0.5:
                return LanguageType.LD
            elif re.search(r"\b(LD|ST|AND|OR|NETWORK)\b", content, re.IGNORECASE):
                return LanguageType.AWL
            elif re.search(r"\b(PROGRAM|FUNCTION|IF|THEN|VAR)\b", content, re.IGNORECASE):
                return LanguageType.SCL
        
        return LanguageType.UNKNOWN

    def _get_confidence_level(self, score: float) -> ConfidenceLevel:
        """Get confidence level from score.
        
        Args:
            score: Confidence score 0.0-1.0
            
        Returns:
            ConfidenceLevel
        """
        if score >= 0.8:
            return ConfidenceLevel.HIGH
        elif score >= 0.6:
            return ConfidenceLevel.MEDIUM
        elif score >= 0.4:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.UNCERTAIN

    def _create_negative_result(self, file_path: str) -> DetectionResult:
        """Create a negative detection result.
        
        Args:
            file_path: File path
            
        Returns:
            Negative DetectionResult
        """
        return DetectionResult(
            is_tia_portal=False,
            confidence=ConfidenceLevel.UNCERTAIN,
            confidence_score=0.0,
            program_metadata=None,
            detected_features=[],
        )
