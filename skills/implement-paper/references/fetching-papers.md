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
