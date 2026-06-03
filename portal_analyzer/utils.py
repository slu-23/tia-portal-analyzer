"""Utility functions for TIA Portal analyzer."""

import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
from .models import AnalysisResult


def save_result_to_json(result: AnalysisResult, output_path: str) -> None:
    """Save analysis result to JSON file.
    
    Args:
        result: AnalysisResult to save
        output_path: Output file path
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(result.model_dump(), f, indent=2, default=str)


def load_result_from_json(input_path: str) -> Dict[str, Any]:
    """Load analysis result from JSON file.
    
    Args:
        input_path: Input file path
        
    Returns:
        Loaded result dictionary
    """
    with open(input_path, 'r') as f:
        return json.load(f)


def generate_html_report(result: AnalysisResult, output_path: str) -> None:
    """Generate HTML report from analysis result.
    
    Args:
        result: AnalysisResult
        output_path: Output HTML file path
    """
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>TIA Portal Analysis Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f0f0; padding: 10px; border-radius: 5px; }}
        .section {{ margin-top: 20px; padding: 15px; border-left: 4px solid #0066cc; }}
        .metric {{ display: inline-block; margin: 10px 20px 10px 0; }}
        .high-risk {{ color: #d32f2f; font-weight: bold; }}
        .medium-risk {{ color: #f57c00; font-weight: bold; }}
        .low-risk {{ color: #388e3c; font-weight: bold; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f0f0f0; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>TIA Portal Program Analysis Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="section">
        <h2>Program Information</h2>
        <p><strong>File:</strong> {result.file_path}</p>
        <p><strong>Is TIA Portal:</strong> {result.detection_result.is_tia_portal}</p>
        <p><strong>Confidence:</strong> {result.detection_result.confidence.value} ({result.detection_result.confidence_score:.1%})</p>
    </div>
    
    <div class="section">
        <h2>Code Metrics</h2>
        <div class="metric">Lines of Code: <strong>{result.metrics.lines_of_code}</strong></div>
        <div class="metric">Complexity: <strong>{result.metrics.cyclomatic_complexity:.2f}</strong></div>
        <div class="metric">Nesting Depth: <strong>{result.metrics.nesting_depth}</strong></div>
        <div class="metric">Functions: <strong>{result.metrics.functions_count}</strong></div>
        <div class="metric">Variables: <strong>{result.metrics.variables_count}</strong></div>
    </div>
    
    <div class="section">
        <h2>Risk Assessment</h2>
        <p>Risk Score: <span class="high-risk">{result.risk_assessment.get('risk_score', 0):.1%}</span></p>
        <p>Complexity Level: <strong>{result.risk_assessment.get('complexity_level', 'Unknown')}</strong></p>
    </div>
    
    <div class="section">
        <h2>Recommendations</h2>
        <ul>
            {''.join(f'<li>{rec}</li>' for rec in result.recommendations)}
        </ul>
    </div>
</body>
</html>
    """
    
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write(html_content)
