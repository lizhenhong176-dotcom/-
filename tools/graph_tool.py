#!/usr/bin/env python3
"""
HAL Graph Algorithm 插件封装。
基于 igraph 的图算法：连通分量、邻域、最短路径、子图。
API 经 check_plugins.py 验证。
"""
from __future__ import annotations

import sys
from typing import Any

sys.path.insert(0, "/home/i/hal/build/lib/hal_plugins/")


class GraphTool:
    """HAL graph_algorithm 插件封装。"""

    def __init__(self, plugin_manager=None):
        # plugin_manager kept for API compatibility, graph_algorithm is self-contained
        self._graph = None
        self._netlist = None

    def _ensure_graph(self, netlist):
        """构建 NetlistGraph，如果未构建或 netlist 变了。"""
        if self._graph is None or self._netlist is not netlist:
            import graph_algorithm as ga
            self._graph = ga.NetlistGraph.from_netlist(netlist)
            self._netlist = netlist
        return self._graph

    @property
    def Direction(self):
        import graph_algorithm as ga
        return ga.NetlistGraph.Direction

    def connected_components(self, netlist, strong: bool = True,
                             min_size: int = 0) -> list[list[int]]:
        """计算连通分量。返回 vertex ID 列表的列表。"""
        import graph_algorithm as ga
        graph = self._ensure_graph(netlist)
        result = ga.get_connected_components(graph, strong, min_size)
        return result if result else []

    def get_neighborhood(self, netlist, start_gates: list,
                         order: int = 2,
                         direction=None,
                         min_dist: int = 0) -> list[list[int]]:
        """获取以 start_gates 为中心的邻域子图。"""
        import graph_algorithm as ga
        graph = self._ensure_graph(netlist)
        if direction is None:
            direction = ga.NetlistGraph.Direction.ALL
        result = ga.get_neighborhood(graph, start_gates, order,
                                     direction, min_dist)
        return result if result else []

    def get_shortest_paths(self, netlist, from_gate, to_gates: list,
                           direction=None) -> list[list[int]]:
        """获取 from_gate 到 to_gates 的最短路径。"""
        import graph_algorithm as ga
        graph = self._ensure_graph(netlist)
        if direction is None:
            direction = ga.NetlistGraph.Direction.ALL
        result = ga.get_shortest_paths(graph, from_gate, to_gates, direction)
        return result if result else []

    def get_subgraph(self, netlist, gates: list):
        """提取子图。"""
        import graph_algorithm as ga
        graph = self._ensure_graph(netlist)
        return ga.get_subgraph(graph, gates)

    def vertex_to_gate(self, vertex: int):
        """vertex ID → Gate 对象。"""
        if self._graph is None:
            return None
        return self._graph.get_gate_from_vertex(vertex)

    def gate_to_vertex(self, gate) -> int | None:
        """Gate 对象 → vertex ID。"""
        if self._graph is None:
            return None
        return self._graph.get_vertex_from_gate(gate)
