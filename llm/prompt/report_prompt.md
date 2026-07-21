# 木马检测报告分析 Prompt

你是硬件安全专家。基于以下检测数据，分析该设计中是否存在硬件木马。

## 设计信息
- 设计名: {{design_name}}
- 总门数: {{total_gates}}
- 总网表数: {{total_nets}}
- 总寄存器数: {{total_registers}}

## 分析结果

### 模块分析
{{module_analysis}}

### 门级分析
{{gate_analysis}}

### 寄存器分析
{{register_analysis}}

### 锥形分析
{{cone_analysis}}

### 策略检测结果
{{strategy_results}}

## 任务
1. 判断设计是否可能包含硬件木马 (是/否/不确定)
2. 列出最可疑的 3 个区域
3. 给出风险评级 (低/中/高/严重)
4. 提供进一步验证建议

## 输出格式 (JSON)
```json
{
  "has_trojan": "是/否/不确定",
  "confidence": 0.0-1.0,
  "risk_level": "低/中/高/严重",
  "top_3_suspicious": [
    {"location": "", "reason": "", "severity": ""}
  ],
  "recommendations": [""]
}
```
