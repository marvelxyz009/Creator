# Creator Story Studio

Primary implementation is `story_studio/`, tests in `tests/`, active skills in `story_studio/skills/`.
The older framework, sample schemas and prose prompts are preserved under `legacy/`; do not use their manual workflow as the new app entrypoint.

The product is multi-genre. Prose is the canonical source and manga is its revision-linked adaptation. Never let an unapproved/latest stale source drive new manga. Visual quality review must inspect actual images. Never claim image prompts are generated pages.

Keep project content and credentials out of Git by default. Store generated project artifacts under the configured data root. Run `python -m unittest discover -s tests -v` for core changes and check the local UI for interface changes.
