#!/usr/bin/env python3
"""Basic example of using the TIA Portal Analyzer."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from portal_analyzer import PortalAnalyzerAgent, PortalProgramDetector
from portal_analyzer.utils import save_result_to_json


def example_detector():
    """Example using the detector directly."""
    print("=" * 60)
    print("EXAMPLE 1: Using PortalProgramDetector")
    print("=" * 60)
    
    detector = PortalProgramDetector(verbose=True)
    
    # Create a sample TIA Portal AWL file
    sample_file = "sample_program.awl"
    with open(sample_file, 'w') as f:
        f.write("""
TITLE "Sample TIA Portal Program"
AUTHOR "Developer"
VERSION 1.0

ORGANIZATION_BLOCK OB1
VAR
  counter : INT := 0;
  timer : TIME := T#0ms;
END_VAR
BEGIN
  NETWORK 1
  TITLE "Counter Logic"
  LD counter
  ADD 1
  ST counter
  
  NETWORK 2
  TITLE "Timer Logic"
  LD timer
  ADD T#100ms
  ST timer
END_ORGANIZATION_BLOCK
""")
    
    # Detect the file
    result = detector.detect_file(sample_file)
    
    print(f"\nDetection Result:")
    print(f"  Is TIA Portal: {result.is_tia_portal}")
    print(f"  Confidence: {result.confidence.value}")
    print(f"  Score: {result.confidence_score:.2%}")
    print(f"  Features: {', '.join(result.detected_features)}")
    
    if result.program_metadata:
        print(f"\nProgram Metadata:")
        print(f"  Name: {result.program_metadata.name}")
        print(f"  Type: {result.program_metadata.program_type.value}")
        print(f"  Language: {result.program_metadata.language.value}")
    
    # Cleanup
    Path(sample_file).unlink()


def example_agent():
    """Example using the AI Agent."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Using PortalAnalyzerAgent (AI-Powered)")
    print("=" * 60)
    
    agent = PortalAnalyzerAgent(verbose=True)
    
    # Create a more complex sample program
    sample_file = "sample_program_complex.awl"
    with open(sample_file, 'w') as f:
        f.write("""
TITLE "Complex TIA Portal Program"
VERSION 1.0

FUNCTION_BLOCK FB_Counter
VAR_INPUT
  reset : BOOL;
  enable : BOOL;
END_VAR
VAR_OUTPUT
  value : INT;
END_VAR
VAR
  counter : INT := 0;
END_VAR
BEGIN
  IF reset THEN
    counter := 0;
  ELSIF enable THEN
    IF counter < 100 THEN
      counter := counter + 1;
    ELSE
      counter := 0;
    END_IF;
  END_IF;
  
  value := counter;
END_FUNCTION_BLOCK

ORGANIZATION_BLOCK OB1
VAR
  fb_counter : FB_Counter;
  counter_output : INT;
END_VAR
BEGIN
  CALL fb_counter(
    reset := FALSE,
    enable := TRUE,
    value => counter_output
  );
END_ORGANIZATION_BLOCK
""")
    
    # Analyze with AI Agent
    result = agent.analyze_program(sample_file)
    
    # Print report
    print("\n" + result.report())
    
    # Save result to JSON
    save_result_to_json(result, "analysis_result.json")
    print("\nResult saved to: analysis_result.json")
    
    # Print agent reasoning
    print("\n" + "=" * 60)
    print("AGENT REASONING PROCESS")
    print("=" * 60)
    print(result.agent_reasoning)
    
    # Cleanup
    Path(sample_file).unlink()


if __name__ == "__main__":
    example_detector()
    example_agent()
    print("\n✓ Examples completed successfully!")
