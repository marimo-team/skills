# Skills

This repository contains
[skills](https://support.claude.com/en/articles/12512176-what-are-skills) for
use with marimo.

Install these skills with:

```
npx skills add marimo-team/skills
```

The benefit of `npx skills` is that it supports [many agents](https://github.com/vercel-labs/skills?tab=readme-ov-file#supported-agents). So you can do things like:

```
npx skills add marimo-team/skills --agent claude-code
npx skills add marimo-team/skills --agent opencode
```

We welcome feedback: [issues](https://github.com/marimo-team/skills/issues) and
pull requests are welcome. You can also join our
[Discord](https://discord.com/invite/QdpFxJWhyt) or
[Reddit](https://www.reddit.com/r/marimo_notebook/) to get in touch.

## Available skills

| Skill | Description |
|-------|-------------|
| [`marimo-notebook`](skills/marimo-notebook) | Write a marimo notebook in a Python file in the right format. |
| [`jupyter-to-marimo`](skills/jupyter-to-marimo) | Convert a Jupyter notebook (`.ipynb`) to a marimo notebook (`.py`). |
| [`streamlit-to-marimo`](skills/streamlit-to-marimo) | Convert a Streamlit app to a marimo notebook. |
| [`anywidget`](skills/anywidget) | Generate anywidget components for marimo notebooks. |
| [`marimo-batch`](skills/marimo-batch) | Prepare a marimo notebook for a scheduled / batch run. |
| [`wasm-compatibility`](skills/wasm-compatibility) | Check whether a marimo notebook is WebAssembly (WASM) compatible and report issues. |
| [`add-molab-badge`](skills/add-molab-badge) | Add "Open in molab" badge(s) linking to marimo notebooks in READMEs, docs, or websites. |
| [`implement-paper`](skills/implement-paper) | Implement a research paper as an interactive marimo notebook, together with the user. |
| [`implement-paper-auto`](skills/implement-paper-auto) | Implement a research paper in a marimo notebook fully automatically (no extra input). |
| [`auto-paper-demo`](skills/auto-paper-demo) | Make a demo of a research paper in a marimo notebook fully automatically. |

## What are skills?

Skills are folders of instructions, scripts, and resources
that Claude (and many other agents) loads dynamically to improve performance on
specialized tasks.

For more information, check out:

- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [skills.sh](https://skills.sh/)

[GitHub issues](https://github.com/marimo-team/issues) and pull requests are
welcome. You can join our [Discord](https://discord.com/invite/QdpFxJWhyt) or
[Reddit](https://www.reddit.com/r/marimo_notebook/) to get in touch!
