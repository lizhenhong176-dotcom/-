#!/usr/bin/env python3
"""
网表级分析。
连接性分析、关键路径、可疑子图检测、未连接端点。
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class NetInfo:
    """网表信息。"""

    name: str
    source_gate: str | None = None
    dest_gates: list[str] = field(default_factory=list)
    is_primary_input: bool = False
    is_primary_output: bool = False
    fanout: int = 0


def analyze_nets(netlist) -> dict:
    """网表分析主入口。"""
    nets = netlist.get_nets()

    result = {
        "total_nets": len(nets),
        "primary_inputs": [],
        "primary_outputs": [],
        "internal_nets": [],
        "single_driver_nets": 0,
        "multi_driver_nets": 0,
        "undriven_nets": [],
    }

    for net in nets:
        sources = net.get_sources()
        dests = net.get_destinations()

        if len(sources) == 0:
            result["undriven_nets"].append(net.get_name())
        elif len(sources) == 1:
            result["single_driver_nets"] += 1
        else:
            result["multi_driver_nets"] += 1

        if net.is_global_input_net():
            result["primary_inputs"].append(net.get_name())
        elif net.is_global_output_net():
            result["primary_outputs"].append(net.get_name())
        else:
            result["internal_nets"].append(net.get_name())

    return result


def find_floating_nets(netlist) -> list[str]:
    """查找悬空网表 (无驱动或无负载)。"""
    floating = []
    for net in netlist.get_nets():
        if len(net.get_sources()) == 0 or len(net.get_destinations()) == 0:
            floating.append(net.get_name())
    return floating


def find_high_fanout_nets(netlist, threshold: int = 100) -> list[dict]:
    """查找高扇出网表 (可能为时钟、复位或可疑信号)。"""
    result = []
    for net in netlist.get_nets():
        fo = len(net.get_destinations())
        if fo > threshold:
            result.append({
                "name": net.get_name(),
                "fanout": fo,
                "source": net.get_sources()[0].get_name() if net.get_sources() else None,
            })
    return result
