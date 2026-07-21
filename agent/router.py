#!/usr/bin/env python3
"""
Agent 路由器。
根据模块分析结果选择合适的检测策略。
"""

from __future__ import annotations

import logging
from typing import Any

from strategies.base_strategy import BaseStrategy, StrategyResult
from strategies.uart_strategy import UARTStrategy
from strategies.crypto_strategy import CryptoStrategy
from strategies.fsm_strategy import FSMStrategy
from strategies.dataflow_strategy import DataflowStrategy
from strategies.output_cone_strategy import OutputConeStrategy

logger = logging.getLogger(__name__)


class StrategyRouter:
    """策略路由器：根据模块特征选择并调度检测策略。"""

    STRATEGIES: list[type[BaseStrategy]] = [
        UARTStrategy,
        CryptoStrategy,
        FSMStrategy,
        DataflowStrategy,
        OutputConeStrategy,
    ]

    def __init__(self, config: dict):
        self.config = config
        self._instances: dict[str, BaseStrategy] = {}
        self._init_strategies()

    def _init_strategies(self):
        enabled = self.config.get("strategies", {}).get("enabled", [])
        for cls in self.STRATEGIES:
            instance = cls(self.config)
            if instance.name in enabled or not enabled:
                self._instances[instance.name] = instance

    def route(self, module_info) -> list[BaseStrategy]:
        """返回适用于该模块的策略列表。"""
        return [
            s for s in self._instances.values()
            if s.applicable_to(module_info)
        ]

    def run_all(self, netlist, module_info) -> list[StrategyResult]:
        """执行所有适用策略。"""
        strategies = self.route(module_info)
        logger.info(f"Routing {len(strategies)} strategies for module: {module_info.name}")

        results = []
        for strategy in strategies:
            try:
                logger.info(f"Running: {strategy.name}")
                result = strategy.analyze(netlist)
                results.append(result)
            except Exception as e:
                logger.error(f"Strategy {strategy.name} failed: {e}")
                results.append(StrategyResult(
                    strategy_name=strategy.name,
                    findings=[],
                    error=str(e),
                ))

        return results

    def list_strategies(self) -> list[dict]:
        """列出所有注册的策略。"""
        return [
            {"name": s.name, "description": s.description}
            for s in self._instances.values()
        ]
