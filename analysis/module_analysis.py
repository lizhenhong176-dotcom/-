#!/usr/bin/env python3
"""
模块级分析。
识别设计层次结构、模块功能分类、接口分析。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ModuleInfo:
    """模块分析结果。"""

    name: str
    module_type: str = "unknown"  # datapath | controller | interface | crypto | mixed
    gate_count: int = 0
    ff_count: int = 0
    input_count: int = 0
    output_count: int = 0
    submodules: list[str] = field(default_factory=list)
    suspicious_score: float = 0.0
    notes: list[str] = field(default_factory=list)


def analyze_module(module, netlist) -> ModuleInfo:
    """对单个模块执行完整分析。"""
    info = ModuleInfo(name=module.get_name())

    # 统计门数和寄存器数
    gates = module.get_gates()
    info.gate_count = len(gates)
    info.ff_count = sum(1 for g in gates if _is_ff(g))

    # 统计 IO
    import hal_py
    pins = module.get_pins()
    info.input_count = sum(1 for p in pins
                           if p.get_direction() == hal_py.PinDirection.input)
    info.output_count = sum(1 for p in pins
                            if p.get_direction() == hal_py.PinDirection.output)

    # 子模块
    info.submodules = [sm.get_name() for sm in module.get_submodules()]

    # 模块类型分类 (启发式)
    info.module_type = _classify_module(info, module)

    return info


def analyze_all_modules(netlist) -> list[ModuleInfo]:
    """分析网表中所有模块。"""
    return [analyze_module(m, netlist) for m in netlist.get_modules()]


def _is_ff(gate) -> bool:
    """判断门是否为触发器。"""
    t = gate.get_type().get_name().upper()
    return any(k in t for k in ("DFF", "SDFF", "LATCH", "DLATCH"))


def _classify_module(info: ModuleInfo, module) -> str:
    """启发式模块分类。"""
    name_lower = info.name.lower()
    if any(k in name_lower for k in ("uart", "rs232", "serial", "tx", "rx")):
        return "interface"
    if any(k in name_lower for k in ("aes", "des", "crypto", "encrypt", "decrypt")):
        return "crypto"
    if any(k in name_lower for k in ("fsm", "ctrl", "control", "state")):
        return "controller"
    if info.ff_count > info.gate_count * 0.3:
        return "controller"
    if info.gate_count > 50 and info.ff_count < info.gate_count * 0.1:
        return "datapath"
    return "unknown"
