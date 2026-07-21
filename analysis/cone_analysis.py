#!/usr/bin/env python3
"""
逻辑锥分析。
从输出反向追踪、识别关键锥体、检测异常锥体结构。
用于检测输出锥体木马 (rare-trigger output manipulation)。
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LogicCone:
    """逻辑锥体。"""

    root_signal: str
    depth: int = 0
    gate_count: int = 0
    ff_count: int = 0
    input_signals: list[str] = field(default_factory=list)
    suspicious: bool = False


def analyze_cones(netlist, max_depth: int = 10) -> list[LogicCone]:
    """从所有输出端口反向追踪逻辑锥。"""
    cones = []
    top = netlist.get_top_module()

    import hal_py

    for pin in top.get_pins():
        if pin.get_direction() != hal_py.PinDirection.output:
            continue

        net = pin.get_net()
        if not net:
            continue

        cone = _trace_cone(net, max_depth)
        cone.root_signal = pin.get_name()
        cones.append(cone)

    return cones


def analyze_input_cones(netlist, max_depth: int = 10) -> list[LogicCone]:
    """从所有输入端口前向追踪逻辑锥。"""
    cones = []
    top = netlist.get_top_module()

    import hal_py

    for pin in top.get_pins():
        if pin.get_direction() != hal_py.PinDirection.input:
            continue

        net = pin.get_net()
        if not net:
            continue

        cone = _trace_forward_cone(net, max_depth)
        cone.root_signal = pin.get_name()
        cones.append(cone)

    return cones


def _trace_cone(start_net, max_depth: int) -> LogicCone:
    """反向追踪单个逻辑锥 (BFS)。"""
    cone = LogicCone(root_signal="")
    visited = set()
    queue = [(start_net, 0)]

    while queue:
        net, depth = queue.pop(0)
        if depth > max_depth:
            continue

        net_id = id(net)
        if net_id in visited:
            continue
        visited.add(net_id)

        cone.depth = max(cone.depth, depth)

        for source in net.get_sources():
            gate = source.get_gate()
            if gate is None:
                cone.input_signals.append(source.get_name())
                continue

            cone.gate_count += 1
            gtype = gate.get_type().get_name().upper()
            if any(k in gtype for k in ("DFF", "LATCH")):
                cone.ff_count += 1

            for next_net in gate.get_fan_in_nets():
                if next_net:
                    queue.append((next_net, depth + 1))

    return cone


def _trace_forward_cone(start_net, max_depth: int) -> LogicCone:
    """前向追踪单个逻辑锥 (BFS)。"""
    cone = LogicCone(root_signal="")
    visited = set()
    queue = [(start_net, 0)]

    while queue:
        net, depth = queue.pop(0)
        if depth > max_depth:
            continue

        net_id = id(net)
        if net_id in visited:
            continue
        visited.add(net_id)

        cone.depth = max(cone.depth, depth)

        for dest in net.get_destinations():
            gate = dest.get_gate()
            if gate is None:
                continue

            cone.gate_count += 1
            gtype = gate.get_type().get_name().upper()
            if any(k in gtype for k in ("DFF", "LATCH")):
                cone.ff_count += 1

            for next_net in gate.get_fan_out_nets():
                if next_net:
                    queue.append((next_net, depth + 1))

    return cone
