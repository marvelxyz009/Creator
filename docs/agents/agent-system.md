# Agent System

AetherForge is a **multi-agent narrative workflow**. Each agent is a specialist with a narrow role, a typed input/output contract, and an explicit place in the [[narrative-pipeline]].

## Design Principles

1. **One job per agent.** No "story agent". Specialists only.
2. **Typed contracts.** Every agent has a schema-validated input and output (see [[agent-contracts]]).
3. **Adversarial pairs.** Generative agents are paired with adversarial validators (Prose ↔ Revision, World ↔ Continuity).
4. **No hidden state.** All inter-agent state lives in artifacts or the [[memory-graph]].

## Roster

### Generative Agents

| Agent | Role | Stage |
|---|---|---|
| **Vision Agent** | Translate brief + references into a single-page vision document. | 1 |
| **Theme Architect** | Extract and formalize the work's theme(s), core question, and thematic oppositions. | 2 |
| **World Architect** | Build the world's logic, constraints, and texture in service of theme. | 3 |
| **Character Psychologist** | Generate characters as systems of contradiction, not bundles of traits. | 4 |
| **Plot Architect** | Build the act/beat tree, pacing, and tension curves. | 5 |
| **Scene Designer** | Translate beats into scene specs (goal, conflict, turn, residue). | 6 |
| **Dialogue Agent** | Voice-specific dialogue honoring each character's signature. | 7 |
| **Prose Agent** | Render scene + dialogue into prose. | 8 |

### Adversarial / Validating Agents

| Agent | Role | Stage |
|---|---|---|
| **Theme Sentinel** | Reject scenes that fail to advance, complicate, or invert theme. | 9 |
| **Smell Detector** | Flag [[ai-smells]] in prose. | 9 |
| **Voice Auditor** | Verify each POV/dialogue line matches the character's voice signature. | 9 |
| **Continuity Agent** | Validate draft against [[memory-graph]]. | 10 |
| **Humanization Agent** | Perturb statistically-median prose into specific, surprising prose. | 11 |

### Service Agents

| Agent | Role |
|---|---|
| **Context Assembler** | Builds tailored context bundles. See [[context-assembly]]. |
| **Graph Curator** | Maintains the [[memory-graph]]: writes nodes/edges as artifacts produce them, resolves debts, audits dangling symbols. |
| **Reference Analyst** | Extracts structural patterns from reference works. See [[reference-analysis-system]]. |

## Coordination

Agents do **not** call each other directly. The pipeline runner:
1. Selects the next stage.
2. Asks Context Assembler for the bundle.
3. Invokes the stage's agent(s).
4. Validates output against the agent's contract.
5. Routes the output to the next stage (or to adversarial review).

This keeps agents stateless, swappable, and individually testable.

## Related

- [[agent-contracts]]
- [[narrative-pipeline]]
- [[context-assembly]]
