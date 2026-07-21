#!/usr/bin/env python3
"""
FSM 木马检测策略。
检测状态机中的死态、隐态、额外状态转换、未授权状态路径。
"""

from __future__ import annotations

from strategies.base_strategy import BaseStrategy, StrategyResult


class FSMStrategy(BaseStrategy):
    """有限状态机木马检测。"""

    name = "fsm_strategy"
    description = "检测 FSM 中的木马：死态、隐态、异常转换、rare-trigger 条件"

    def applicable_to(self, module_info) -> bool:
        return module_info.module_type == "controller"

    def analyze(self, netlist, **kwargs) -> StrategyResult:
        findings = []

        # 1. 提取所有 FSM
        # 2. 分析状态可达性
        # 3. 检测死态 (dead states)
        # 4. 检测隐态 (unreachable states)
        # 5. 检测 Rare-trigger 转换条件

        findings.extend(self._extract_fsms(netlist))
        findings.extend(self._check_dead_states(netlist))
        findings.extend(self._check_hidden_states(netlist))
        findings.extend(self._check_rare_triggers(netlist))

        return StrategyResult(
            strategy_name=self.name,
            findings=findings,
        )

    def _extract_fsms(self, netlist) -> list:
        return []

    def _check_dead_states(self, netlist) -> list:
        return []

    def _check_hidden_states(self, netlist) -> list:
        return []

    def _check_rare_triggers(self, netlist) -> list:
        return []
