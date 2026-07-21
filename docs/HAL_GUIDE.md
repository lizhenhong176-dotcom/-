# HAL Hardware Analyzer Guide

## Official Documentation

- Docs: https://emsec.github.io/hal/doc/
- GitHub: https://github.com/emsec/hal
- Wiki: https://github.com/emsec/hal/wiki

## HAL 在项目中的角色

```
Gate-level Netlist (.v)
        │
        ▼
    HAL Loader ─── Gate Library (.hgl)
        │
        ├── Module Analysis
        ├── Gate Analysis
        ├── Register Analysis
        ├── Net Analysis
        └── Cone Analysis
                │
                ▼
        Analysis JSON ─── Agent Router ─── Detection Strategies
```

## 核心概念

| 概念 | 说明 | API |
|------|------|-----|
| **Gate** | 基本逻辑单元 (AND, OR, DFF, MUX...) | `netlist.get_gates()` |
| **Net** | 门之间的连线 | `netlist.get_nets()` |
| **Module** | 设计层次模块 | `netlist.get_modules()` |
| **Fan-in** | 门的输入依赖 | `gate.get_fan_in_nets()` |
| **Fan-out** | 门的输出驱动 | `gate.get_fan_out_nets()` |
| **Pin** | 模块 IO 端口 | `module.get_pins()` |
| **Top Module** | 顶层模块 | `netlist.get_top_module()` |

## 加载流程

```
1. hal_py.plugin_manager.load_all_plugins([PLUGIN_DIR])
2. hal_py.NetlistFactory.load_netlist(netlist_path, hgl_path)
3. 分析 passes
```

**必须**先加载插件再加载网表，否则 HGL parser 不工作。

## 已知 Bug

- **HAL Python bindings segfault on exit (exit code 139)**：分析完成后进程崩溃，不影响结果。
  JSON 在 segfault 前已写入，可安全忽略。
