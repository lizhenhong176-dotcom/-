#!/usr/bin/env python3
"""
HAL Analysis Core — 木马检测感知层。
用法: python analyze.py <netlist.v>
输出: 终端结构化分析 + results/<design>_analysis.json
"""

import json
import sys
from pathlib import Path

import yaml

from hal.loader import HALLoader
from hal.query import gate_type_counts, find_input_pins, find_output_pins
from analysis.module_analysis import analyze_all_modules
from analysis.gate_analysis import analyze_gates
from analysis.register_analysis import analyze_registers
from analysis.net_analysis import analyze_nets, find_floating_nets
from analysis.cone_analysis import analyze_cones


def load_config():
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def print_report(netlist, modules, gates, registers, nets, cones, design_name, lib_name):
    """终端输出结构化分析。"""
    top = netlist.get_top_module()
    top_name = top.get_name()

    print("========== HAL Analysis Core ==========\n")
    print(f"Design:       {design_name}")
    print(f"Gate Library: {lib_name}")

    # --- Module ---
    print(f"\n--- Module ---")
    print(f"Top:    {top_name} ({len(top.get_gates())} gates)")
    for m in modules:
        if m.name != top_name:
            print(f"  Sub:  {m.name} ({m.gate_count} gates, type={m.module_type})")

    # --- Gates ---
    print(f"\n--- Gate Count ---")
    print(f"Total: {gates['total_gates']}")
    gtc = gate_type_counts(netlist)
    for t, c in sorted(gtc.items(), key=lambda x: -x[1])[:10]:
        print(f"  {t:20s} {c}")

    # --- Registers ---
    print(f"\n--- Registers ({registers['total_registers']}) ---")
    for r in registers["registers"][:10]:
        print(f"  {r.name:35s} {r.gate_type:12s} fan_in={len(_fan_in_nets(r, netlist))}  fan_out={r.fanout}")
    if registers["total_registers"] > 10:
        print(f"  ... ({registers['total_registers'] - 10} more)")

    # --- Nets ---
    print(f"\n--- Nets ---")
    print(f"Total:    {nets['total_nets']}")
    floating = find_floating_nets(netlist)
    print(f"Floating: {len(floating)}")

    # --- Cones ---
    print(f"\n--- Output Cones ---")
    for c in cones[:10]:
        if c.gate_count > 0:
            print(f"  {c.root_signal:25s} depth={c.depth}  gates={c.gate_count}  ff={c.ff_count}")

    # --- I/O ---
    inputs = find_input_pins(netlist)
    outputs = find_output_pins(netlist)
    print(f"\n--- I/O ---")
    print(f"Inputs:  {len(inputs)}")
    for p in inputs:
        print(f"  {p.get_name()}")
    print(f"Outputs: {len(outputs)}")
    for p in outputs:
        print(f"  {p.get_name()}")

    print(f"\nReady for Trojan Analysis.")


def build_json(netlist, modules, gates, registers, nets, cones, design_name, lib_name):
    """构建 JSON 输出。"""
    top = netlist.get_top_module()
    top_name = top.get_name()
    gtc = gate_type_counts(netlist)
    inputs = find_input_pins(netlist)
    outputs = find_output_pins(netlist)
    floating = find_floating_nets(netlist)

    return {
        "design": design_name,
        "gate_library": lib_name,
        "module": {
            "top": top_name,
            "submodules": [m.name for m in modules if m.name != top_name],
            "types": {m.name: m.module_type for m in modules},
        },
        "gates": {
            "total": gates["total_gates"],
            "cell_types": gtc,
        },
        "registers": [
            {
                "name": r.name,
                "type": r.gate_type,
                "fan_in": len(_fan_in_nets(r, netlist)),
                "fan_out": r.fanout,
            }
            for r in registers["registers"]
        ],
        "nets": {
            "total": nets["total_nets"],
            "floating": len(floating),
        },
        "cones": [
            {"output": c.root_signal, "depth": c.depth,
             "gate_count": c.gate_count, "ff_count": c.ff_count}
            for c in cones if c.gate_count > 0
        ],
        "io": {
            "inputs": [p.get_name() for p in inputs],
            "outputs": [p.get_name() for p in outputs],
        },
    }


def _fan_in_nets(reg_info, netlist):
    """从网表中找到对应门并获取扇入网表。"""
    from hal.query import get_gate_by_name, get_fan_in
    gate = get_gate_by_name(netlist, reg_info.name)
    if gate:
        return get_fan_in(gate)
    return []


def main(netlist_path: str):
    config = load_config()
    netlist_path = Path(netlist_path)

    design_name = netlist_path.stem
    lib_name = Path(config["hal"]["netlist"]["hgl"]).stem

    # 1. Load
    loader = HALLoader(config)
    netlist = loader.load_netlist(netlist_path)

    # 2. Analyze
    modules = analyze_all_modules(netlist)
    gates = analyze_gates(netlist)
    registers = analyze_registers(netlist)
    nets = analyze_nets(netlist)
    cones = analyze_cones(netlist)

    # 3. Print
    print_report(netlist, modules, gates, registers, nets, cones, design_name, lib_name)

    # 4. JSON
    result_dir = Path("results")
    result_dir.mkdir(exist_ok=True)
    json_path = result_dir / f"{design_name}_analysis.json"
    data = build_json(netlist, modules, gates, registers, nets, cones, design_name, lib_name)
    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"\nJSON written: {json_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python analyze.py <netlist.v>")
        sys.exit(1)
    main(sys.argv[1])
