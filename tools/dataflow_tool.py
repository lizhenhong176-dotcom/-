#!/usr/bin/env python3
"""
HAL Dataflow 插件封装。
提供数据流方向分析、扇入/扇出查询、路径追踪。
"""

from __future__ import annotations

from typing import Any


class DataflowTool:
    """HAL dataflow 插件封装。"""

    def __init__(self, plugin_manager):
        self._pm = plugin_manager

    def get_direction(self, src_gate, dst_gate) -> str | None:
        """返回两个门之间的数据流方向。"""
        df = self._pm.dataflow
        return df.get_direction(src_gate, dst_gate)

    def get_fan_in(self, gate) -> list:
        """获取门的所有扇入门。"""
        df = self._pm.dataflow
        return df.get_fan_in(gate)

    def get_fan_out(self, gate) -> list:
        """获取门的所有扇出门。"""
        df = self._pm.dataflow
        return df.get_fan_out(gate)

    def trace_path(self, start_gate, end_gate_name: str) -> list | None:
        """追踪两个门之间的数据路径。"""
        df = self._pm.dataflow
        paths = df.get_paths(start_gate, end_gate_name)
        return paths[0] if paths else None

    def find_all_sinks(self, start_gate) -> list:
        """找到所有数据终点。"""
        df = self._pm.dataflow
        return df.get_all_sinks(start_gate)
