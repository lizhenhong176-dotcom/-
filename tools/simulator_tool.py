#!/usr/bin/env python3
"""
HAL Simulator 插件封装。
门级仿真、测试向量生成、覆盖率分析。
"""

from __future__ import annotations

from typing import Any


class SimulatorTool:
    """HAL simulator 插件封装。"""

    def __init__(self, plugin_manager):
        self._pm = plugin_manager

    def simulate(self, netlist, vectors: list[dict], duration_ns: float = 100.0) -> dict:
        """运行门级仿真。"""
        sim = self._pm.simulator
        sim.set_input_vectors(vectors)
        sim.run(duration_ns)
        return sim.get_results()

    def get_signal_trace(self, netlist, signal_name: str) -> list:
        """获取信号波形。"""
        sim = self._pm.simulator
        return sim.get_trace(signal_name)

    def check_toggle(self, netlist, gate_name: str) -> bool:
        """检查门是否发生过翻转。"""
        sim = self._pm.simulator
        return sim.gate_toggled(gate_name)

    def find_idle_gates(self, netlist) -> list:
        """查找仿真期间从未翻转的门 (可能是隐藏逻辑)。"""
        sim = self._pm.simulator
        idle = []
        for gate in netlist.get_gates():
            if not sim.gate_toggled(gate.get_name()):
                idle.append(gate.get_name())
        return idle
