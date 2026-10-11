# Creator chat workshop

Operate entirely in the active chat. Entry skill: story_studio/skills/creator-studio/SKILL.md. Ask meaningful creative choices directly here; no web UI, background model jobs, provider API or nested Codex/Claude process. Use available session image tools for manga. Read saved progress before continuing.

Primary code: story_studio/. Tests: tests/. Active role skills: story_studio/skills/. The product covers multiple genres and independent worlds; XEROTH is never assumed for unrelated projects.

Prose is canonical. Current audited edited prose is required for manga. Preserve source-linked revisions and invalidate downstream artifacts when a source changes. Inspect actual images before recording visual approval. Never claim an image prompt is a rendered page or a schema check is a visual review.

Save actual output and checkpoints locally under stories/ (or configured STUDIO_DATA). Keep stories/, old .studio/ data and credentials out of Git by default. Do not delete old project data. Commit/push code or skills when requested. Run python -m unittest discover -s tests -v for changes.
