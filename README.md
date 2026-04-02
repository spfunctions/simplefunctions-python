# SimpleFunctions

Calibrated world model for AI agents. Real-time probabilities from 9,706 prediction markets.

Your agent doesn't know what's happening in the world. Web search returns narratives ("tensions remain elevated"). SimpleFunctions returns calibrated numbers backed by real money: `Iran invasion: 53% (+5c, $225K volume)`.

## Install

```bash
pip install simplefunctions
```

## Quick Start

```python
from simplefunctions import world, delta, scan

# What's happening in the world right now? (~800 tokens, markdown)
print(world())

# What changed in the last hour? (~30-50 tokens)
print(delta(since="1h"))

# Search prediction markets
results = scan("fed rate cut")
for m in results["markets"][:5]:
    print(f"{m['title']}: {m['price']}c")
```

No API key needed. Free. Data from Kalshi (CFTC-regulated) and Polymarket, updated every 15 minutes.

## Give Your Agent World Awareness

### System prompt injection (simplest)

```python
from simplefunctions import world
import anthropic

client = anthropic.Anthropic()
state = world()

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system=f"You are a research analyst.\n\n{state}",
    messages=[{"role": "user", "content": "What's the recession probability?"}],
)
# Agent cites "33%" instead of hallucinating
```

### Tool definitions (one line per framework)

```python
from simplefunctions.integrations import openai_tools, anthropic_tools, mistral_tools

# OpenAI Agents SDK / Responses API
tools = openai_tools()

# Anthropic Claude
tools = anthropic_tools()

# Mistral
tools = mistral_tools()
```

### Tool execution (framework-agnostic)

```python
from simplefunctions.integrations import execute_tool

# Works with any framework's tool call output
result = execute_tool("get_world_state", {"focus": "energy,geopolitics"})
result = execute_tool("search_prediction_markets", {"query": "iran oil"})
result = execute_tool("get_world_delta", {"since": "1h"})
```

## API Reference

### World State

| Function | Description | Tokens |
|----------|-------------|--------|
| `world()` | Full world state — 6 topics, anchor contracts, edges, divergences | ~800 |
| `world(focus="energy,geo")` | Same budget, concentrated on fewer topics | ~800 |
| `delta(since="1h")` | Only what changed since timestamp | ~30-50 |

### Market Data

| Function | Description |
|----------|-------------|
| `scan("iran oil")` | Cross-venue market search with relevance ranking |
| `market("KXRECESSION-26DEC31")` | Single market profile with optional orderbook |
| `contagion(window="6h")` | Cross-market anomaly detection |
| `index()` | SF Prediction Market Index (uncertainty, geo risk, momentum) |
| `query("fed rate cut?")` | LLM-synthesized answer with live data |
| `edges()` | Top mispriced markets across all theses |
| `briefing(topic="iran")` | Daily topic briefing with X sentiment |
| `diff(topic="energy")` | Market derivatives over time |
| `changes(type="price_move")` | Recent price moves, new contracts, settlements |
| `context()` | Global market intelligence snapshot |

### Focused World State

```python
# Default: 4 contracts per topic across 6 topics
world()

# Focused: 10 contracts per topic across 2 topics
world(focus="geopolitics,energy")

# All topics: geopolitics, economy, energy, elections, crypto, tech
```

### Incremental Updates

```python
# Full state at session start
state = world()

# Periodic refresh — only changes (~30-50 tokens)
changes = delta(since="1h")
changes = delta(since="6h")
changes = delta(since="2026-04-02T08:00:00Z")
```

## MCP Server

For Claude Code, Cursor, or any MCP-compatible agent:

```bash
claude mcp add simplefunctions --url https://simplefunctions.dev/api/mcp/mcp
```

40 tools, no API key needed for public endpoints.

## Why Prediction Markets?

A prediction market price of 53c on "Iran invasion" encodes the aggregate judgment of everyone with money at risk on that question. Get it wrong, lose money. This punishment mechanism produces calibrated probabilities more reliable than any analyst report, news summary, or LLM reasoning.

| | Web Search | News API | SimpleFunctions |
|---|---|---|---|
| **Output** | Narrative text | Headlines | Calibrated probabilities |
| **Token cost** | 2,000-5,000 | 500-1,000 | ~800 for everything |
| **Latency** | 2-5 seconds | 500ms | ~200ms (cached) |
| **Calibration** | None | None | Real money at risk |

## Links

- [World State API](https://simplefunctions.dev/api/agent/world) — try it now
- [Interactive demo](https://simplefunctions.dev/world)
- [Documentation](https://simplefunctions.dev/docs/guide)
- [All endpoints](https://simplefunctions.dev/api/tools)
- [MCP Server](https://simplefunctions.dev/api/mcp/mcp)
- [npm CLI](https://www.npmjs.com/package/@spfunctions/cli) — `npm install -g @spfunctions/cli`

## License

MIT
