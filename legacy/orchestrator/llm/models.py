"""Model registry: agent_id → preferred Claude model.

The MVP runs every agent on Opus 4.7. The registry exists so a future
implementation can route validators to cheaper models (Sonnet/Haiku) without
touching workflow code.
"""

from __future__ import annotations

# Anthropic model IDs (as of 2026-05). See orchestrator/README.md for refresh policy.
OPUS_4_7 = "claude-opus-4-7"
SONNET_4_6 = "claude-sonnet-4-6"
HAIKU_4_5 = "claude-haiku-4-5-20251001"


# MVP routing: everyone on Opus. Tighten later when each agent's contract is
# stable enough to allow model downgrade without quality regression.
AGENT_MODEL_REGISTRY: dict[str, str] = {
    # Generative agents
    "vision-keeper": OPUS_4_7,
    "theme-analyst": OPUS_4_7,
    "lore-architect": OPUS_4_7,
    "character-psychologist": OPUS_4_7,
    "plot-engineer": OPUS_4_7,
    "scene-director": OPUS_4_7,
    "dialogue-specialist": OPUS_4_7,
    # Adversarial validators
    "symbolism-tracker": OPUS_4_7,
    "continuity-auditor": OPUS_4_7,
    "anti-ai-editor": OPUS_4_7,
    # Cultural layer
    "cultural-adapter": OPUS_4_7,
    "cultural-dialogue-specialist": OPUS_4_7,
    "prose-rhythm-agent": OPUS_4_7,
    "language-style-validator": OPUS_4_7,
}


def model_for_agent(agent_id: str, default: str = OPUS_4_7) -> str:
    """Return the model id for an agent. Falls back to `default` if unknown."""
    return AGENT_MODEL_REGISTRY.get(agent_id, default)
