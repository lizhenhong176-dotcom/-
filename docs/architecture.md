# HAL Trojan Agent 架构

## 概述
基于 HAL 框架的多层次硬件木马检测系统。采用 Agent 模式：分析→策略路由→LLM推理→报告。

## 架构图

```
┌──────────────────────────────────────────────────┐
│                   Agent Core                      │
│  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │  Router  │→ │ Planner  │→ │   Executor    │  │
│  └──────────┘  └──────────┘  └───────────────┘  │
│        │                            │            │
│        ▼                            ▼            │
│  ┌──────────┐                 ┌──────────┐      │
│  │ Strategies│                │  Report   │      │
│  └──────────┘                 └──────────┘      │
└──────────────────────────────────────────────────┘
         │              │              │
         ▼              ▼              ▼
┌──────────┐   ┌──────────┐   ┌──────────┐
│ HAL API  │   │  Tools   │   │   LLM    │
└──────────┘   └──────────┘   └──────────┘
      │
      ▼
┌──────────┐
│ Netlist  │  (Yosys 综合输出)
└──────────┘
```

## 核心组件

### 1. HAL 接口层 (`hal/`)
- `hal_loader.py`: 网表加载，插件初始化
- `hal_utils.py`: 通用工具函数
- `plugin_manager.py`: 插件生命周期管理

### 2. 分析层 (`analysis/`)
- `module_analysis.py`: 模块级 — 层次结构、功能分类
- `gate_analysis.py`: 门级 — 异常门类型、冗余逻辑
- `net_analysis.py`: 网表级 — 连接性、悬空网表
- `register_analysis.py`: 寄存器级 — 时钟域、可疑寄存器
- `cone_analysis.py`: 锥形分析 — I/O 逻辑锥体追踪

### 3. 策略层 (`strategies/`)
- `uart_strategy.py`: UART 接口木马
- `crypto_strategy.py`: 加密模块木马
- `fsm_strategy.py`: FSM 状态机木马
- `dataflow_strategy.py`: 数据流异常
- `output_cone_strategy.py`: 输出锥体木马

### 4. 工具层 (`tools/`)
封装 HAL 五个核心插件：dataflow, fsm, graph, simulator, influence

### 5. Agent 核心 (`agent/`)
- `router.py`: 策略路由选择
- `planner.py`: 分析计划生成
- `executor.py`: 步骤调度执行
- `report.py`: 报告生成 (Markdown/JSON)

### 6. LLM 接口 (`llm/`)
- `llm_client.py`: Anthropic/OpenAI 统一客户端
- `prompt/`: 分类和报告分析 prompt 模板

### 7. LangGraph 工作流 (`langgraph/`)
- `workflow.py`: 状态图定义
- `nodes.py`: 各节点实现

## 数据流

```
RTL → Yosys → Gate Netlist → HAL Load → Module Analysis
                                              │
                    ┌─────────────────────────┘
                    ▼
            Gate/Net/Register/Cone Analysis
                    │
                    ▼
            Module Classification (LLM)
                    │
                    ▼
            Strategy Router → Match & Execute
                    │
                    ▼
            LLM Review & Report Generation
```

## 扩展点
- 新策略: 继承 `BaseStrategy`，实现 `analyze()` 和 `applicable_to()`
- 新工具: 封装 HAL 其他插件
- 新分析: 在 `analysis/` 添加模块，在 `Planner.DEFAULT_STEPS` 注册
