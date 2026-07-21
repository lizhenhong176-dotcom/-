#!/usr/bin/env python3
"""
HAL Boolean Influence 插件封装。
插件在当前 HAL build 中不可用 — 保持 stub。
"""
from __future__ import annotations


class InfluenceTool:
    """HAL boolean_influence 插件封装 (stub)。

    当前 HAL build 未编译 boolean_influence 插件。
    待重新编译 HAL 后实现。
    """

    def __init__(self, plugin_manager=None):
        self._pm = plugin_manager

    def compute_influence(self, netlist, output_signal: str) -> dict:
        raise NotImplementedError(
            "InfluenceTool: boolean_influence plugin 未编译"
        )

    def find_high_influence_inputs(self, netlist, output_signal: str,
                                   threshold: float = 0.5) -> list[dict]:
        raise NotImplementedError("InfluenceTool: stub")

    def compare_influence(self, netlist, output_signal: str,
                          golden_influence: dict) -> list[dict]:
        raise NotImplementedError("InfluenceTool: stub")
