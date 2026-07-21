#!/usr/bin/env python3
"""HAL 工具函数集。"""

from __future__ import annotations

from typing import Any


def get_gate_by_name(netlist, name: str):
    """按名称查找门。"""
    for gate in netlist.get_gates():
        if gate.get_name() == name:
            return gate
    return None


def get_net_by_name(netlist, name: str):
    """按名称查找网表。"""
    for net in netlist.get_nets():
        if net.get_name() == name:
            return net
    return None


def get_module_by_name(netlist, name: str):
    """按名称查找模块。"""
    for module in netlist.get_modules():
        if module.get_name() == name:
            return module
    return None


def get_fan_in(gate) -> list:
    """获取门的所有扇入网表。"""
    return list(gate.get_fan_in_nets())


def get_fan_out(gate) -> list:
    """获取门的所有扇出网表。"""
    return list(gate.get_fan_out_nets())


def gate_type_counts(netlist) -> dict[str, int]:
    """统计各类门数量。"""
    counts: dict[str, int] = {}
    for gate in netlist.get_gates():
        gtype = gate.get_type().get_name()
        counts[gtype] = counts.get(gtype, 0) + 1
    return counts


def is_sequential(gate) -> bool:
    """判断是否为时序门 (FF/Latch)。"""
    seq_types = {"DFF", "LATCH", "DLATCH", "SDFF", "DFFSR"}
    gtype = gate.get_type().get_name()
    return any(t in gtype.upper() for t in seq_types)


def find_input_pins(netlist) -> list:
    """找到所有顶层输入引脚。"""
    import hal_py
    top = netlist.get_top_module()
    return [pin for pin in top.get_pins()
            if pin.get_direction() == hal_py.PinDirection.input]


def find_output_pins(netlist) -> list:
    """找到所有顶层输出引脚。"""
    import hal_py
    top = netlist.get_top_module()
    return [pin for pin in top.get_pins()
            if pin.get_direction() == hal_py.PinDirection.output]
