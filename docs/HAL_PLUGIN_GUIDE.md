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

## 已验证插件 API (Phase 2)

插件 `.so` 通过 `hal_py.plugin_manager.load_all_plugins()` 注册后，
**需单独 `__import__()` 导入以获取 Python API**：

```python
import hal_py
hal_py.plugin_manager.load_all_plugins(["/home/i/hal/build/lib/hal_plugins/"])
# 加载网表后：
import graph_algorithm as ga
import dataflow
import solve_fsm
```

### graph_algorithm (100% 验证通过)

| API | 签名 |
|-----|------|
| `NetlistGraph.from_netlist` | `(Netlist, bool=False, filter=None) → NetlistGraph` |
| `graph.get_num_vertices` | `(only_connected=False) → int` |
| `graph.get_num_edges` | `() → int` |
| `graph.get_vertex_from_gate` | `(Gate) → int` |
| `graph.get_gate_from_vertex` | `(int) → Gate` |
| `get_connected_components` | `(graph, strong, min_size=0) → list[list[int]]` |
| `get_neighborhood` | `(graph, list[Gate], order, Direction, min_dist=0) → list[list[int]]` |
| `get_shortest_paths` | `(graph, from_gate, list[Gate], Direction) → list[list[int]]` |
| `get_subgraph` | `(graph, list[Gate]) → NetlistGraph` |
| `Direction` enum | `NONE, IN, OUT, ALL` (on `NetlistGraph.Direction`) |

### dataflow (DANA) (API 正确，小设计可能返回 None)

| API | 签名 |
|-----|------|
| `dataflow.Configuration` | `(Netlist) → Configuration` |
| `dataflow.analyze` | `(Configuration) → Result | None` |
| `Result.get_groups` | `() → dict[int, set[Gate]]` |
| `Result.get_gate_predecessors` | `(Gate) → set[Gate]` |
| `Result.get_gate_successors` | `(Gate) → set[Gate]` |
| `Result.get_group_id_of_gate` | `(Gate) → int | None` |
| `Result.get_gates_of_group` | `(int) → set[Gate] | None` |

### solve_fsm (API 正确，需选对状态寄存器)

| API | 签名 |
|-----|------|
| `solve_fsm.solve_fsm_brute_force` | `(Netlist, list[Gate], list[Gate]) → dict[int, dict[int, BooleanFunction]] | None` |
| `solve_fsm.solve_fsm` | `(Netlist, list[Gate], list[Gate], initial_state=dict, timeout=600000) → dict | None` |
| `solve_fsm.generate_dot_graph` | `(list[Gate], dict, str, max_len=128, base=10) → None` |

### netlist_simulator (API 待验证)

模块可导入: `NetlistSimulator`, `NetlistSimulatorPlugin`, `Simulation`

### boolean_influence (未编译)

当前 HAL build 不含此插件。
