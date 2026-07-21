# Yosys Usage Guide

## Official Documentation

- Main: https://yosyshq.readthedocs.io/
- Command Reference: https://yosyshq.readthedocs.io/projects/yosys/en/latest/cmd/
- Source: https://github.com/YosysHQ/yosys

**Current version: Yosys 0.57**

## TCL Script Mode (`-c` flag)

使用 `yosys -c script.tcl` 时，**所有 Yosys 命令必须加 `yosys` 前缀**：

```tcl
# 正确
yosys read_verilog design.v
yosys hierarchy -check -top top_module
yosys proc
yosys opt

# 错误 — 缺少 yosys 前缀
read_verilog design.v
hierarchy -check -top top_module
```

## 参数传递

Yosys `-c` 模式下 `$argv` 会被当作输入文件处理。用**环境变量**传参：

```bash
# 正确
YOSYS_DESIGN="rs232" yosys -c synth.tcl
```

```tcl
# TCL 中读取
set design $env(YOSYS_DESIGN)
```

## Nangate45 标准综合流程

```tcl
set design $env(YOSYS_DESIGN)
set rtl_dir "../rtl/${design}"
set top "uart"

# 读取源文件
foreach f [glob -nocomplain ${rtl_dir}/*.v] {
    yosys read_verilog -I${rtl_dir} $f
}

yosys hierarchy -check -top $top
yosys proc
yosys opt
yosys fsm
yosys memory
yosys opt
yosys techmap

# Nangate45 工艺映射
yosys dfflibmap -liberty /usr/local/share/yosys/NangateOpenCellLibrary_typical.lib
yosys abc -liberty /usr/local/share/yosys/NangateOpenCellLibrary_typical.lib

yosys clean
yosys write_verilog ../netlist/gate/${design}_gate.v
```

## 已知问题

- **TCL 中文注释导致解析失败**：Yosys 0.57 TCL 解释器遇到 UTF-8 中文字符会误解析后续行。
  所有 `.tcl` 脚本用 ASCII-only 注释。

- `-T` 标志只抑制 footer，不加载脚本。用 `-c` 加载 TCL。

## 项目脚本位置

- `yosys/run_yosys.sh` — 综合入口
- `yosys/scripts/synth_nangate45.tcl` — Nangate45 工艺综合
- `yosys/scripts/synth_generic.tcl` — 通用综合（调试用）
