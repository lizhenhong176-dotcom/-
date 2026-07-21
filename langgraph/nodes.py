#!/usr/bin/env python3
"""
LangGraph 节点实现。
每个节点对应工作流中的一个分析步骤。
"""

from __future__ import annotations

import logging

from langgraph.workflow import AgentState

logger = logging.getLogger(__name__)


def load_netlist_node(state: AgentState) -> AgentState:
    """节点: 加载网表到 HAL。"""
    from hal.loader import HALLoader

    loader = HALLoader(state["config"])
    try:
        netlist = loader.load_netlist(state["netlist_path"])
        loader.load_analysis_plugins()
        state["netlist"] = netlist
    except Exception as e:
        state["error"] = f"Netlist load failed: {e}"
        logger.error(state["error"])
    return state


def analysis_node(state: AgentState) -> AgentState:
    """节点: 运行基础分析 (module, gate, net, register, cone)。"""
    if state["error"]:
        return state

    from agent.executor import Executor
    from agent.planner import Planner

    state["analysis_results"] = {
        "module": {},
        "gate": {},
        "net": {},
        "register": {},
        "cone": {},
    }

    return state


def classify_node(state: AgentState) -> AgentState:
    """节点: LLM 模块分类。"""
    if state["error"]:
        return state

    from llm.llm_client import LLMClient

    client = LLMClient(state["config"])
    # 对每个模块调用 LLM 分类
    state["module_infos"] = state.get("module_infos", [])
    return state


def strategy_node(state: AgentState) -> AgentState:
    """节点: 运行检测策略。"""
    if state["error"]:
        return state

    from agent.router import StrategyRouter

    router = StrategyRouter(state["config"])
    # 对每个模块运行匹配的策略
    state["strategy_results"] = []
    return state


def report_node(state: AgentState) -> AgentState:
    """节点: 生成最终报告。"""
    if state["error"]:
        return state

    from agent.report import ReportGenerator

    generator = ReportGenerator(state["config"])
    report = generator.generate(
        design_name=state["design_name"],
        execution_results=state.get("analysis_results", {}),
        strategy_results=state.get("strategy_results", []),
        llm_insights=state.get("llm_insights", ""),
    )
    state["report"] = report
    return state
