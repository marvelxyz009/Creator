"""Thin wrapper around the Anthropic SDK.

Single responsibility: take a system prompt + user prompt, return text. No
caching, no streaming for MVP. Prompt-caching can be layered later via the
SDK's extended_caching beta headers when prompts stabilize.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """A normalized LLM response. Holds text + token usage."""

    text: str
    input_tokens: int
    output_tokens: int
    model: str
    stop_reason: str


class LLMClient:
    """Anthropic SDK wrapper. Lazy-imports `anthropic` so import doesn't fail
    if the package is not installed in environments running only tests."""

    def __init__(self, api_key: str, default_model: str, default_max_tokens: int = 4096):
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY is not set. Copy .env.example to .env and fill it in."
            )
        self.api_key = api_key
        self.default_model = default_model
        self.default_max_tokens = default_max_tokens
        self._sdk_client = None   # lazy

    def _get_client(self):
        if self._sdk_client is None:
            try:
                from anthropic import Anthropic
            except ImportError as exc:
                raise ImportError(
                    "The 'anthropic' package is not installed. Run `pip install anthropic`."
                ) from exc
            self._sdk_client = Anthropic(api_key=self.api_key)
        return self._sdk_client

    def call(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float = 1.0,
    ) -> LLMResponse:
        """Synchronous call. Returns LLMResponse. Raises on API error."""
        client = self._get_client()
        model = model or self.default_model
        max_tokens = max_tokens or self.default_max_tokens

        logger.debug("LLM call: model=%s max_tokens=%d", model, max_tokens)

        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        # Anthropic responses return a list of content blocks; concatenate any text.
        text = "".join(
            block.text for block in response.content if getattr(block, "type", None) == "text"
        )
        return LLMResponse(
            text=text,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            model=response.model,
            stop_reason=response.stop_reason or "",
        )
