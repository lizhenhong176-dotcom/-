#!/usr/bin/env python3
"""
Phase 2: HAL 插件 API 验证脚本。
插件 .so 需在 hal_py 加载后通过 __import__ 导入。
用法: python check_plugins.py [netlist.v]
"""
import sys
sys.path.insert(0, "/home/i/hal/build/lib/hal_plugins/")

HGL = "/home/i/hal/plugins/gate_libraries/definitions/NangateOpenCellLibrary.hgl"
PLUGIN_DIR = "/home/i/hal/build/lib/hal_plugins/"


def section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def check(name: str, ok: bool, detail: str = ""):
    mark = "OK" if ok else "FAIL"
    print(f"  [{mark}] {name}" + (f" -- {detail}" if detail else ""))


def load_all(netlist_path: str):
    import hal_py
    hal_py.plugin_manager.load_all_plugins([PLUGIN_DIR])
    return hal_py.NetlistFactory.load_netlist(str(netlist_path), HGL)


def verify_dataflow(netlist):
    section("dataflow (DANA)")
    try:
        import dataflow
        check("import dataflow", True,
              str([n for n in dir(dataflow) if not n.startswith("_")]))

        cfg = dataflow.Configuration(netlist)
        check("Configuration(netlist)", True, "")

        result = dataflow.analyze(cfg)
        check("dataflow.analyze(cfg)", result is not None,
              f"type={type(result).__name__}")

        if result:
            groups = result.get_groups()
            check("get_groups()", isinstance(groups, dict),
                  f"{len(groups)} groups")

            gates = netlist.get_gates()
            if gates:
                g = gates[0]
                succs = result.get_gate_successors(g)
                check("get_gate_successors(gate)",
                      isinstance(succs, set), f"{len(succs)} succ")
                preds = result.get_gate_predecessors(g)
                check("get_gate_predecessors(gate)",
                      isinstance(preds, set), f"{len(preds)} pred")
                gid = result.get_group_id_of_gate(g)
                check("get_group_id_of_gate(gate)",
                      gid is not None, f"group={gid}")
    except Exception as e:
        check("dataflow", False, f"{type(e).__name__}: {e}")


def verify_graph_algorithm(netlist):
    section("graph_algorithm")
    try:
        import graph_algorithm as ga
        check("import graph_algorithm", True,
              str([n for n in dir(ga) if not n.startswith("_")]))

        # Direction enum
        check("Direction enum", hasattr(ga.NetlistGraph, "Direction"),
              str([d for d in dir(ga.NetlistGraph.Direction)
                   if not d.startswith("_")]))

        # Build graph
        graph = ga.NetlistGraph.from_netlist(netlist)
        check("NetlistGraph.from_netlist(nl)", graph is not None,
              f"V={graph.get_num_vertices()}, E={graph.get_num_edges()}")

        # Vertex conversion
        gates = netlist.get_gates()
        g0 = gates[0]
        v0 = graph.get_vertex_from_gate(g0)
        check("get_vertex_from_gate()", v0 is not None, f"v={v0}")
        gb = graph.get_gate_from_vertex(v0)
        check("get_gate_from_vertex()", gb is not None, gb.get_name())

        # Connected components
        comps = ga.get_connected_components(graph, True)
        check("get_connected_components(graph, strong=True)",
              isinstance(comps, list), f"{len(comps)} components")

        # Neighborhood
        D = ga.NetlistGraph.Direction
        nb = ga.get_neighborhood(graph, [gates[0]], 2, D.ALL, 0)
        check("get_neighborhood(graph, [g0], 2, ALL, 0)",
              isinstance(nb, list),
              f"{len(nb)} levels, sizes={[len(l) for l in nb]}")

        # Shortest paths
        if len(gates) >= 2:
            paths = ga.get_shortest_paths(graph, gates[0], [gates[1]], D.ALL)
            check("get_shortest_paths(graph, g0, [g1], ALL)",
                  isinstance(paths, list), f"{len(paths)} paths")

        # Subgraph
        sub = ga.get_subgraph(graph, gates[:5])
        check("get_subgraph(graph, gates[:5])", sub is not None,
              f"V={sub.get_num_vertices() if sub else 'None'}")

    except Exception as e:
        import traceback
        check("graph_algorithm", False, f"{type(e).__name__}: {e}")
        traceback.print_exc()


def verify_solve_fsm(netlist):
    section("solve_fsm")
    try:
        import solve_fsm
        check("import solve_fsm", True,
              str([n for n in dir(solve_fsm) if not n.startswith("_")]))

        # Find DFF gates
        dff_gates = [g for g in netlist.get_gates()
                     if "DFF" in g.get_type().get_name().upper()]
        check(f"Found {len(dff_gates)} DFF gates", len(dff_gates) > 0, "")

        if dff_gates:
            # Try brute force with small subset
            state_reg = dff_gates[:3]
            all_gates = netlist.get_gates()
            result = solve_fsm.solve_fsm_brute_force(
                netlist, state_reg, all_gates)
            check("solve_fsm_brute_force(nl, [3 DFFs], all_gates)",
                  result is not None, f"type={type(result).__name__}")
            if isinstance(result, dict):
                check("  transition dict size", len(result) > 0,
                      f"{len(result)} states")
                # Show first entry
                for k, v in list(result.items())[:1]:
                    check(f"  state {k}", isinstance(v, dict),
                          f"{len(v)} transitions")
    except Exception as e:
        check("solve_fsm", False, f"{type(e).__name__}: {e}")


def verify_simulator(netlist):
    section("netlist_simulator")
    try:
        import netlist_simulator
        check("import netlist_simulator", True,
              str([n for n in dir(netlist_simulator)
                   if not n.startswith("_")][:20]))
    except Exception as e:
        check("netlist_simulator", False, f"{type(e).__name__}: {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_plugins.py <netlist.v>")
        sys.exit(1)

    netlist_path = sys.argv[1]
    print(f"Loading: {netlist_path}")
    netlist = load_all(netlist_path)
    print(f"Loaded: {len(netlist.get_gates())} gates, "
          f"{len(netlist.get_nets())} nets")

    verify_dataflow(netlist)
    verify_graph_algorithm(netlist)
    verify_solve_fsm(netlist)
    verify_simulator(netlist)

    print(f"\n{'='*60}")
    print("  Phase 2 plugin verification complete.")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
