# TIA Portal 分析器 - AI驱动的程序检测工具

一个智能AI Agent系统，用于自动检测、分析和分类TIA Portal（西门子S7）PLC程序。

## 功能特性

✨ **AI智能检测**
- 自动识别TIA Portal程序结构
- PLC程序类型分类（FB、FC、OB、DB）
- 代码模式识别和分析
- 智能XML/AWL/SCL/LD语法检测

🤖 **Agent智能体能力**
- 多步骤分析流程
- 基于程序特征的智能决策
- 详细的程序元数据提取
- 风险和复杂度评估

📊 **分析功能**
- 程序结构分析
- 功能块识别
- 数据块解析
- 依赖关系追踪
- 质量指标计算
- 梯形图（LD）专用分析

## 安装

```bash
git clone https://github.com/slu-23/tia-portal-analyzer.git
cd tia-portal-analyzer
pip install -r requirements.txt
```

## 快速开始

### 基础用法

```python
from portal_analyzer.agent import PortalAnalyzerAgent
from portal_analyzer.detector import PortalProgramDetector

# 初始化检测器
detector = PortalProgramDetector()

# 分析文件
result = detector.analyze_file("path/to/program.xml")
print(result)

# 或使用AI Agent进行智能分析
agent = PortalAnalyzerAgent()
analysis = agent.analyze_program("path/to/program.awl")
print(analysis.report())
```

### 命令行使用

```bash
python -m portal_analyzer.cli analyze --file program.xml --format json
python -m portal_analyzer.cli detect --directory ./plc_programs --recursive
python -m portal_analyzer.cli report --input analysis.json --output report.html
```

## 项目结构

```
tia-portal-analyzer/
├── portal_analyzer/
│   ├── __init__.py
│   ├── agent.py              # AI Agent实现
│   ├── detector.py           # 程序检测引擎
│   ├── analyzer.py           # 分析引擎
│   ├── parser.py             # TIA Portal格式解析器
│   ├── classifier.py         # 程序类型分类器
│   ├── models.py             # 数据模型
│   ├── utils.py              # 工具函数
│   └── cli.py                # 命令行接口
├── tests/
│   ├── __init__.py
│   ├── test_detector.py
│   ├── test_agent.py
│   └── test_analyzer.py
├── examples/
│   ├── sample_program.xml
│   ├── sample_program.awl
│   ├── example_basic.py
│   └── example_ladder_diagram.py
├── requirements.txt
├── setup.py
└── README.md
```

## TIA Portal程序类型

分析器可以识别以下程序类型：

- **OB（组织块）** - 循环程序、中断处理程序
- **FC（函数）** - 无内存的可重用代码块
- **FB（功能块）** - 有状态的可重用代码块
- **DB（数据块）** - 实例数据存储
- **UDT（用户定义类型）** - 自定义数据结构

## 支持的编程语言

- **XML** - TIA Portal原生格式
- **AWL/STL** - 语句表（指令表）
- **SCL** - 结构化文本
- **LD** - 梯形图（新增）
- **GRAPH** - 顺序功能图

## AI Agent架构

系统采用多阶段AI Agent方法：

1. **侦察阶段** - 文件格式检测和初始解析
2. **分析阶段** - 深度代码结构分析
3. **分类阶段** - 程序类型和目的分类
4. **评估阶段** - 质量、复杂度和风险评估
5. **报告阶段** - 生成综合分析报告

### 多步骤推理流程

Agent分析过程包括4个主要阶段：

```
[阶段1] 侦察 - 检测程序类型
         ↓
[阶段2] 深度分析 - 代码结构与指标分析
         ↓
[阶段3] 评估 - 质量和风险评估
         ↓
[阶段4] 建议 - 生成改进建议
```

## 配置

创建 `config.yaml` 文件：

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

## 使用示例

### 基础分析

```python
from portal_analyzer import PortalAnalyzerAgent

# 初始化Agent
agent = PortalAnalyzerAgent(verbose=True)

# 分析单个程序
result = agent.analyze_program("pump_control.ld")

# 打印报告
print(result.report())

# 打印AI推理过程
print(result.agent_reasoning)
```

### 梯形图分析

```python
# 梯形图专用分析
result = agent.analyze_program("control_logic.ld")

# 获取梯形图特定指标
print(f"网络数量: {result.metrics.rung_count}")
print(f"接触点数: {result.metrics.contact_count}")
print(f"线圈数: {result.metrics.coil_count}")
```

### 批量分析

```python
# 批量分析目录中的所有PLC程序
results = agent.batch_analyze("./plc_programs", recursive=True)

# 获取分析摘要
summary = agent.get_summary()
print(f"总分析数: {summary['total_analyses']}")
print(f"TIA Portal程序数: {summary['tia_portal_programs']}")
```

### 检测器使用

```python
from portal_analyzer import PortalProgramDetector

detector = PortalProgramDetector(verbose=True)

# 检测文件
result = detector.detect_file("my_program.xml")

print(f"是否为TIA Portal程序: {result.is_tia_portal}")
print(f"置信度: {result.confidence.value}")
print(f"置信分数: {result.confidence_score:.2%}")
print(f"检测到的特征: {result.detected_features}")

if result.program_metadata:
    print(f"程序类型: {result.program_metadata.program_type.value}")
    print(f"编程语言: {result.program_metadata.language.value}")
```

## API文档

详见 [API文档](./docs/api.md)

## 示例

查看 `examples/` 目录获取完整的工作示例：

- `example_basic.py` - 基础使用示例
- `example_ladder_diagram.py` - 梯形图分析示例

运行示例：

```bash
python examples/example_basic.py
python examples/example_ladder_diagram.py
```

## 梯形图支持

TIA Portal分析器现已完全支持梯形图（LD）编程语言：

### 支持的梯形图元素

| 元素 | 符号 | 支持状态 |
|------|------|--------|
| 网络 | NETWORK | ✅ |
| 加载指令 | LD | ✅ |
| 存储指令 | ST | ✅ |
| 逻辑与 | AND | ✅ |
| 逻辑或 | OR | ✅ |
| 逻辑非 | NOT | ✅ |
| 异或 | XOR | ✅ |
| 设置线圈 | S | ✅ |
| 重置线圈 | R | ✅ |
| 取反接触点 | /\| | ✅ |

### 梯形图分析指标

- **运行数（Rungs）** - 梯形图网络的数量
- **接触点数（Contacts）** - 所有输入接触点的计数
- **线圈数（Coils）** - 所有输出线圈的计数
- **复杂度分析** - 基于接触点和线圈的复杂性评估

## 输出报告

分析结果包含以下信息：

```
============================================================
TIA PORTAL PROGRAM ANALYSIS REPORT
============================================================

File: pump_control.ld
Analysis Time: 2026-06-03 10:59:42

--- DETECTION RESULTS ---
Is TIA Portal Program: True
Confidence Level: HIGH
Confidence Score: 95.00%

--- PROGRAM METADATA ---
Name: pump_control
Type: OB
Language: LD
File Size: 2048 bytes

--- CODE METRICS ---
Lines of Code: 45
Cyclomatic Complexity: 3.50
Nesting Depth: 2
Functions: 1
Variables: 8

--- LADDER DIAGRAM METRICS ---
Rungs: 5
Contacts: 12
Coils: 4

--- RECOMMENDATIONS ---
1. Add more code comments and documentation for better maintainability
2. Consider adding unit tests for critical functions
3. Document all public interfaces and function signatures

--- AGENT ANALYSIS ---
[AGENT] Starting analysis of pump_control.ld
[STAGE 1] RECONNAISSANCE - Detecting program type...
  ✓ Detection confidence: HIGH
  ✓ Detected features: Ladder diagram patterns detected
[STAGE 2] DEEP ANALYSIS - Analyzing code structure...
  ✓ Lines of code: 45
...
```

## 贡献

欢迎贡献！请阅读我们的 [贡献指南](./CONTRIBUTING.md)。

## 许可证

MIT许可证 - 详见LICENSE文件

## 支持

如有问题、建议或反馈，请在GitHub上提出issue。

## 相关资源

- [西门子TIA Portal文档](https://support.industry.siemens.com/)
- [S7 PLC编程指南](https://support.industry.siemens.com/)
- [IEC 61131-3标准](https://en.wikipedia.org/wiki/IEC_61131-3)

---

**作者**: slu-23  
**项目链接**: [GitHub仓库](https://github.com/slu-23/tia-portal-analyzer)  
**最后更新**: 2026年6月
