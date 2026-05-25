"""Jinja2 hydration of prompts with runtime bundles.

The SYSTEM prompt is the agent's prompt template body (the .prompt.md document
itself, served verbatim — Jinja2 is not applied here, because the templates
contain literal {{ ... }} examples that would otherwise be substituted).

The USER prompt is a small Jinja2-rendered scaffold that embeds the bundle as
YAML and asks the agent to produce its declared output format.

Design choice: NOT rendering Jinja2 over the prompt template itself avoids
collision with literal braces in YAML examples inside the templates. Jinja2
is reserved for the user-prompt scaffold only.
"""

from __future__ import annotations

import logging

import yaml
from jinja2 import Environment, StrictUndefined

from orchestrator.core.bundle import Bundle

logger = logging.getLogger(__name__)


_USER_PROMPT_TEMPLATE = """\
You are operating as the {{ agent_id }} agent of the AetherForge Creator Framework.

Your full agent contract (identity, responsibilities, inputs, output format,
validation checklist, anti-patterns) is in the SYSTEM prompt. Honor it.

## Bundle (your tailored context)

```yaml
{{ bundle_yaml }}
```

## Instructions

1. Follow your agent contract from the system prompt.
2. Use ONLY information present in the bundle above. Do not invent or hallucinate.
3. If a required input is missing from the bundle, emit `status: escalate` and
   name the missing input. Do not improvise.
4. Honor every constraint in `bundle.constraints.rules` (these are the
   global narrative laws — see shared/global-narrative-rules.md).
5. Emit your output as a single YAML document, starting at column 0.
6. Wrap your YAML output in a ```yaml ... ``` fenced block.
7. After the fenced block, do not write anything else.
{% if revision_directive %}

## Revision directive

{{ revision_directive }}
{% endif %}
"""


_jinja_env = Environment(
    undefined=StrictUndefined,
    autoescape=False,
    trim_blocks=True,
    lstrip_blocks=True,
)
_user_template = _jinja_env.from_string(_USER_PROMPT_TEMPLATE)


def render_user_prompt(bundle: Bundle) -> str:
    """Render the user prompt for an agent invocation from a Bundle."""
    bundle_yaml = yaml.safe_dump(
        bundle.to_dict(),
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        indent=2,
    )
    return _user_template.render(
        agent_id=bundle.for_agent,
        bundle_yaml=bundle_yaml.strip(),
        revision_directive=bundle.revision_directive,
    )


def render_system_prompt(prompt_template_body: str) -> str:
    """The system prompt is the agent's prompt template body, served verbatim."""
    return prompt_template_body


def extract_yaml_from_response(text: str) -> dict | None:
    """Extract the YAML block from an agent's response.

    The user prompt asks for a single ```yaml ... ``` fenced block. This helper
    extracts and parses it. Returns None on failure — callers decide whether
    that constitutes a hard_reject.
    """
    import re

    match = re.search(r"```yaml\s*\n(.*?)\n```", text, re.DOTALL)
    if match is None:
        # Fallback: try the entire response as YAML.
        try:
            data = yaml.safe_load(text)
            return data if isinstance(data, dict) else None
        except yaml.YAMLError:
            return None

    block = match.group(1)
    try:
        data = yaml.safe_load(block)
    except yaml.YAMLError as exc:
        logger.warning("YAML parse failed: %s", exc)
        return None
    return data if isinstance(data, dict) else None
