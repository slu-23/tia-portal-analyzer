# TIA Portal Analyzer - AI-Powered Program Detector

An intelligent AI Agent system for automatically detecting, analyzing, and classifying TIA Portal (Siemens S7) PLC programs.

## Features

✨ **AI-Powered Detection**
- Automatic identification of TIA Portal program structures
- PLC program type classification (FB, FC, OB, DB)
- Code pattern recognition and analysis
- Intelligent XML/AWL/SCL syntax detection

🤖 **Agent Capabilities**
- Multi-step analysis pipeline
- Intelligent decision-making based on program characteristics
- Detailed program metadata extraction
- Risk and complexity assessment

📊 **Analysis Features**
- Program structure analysis
- Function block identification
- Data block parsing
- Dependency tracking
- Quality metrics calculation

## Installation

```bash
git clone https://github.com/slu-23/tia-portal-analyzer.git
cd tia-portal-analyzer
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from portal_analyzer.agent import PortalAnalyzerAgent
from portal_analyzer.detector import PortalProgramDetector

# Initialize detector
detector = PortalProgramDetector()

# Analyze a file
result = detector.analyze_file("path/to/program.xml")
print(result)

# Or use the AI Agent for intelligent analysis
agent = PortalAnalyzerAgent()
analysis = agent.analyze_program("path/to/program.awl")
print(analysis.report())
```

### Command Line

```bash
python -m portal_analyzer.cli analyze --file program.xml --format json
python -m portal_analyzer.cli detect --directory ./plc_programs --recursive
python -m portal_analyzer.cli report --input analysis.json --output report.html
```

## Project Structure

```
tia-portal-analyzer/
├── portal_analyzer/
│   ├── __init__.py
│   ├── agent.py              # AI Agent implementation
│   ├── detector.py           # Program detection engine
│   ├── analyzer.py           # Analysis engine
│   ├── parser.py             # TIA Portal format parser
│   ├── classifier.py         # Program type classifier
│   ├── models.py             # Data models
│   ├── utils.py              # Utility functions
│   └── cli.py                # Command-line interface
├── tests/
│   ├── __init__.py
│   ├── test_detector.py
│   ├── test_agent.py
│   └── test_analyzer.py
├── examples/
│   ├── sample_program.xml
│   ├── sample_program.awl
│   └── example_analysis.py
├── requirements.txt
├── setup.py
└── README.md
```

## TIA Portal Program Types

The analyzer can identify:

- **OB (Organization Block)** - Cyclic programs, interrupt handlers
- **FC (Function)** - Reusable code blocks without memory
- **FB (Function Block)** - Stateful reusable code blocks
- **DB (Data Block)** - Instance data storage
- **UDT (User Defined Type)** - Custom data structures

## Supported Formats

- XML (TIA Portal native format)
- AWL/STL (Statement List)
- SCL (Structured Control Language)
- GRAPH (Sequential function chart)

## AI Agent Architecture

The system uses a multi-stage AI Agent approach:

1. **Reconnaissance** - File format detection and initial parsing
2. **Analysis** - Deep code structure analysis
3. **Classification** - Program type and purpose classification
4. **Assessment** - Quality, complexity, and risk assessment
5. **Reporting** - Comprehensive analysis report generation

## Configuration

Create a `config.yaml` file:

```yaml
analyzer:
  max_file_size: 10MB
  timeout: 30
  recursive_analysis: true
  
detector:
  confidence_threshold: 0.8
  enable_ml_features: true
  
agent:
  verbose_mode: true
  save_intermediate_results: false
```

## API Reference

See [API Documentation](./docs/api.md) for detailed API reference.

## Examples

Check the `examples/` directory for complete working examples.

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](./CONTRIBUTING.md).

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## References

- [Siemens TIA Portal Documentation](https://support.industry.siemens.com/)
- [S7 PLC Programming Guide](https://support.industry.siemens.com/)
- [IEC 61131-3 Standard](https://en.wikipedia.org/wiki/IEC_61131-3)
