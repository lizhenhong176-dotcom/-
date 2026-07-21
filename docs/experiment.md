# 实验设计

## 实验目标
验证 HAL Trojan Agent 在多种木马场景下的检测能力。

## 实验设计

### 测试设计
1. **RS232 UART** — 通信接口木马
2. **AES-128** — 加密模块木马

### 木马类型覆盖

| 木马类型 | 描述 | RS232 | AES |
|----------|------|-------|-----|
| 数据泄漏 | 敏感数据通过非预期路径输出 | TX泄漏 | 密钥泄漏 |
| 功能篡改 | 修改核心功能 | 波特率篡改 | S-Box弱化 |
| FSM隐藏 | 隐藏状态/转换 | 中断异常 | 轮数减少 |
| 侧信道 | 通过侧信道泄漏 | - | 功耗泄漏 |
| 死域触发 | rare-trigger 条件激活 | 特殊字符触发 | 特殊明文触发 |

### 评估指标

| 指标 | 含义 |
|------|------|
| 检出率 (TPR) | 正确检出的木马比例 |
| 漏报率 (FNR) | 未能检出的木马比例 |
| 误报率 (FPR) | 误报为木马的比例 |
| 分析时间 | 端到端分析耗时 |
| 置信度 | 检测结果的平均置信度 |

## 运行

```bash
# RS232 实验
python -m langgraph.workflow --design rs232 --netlist netlist/gate/rs232_gate.v

# AES 实验
python -m langgraph.workflow --design aes --netlist netlist/gate/aes_gate.v
```

## 结果记录
结果输出到 `experiments/results/`。
