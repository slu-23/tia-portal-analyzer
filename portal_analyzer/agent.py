"""AI Agent for intelligent TIA Portal program analysis."""

from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
from loguru import logger

from .detector import PortalProgramDetector
from .analyzer import ProgramAnalyzer
from .models import AnalysisResult, DetectionResult, CodeMetrics, DependencyInfo


class PortalAnalyzerAgent:
    """Intelligent AI Agent for TIA Portal program analysis.
    
    The agent follows a multi-stage reasoning process:
    1. Reconnaissance - Detect and identify program type
    2. Deep Analysis - Analyze code structure and metrics
    3. Assessment - Evaluate quality and risks
    4. Reporting - Generate comprehensive report
    """

    def __init__(self, verbose: bool = True):
        """Initialize the AI Agent.
        
        Args:
            verbose: Enable verbose logging
        """
        self.verbose = verbose
        self.detector = PortalProgramDetector(verbose=verbose)
        self.analyzer = ProgramAnalyzer(verbose=verbose)
        self.analysis_history = []

    def analyze_program(self, file_path: str) -> AnalysisResult:
        """Analyze a TIA Portal program using multi-stage agent reasoning.
        
        Args:
            file_path: Path to program file
            
        Returns:
            Complete AnalysisResult
        """
        reasoning = []
        reasoning.append(f"[AGENT] Starting analysis of {file_path}")
        
        # Stage 1: Reconnaissance
        reasoning.append("\n[STAGE 1] RECONNAISSANCE - Detecting program type...")
        detection_result = self.detector.detect_file(file_path)
        reasoning.append(f"  ✓ Detection confidence: {detection_result.confidence.value}")
        reasoning.append(f"  ✓ Detected features: {', '.join(detection_result.detected_features)}")
        
        if not detection_result.is_tia_portal:
            reasoning.append("\n[DECISION] Not a TIA Portal program. Stopping analysis.")
            return self._create_empty_result(file_path, detection_result, reasoning)
        
        reasoning.append("\n✓ Confirmed TIA Portal program detected")
        
        # Stage 2: Deep Analysis
        reasoning.append("\n[STAGE 2] DEEP ANALYSIS - Analyzing code structure...")
        metrics = self._analyze_metrics(file_path)
        reasoning.append(f"  ✓ Lines of code: {metrics.lines_of_code}")
        reasoning.append(f"  ✓ Cyclomatic complexity: {metrics.cyclomatic_complexity:.2f}")
        reasoning.append(f"  ✓ Functions found: {metrics.functions_count}")
        
        dependencies = self._extract_dependencies(file_path)
        reasoning.append(f"  ✓ Dependencies found: {len(dependencies)}")
        
        # Stage 3: Assessment
        reasoning.append("\n[STAGE 3] ASSESSMENT - Evaluating quality and risks...")
        risk_assessment = self._assess_risks(metrics, dependencies)
        reasoning.append(f"  ✓ Complexity level: {risk_assessment['complexity_level']}")
        reasoning.append(f"  ✓ Risk score: {risk_assessment['risk_score']:.1%}")
        
        # Stage 4: Generate Recommendations
        reasoning.append("\n[STAGE 4] RECOMMENDATIONS - Generating improvement suggestions...")
        recommendations = self._generate_recommendations(metrics, risk_assessment, dependencies)
        for i, rec in enumerate(recommendations, 1):
            reasoning.append(f"  {i}. {rec}")
        
        reasoning.append("\n[AGENT] Analysis complete.")
        
        # Compile results
        result = AnalysisResult(
            file_path=file_path,
            detection_result=detection_result,
            metadata=detection_result.program_metadata,
            metrics=metrics,
            dependencies=dependencies,
            risk_assessment=risk_assessment,
            recommendations=recommendations,
            agent_reasoning="\n".join(reasoning),
        )
        
        self.analysis_history.append(result)
        return result

    def batch_analyze(self, directory: str, recursive: bool = True) -> List[AnalysisResult]:
        """Analyze multiple programs in a directory.
        
        Args:
            directory: Directory path
            recursive: Whether to search recursively
            
        Returns:
            List of AnalysisResult
        """
        results = []
        path = Path(directory)
        
        # Find all potential TIA Portal files
        patterns = [
            "*.xml", "*.awl", "*.stl", "*.scl", "*.sce", "*.graph",
            "*.s7p", "*.s7pt"
        ]
        
        for pattern in patterns:
            files = path.rglob(pattern) if recursive else path.glob(pattern)
            for file_path in files:
                try:
                    result = self.analyze_program(str(file_path))
                    results.append(result)
                except Exception as e:
                    logger.error(f"Error analyzing {file_path}: {e}")
        
        return results

    def _analyze_metrics(self, file_path: str) -> CodeMetrics:
        """Analyze code metrics.
        
        Args:
            file_path: File path
            
        Returns:
            CodeMetrics
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            return self.analyzer.calculate_metrics(content)
        except Exception as e:
            logger.error(f"Error analyzing metrics: {e}")
            return CodeMetrics()

    def _extract_dependencies(self, file_path: str) -> List[DependencyInfo]:
        """Extract program dependencies.
        
        Args:
            file_path: File path
            
        Returns:
            List of DependencyInfo
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            return self.analyzer.extract_dependencies(content)
        except Exception as e:
            logger.error(f"Error extracting dependencies: {e}")
            return []

    def _assess_risks(self, metrics: CodeMetrics, dependencies: List[DependencyInfo]) -> Dict:
        """Assess program risks.
        
        Args:
            metrics: Code metrics
            dependencies: Program dependencies
            
        Returns:
            Risk assessment dictionary
        """
        risk_score = 0.0
        complexity_level = "Low"
        issues = []
        
        # Complexity assessment
        if metrics.cyclomatic_complexity > 20:
            risk_score += 0.3
            complexity_level = "Very High"
            issues.append("Very high cyclomatic complexity")
        elif metrics.cyclomatic_complexity > 10:
            risk_score += 0.2
            complexity_level = "High"
            issues.append("High cyclomatic complexity")
        elif metrics.cyclomatic_complexity > 5:
            risk_score += 0.1
            complexity_level = "Medium"
        
        # Nesting depth assessment
        if metrics.nesting_depth > 5:
            risk_score += 0.2
            issues.append(f"Deep nesting (depth: {metrics.nesting_depth})")
        
        # Code size assessment
        if metrics.lines_of_code > 500:
            risk_score += 0.15
            issues.append("Large program (LOC > 500)")
        elif metrics.lines_of_code > 1000:
            risk_score += 0.25
            issues.append("Very large program (LOC > 1000)")
        
        # Dependency assessment
        if len(dependencies) > 10:
            risk_score += 0.1
            issues.append(f"Many dependencies ({len(dependencies)})")
        
        return {
            "risk_score": min(1.0, risk_score),
            "complexity_level": complexity_level,
            "identified_issues": issues,
        }

    def _generate_recommendations(self, metrics: CodeMetrics, risk: Dict, deps: List[DependencyInfo]) -> List[str]:
        """Generate improvement recommendations.
        
        Args:
            metrics: Code metrics
            risk: Risk assessment
            deps: Dependencies
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Complexity recommendations
        if metrics.cyclomatic_complexity > 10:
            recommendations.append("Refactor to reduce cyclomatic complexity - consider breaking into smaller functions")
        
        if metrics.nesting_depth > 5:
            recommendations.append("Reduce nesting depth - use guard clauses and extract nested blocks into functions")
        
        # Code size recommendations
        if metrics.lines_of_code > 500:
            recommendations.append("Consider splitting large program into multiple function blocks")
        
        # Comments recommendations
        if metrics.comments_ratio < 0.1:
            recommendations.append("Add more code comments and documentation for better maintainability")
        
        # Dependencies recommendations
        if len(deps) > 10:
            recommendations.append(f"Review {len(deps)} dependencies - consider consolidating or simplifying dependencies")
        
        # General best practices
        if not recommendations:
            recommendations.append("Code quality looks good - maintain current standards")
        
        recommendations.append("Consider adding unit tests for critical functions")
        recommendations.append("Document all public interfaces and function signatures")
        
        return recommendations[:5]  # Return top 5 recommendations

    def _create_empty_result(self, file_path: str, detection: DetectionResult, reasoning: List[str]) -> AnalysisResult:
        """Create empty analysis result for non-TIA files.
        
        Args:
            file_path: File path
            detection: Detection result
            reasoning: Reasoning log
            
        Returns:
            AnalysisResult
        """
        return AnalysisResult(
            file_path=file_path,
            detection_result=detection,
            metrics=CodeMetrics(),
            agent_reasoning="\n".join(reasoning),
        )

    def get_history(self) -> List[AnalysisResult]:
        """Get analysis history.
        
        Returns:
            List of previous analysis results
        """
        return self.analysis_history

    def get_summary(self) -> Dict:
        """Get analysis summary statistics.
        
        Returns:
            Summary statistics
        """
        if not self.analysis_history:
            return {"total_analyses": 0}
        
        tia_count = sum(1 for r in self.analysis_history if r.detection_result.is_tia_portal)
        avg_complexity = sum(r.metrics.cyclomatic_complexity for r in self.analysis_history) / len(self.analysis_history)
        
        return {
            "total_analyses": len(self.analysis_history),
            "tia_portal_programs": tia_count,
            "other_files": len(self.analysis_history) - tia_count,
            "average_complexity": avg_complexity,
        }
