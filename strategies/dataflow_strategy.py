#!/usr/bin/env python3
"""
数据流木马检测策略。
通过 HAL dataflow 插件追踪数据流，检测异常数据路径。
"""

from __future__ import annotations

from strategies.base_strategy import BaseStrategy, StrategyResult


class DataflowStrategy(BaseStrategy):
    """数据流木马检测。"""

    name = "dataflow_strategy"
    description = "检测数据流中的木马：隐藏数据路径、异常扇出、条件触发数据窃取"

    def applicable_to(self, module_info) -> bool:
        return True  # 适用于所有模块类型

    def analyze(self, netlist, **kwargs) -> StrategyResult:
        findings = []

        # 1. 全芯片数据流追踪
        # 2. 输入→输出关键路径检测
        # 3. 敏感数据扇出异常
        # 4. 条件触发数据路径

        return StrategyResult(
            strategy_name=self.name,
            findings=findings,
        )
