# NangateOpenCellLibrary

标准单元库文件，用于 Yosys 门级综合和 HAL 网表加载。

## 文件
- `NangateOpenCellLibrary.lib`: Liberty 格式时序库
- `NangateOpenCellLibrary.hgl`: HAL Gate Library 格式

## 来源
Nangate 45nm Open Cell Library (FreePDK45)

## 用途
- Yosys `synth_nangate45.tcl` 引用 `.lib` 进行工艺映射
- HAL `hal_loader.py` 引用 `.hgl` 进行门级网表解析
