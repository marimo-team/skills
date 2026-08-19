---
name: jupyter-to-marimo
description: Convert a Jupyter notebook (.ipynb) to a marimo notebook (.py).
---

# Converting Jupyter Notebooks to Marimo

## Convert first

**Important:** Run the converter before you read the source notebook:

```bash
uvx marimo convert <notebook.ipynb> -o <notebook.py>
```

Read the `.ipynb` file only if conversion fails or the generated file omits required information. Treat the generated file as a first draft.

Run this command after conversion and after substantial edits:

```bash
uvx marimo check <notebook.py>
```

## Review the conversion

- Verify all required packages in the PEP 723 metadata. The converter can miss some package-installation forms.
- Remove residual installation cells and stale installation prose. Add version constraints only when required.
- Use `--sandbox` when a notebook uses PEP 723 metadata.
- Preserve the purpose and intended workflow of the source notebook.
- Arrange cells for presentation. marimo determines execution order from variable definitions and references.
- A cell can appear before a cell that defines its input.
- Merge or split cells when the current boundaries reduce clarity.
- Remove redundant Jupyter artifacts, such as unnecessary `display()` calls.
- Review converted magic commands. Keep valid conversions, and resolve comments that report unsupported magics.
- Put the value to render in the final expression of each cell.
- Keep added UI and helper functions proportional to the notebook purpose.
- Replace interactive input methods that wait for terminal input or do not work in the target interface. Use suitable UI controls, script parameters, or environment values.
- Do not print, log, or save secrets. Consider [EnvConfig](https://koaning.github.io/wigglystuff/reference/env-config.md) for multiple environment values.
- Identify expensive work and external side effects. If work must wait, gate it with `mo.stop()` and a suitable UI element.
- Use a form if the user must submit multiple values together.
- Define downstream values after the gate so the dependency graph defers dependent cells.
- Present useful results with simple native components. Add live refresh only when the intended workflow requires it.
- For ipywidgets, read [`references/widgets.md`](references/widgets.md).
- For LaTeX and MathJax, read [`references/latex.md`](references/latex.md).

## Validate the result

- **Run `marimo check` again** after all edits.
- Run the notebook in each intended mode. Confirm that it has the intended behavior.
- When practical, open the source and converted notebooks side by side and invite the user to review.
- Compare content, controls, outputs, and workflow. Cell order and layout can differ.
- Inspect changed files for secrets, generated data, caches, logs, and other runtime files.
