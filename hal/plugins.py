#!/usr/bin/env python3
"""HAL 插件管理器 — 加载分析插件并暴露便捷属性。"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

# HAL 已编译插件目录
PLUGIN_DIR = "/home/i/hal/build/lib/hal_plugins/"


class Plugins:
    """HAL 插件生命周期管理。"""

    # 实际已编译可用的分析插件 (对齐 config.yaml hal.plugins)
    REQUIRED_PLUGINS = [
        "dataflow",
        "solve_fsm",
        "graph_algorithm",
        "netlist_simulator",
        "hawkeye",
        "z3_utils",
        "boolean_influence",
    ]

    def __init__(self):
        self._loaded: dict[str, Any] = {}

    def load_all(self) -> dict[str, bool]:
        """加载所有必需插件。"""
        import hal_py

        # 先批量加载所有 .so
        hal_py.plugin_manager.load_all_plugins([PLUGIN_DIR])
        available = hal_py.plugin_manager.get_plugin_names()

        results = {}
        for plugin in self.REQUIRED_PLUGINS:
            if plugin not in available:
                results[plugin] = False
                logger.warning(f"Plugin not compiled: {plugin}")
                continue
            try:
                self._loaded[plugin] = hal_py.plugin_manager.get_plugin_instance(plugin)
                results[plugin] = True
                logger.info(f"Plugin loaded: {plugin}")
            except Exception as e:
                results[plugin] = False
                logger.error(f"Failed to init plugin '{plugin}': {e}")
        return results

    def get(self, name: str):
        if name not in self._loaded:
            raise KeyError(f"Plugin not loaded: {name}")
        return self._loaded[name]

    @property
    def dataflow(self):           return self.get("dataflow")
    @property
    def fsm(self):                return self.get("solve_fsm")
    @property
    def graph_algorithm(self):    return self.get("graph_algorithm")
    @property
    def simulator(self):          return self.get("netlist_simulator")
    @property
    def hawkeye(self):            return self.get("hawkeye")
    @property
    def z3(self):                 return self.get("z3_utils")
    @property
    def boolean_influence(self):  return self.get("boolean_influence")
