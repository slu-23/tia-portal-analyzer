#!/usr/bin/env python3
"""Example of analyzing ladder diagram programs."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from portal_analyzer import PortalAnalyzerAgent, PortalProgramDetector
from portal_analyzer.utils import save_result_to_json


def example_ladder_diagram():
    """Example analyzing a ladder diagram program."""
    print("=" * 60)
    print("EXAMPLE: Analyzing Ladder Diagram Program (梯形图)")
    print("=" * 60)
    
    agent = PortalAnalyzerAgent(verbose=True)
    
    # Create a sample ladder diagram
    sample_file = "sample_ladder_diagram.ld"
    with open(sample_file, 'w') as f:
        f.write("""
TITLE "Pump Control Ladder Diagram"
AUTHOR "Control Engineer"
VERSION 1.0

NETWORK 1
TITLE "Start Button Logic"
LD start_button
AND pump_ready
AND NOT pump_running
OR auto_start
ST pump_run_signal

NETWORK 2  
TITLE "Pump Motor Control"
LD pump_run_signal
AND pressure_ok
AND NOT high_temp_alarm
S pump_motor_on

NETWORK 3
TITLE "Stop Logic"
LD stop_button
OR high_temp_alarm
OR pressure_fault
R pump_motor_on

NETWORK 4
TITLE "Output Status"
LD pump_motor_on
ST pump_output

NETWORK 5
TITLE "Alarm Indicator"
LD high_temp_alarm
OR pressure_fault
ST alarm_light

END_PROGRAM
""")
    
    # Analyze with AI Agent
    result = agent.analyze_program(sample_file)
    
    # Print report
    print("\n" + result.report())
    
    # Save result
    save_result_to_json(result, "ladder_diagram_analysis.json")
    print("\nResult saved to: ladder_diagram_analysis.json")
    
    # Print agent reasoning
    print("\n" + "=" * 60)
    print("AGENT REASONING PROCESS")
    print("=" * 60)
    print(result.agent_reasoning)
    
    # Cleanup
    Path(sample_file).unlink()


def example_detector_ladder():
    """Example detecting ladder diagram files."""
    print("\n" + "=" * 60)
    print("DETECTOR: Identifying Ladder Diagram Files")
    print("=" * 60)
    
    detector = PortalProgramDetector(verbose=True)
    
    # Create a ladder diagram file
    sample_file = "simple_control.ld"
    with open(sample_file, 'w') as f:
        f.write("""
NETWORK 1
LD input1
AND input2
OR input3
ST output1

NETWORK 2
LD output1
AND timer1
S output2

END_PROGRAM
""")
    
    # Detect
    result = detector.detect_file(sample_file)
    
    print(f"\nDetection Result:")
    print(f"  Is TIA Portal: {result.is_tia_portal}")
    print(f"  Confidence: {result.confidence.value}")
    print(f"  Score: {result.confidence_score:.2%}")
    print(f"  Language: {result.program_metadata.language.value if result.program_metadata else 'N/A'}")
    print(f"  Features: {', '.join(result.detected_features)}")
    
    # Cleanup
    Path(sample_file).unlink()


if __name__ == "__main__":
    example_detector_ladder()
    example_ladder_diagram()
    print("\n✓ Ladder diagram examples completed successfully!")
