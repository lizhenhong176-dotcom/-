# CLAUDE.md - HAL Trojan Agent 项目说明

## 项目目标
基于 HAL 框架的硬件木马自动检测系统。读取综合后的门级网表，利用 HAL 插件进行结构/功能分析，通过 LLM 驱动的策略引擎识别潜在木马。

## 技术栈
- **综合**: Yosys + Nangate45 标准单元库
- **分析**: HAL (C++ core + Python API)
- **AI**: LLM (Claude API) + LangGraph 工作流
- **语言**: Python 3.10+

## 工作流程
```
RTL → Yosys综合 → 门级网表 → HAL加载 → 
  ├── 模块分析 (module_analysis)
  ├── 门级分析 (gate_analysis)  
  ├── 网表分析 (net_analysis)
  ├── 寄存器分析 (register_analysis)
  └── 锥形分析 (cone_analysis)
    → Agent路由 → 策略匹配 → LLM推理 → 报告生成
```

## 关键文件
- `hal/hal_loader.py`: HAL 网表加载器
- `agent/router.py`: 策略路由器
- `tools/`: HAL 插件封装层
- `strategies/`: 各类型木马检测策略
- `llm/prompt/`: LLM prompt 模板
- `langgraph/workflow.py`: LangGraph 工作流定义

## 开发约定
- Python 类型标注 (typing)
- 策略模式用于检测策略扩展
- 所有分析模块返回统一的数据结构
