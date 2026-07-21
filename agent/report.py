#!/usr/bin/env python3
"""
Agent 报告生成器。
汇总所有分析结果，生成可读的木马检测报告 (Markdown/JSON)。
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from strategies.base_strategy import Finding


@dataclass
class TrojanReport:
    """木马检测报告。"""

    design_name: str
    timestamp: str
    summary: dict = field(default_factory=dict)
    findings: list[Finding] = field(default_factory=list)
    stats: dict = field(default_factory=dict)
    risk_score: float = 0.0  # 0-100
    recommendation: str = ""

    def to_markdown(self) -> str:
        """生成 Markdown 报告。"""
        lines = [
            f"# 硬件木马检测报告",
            f"",
            f"**设计**: {self.design_name}",
            f"**时间**: {self.timestamp}",
            f"**风险评分**: {self.risk_score:.1f}/100",
            f"",
            f"## 概览",
            f"",
            f"| 指标 | 数值 |",
            f"|------|------|",
        ]
        for k, v in self.summary.items():
            lines.append(f"| {k} | {v} |")

        lines += ["", "## 检测发现", ""]
        if not self.findings:
            lines.append("未发现可疑项。")
        else:
            for i, f in enumerate(self.findings, 1):
                severity_emoji = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}
                emoji = severity_emoji.get(f.severity, "⚪")
                lines += [
                    f"### {i}. {emoji} {f.title}",
                    f"",
                    f"- **严重程度**: {f.severity}",
                    f"- **置信度**: {f.confidence:.0%}",
                    f"- **位置**: `{f.location}`",
                    f"- **描述**: {f.description}",
                ]
                if f.evidence:
                    lines.append(f"- **证据**: {', '.join(f.evidence)}")
                if f.recommendation:
                    lines.append(f"- **建议**: {f.recommendation}")
                lines.append("")

        lines += [
            "## 统计",
            "",
            "```json",
            json.dumps(self.stats, indent=2, ensure_ascii=False),
            "```",
            "",
            f"## 建议",
            f"",
            self.recommendation,
        ]
        return "\n".join(lines)

    def to_json(self, path: str | Path):
        """导出 JSON。"""
        path = Path(path)
        data = {
            "design_name": self.design_name,
            "timestamp": self.timestamp,
            "risk_score": self.risk_score,
            "summary": self.summary,
            "findings": [
                {
                    "title": f.title, "description": f.description,
                    "severity": f.severity, "confidence": f.confidence,
                    "location": f.location, "evidence": f.evidence,
                    "recommendation": f.recommendation,
                }
                for f in self.findings
            ],
            "stats": self.stats,
            "recommendation": self.recommendation,
        }
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False))


class ReportGenerator:
    """报告生成器。"""

    def __init__(self, config: dict):
        self.config = config

    def generate(
        self, design_name: str, execution_results: dict,
        strategy_results: list, llm_insights: str = "",
    ) -> TrojanReport:
        """汇总所有结果生成报告。"""
        from datetime import datetime

        # 收集所有 findings
        all_findings = []
        for sr in strategy_results:
            if sr and sr.findings:
                all_findings.extend(sr.findings)

        # 计算风险评分
        risk_score = self._compute_risk_score(all_findings)

        # 统计
        stats = self._compute_stats(execution_results, all_findings)

        # 生成建议
        recommendation = self._generate_recommendation(all_findings, risk_score)

        return TrojanReport(
            design_name=design_name,
            timestamp=datetime.now().isoformat(),
            summary={
                "总发现数": len(all_findings),
                "高危发现": sum(1 for f in all_findings if f.severity in ("high", "critical")),
                "风险评分": f"{risk_score:.1f}/100",
            },
            findings=all_findings,
            stats=stats,
            risk_score=risk_score,
            recommendation=recommendation or llm_insights,
        )

    def _compute_risk_score(self, findings: list[Finding]) -> float:
        severity_weights = {"low": 5, "medium": 15, "high": 30, "critical": 50}
        total = sum(
            severity_weights.get(f.severity, 5) * f.confidence
            for f in findings
        )
        return min(total, 100.0)

    def _compute_stats(self, exec_results: dict, findings: list[Finding]) -> dict:
        return {
            "total_steps": len(exec_results),
            "successful_steps": sum(1 for r in exec_results.values() if r["status"] == "ok"),
            "failed_steps": sum(1 for r in exec_results.values() if r["status"] != "ok"),
            "total_findings": len(findings),
            "by_severity": {
                sev: sum(1 for f in findings if f.severity == sev)
                for sev in ("low", "medium", "high", "critical")
            },
            "total_elapsed": sum(r.get("elapsed", 0) for r in exec_results.values()),
        }

    def _generate_recommendation(self, findings: list[Finding], risk_score: float) -> str:
        if risk_score >= 70:
            return "⚠️ 高风险：建议立即进行人工审查，可能存在功能级木马。"
        elif risk_score >= 30:
            return "⚡ 中等风险：建议对有疑问的模块进行门级仿真验证。"
        elif risk_score > 0:
            return "✅ 低风险：少量可疑项，建议定期复查。"
        return "✅ 未检测到明显木马特征。"
