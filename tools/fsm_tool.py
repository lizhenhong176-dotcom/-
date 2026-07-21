#!/usr/bin/env python3
"""
HAL FSM (solve_fsm) 插件封装。
从门级网表提取有限状态机：状态寄存器、状态转换图。
API 经 check_plugins.py 验证。
"""
from __future__ import annotations

import sys
from typing import Any

sys.path.insert(0, "/home/i/hal/build/lib/hal_plugins/")


class FSMTool:
    """HAL solve_fsm 插件封装。"""

    def __init__(self, plugin_manager=None):
        self._plugin_manager = plugin_manager

    def extract_fsms(self, netlist,
                     state_regs: list | None = None,
                     transition_logic: list | None = None) -> dict | None:
        """
        提取 FSM 状态转换图。
        返回 {state: {next_state: BooleanFunction}} 或 None。
        """
        import solve_fsm

        if state_regs is None:
            # 自动找所有 DFF 作为候选状态寄存器
            state_regs = [g for g in netlist.get_gates()
                          if "DFF" in g.get_type().get_name().upper()]
        if transition_logic is None:
            transition_logic = list(netlist.get_gates())

        return solve_fsm.solve_fsm_brute_force(
            netlist, state_regs, transition_logic)

    def get_states(self, transition_dict: dict) -> list[int]:
        """从 transition dict 获取所有状态 ID。"""
        if transition_dict is None:
            return []
        return list(transition_dict.keys())

    def get_transitions(self, transition_dict: dict,
                        from_state: int) -> dict[int, Any]:
        """获取从某状态出发的所有转换。"""
        if transition_dict is None:
            return {}
        return transition_dict.get(from_state, {})

    def find_dead_states(self, transition_dict: dict) -> list[int]:
        """查找死态 (无出边的状态)。"""
        if transition_dict is None:
            return []
        return [s for s, trans in transition_dict.items()
                if not trans]

    def find_unreachable_states(self, transition_dict: dict,
                                initial_state: int = 0) -> list[int]:
        """BFS 查找从初始状态不可达的状态。"""
        if transition_dict is None:
            return []

        all_states = set(transition_dict.keys())
        reachable = set()
        queue = [initial_state]

        while queue:
            s = queue.pop(0)
            if s in reachable:
                continue
            if s not in transition_dict:
                continue
            reachable.add(s)
            for next_s in transition_dict[s]:
                if next_s not in reachable:
                    queue.append(next_s)

        return list(all_states - reachable)

    def generate_dot(self, transition_dict: dict,
                     state_regs: list,
                     graph_path: str = "fsm_graph.dot") -> bool:
        """生成 FSM 状态图的 DOT 文件。"""
        import solve_fsm
        try:
            solve_fsm.generate_dot_graph(state_regs, transition_dict,
                                         graph_path)
            return True
        except Exception:
            return False
