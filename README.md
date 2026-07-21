# HAL Trojan Agent

基于 HAL (Hardware Analyzer) 的硬件木马检测框架。

## 目录结构

```
hal_trojan_agent/
├── library/          # 标准单元库 (.lib, .hgl)
├── rtl/              # 输入 RTL 设计
├── yosys/            # Yosys 综合脚本
├── netlist/          # 综合输出网表
├── hal/              # HAL Python 接口
├── analysis/         # 木马检测基础分析模块
├── strategies/       # 检测策略库
├── tools/            # HAL 插件封装
├── agent/            # Agent 核心 (路由/规划/执行/报告)
├── llm/              # LLM 接口与 prompt
├── langgraph/        # LangGraph 工作流
├── experiments/      # 实验记录与结果
└── docs/             # 文档
```

## 快速开始

```bash
pip install -r requirements.txt
python -m agent.router --help
```
