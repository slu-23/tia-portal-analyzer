"""Code analysis engine for TIA Portal programs."""

import re
from typing import List, Dict, Optional
from loguru import logger

from .models import CodeMetrics, DependencyInfo


class ProgramAnalyzer:
    """Analyzes TIA Portal program code metrics and structure."""

    def __init__(self, verbose: bool = False):
        """Initialize analyzer.
        
        Args:
            verbose: Enable verbose logging
        """
        self.verbose = verbose

    def calculate_metrics(self, content: str) -> CodeMetrics:
        """Calculate code metrics.
        
        Args:
            content: Program content
            
        Returns:
            CodeMetrics
        """
        lines = content.split('\n')
        
        loc = self._count_lines_of_code(lines)
        complexity = self._calculate_cyclomatic_complexity(content)
        nesting = self._calculate_max_nesting_depth(lines)
        functions = self._count_functions(content)
        variables = self._count_variables(content)
        comments_ratio = self._calculate_comment_ratio(lines)
        
        return CodeMetrics(
            lines_of_code=loc,
            cyclomatic_complexity=complexity,
            nesting_depth=nesting,
            functions_count=functions,
            variables_count=variables,
            comments_ratio=comments_ratio,
            code_coverage=0.0,  # Would need test data
        )

    def extract_dependencies(self, content: str) -> List[DependencyInfo]:
        """Extract program dependencies.
        
        Args:
            content: Program content
            
        Returns:
            List of dependencies
        """
        dependencies = []
        
        # Find CALL statements
        call_pattern = r"CALL\s+([A-Za-z0-9_]+)"
        for match in re.finditer(call_pattern, content, re.IGNORECASE):
            name = match.group(1)
            if name.upper() not in ["UB", "UN"]:
                dependencies.append(DependencyInfo(
                    name=name,
                    type="FUNCTION_CALL",
                    line_number=content[:match.start()].count('\n') + 1,
                ))
        
        # Find function block instantiations
        fb_pattern = r"([A-Za-z0-9_]+)\s*:\s*(FB|FUNCTION_BLOCK)\s*([A-Za-z0-9_]+)"
        for match in re.finditer(fb_pattern, content, re.IGNORECASE):
            dependencies.append(DependencyInfo(
                name=match.group(3),
                type="FUNCTION_BLOCK",
                line_number=content[:match.start()].count('\n') + 1,
            ))
        
        # Find data block references
        db_pattern = r"DB\s+(\d+)"
        for match in re.finditer(db_pattern, content, re.IGNORECASE):
            dependencies.append(DependencyInfo(
                name=f"DB{match.group(1)}",
                type="DATA_BLOCK",
                line_number=content[:match.start()].count('\n') + 1,
            ))
        
        # Remove duplicates
        seen = set()
        unique_deps = []
        for dep in dependencies:
            key = (dep.name, dep.type)
            if key not in seen:
                seen.add(key)
                unique_deps.append(dep)
        
        return unique_deps

    def _count_lines_of_code(self, lines: List[str]) -> int:
        """Count non-blank, non-comment lines.
        
        Args:
            lines: Code lines
            
        Returns:
            Line count
        """
        count = 0
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('//'):
                count += 1
        return count

    def _calculate_cyclomatic_complexity(self, content: str) -> float:
        """Calculate cyclomatic complexity.
        
        Args:
            content: Program content
            
        Returns:
            Complexity score
        """
        # Count decision points
        decision_keywords = [
            r"\bIF\b",
            r"\bTHEN\b",
            r"\bELSE\b",
            r"\bELSIF\b",
            r"\bFOR\b",
            r"\bWHILE\b",
            r"\bCASE\b",
            r"\bWHEN\b",
            r"\bJMPC\b",
            r"\bJMP\b",
        ]
        
        complexity = 1.0  # Base complexity
        for keyword in decision_keywords:
            matches = len(re.findall(keyword, content, re.IGNORECASE))
            if keyword == r"\bIF\b" or keyword == r"\bWHILE\b" or keyword == r"\bFOR\b":
                complexity += matches
            elif keyword == r"\bELSIF\b" or keyword == r"\bELSE\b":
                complexity += matches * 0.5
            elif keyword == r"\bCASE\b" or keyword == r"\bWHEN\b":
                complexity += matches * 0.5
        
        return complexity

    def _calculate_max_nesting_depth(self, lines: List[str]) -> int:
        """Calculate maximum nesting depth.
        
        Args:
            lines: Code lines
            
        Returns:
            Max nesting depth
        """
        max_depth = 0
        current_depth = 0
        
        nesting_start = [r"\bIF\b", r"\bFOR\b", r"\bWHILE\b", r"\bCASE\b", r"\bBEGIN\b"]
        nesting_end = [r"\bEND_IF\b", r"\bEND_FOR\b", r"\bEND_WHILE\b", r"\bEND_CASE\b", r"\bEND\b"]
        
        for line in lines:
            # Check for nesting start
            for start_pattern in nesting_start:
                if re.search(start_pattern, line, re.IGNORECASE):
                    current_depth += 1
                    max_depth = max(max_depth, current_depth)
            
            # Check for nesting end
            for end_pattern in nesting_end:
                if re.search(end_pattern, line, re.IGNORECASE):
                    current_depth = max(0, current_depth - 1)
        
        return max_depth

    def _count_functions(self, content: str) -> int:
        """Count functions and function blocks.
        
        Args:
            content: Program content
            
        Returns:
            Function count
        """
        patterns = [
            r"FUNCTION\s+([A-Za-z0-9_]+)",
            r"FUNCTION_BLOCK\s+([A-Za-z0-9_]+)",
            r"FC\s+\d+",
            r"FB\s+\d+",
        ]
        
        count = 0
        for pattern in patterns:
            count += len(re.findall(pattern, content, re.IGNORECASE))
        
        return count

    def _count_variables(self, content: str) -> int:
        """Count declared variables.
        
        Args:
            content: Program content
            
        Returns:
            Variable count
        """
        # Find VAR sections and count declarations
        var_pattern = r"\bVAR\b.*?\bEND_VAR\b"
        var_sections = re.findall(var_pattern, content, re.IGNORECASE | re.DOTALL)
        
        count = 0
        for section in var_sections:
            # Count lines that look like variable declarations
            lines = section.split('\n')
            for line in lines:
                if ':' in line and not line.strip().startswith('//') and 'VAR' not in line:
                    count += 1
        
        return count

    def _calculate_comment_ratio(self, lines: List[str]) -> float:
        """Calculate comment to code ratio.
        
        Args:
            lines: Code lines
            
        Returns:
            Comment ratio 0.0-1.0
        """
        comment_count = 0
        code_count = 0
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            
            if stripped.startswith('//'):
                comment_count += 1
            else:
                code_count += 1
        
        if code_count == 0:
            return 0.0
        
        return comment_count / (comment_count + code_count)
