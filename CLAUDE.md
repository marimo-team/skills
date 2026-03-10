# Skills Repository

## Shared references

Some skills include reference copies of other skills' content so they work standalone.
The source of truth for shared content lives in the original skill's `SKILL.md`.

Current shared references:

| Source | Copied to |
|--------|-----------|
| `skills/anywidget/SKILL.md` | `skills/marimo-notebook/references/ANYWIDGET.md` |
| `skills/anywidget/SKILL.md` | `skills/implement-paper/references/anywidget.md` |

After editing `skills/anywidget/SKILL.md`, run:

```bash
make sync
```

This copies the source file to all dependent locations. See the `Makefile` for details.
