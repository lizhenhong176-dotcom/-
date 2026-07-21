#!/usr/bin/env python3
"""
UART/串行接口木马检测策略。
关注：空闲状态异常活动、未连接引脚的数据泄漏、波特率异常。
"""

from __future__ import annotations

from strategies.base_strategy import BaseStrategy, StrategyResult


class UARTStrategy(BaseStrategy):
    """UART 通信接口木马检测。"""

    name = "uart_strategy"
    description = "检测 UART/串行接口中的木马：数据泄漏、异常发送、配置篡改"

    def applicable_to(self, module_info) -> bool:
        return module_info.module_type == "interface"

    def analyze(self, netlist, **kwargs) -> StrategyResult:
        findings = []

        # 1. 检测 TX 路径异常
        findings.extend(self._check_tx_path(netlist))

        # 2. 检测未连接引脚
        findings.extend(self._check_floating_pins(netlist))

        # 3. 检测波特率生成器
        findings.extend(self._check_baud_generator(netlist))

        # 4. 检测 RX→TX 绕过路径 (可能是数据泄漏)
        findings.extend(self._check_rx_tx_bypass(netlist))

        return StrategyResult(
            strategy_name=self.name,
            findings=findings,
        )

    def _check_tx_path(self, netlist) -> list:
        """检查 TX 信号路径是否有额外的驱动源。"""
        results = []
        # ponytail: 遍历顶层输出找 tx，检查多驱动
        return results

    def _check_floating_pins(self, netlist) -> list:
        """检查关键模块的未连接引脚。"""
        results = []
        return results

    def _check_baud_generator(self, netlist) -> list:
        """检查波特率生成逻辑是否有异常分频器。"""
        results = []
        return results

    def _check_rx_tx_bypass(self, netlist) -> list:
        """检查是否有从接收到发送的绕过路径。"""
        results = []
        return results
