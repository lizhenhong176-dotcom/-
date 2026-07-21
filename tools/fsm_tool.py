#!/usr/bin/env python3
"""
HAL FSM 插件封装。
FSM 提取、状态分析、转换路径分析。
"""

from __future__ import annotations

from typing import Any


class FSMTool:
    """HAL FSM 插件封装。"""

    def __init__(self, plugin_manager):
        self._pm = plugin_manager

    def extract_fsms(self, netlist) -> list:
        """提取网表中所有 FSM。"""
        fsm_plugin = self._pm.fsm
        return fsm_plugin.extract_fsms(netlist)

    def get_states(self, fsm) -> list:
        """获取 FSM 的所有状态。"""
        return fsm.get_states()

    def get_transitions(self, fsm) -> list:
        """获取 FSM 的所有状态转换。"""
        return fsm.get_transitions()

    def find_dead_states(self, fsm) -> list:
        """查找不可达状态 (死态)。"""
        states = set(self.get_states(fsm))
        reachable = self._compute_reachable(fsm)
        return list(states - reachable)

    def find_unreachable_states(self, fsm) -> list:
        """查找从初始状态无法到达的状态。"""
        return self.find_dead_states(fsm)

    def _compute_reachable(self, fsm) -> set:
        """计算从初始状态可达的状态集。"""
        reachable = set()
        initial = fsm.get_initial_state()
        if not initial:
            return reachable

        stack = [initial]
        while stack:
            state = stack.pop()
            if state in reachable:
                continue
            reachable.add(state)
            for trans in fsm.get_transitions_from(state):
                stack.append(trans.get_target())
        return reachable
