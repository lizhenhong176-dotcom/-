#!/usr/bin/env python3
"""
检测策略基类。
所有木马检测策略继承此类，实现统一的接口。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Finding:
    """检测发现。"""

    title: str
    description: str
    severity: str  # low | medium | high | critical
    confidence: float  # 0.0 - 1.0
    location: str  # 模块/门/网表名
    evidence: list[str] = field(default_factory=list)
    recommendation: str = ""


@dataclass
class StrategyResult:
    """策略执行结果。"""

    strategy_name: str
    findings: list[Finding]
    execution_time: float = 0.0
    error: str | None = None


class BaseStrategy(ABC):
    """检测策略基类。"""

    name: str = "base"
    description: str = "基础检测策略"

    def __init__(self, config: dict | None = None):
        self.config = config or {}

    @abstractmethod
    def analyze(self, netlist, **kwargs) -> StrategyResult:
        """执行检测分析。子类必须实现。"""
        ...

    @abstractmethod
    def applicable_to(self, module_info) -> bool:
        """判断策略是否适用于该模块。"""
        ...

    def _make_finding(
        self, title: str, desc: str, severity: str, confidence: float, location: str,
        evidence: list[str] | None = None, recommendation: str = "",
    ) -> Finding:
        """快捷创建 Finding。"""
        return Finding(
            title=title, description=desc, severity=severity,
            confidence=confidence, location=location,
            evidence=evidence or [], recommendation=recommendation,
        )
