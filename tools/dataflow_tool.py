#!/usr/bin/env python3
"""
HAL Dataflow (DANA) 插件封装。
门级数据流分析：寄存器分组、前驱/后继查询、创建高层模块。
API 经 check_plugins.py 验证。
"""
from __future__ import annotations

from collections import deque
from typing import Any


class DataflowTool:
    """HAL dataflow (DANA) 插件封装。"""

    def __init__(self, plugin_manager=None):
        self._result = None
        self._netlist = None

    def _ensure_analyzed(self, netlist) -> Any | None:
        """运行 DANA 分析。返回 Result 或 None。"""
        if self._result is not None and self._netlist is netlist:
            return self._result

        import dataflow
        cfg = dataflow.Configuration(netlist)
        self._result = dataflow.analyze(cfg)
        self._netlist = netlist
        return self._result

    def get_groups(self, netlist) -> dict[int, set]:
        """获取所有 DANA 分组。返回 {group_id: {Gate, ...}}。"""
        result = self._ensure_analyzed(netlist)
        if result is None:
            return {}
        return result.get_groups()

    def get_gate_predecessors(self, netlist, gate) -> set:
        """获取门的所有前驱门 (扇入)。"""
        result = self._ensure_analyzed(netlist)
        if result is None:
            return set()
        return result.get_gate_predecessors(gate)

    def get_gate_successors(self, netlist, gate) -> set:
        """获取门的所有后继门 (扇出)。"""
        result = self._ensure_analyzed(netlist)
        if result is None:
            return set()
        return result.get_gate_successors(gate)

    def get_group_id(self, netlist, gate) -> int | None:
        """获取门所属的 DANA group ID。"""
        result = self._ensure_analyzed(netlist)
        if result is None:
            return None
        return result.get_group_id_of_gate(gate)

    def get_gates_of_group(self, netlist, group_id: int) -> set:
        """获取指定 group 中的所有门。"""
        result = self._ensure_analyzed(netlist)
        if result is None:
            return set()
        g = result.get_gates_of_group(group_id)
        return g if g else set()

    def find_all_sinks(self, netlist, start_gate) -> list:
        """ponytail: BFS 遍历 successors 找到所有终点。"""
        sinks = []
        visited = set()
        queue = deque([start_gate])
        while queue:
            g = queue.popleft()
            gid = id(g)
            if gid in visited:
                continue
            visited.add(gid)
            succs = self.get_gate_successors(netlist, g)
            if not succs:
                sinks.append(g)
            else:
                queue.extend(succs)
        return sinks
