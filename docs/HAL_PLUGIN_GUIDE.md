# HAL Plugin Guide

## Official Documentation

- Plugin docs: https://emsec.github.io/hal/doc/group__plugins.html
- Source: https://github.com/emsec/hal

## 本项目可用插件

| 插件名 | .so 文件 | 用途 |
|--------|----------|------|
| `verilog_parser` | `verilog_parser.so` | Verilog 门级网表解析 |
| `hgl_parser` | `hgl_parser.so` | HGL 门库解析 |
| `liberty_parser` | `liberty_parser.so` | Liberty 门库解析 |
| `dataflow` | `dataflow.so` | 数据流方向分析 |
| `solve_fsm` | `solve_fsm.so` | FSM 提取与分析 |
| `graph_algorithm` | `graph_algorithm.so` | 图算法（连通分量、环路） |
| `netlist_simulator` | `netlist_simulator_controller.so` | 网表仿真 |
| `hawkeye` | `hawkeye.so` | 结构异常检测 |
| `z3_utils` | `z3_utils.so` | SMT 形式验证 |
| `boolean_influence` | — | 布尔影响力分析 |
| `verilog_writer` | `verilog_writer.so` | Verilog 导出 |
| `gexf_writer` | `gexf_writer.so` | GEXF 图导出 |

## 加载时机

```python
import hal_py

# 必须在 load_netlist 之前！
hal_py.plugin_manager.load_all_plugins(["/home/i/hal/build/lib/hal_plugins/"])

# 然后才能加载网表
netlist = hal_py.NetlistFactory.load_netlist(path, hgl_path)
```

**不先加载插件就 load_netlist → HGL parser 不工作 → 加载失败。**

## PLUGIN_DIR

```
/home/i/hal/build/lib/hal_plugins/
```

项目 `config.yaml` 中配置：`hal.plugin_dir`

## 插件封装的 Python 类

项目中 `tools/` 目录封装了常用插件：

| 类 | 封装的插件 | 文件 |
|----|-----------|------|
| `DataflowTool` | `dataflow` | `tools/dataflow_tool.py` |
| `FSMTool` | `solve_fsm` | `tools/fsm_tool.py` |
| `GraphTool` | `graph_algorithm` | `tools/graph_tool.py` |
| `SimulatorTool` | `netlist_simulator` | `tools/simulator_tool.py` |
| `InfluenceTool` | `boolean_influence` | `tools/influence_tool.py` |

## 插件管理

`hal/plugins.py` 的 `Plugins` 类负责统一管理插件生命周期：

```python
from hal.plugins import Plugins

pm = Plugins()
result = pm.load_all()      # 返回 {"dataflow": True, "solve_fsm": True, ...}
df = pm.dataflow            # 便捷属性访问
fsm = pm.fsm
```
