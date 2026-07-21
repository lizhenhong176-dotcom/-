#!/usr/bin/env python3
"""
Phase 0 验证：加载门级网表到 HAL，打印基本统计。
用法: python check_hal.py <netlist.v>
"""

import sys
import hal_py
from pathlib import Path

HGL = "/home/i/hal/plugins/gate_libraries/definitions/NangateOpenCellLibrary.hgl"
PLUGIN_DIR = "/home/i/hal/build/lib/hal_plugins/"


def main(netlist_path: str):
    p = Path(netlist_path)
    if not p.exists():
        print(f"ERROR: netlist not found: {p}")
        sys.exit(1)

    # 1. 加载插件 (必须先加载 verilog_parser + hgl_parser)
    print("Loading plugins...")
    hal_py.plugin_manager.load_all_plugins([PLUGIN_DIR])
    names = hal_py.plugin_manager.get_plugin_names()
    print(f"  Loaded {len(names)} plugins")

    # 2. 加载网表
    print(f"\nNetlist: {p}")
    print(f"HGL:     {HGL}")
    netlist = hal_py.NetlistFactory.load_netlist(str(p), HGL)

    if netlist is None:
        print("ERROR: netlist is None — check netlist format and gate library compatibility")
        sys.exit(1)

    gates = netlist.get_gates()
    nets = netlist.get_nets()
    modules = netlist.get_modules()

    print(f"\n=== Netlist Stats ===")
    print(f"Modules:  {len(modules)}")
    for m in modules:
        print(f"  - {m.get_name()} ({len(m.get_gates())} gates)")

    print(f"Gates:    {len(gates)}")
    print(f"Nets:     {len(nets)}")

    # 门类型分布
    from collections import Counter
    gtypes = Counter(g.get_type().get_name() for g in gates)
    print(f"\n=== Gate Types (top 10) ===")
    for t, c in gtypes.most_common(10):
        print(f"  {t}: {c}")

    # 顶层 IO
    top = netlist.get_top_module()
    if top:
        print(f"\n=== Top Module: {top.get_name()} ===")
        for pin in top.get_pins():
            print(f"  {pin.get_name():20s} {pin.get_direction()}")

    print("\n=== Phase 0 OK ===")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <netlist.v>")
        sys.exit(1)
    main(sys.argv[1])
