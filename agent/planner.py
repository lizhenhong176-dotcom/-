#!/usr/bin/env python3
"""
Agent 规划器。
根据网表特征生成分析计划：确定分析步骤、参数和优先级。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AnalysisStep:
    """分析步骤。"""

    name: str
    description: str
    tool: str  # 工具名
    target: str  # 分析目标 (模块/门/网表)
    params: dict = field(default_factory=dict)
    priority: int = 0  # 0=最高
    depends_on: list[str] = field(default_factory=list)  # 依赖步骤名


@dataclass
class AnalysisPlan:
    """分析计划。"""

    design_name: str
    steps: list[AnalysisStep]
    llm_reasoning: str = ""  # LLM 推理的补充说明

    def sorted_steps(self) -> list[AnalysisStep]:
        """按依赖关系排序步骤。"""
        done = set()
        ordered = []
        remaining = list(self.steps)
        # ponytail: 最多 100 次迭代，防止循环依赖导致死循环
        max_iter = len(remaining) * len(remaining) + 1
        while remaining:
            made_progress = False
            for step in list(remaining):
                if all(d in done for d in step.depends_on):
                    ordered.append(step)
                    done.add(step.name)
                    remaining.remove(step)
                    made_progress = True
            max_iter -= 1
            if max_iter <= 0:
                raise RuntimeError(f"Circular or missing dependency in steps: {[s.name for s in remaining]}")
        return ordered


class Planner:
    """分析计划生成器。"""

    DEFAULT_STEPS = [
        AnalysisStep("module", "模块级分析", "module_analysis", "all", priority=0),
        AnalysisStep("gate", "门级分析", "gate_analysis", "all", priority=1, depends_on=["module"]),
        AnalysisStep("net", "网表级分析", "net_analysis", "all", priority=1, depends_on=["module"]),
        AnalysisStep("register", "寄存器分析", "register_analysis", "all", priority=2, depends_on=["gate"]),
        AnalysisStep("cone", "锥形分析", "cone_analysis", "all", priority=3, depends_on=["net"]),
    ]

    def __init__(self, config: dict):
        self.config = config

    def generate_plan(self, design_name: str, netlist, module_infos: list) -> AnalysisPlan:
        """根据设计特征生成分析计划。"""
        steps = list(self.DEFAULT_STEPS)

        # 根据模块类型添加定制步骤
        for mi in module_infos:
            if mi.module_type == "interface":
                steps.append(AnalysisStep(
                    f"uart_check_{mi.name}", "UART 木马检测",
                    "uart_strategy", mi.name, priority=4,
                    depends_on=["cone"],
                ))
            elif mi.module_type == "crypto":
                steps.append(AnalysisStep(
                    f"crypto_check_{mi.name}", "加密模块木马检测",
                    "crypto_strategy", mi.name, priority=4,
                    depends_on=["cone"],
                ))
            elif mi.module_type == "controller":
                steps.append(AnalysisStep(
                    f"fsm_check_{mi.name}", "FSM 木马检测",
                    "fsm_strategy", mi.name, priority=4,
                    depends_on=["register"],
                ))

        return AnalysisPlan(design_name=design_name, steps=steps)
