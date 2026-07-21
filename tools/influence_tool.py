#!/usr/bin/env python3
"""
HAL Boolean Influence 插件封装。
布尔影响力分析：检测哪些信号对输出有异常影响。
"""

from __future__ import annotations

from typing import Any


class InfluenceTool:
    """HAL boolean_influence 插件封装。"""

    def __init__(self, plugin_manager):
        self._pm = plugin_manager

    def compute_influence(self, netlist, output_signal: str) -> dict:
        """计算所有信号对指定输出的布尔影响力度量。"""
        bi = self._pm.boolean_influence
        return bi.compute_influence(netlist, output_signal)

    def find_high_influence_inputs(
        self, netlist, output_signal: str, threshold: float = 0.5
    ) -> list[dict]:
        """找到对输出有高于阈值影响力的输入信号。"""
        bi = self._pm.boolean_influence
        influence = bi.compute_influence(netlist, output_signal)
        return [
            {"signal": sig, "influence": val}
            for sig, val in influence.items()
            if val > threshold
        ]

    def compare_influence(
        self, netlist, output_signal: str, golden_influence: dict
    ) -> list[dict]:
        """比较实际影响力与参考基准，检测偏差。"""
        actual = self._pm.boolean_influence.compute_influence(netlist, output_signal)
        diffs = []
        for sig in set(actual) | set(golden_influence):
            diff = actual.get(sig, 0.0) - golden_influence.get(sig, 0.0)
            if abs(diff) > 0.1:
                diffs.append({"signal": sig, "actual": actual.get(sig, 0.0),
                              "golden": golden_influence.get(sig, 0.0), "delta": diff})
        return diffs
