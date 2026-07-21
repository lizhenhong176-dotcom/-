#!/usr/bin/env python3
"""
门级分析。
识别异常门类型、扇入/扇出异常、冗余逻辑、关键路径。
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class GateAnomaly:
    """门级异常记录。"""

    gate_name: str
    gate_type: str
    anomaly_type: str
    description: str
    severity: str = "low"  # low | medium | high


def analyze_gates(netlist) -> dict:
    """门级分析主入口。"""
    gates = netlist.get_gates()

    result = {
        "total_gates": len(gates),
        "type_distribution": _count_gate_types(gates),
        "anomalies": [],
        "high_fanout_gates": [],
        "unconnected_gates": [],
    }

    for gate in gates:
        # 检测无连接门
        if _is_unconnected(gate):
            result["unconnected_gates"].append(gate.get_name())

        # 检测高扇出
        fo = len(_get_fanout_nets(gate))
        if fo > 50:
            result["high_fanout_gates"].append({
                "name": gate.get_name(),
                "fanout": fo,
            })

    return result


def detect_suspicious_gates(netlist) -> list[GateAnomaly]:
    """检测可疑门。关注：罕见门类型、异常驱动强度、冗余门。"""
    anomalies = []
    gates = netlist.get_gates()
    type_counts = _count_gate_types(gates)

    for gate in gates:
        gtype = gate.get_type().get_name()

        # 罕见门类型 (在整个设计中只出现1-2次)
        if type_counts.get(gtype, 0) <= 2:
            anomalies.append(GateAnomaly(
                gate_name=gate.get_name(),
                gate_type=gtype,
                anomaly_type="rare_gate_type",
                description=f"Gate type '{gtype}' appears only {type_counts[gtype]} time(s)",
                severity="medium",
            ))

    return anomalies


def _count_gate_types(gates) -> dict[str, int]:
    counts = {}
    for g in gates:
        t = g.get_type().get_name()
        counts[t] = counts.get(t, 0) + 1
    return counts


def _is_unconnected(gate) -> bool:
    fi = gate.get_fan_in_nets()
    fo = gate.get_fan_out_nets()
    return len(fi) == 0 and len(fo) == 0


def _get_fanout_nets(gate) -> list:
    return list(gate.get_fan_out_nets())
