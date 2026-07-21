# HAL Python API Guide — 本项目已验证用法

## Official API Reference

API 查找优先级：
1. **本项目 docs/** (YOSYS_GUIDE, HAL_GUIDE, HAL_PLUGIN_GUIDE)
2. HAL Core Python API: https://emsec.github.io/hal/pydoc/hal_py.html
3. HAL Plugins Python API: https://emsec.github.io/hal/pydoc/plugins.html
4. C++ Doxygen: https://emsec.github.io/hal/doc/modules.html

## 导入

```python
import hal_py
```

项目中推荐延迟导入（`import hal_py` 放在函数内），避免未安装环境下的 ImportError。

## API 对照表 — 常见错误 vs 正确写法

### 网表加载

| ❌ 错误 | ✅ 正确 |
|----------|----------|
| `hal_py.create_netlist(path)` | `hal_py.NetlistFactory.load_netlist(path, hgl_path)` |
| 直接 load 不加载插件 | **先** `hal_py.plugin_manager.load_all_plugins([dir])` |

```python
# 完整加载流程
hal_py.plugin_manager.load_all_plugins(["/home/i/hal/build/lib/hal_plugins/"])
netlist = hal_py.NetlistFactory.load_netlist("/path/to/netlist.v", "/path/to/library.hgl")
```

### Gate 操作

| ❌ 错误 | ✅ 正确 |
|----------|----------|
| `gate.get_input_pins()` | `gate.get_fan_in_nets()` 返回 net 列表 |
| `gate.get_output_pins()` | `gate.get_fan_out_nets()` 返回 net 列表 |
| `gate.get_fan_in()` | `gate.get_fan_in_nets()` |
| `gate.get_fan_out()` | `gate.get_fan_out_nets()` |

```python
# 正确
gates = netlist.get_gates()
for gate in gates:
    gtype = gate.get_type().get_name()       # e.g. "DFFR_X1", "AND2_X1"
    fan_in = list(gate.get_fan_in_nets())    # list[Net]
    fan_out = list(gate.get_fan_out_nets())  # list[Net]
```

### Net 操作

| ❌ 错误 | ✅ 正确 |
|----------|----------|
| `net.is_primary_input()` | `net.is_global_input_net()` |
| `net.is_primary_output()` | `net.is_global_output_net()` |

```python
# 正确
for net in netlist.get_nets():
    sources = net.get_sources()          # 驱动源
    dests = net.get_destinations()       # 负载
    if net.is_global_input_net(): ...    # 顶层输入
    if net.is_global_output_net(): ...   # 顶层输出
```

### Pin 操作

| ❌ 错误 | ✅ 正确 |
|----------|----------|
| `pin.get_direction() == "input"` | `pin.get_direction() == hal_py.PinDirection.input` |
| `pin.get_direction() == "output"` | `pin.get_direction() == hal_py.PinDirection.output` |

**`PinDirection` 是 enum，不是字符串。**

```python
import hal_py

for pin in module.get_pins():
    if pin.get_direction() == hal_py.PinDirection.input:
        print(f"Input:  {pin.get_name()}")
    elif pin.get_direction() == hal_py.PinDirection.output:
        print(f"Output: {pin.get_name()}")
```

### Module 操作

```python
modules = netlist.get_modules()
top = netlist.get_top_module()

for m in modules:
    m.get_name()           # 模块名
    m.get_gates()          # 本模块的门
    m.get_pins()           # IO 端口
    m.get_submodules()     # 子模块
```

### 插件操作

```python
# 批量加载所有 .so
hal_py.plugin_manager.load_all_plugins(["/home/i/hal/build/lib/hal_plugins/"])

# 列出可用插件
hal_py.plugin_manager.get_plugin_names()

# 获取插件实例
hal_py.plugin_manager.get_plugin_instance("dataflow")
```

## 类型判断

```python
def is_sequential(gate) -> bool:
    """判断是否为时序元件。"""
    gtype = gate.get_type().get_name().upper()
    return any(k in gtype for k in ("DFF", "SDFF", "LATCH", "DLATCH"))
```

## 已知问题

- **进程退出 segfault (exit 139)**：HAL Python bindings 在进程退出时崩溃，属已知良性 bug。
  所有数据在 segfault 前已处理完毕，可安全忽略。
