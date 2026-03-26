---
name: implement-paper-auto
description: Implement a research paper in a marimo notebook fully automatically without extra user input.
---

You need to come up with a compelling story to tell from a paper. Do not ask the user for feedback/input. You need to apply thinking and come up with the best story yourself.

# Fetching Papers via AlphaXiv

Use alphaxiv.org to get structured, LLM-friendly paper content. This is faster and more reliable than trying to read a raw PDF.

## Extract the paper ID

Parse the paper ID from whatever the user provides:

| Input | Paper ID |
|-------|----------|
| `https://arxiv.org/abs/2401.12345` | `2401.12345` |
| `https://arxiv.org/pdf/2401.12345` | `2401.12345` |
| `https://alphaxiv.org/overview/2401.12345` | `2401.12345` |
| `2401.12345v2` | `2401.12345v2` |
| `2401.12345` | `2401.12345` |

## Fetch the AI-generated overview (try this first)

```bash
curl -s "https://alphaxiv.org/overview/{PAPER_ID}.md"
```

Returns a structured, detailed analysis of the paper as plain markdown. One call, no JSON parsing.

## Fetch the full paper text (fallback)

If the overview doesn't contain the specific detail you need (e.g., a particular equation, table, or proof):

```bash
curl -s "https://alphaxiv.org/abs/{PAPER_ID}.md"
```

Returns the full extracted text of the paper as markdown.

## Error handling

- **404 on the overview**: Report hasn't been generated for this paper yet. Try the full text instead.
- **404 on the full text**: Text hasn't been processed yet. As a last resort, direct the user to the PDF at `https://arxiv.org/pdf/{PAPER_ID}`.
- No authentication is required — these are public endpoints.

## What is a good implementation? 

A good implementation tells a story, that's the most important thing. The story should be simple, but it should not be missing. 

Papers typically have more than one concept in them. So that means you need to pick a story! It isn't the goal to fully implement the paper or to rerun a giant benchmark. The goal is to take a lesson/idea and to explain that very clearly in a notebook that can simply run on a CPU. That way, a user can easily run learn something from it. When you look at the notebook, what is the main concept or idea that you think is worth exploring? What is the concept that tells a story? 

Pick the idea that is easiest to explain with a minimum code example. For a minimum code example to really work, it tends to help to have one, maybe two charts to look at. Maybe there's a dropdown that lets you try out different settings. Possibly even a slider. But the one thing we would want to do is prevent that the user needs to do a lot of scrolling. 

It will be typical that you'll want to compare two approaches. But take a moment to think about the example, because that matters most to the story. Most of the time you don't want to use a toy example. They're not informative and they are overdone. It may be better to generate a creative example that shows where one approach can really shine. We don't want to cherry pick, but we also don't want to do examples that have been overdone either. 

I cannot stress enough how important it is to actually think about the story and the example before you write any code whatsoever. You should really ultra think this. Give the user some interaction but really try to prevent scrolling. A good example tells a story, it doesn't just state some facts. 

Feel free to think about this decision, but once you've got it clear what idea is best to showcase, immediately proceed to build the marimo notebook. 

Use the marimo-notebook skill for this, and possibly the anywidget skill, but only if a custom widget makes for a better story. If you strongly feel that it makes sense to use a custom anywidget, refer to [references/ANYWIDGET.md](references/ANYWIDGET.md).

When you are ready, make sure that you hide all the code and that you move the cells with inputs/outputs to the top of the file. 

Example: 

```
@app.cell
def _(hide_code=True):
    import marimo as mo
    return mo
```