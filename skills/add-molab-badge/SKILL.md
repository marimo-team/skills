---
name: add-molab-badge
description: Add "Open in molab" badge(s) to a GitHub repository's README, linking to marimo notebooks.
---

# Add molab badge

Add "Open in molab" badge(s) to a GitHub repository's README, linking to marimo notebooks.

## Instructions

1. Read the repository's README file.

2. Find all marimo notebook files (`.py` files) in the repository. Use `Glob` with patterns like `**/*.py` and then check for the marimo header (`import marimo` or `app = marimo.App`) to confirm they are marimo notebooks.

3. Determine which notebooks should get badges. If the README already has links to notebooks (e.g., via `marimo.app` links or existing badges), replace those. Otherwise, ask the user which notebooks should be linked.

4. Construct the molab URL for each notebook using this format:

   ```
   https://molab.marimo.io/github/{owner}/{repo}/blob/{branch}/{path_to_notebook}
   ```

   - `{owner}/{repo}`: the GitHub owner and repository name. Determine from the git remote (`git remote get-url origin`).
   - `{branch}`: typically `main`. Confirm from the repository's default branch.
   - `{path_to_notebook}`: the path to the `.py` notebook file relative to the repository root.

5. Apply the `/wasm` suffix rules:
   - If **replacing** an existing `marimo.app` link, append `/wasm` to the molab URL. This is because `marimo.app` runs notebooks client-side (WASM), so the molab equivalent needs the `/wasm` suffix to preserve that behavior.
   - If adding a **new** badge (not replacing a `marimo.app` link), do **not** append `/wasm` unless the user explicitly requests it.

6. Use the following markdown badge format:

   ```markdown
   [![Open in molab](https://marimo.io/molab-shield.svg)](URL)
   ```

   Where `URL` is the constructed molab URL (with or without `/wasm` per the rules above).

7. When replacing existing badges or links:
   - Replace `marimo.app` URLs with the equivalent `molab.marimo.io` URLs.
   - Replace old shield image URLs (e.g., `https://marimo.io/shield.svg` or camo-proxied versions) with `https://marimo.io/molab-shield.svg`.
   - Set the alt text to `Open in molab`.
   - Preserve surrounding text and markdown structure.

8. Edit the README in place. Do not rewrite unrelated sections.

## Examples

**Replacing a marimo.app badge:**

Before:
```markdown
[![](https://marimo.io/shield.svg)](https://marimo.app/github.com/owner/repo/blob/main/notebook.py)
```

After:
```markdown
[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/owner/repo/blob/main/notebook.py/wasm)
```

Note: `/wasm` is appended because this replaces a `marimo.app` link.

**Adding a new badge (no existing marimo.app link):**

```markdown
[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/owner/repo/blob/main/notebooks/demo.py)
```

Note: no `/wasm` suffix by default for new badges.
