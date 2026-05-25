"""JSON-backed memory graph.

Plain JSON file on disk, plain Python dicts in memory. Inspectable in any
editor. Versionable with git. No graph library dependencies.

Design choices:
  - Nodes and edges are dicts with a `type` key and a `data` payload.
  - Nodes are keyed by their string id ("char:mira", "sym:cracked-glass").
  - Edges are a flat list (NOT keyed) — most graph operations are
    "find all edges where X" which is O(N) over the edge list. Fine at MVP scale.
  - Mutations go through MemoryGraph methods (apply_writes, query) so an audit
    trail is easy to add later.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class MemoryGraph:
    """In-memory graph backed by a JSON file."""

    nodes: dict[str, dict[str, Any]] = field(default_factory=dict)
    edges: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    path: Path | None = None

    # ─── Persistence ─────────────────────────────────────────────────────────

    @classmethod
    def load(cls, path: Path) -> MemoryGraph:
        """Load a graph from a JSON file. Returns an empty graph if file missing."""
        if not path.exists():
            logger.info("Memory graph file not found; starting empty: %s", path)
            return cls(path=path)
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        return cls(
            nodes=data.get("nodes", {}),
            edges=data.get("edges", []),
            metadata=data.get("metadata", {}),
            path=path,
        )

    @classmethod
    def from_excerpt(cls, excerpt: dict[str, Any]) -> MemoryGraph:
        """Build a graph from a graph_excerpt YAML dict (as in sample inputs).

        Converts the sample's nested-by-category structure (excerpt.nodes.characters,
        excerpt.nodes.symbols, etc.) into the flat node/edge representation.
        """
        g = cls()
        ex_nodes = excerpt.get("nodes", {}) or {}

        for category in ("characters", "symbols", "events", "locations", "debts"):
            for entry in ex_nodes.get(category, []) or []:
                nid = entry.get("id")
                if not nid:
                    continue
                node_type = {
                    "characters": "character",
                    "symbols": "symbol",
                    "events": "event",
                    "locations": "location",
                    "debts": "debt",
                }[category]
                g.nodes[nid] = {"type": node_type, "data": dict(entry)}

        ex_edges = excerpt.get("edges", {}) or {}
        for edge_type, entries in ex_edges.items():
            for entry in entries or []:
                e = dict(entry)
                e["type"] = edge_type
                g.edges.append(e)

        return g

    def save(self, path: Path | None = None) -> None:
        target = path or self.path
        if target is None:
            raise ValueError("save() requires either a `path` arg or graph.path set")
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", encoding="utf-8") as fh:
            json.dump(
                {"nodes": self.nodes, "edges": self.edges, "metadata": self.metadata},
                fh,
                indent=2,
                ensure_ascii=False,
                sort_keys=False,
            )
        logger.debug("Saved memory graph: %s", target)

    # ─── Queries ─────────────────────────────────────────────────────────────

    def get_node(self, node_id: str) -> dict[str, Any] | None:
        return self.nodes.get(node_id)

    def find_edges(
        self,
        edge_type: str | None = None,
        subject: str | None = None,
        object_: str | None = None,
    ) -> list[dict[str, Any]]:
        """Linear scan; sufficient at MVP scale."""
        result = []
        for e in self.edges:
            if edge_type and e.get("type") != edge_type:
                continue
            if subject and e.get("subject") != subject:
                continue
            if object_ and e.get("object") != object_:
                continue
            result.append(e)
        return result

    def symbol_state(self, symbol_id: str) -> str | None:
        """Return current state of a symbol node, or None if not present."""
        node = self.get_node(symbol_id)
        if not node or node.get("type") != "symbol":
            return None
        return node.get("data", {}).get("state")

    # ─── Mutations ───────────────────────────────────────────────────────────

    def upsert_node(self, node_id: str, node_type: str, data: dict[str, Any]) -> None:
        self.nodes[node_id] = {"type": node_type, "data": data}

    def add_edge(self, edge_type: str, **kwargs: Any) -> None:
        edge = {"type": edge_type, **kwargs}
        self.edges.append(edge)

    def set_symbol_state(self, symbol_id: str, new_state: str) -> None:
        """Update a symbol node's state. Validation happens at the agent layer."""
        node = self.nodes.setdefault(
            symbol_id, {"type": "symbol", "data": {"id": symbol_id}}
        )
        node["data"]["state"] = new_state
