#!/usr/bin/env python3
"""
HAL 网表加载器。
负责将门级网表加载到 HAL 框架，初始化插件。
"""

from __future__ import annotations

import logging
from pathlib import Path

import hal_py

logger = logging.getLogger(__name__)

# HAL 插件 .so 目录
PLUGIN_DIR = "/home/i/hal/build/lib/hal_plugins/"


class HALLoader:
    """HAL 网表加载与插件管理。"""

    def __init__(self, config: dict):
        self.config = config
        self.netlist = None
        self._plugins_loaded: bool = False

    def _ensure_plugins(self):
        """确保 HAL 解析插件已加载 (verilog_parser, hgl_parser 等)。"""
        if self._plugins_loaded:
            return
        # 注册插件目录到 sys.path，使 tools/ 可直接 import dataflow/graph_algorithm 等
        import sys
        if PLUGIN_DIR not in sys.path:
            sys.path.insert(0, PLUGIN_DIR)
        hal_py.plugin_manager.load_all_plugins([PLUGIN_DIR])
        self._plugins_loaded = True
        names = hal_py.plugin_manager.get_plugin_names()
        logger.info(f"HAL plugins loaded: {len(names)}")

    def load_netlist(self, netlist_path: str | Path) -> hal_py.Netlist:
        """加载门级网表到 HAL。"""
        netlist_path = Path(netlist_path)
        hgl_path = self.config["hal"]["netlist"]["hgl"]

        if not netlist_path.exists():
            raise FileNotFoundError(f"Netlist not found: {netlist_path}")

        self._ensure_plugins()

        logger.info(f"Loading netlist: {netlist_path}")
        self.netlist = hal_py.NetlistFactory.load_netlist(
            str(netlist_path), str(hgl_path)
        )

        if self.netlist is None:
            raise RuntimeError(
                f"Failed to load netlist: {netlist_path}. "
                "Check gate library compatibility."
            )

        logger.info(
            f"Loaded: {len(self.netlist.get_gates())} gates, "
            f"{len(self.netlist.get_nets())} nets, "
            f"{len(self.netlist.get_modules())} modules"
        )
        return self.netlist

    def load_analysis_plugins(self) -> list[str]:
        """加载分析插件 (dataflow, fsm, graph_algorithm, simulator 等)。"""
        self._ensure_plugins()
        available = hal_py.plugin_manager.get_plugin_names()
        desired = self.config.get("hal", {}).get("plugins", [])
        loaded = []
        for name in desired:
            if name in available:
                logger.info(f"Plugin ready: {name}")
                loaded.append(name)
            else:
                logger.warning(f"Plugin not available: {name}")
        return loaded

    def get_modules(self) -> list:
        if not self.netlist:
            raise RuntimeError("Netlist not loaded")
        return self.netlist.get_modules()

    def get_top_module(self):
        if not self.netlist:
            raise RuntimeError("Netlist not loaded")
        return self.netlist.get_top_module()
