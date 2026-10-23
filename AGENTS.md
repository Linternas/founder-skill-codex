# Working on founder-skill-codex

This repository distributes eleven Codex skills in `skills/` and four Python
helpers. Keep each skill self-contained, except for the documented sibling
dependencies: pricing and plan use the CFO helper, and offer uses board lenses.
Install and distribute the whole pack so those paths resolve.

- Use `$founder-*` for skill mentions. Resolve bundled files from the loaded
  `SKILL.md` location; keep generated `founder/` files in the user's project.
- Python helpers and the installer use only Python 3.8+ standard-library modules.
- Preserve the separation between simulated research and real customer evidence.
  Board lenses summarize published frameworks without impersonating their authors.
- Keep sub-agent use conditional on session capabilities and authorization, with
  a disclosed sequential fallback. Do not prescribe a model or change permissions.
- Preserve upstream attribution in README.md and LICENSE.

Run the checks from this repository's root:

```bash
python3 -m unittest discover -s tests -v
```

When changing installation or packaging, also verify an installation into a
temporary destination and run helpers from outside the checkout. Never use a
developer's real skill directory as a test fixture.
