> **Note:** This repository contains implementations of skills for use with marimo. 

# Skills

Skills are folders of instructions, scripts, and resources that Claude (and many other agents) loads dynamically to improve performance on specialized tasks. 

For more information, check out:

- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [skills.sh](https://skills.sh/)

## About This Repository

We do our best to keep these skills up to date with the latest version of marimo and the skills specification, but they are not officially supported. Discussions and pull requests are welcome. You can join our [Discord](https://discord.com/invite/QdpFxJWhyt) or [Reddit](https://www.reddit.com/r/marimo_notebook/) to get in touch! 

## Quickstart

You can register this repository as a Claude Code Plugin marketplace by running the following command:

```
npx skills marimo-team/skills
```

The benefit of `npx skills` is that it supports [many many agents](https://github.com/vercel-labs/skills?tab=readme-ov-file#supported-agents). So you can do things like:

```
npx skills --agent claude-code marimo-team/skills
npx skills --agent opencode marimo-team/skills
```

