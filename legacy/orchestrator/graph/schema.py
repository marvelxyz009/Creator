"""Memory graph node/edge type vocabulary.

Mirrors docs/architecture/memory-graph.md. The graph is loose-typed (dicts in
JSON) but agents and validators must use these constants when referencing
node/edge types so the orchestrator can sanity-check graph writes.
"""

from __future__ import annotations

# ─── Node types ──────────────────────────────────────────────────────────────

NODE_CHARACTER = "character"
NODE_RELATION = "relation"
NODE_EVENT = "event"
NODE_SYMBOL = "symbol"
NODE_LOCATION = "location"
NODE_THEME_BEAT = "theme-beat"
NODE_DEBT = "debt"

ALL_NODE_TYPES = {
    NODE_CHARACTER,
    NODE_RELATION,
    NODE_EVENT,
    NODE_SYMBOL,
    NODE_LOCATION,
    NODE_THEME_BEAT,
    NODE_DEBT,
}


# ─── Edge types ──────────────────────────────────────────────────────────────

EDGE_KNOWS = "KNOWS"
EDGE_PRESENT_AT = "PRESENT_AT"
EDGE_OWES = "OWES"
EDGE_SYMBOLIZES = "SYMBOLIZES"
EDGE_CONTRADICTS = "CONTRADICTS"
EDGE_RESOLVES = "RESOLVES"
EDGE_COMPLICATES = "COMPLICATES"
EDGE_INVERTS = "INVERTS"

ALL_EDGE_TYPES = {
    EDGE_KNOWS,
    EDGE_PRESENT_AT,
    EDGE_OWES,
    EDGE_SYMBOLIZES,
    EDGE_CONTRADICTS,
    EDGE_RESOLVES,
    EDGE_COMPLICATES,
    EDGE_INVERTS,
}


# ─── Symbol state machine ────────────────────────────────────────────────────

SYMBOL_STATES = {"not_yet_introduced", "introduced", "transformed", "resolved", "betrayed"}

# Legal state transitions for a symbol.
SYMBOL_LEGAL_TRANSITIONS: dict[str, set[str]] = {
    "not_yet_introduced": {"introduced"},
    "introduced": {"transformed", "resolved", "betrayed"},
    "transformed": {"resolved", "betrayed"},
    "resolved": set(),    # terminal
    "betrayed": set(),    # terminal
}


def is_legal_symbol_transition(from_state: str, to_state: str) -> bool:
    return to_state in SYMBOL_LEGAL_TRANSITIONS.get(from_state, set())


# ─── KNOWS levels ────────────────────────────────────────────────────────────

KNOWS_LEVELS = {"none", "partial", "full", "body_only"}
