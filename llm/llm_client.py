#!/usr/bin/env python3
"""
LLM 客户端。
统一的 LLM 调用接口，支持 Anthropic 和 OpenAI。
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class LLMClient:
    """统一 LLM 客户端。"""

    def __init__(self, config: dict):
        self.config = config
        self.provider = config.get("llm", {}).get("provider", "anthropic")
        self.model = config.get("llm", {}).get("model", "claude-sonnet-4-6")
        self.temperature = config.get("llm", {}).get("temperature", 0.1)
        self.max_tokens = config.get("llm", {}).get("max_tokens", 4096)
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = self._create_client()
        return self._client

    def _create_client(self):
        if self.provider == "anthropic":
            import anthropic
            return anthropic.Anthropic()
        elif self.provider == "openai":
            import openai
            return openai.OpenAI()
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def chat(self, system_prompt: str, user_message: str) -> str:
        """发送对话请求。"""
        if self.provider == "anthropic":
            return self._chat_anthropic(system_prompt, user_message)
        else:
            return self._chat_openai(system_prompt, user_message)

    def classify(self, prompt_path: str, context: dict) -> str:
        """使用 prompt 模板进行分类。"""
        template = Path(f"llm/prompt/{prompt_path}").read_text()
        for k, v in context.items():
            template = template.replace(f"{{{{{k}}}}}", str(v))
        return self.chat("你是硬件安全分析专家。", template)

    def _chat_anthropic(self, system: str, user: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return response.content[0].text

    def _chat_openai(self, system: str, user: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return response.choices[0].message.content
