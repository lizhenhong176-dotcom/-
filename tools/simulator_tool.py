#!/usr/bin/env python3
"""
HAL Netlist Simulator 插件封装。
API 待验证 — 当前为 stub。
真实模块: netlist_simulator (NetlistSimulator, Simulation)
"""
from __future__ import annotations


class SimulatorTool:
    """HAL netlist_simulator 插件封装 (stub)。

    模块已验证可导入: NetlistSimulator, Simulation
    API 细节待 Phase 2 后续验证后实现。
    """

    def __init__(self, plugin_manager=None):
        self._pm = plugin_manager

    def simulate(self, netlist, vectors: list[dict],
                 duration_ns: int = 100) -> dict | None:
        """ponytail: stub — 待 netlist_simulator API 验证后实现。"""
        raise NotImplementedError(
            "SimulatorTool: netlist_simulator API 待验证"
        )

    def get_signal_trace(self, netlist, signal_name: str) -> list | None:
        raise NotImplementedError("SimulatorTool: get_signal_trace stub")

    def check_toggle(self, netlist, gate_name: str) -> bool | None:
        raise NotImplementedError("SimulatorTool: check_toggle stub")

    def find_idle_gates(self, netlist) -> list[str]:
        raise NotImplementedError("SimulatorTool: find_idle_gates stub")
