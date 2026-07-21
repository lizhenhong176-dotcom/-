#!/usr/bin/env python3
"""
HAL Graph Algorithm 插件封装。
图算法分析：连通分量、环路检测、最短路径、子图匹配。
"""

from __future__ import annotations

from typing import Any


class GraphTool:
    """HAL graph_algorithm 插件封装。"""

    def __init__(self, plugin_manager):
        self._pm = plugin_manager

    def connected_components(self, netlist) -> list:
        """计算连通分量。"""
        ga = self._pm.graph_algorithm
        return ga.get_connected_components(netlist)

    def find_cycles(self, netlist) -> list:
        """检测组合逻辑环路。"""
        ga = self._pm.graph_algorithm
        return ga.find_cycles(netlist)

    def shortest_path(self, start_gate, end_gate) -> list | None:
        """最短路径。"""
        ga = self._pm.graph_algorithm
        return ga.shortest_path(start_gate, end_gate)

    def neighborhood(self, gate, depth: int = 2) -> list:
        """获取门的邻域子图。"""
        ga = self._pm.graph_algorithm
        return ga.get_neighborhood(gate, depth)

    def subgraph_match(self, netlist, pattern: dict) -> list:
        """子图匹配 (检测已知木马结构)。"""
        ga = self._pm.graph_algorithm
        return ga.find_subgraph(netlist, pattern)
