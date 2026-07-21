#!/usr/bin/env python3
"""
Agent 执行器。
按分析计划顺序执行各分析步骤，收集结果。
"""

from __future__ import annotations

import logging
import time
from typing import Any

from agent.planner import AnalysisPlan, AnalysisStep

logger = logging.getLogger(__name__)


class Executor:
    """分析执行器。"""

    def __init__(self, hal_loader, tool_registry: dict, strategy_router):
        self.hal = hal_loader
        self.tools = tool_registry
        self.router = strategy_router
        self.results: dict[str, Any] = {}

    def execute_plan(self, plan: AnalysisPlan) -> dict:
        """执行完整分析计划。"""
        logger.info(f"Executing analysis plan for: {plan.design_name}")

        for step in plan.sorted_steps():
            logger.info(f"Step: {step.name} ({step.tool})")
            try:
                start = time.time()
                result = self._execute_step(step)
                elapsed = time.time() - start
                self.results[step.name] = {
                    "status": "ok",
                    "result": result,
                    "elapsed": elapsed,
                }
                logger.info(f"  Done in {elapsed:.2f}s")
            except Exception as e:
                logger.error(f"  Failed: {e}")
                self.results[step.name] = {
                    "status": "error",
                    "error": str(e),
                    "elapsed": 0,
                }

        return self.results

    def _execute_step(self, step: AnalysisStep):
        """执行单个步骤，路由到对应工具。"""
        netlist = self.hal.netlist

        tool_map = {
            "module_analysis": self._run_module_analysis,
            "gate_analysis": self._run_gate_analysis,
            "net_analysis": self._run_net_analysis,
            "register_analysis": self._run_register_analysis,
            "cone_analysis": self._run_cone_analysis,
            "uart_strategy": self._run_strategy,
            "crypto_strategy": self._run_strategy,
            "fsm_strategy": self._run_strategy,
        }

        handler = tool_map.get(step.tool)
        if handler is None:
            raise ValueError(f"Unknown tool: {step.tool}")

        return handler(netlist, step)

    def _run_module_analysis(self, netlist, step):
        from analysis.module_analysis import analyze_all_modules
        return analyze_all_modules(netlist)

    def _run_gate_analysis(self, netlist, step):
        from analysis.gate_analysis import analyze_gates
        return analyze_gates(netlist)

    def _run_net_analysis(self, netlist, step):
        from analysis.net_analysis import analyze_nets
        return analyze_nets(netlist)

    def _run_register_analysis(self, netlist, step):
        from analysis.register_analysis import analyze_registers
        return analyze_registers(netlist)

    def _run_cone_analysis(self, netlist, step):
        from analysis.cone_analysis import analyze_cones
        return analyze_cones(netlist)

    def _run_strategy(self, netlist, step):
        # 通过 router 找到对应策略并执行
        strategies = self.router._instances
        strategy = strategies.get(step.tool)
        if strategy is None:
            raise ValueError(f"Strategy not found: {step.tool}")
        return strategy.analyze(netlist)
