# Yosys 综合流程

## 脚本
- `synth_generic.tcl`: 通用综合 (无工艺映射)
- `synth_nangate45.tcl`: Nangate45 门级综合

## 用法
```bash
cd yosys/
./run_yosys.sh rs232    # 综合 RS232 模块
./run_yosys.sh aes      # 综合 AES 模块
```

## 输出
- `../netlist/generic/<design>_generic.v` — 通用网表
- `../netlist/gate/<design>_gate.v` — 门级网表 (Nangate45)
