#!/usr/bin/env python3
"""
寄存器分析。
识别所有时序元件、分析复位/时钟域、检测可疑寄存器配置。
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RegisterInfo:
    """寄存器信息。"""

    name: str
    gate_type: str
    clock_net: str | None = None
    reset_net: str | None = None
    d_input_net: str | None = None
    q_output_net: str | None = None
    fan_in_nets: list[str] = field(default_factory=list)
    is_toggling: bool | None = None
    fanout: int = 0
    notes: list[str] = field(default_factory=list)


def analyze_registers(netlist) -> dict:
    """寄存器分析主入口。"""
    regs = _find_all_registers(netlist)

    result = {
        "total_registers": len(regs),
        "registers": regs,
        "clock_domains": _identify_clock_domains(regs),
        "reset_domains": _identify_reset_domains(regs),
        "suspicious_regs": [],
    }

    for reg in regs:
        # 无复位寄存器 → 可能隐藏状态
        if not reg.reset_net:
            result["suspicious_regs"].append({
                "name": reg.name,
                "reason": "no_reset",
                "severity": "low",
            })
        # 极高扇出 → 可能是触发信号
        if reg.fanout > 100:
            result["suspicious_regs"].append({
                "name": reg.name,
                "reason": f"high_fanout={reg.fanout}",
                "severity": "medium",
            })
        # 无扇出 → 死代码或隐藏逻辑
        if reg.fanout == 0:
            result["suspicious_regs"].append({
                "name": reg.name,
                "reason": "no_fanout",
                "severity": "high",
            })

    return result


def _find_all_registers(netlist) -> list[RegisterInfo]:
    regs = []
    for gate in netlist.get_gates():
        gtype = gate.get_type().get_name().upper()
        if any(k in gtype for k in ("DFF", "SDFF", "LATCH", "DLATCH")):
            fan_in_nets = list(gate.get_fan_in_nets())
            fan_out_nets = list(gate.get_fan_out_nets())

            reg = RegisterInfo(
                name=gate.get_name(),
                gate_type=gate.get_type().get_name(),
                fan_in_nets=[n.get_name() for n in fan_in_nets],
            )

            # ponytail: pin names not available via HAL API directly;
            # use gate type name heuristics + net order for clock/reset detection
            for net in fan_in_nets:
                nname = net.get_name().upper()
                if any(k in nname for k in ("CLK", "CLOCK", "CK")):
                    reg.clock_net = net.get_name()
                elif any(k in nname for k in ("RST", "RESET", "RN")):
                    reg.reset_net = net.get_name()

            if fan_out_nets:
                qnet = fan_out_nets[0]
                reg.q_output_net = qnet.get_name()
                reg.fanout = len(qnet.get_destinations())

            regs.append(reg)
    return regs


def _identify_clock_domains(regs: list[RegisterInfo]) -> dict[str, int]:
    domains = {}
    for reg in regs:
        if reg.clock_net:
            domains[reg.clock_net] = domains.get(reg.clock_net, 0) + 1
    return domains


def _identify_reset_domains(regs: list[RegisterInfo]) -> dict[str, int]:
    domains = {}
    for reg in regs:
        if reg.reset_net:
            domains[reg.reset_net] = domains.get(reg.reset_net, 0) + 1
    return domains
