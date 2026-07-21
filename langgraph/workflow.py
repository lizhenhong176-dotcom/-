#!/usr/bin/env python3
"""
LangGraph 工作流定义。
编排端到端的木马检测流程：加载 → 分析 → 策略 → LLM → 报告。
"""

from __future__ import annotations

from typing import TypedDict

from langgraph.graph import StateGraph, END


class AgentState(TypedDict):
    """Agent 工作流状态。"""
    design_name: str
    netlist_path: str
    config: dict

    # 中间结果
    netlist: object | None
    module_infos: list | None
    analysis_results: dict | None
    strategy_results: list | None
    llm_insights: str

    # 最终输出
    report: object | None
    error: str | None


def build_workflow() -> StateGraph:
    """构建木马检测工作流。"""
    workflow = StateGraph(AgentState)

    workflow.add_node("load_netlist", _load_netlist)
    workflow.add_node("run_analysis", _run_analysis)
    workflow.add_node("classify_modules", _classify_modules)
    workflow.add_node("run_strategies", _run_strategies)
    workflow.add_node("llm_review", _llm_review)
    workflow.add_node("generate_report", _generate_report)

    workflow.set_entry_point("load_netlist")
    workflow.add_edge("load_netlist", "run_analysis")
    workflow.add_edge("run_analysis", "classify_modules")
    workflow.add_edge("classify_modules", "run_strategies")
    workflow.add_edge("run_strategies", "llm_review")
    workflow.add_edge("llm_review", "generate_report")
    workflow.add_edge("generate_report", END)

    return workflow.compile()


def _load_netlist(state: AgentState) -> AgentState:
    """加载网表节点。"""
    # 由 executor 实际加载
    return state


def _run_analysis(state: AgentState) -> AgentState:
    """执行基础分析节点。"""
    return state


def _classify_modules(state: AgentState) -> AgentState:
    """LLM 模块分类节点。"""
    return state


def _run_strategies(state: AgentState) -> AgentState:
    """执行检测策略节点。"""
    return state


def _llm_review(state: AgentState) -> AgentState:
    """LLM 综合评审节点。"""
    return state


def _generate_report(state: AgentState) -> AgentState:
    """报告生成节点。"""
    return state


# 便捷运行
def run_pipeline(design_name: str, netlist_path: str, config: dict) -> dict:
    """运行完整检测流水线。"""
    workflow = build_workflow()
    initial_state: AgentState = {
        "design_name": design_name,
        "netlist_path": netlist_path,
        "config": config,
        "netlist": None,
        "module_infos": None,
        "analysis_results": None,
        "strategy_results": None,
        "llm_insights": "",
        "report": None,
        "error": None,
    }
    return workflow.invoke(initial_state)
