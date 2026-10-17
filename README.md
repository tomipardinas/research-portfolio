# Jellyfish Research Portfolio: Tomas Pardinas

Tomas Pardinas is a Product Researcher / AI PM at [Jellyfish](https://jellyfish.co). This repository collects the research posts he wrote or co-wrote for Jellyfish Research, with full text and the original charts and figures.

## Posts

| Date | Title | Co-authors | Topics | Takeaway | Links |
|------|-------|------------|--------|----------|-------|
| 2026-10-06 | What is Jev and why you should care about it for your AI-DLC | — | ai industry trends, ai engineering, ai agents, LLM | Jev is a new AI model type from the family of “System One models.” It isn’t an LLM, but it created lots of waves. | [Original](https://jellyfishresearch.substack.com/p/what-is-jev-and-why-you-should-care) · [Local](posts/2026-10-06-what-is-jev-and-why-you-should-care/index.md) |
| 2026-08-17 | Agentic Coding: The Impact Gap Is Closing | — | agents, ai engineering, ai agents, LLM | Agents are spending more tokens, but are they getting more impact in organizations? | [Original](https://jellyfishresearch.substack.com/p/agentic-coding-the-impact-gap-is) · [Local](posts/2026-08-17-agentic-coding-the-impact-gap-is/index.md) |
| 2026-06-23 | The State of AI: H1 2026 | — | — | Exploding Spend, Diverging Returns | [Original](https://jellyfishresearch.substack.com/p/the-state-of-ai-h1-2026) · [Local](posts/2026-06-23-the-state-of-ai-h1-2026/index.md) |
| 2026-06-03 | Product Update: The Jellyfish MCP Is Now Documentation-Aware | Sophie Goldstein | agents, mcp, ai agents, LLM | Grounded answers, plus real docs for your agentic coding loops | [Original](https://jellyfishresearch.substack.com/p/product-update-the-jellyfish-mcp) · [Local](posts/2026-06-03-product-update-the-jellyfish-mcp/index.md) |
| 2026-05-21 | Our Journey with OpenClaw: Jellyclaw | Josiah Bruner | agents, ai agents, Openclaw | At Jellyfish we at the research team are looking for ways to innovate and research new trends. | [Original](https://jellyfishresearch.substack.com/p/our-journey-with-openclaw-jellyclaw) · [Local](posts/2026-05-21-our-journey-with-openclaw-jellyclaw/index.md) |
| 2026-05-07 | AI Agent Autonomy | — | ai industry trends, engineering productivity, agents, ai engineering | We asked ourselves: what does autonomy look like in AI age | [Original](https://jellyfishresearch.substack.com/p/ai-agent-autonomy) · [Local](posts/2026-05-07-ai-agent-autonomy/index.md) |
| 2026-03-23 | Measuring AI Agent Concurrency | — | ai industry trends, agents, ai engineering, ai agents | A research piece on AI agent concurrency using Claude Code telemetry | [Original](https://jellyfishresearch.substack.com/p/measuring-ai-agent-concurrency) · [Local](posts/2026-03-23-measuring-ai-agent-concurrency/index.md) |
| 2026-02-20 | Measuring Agentic Workflows | — | — | A framework to understand what and how agents work and how the new workflows are evolving | [Original](https://jellyfishresearch.substack.com/p/measuring-agentic-workflows) · [Local](posts/2026-02-20-measuring-agentic-workflows/index.md) |
| 2026-01-23 | Measuring ROI in AI era: The language effect | — | ai industry trends, engineering productivity, ai engineering, LLM | An analysis on AI ROI, acceptance rate and programing languages | [Original](https://jellyfishresearch.substack.com/p/measuring-roi-in-ai-era-the-language) · [Local](posts/2026-01-23-measuring-roi-in-ai-era-the-language/index.md) |
| 2025-12-11 | Luddites versus Lovers: is AI Coding Polarized, or is There a Middle Ground? | — | ai industry trends, engineering productivity, ai coding tools | Are we seeing a spectrum of adoption of AI coding tools — or is there a stark divide between engineers who are adopting these new tools enthusiastically, and the resisters who aren’t? | [Original](https://jellyfishresearch.substack.com/p/luddites-versus-lovers-is-ai-coding) · [Local](posts/2025-12-11-luddites-versus-lovers-is-ai-coding/index.md) |

10 posts · 55 images · metadata in [`data/posts.json`](data/posts.json)

## About this archive

These posts were originally published on [Jellyfish Research](https://jellyfishresearch.substack.com). Each post links back to its original page (see the "Original" links above and the `canonical_url` field in each post's frontmatter). The text is reproduced as published, converted to Markdown; images were downloaded at full resolution into each post's `images/` folder.

## Structure

```
posts/YYYY-MM-DD-<slug>/index.md   # full post with YAML frontmatter
posts/YYYY-MM-DD-<slug>/images/    # figures and charts
data/posts.json                    # per-post metadata
scripts/build.py                   # rebuilds posts/ and data/ from the Substack API
```
