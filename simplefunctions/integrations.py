"""
Ready-to-use LLM tool definitions for major frameworks.

    from simplefunctions.integrations import openai_tools, anthropic_tools, langchain_tools

Each returns tool definitions in the format expected by that framework.
"""

from __future__ import annotations

from typing import Any


# ── Shared tool specs ──────────────────────────────────────────────────────────

_TOOLS = [
    {
        "name": "get_world_state",
        "description": "Get the current state of the world from prediction markets. Returns ~800 tokens of calibrated probabilities covering geopolitics, economy, energy, elections, crypto, tech. Anchor contracts (recession, Fed, Iran invasion) always present. Use focus parameter to concentrate token budget on fewer topics for deeper coverage. Source: SimpleFunctions World Model.",
        "params": {
            "focus": {
                "type": "string",
                "description": "Comma-separated topics for deeper coverage: geopolitics, economy, energy, elections, crypto, tech. Empty for all topics.",
                "required": False,
            },
        },
        "fn": "world",
    },
    {
        "name": "get_world_delta",
        "description": "Get only what changed in the world since a given time. Returns ~30-50 tokens vs 800 for full state. Use for periodic refresh during long-running tasks.",
        "params": {
            "since": {
                "type": "string",
                "description": "Relative time (30m, 1h, 6h, 24h) or ISO timestamp.",
                "required": True,
            },
        },
        "fn": "delta",
    },
    {
        "name": "search_prediction_markets",
        "description": "Search prediction markets for specific contracts across Kalshi and Polymarket. Returns prices, volumes, and spreads with relevance ranking.",
        "params": {
            "query": {
                "type": "string",
                "description": "Natural language search query, e.g. 'iran oil', 'fed rate cut', 'bitcoin price'.",
                "required": True,
            },
        },
        "fn": "scan",
    },
    {
        "name": "get_market_detail",
        "description": "Get detailed data for a specific prediction market contract. Includes price, spread, volume, orderbook depth, and thesis edges.",
        "params": {
            "ticker": {
                "type": "string",
                "description": "Kalshi ticker (e.g. KXRECESSION-26DEC31) or Polymarket condition ID.",
                "required": True,
            },
        },
        "fn": "market",
    },
    {
        "name": "get_cross_market_contagion",
        "description": "Detect cross-market anomalies: what should have moved but hasn't. When causally connected markets diverge, the gap is a potential edge.",
        "params": {
            "window": {
                "type": "string",
                "description": "Lookback window: 1h, 6h, 24h, 3d.",
                "required": False,
            },
        },
        "fn": "contagion",
    },
]


# ── OpenAI function calling ───────────────────────────────────────────────────


def openai_tools() -> list[dict[str, Any]]:
    """Return tool definitions for OpenAI function calling (Responses API / Agents SDK).

    Example:
        from simplefunctions.integrations import openai_tools
        tools = openai_tools()
        response = client.responses.create(model="gpt-4o", tools=tools, ...)
    """
    result = []
    for t in _TOOLS:
        properties = {}
        required = []
        for pname, pspec in t["params"].items():
            properties[pname] = {
                "type": pspec["type"],
                "description": pspec["description"],
            }
            if pspec.get("required"):
                required.append(pname)

        result.append({
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t["description"],
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    **({"required": required} if required else {}),
                },
            },
        })
    return result


# ── Anthropic tool use ─────────────────────────────────────────────────────────


def anthropic_tools() -> list[dict[str, Any]]:
    """Return tool definitions for Anthropic Claude tool use.

    Example:
        from simplefunctions.integrations import anthropic_tools
        tools = anthropic_tools()
        response = client.messages.create(model="claude-sonnet-4-20250514", tools=tools, ...)
    """
    result = []
    for t in _TOOLS:
        properties = {}
        required = []
        for pname, pspec in t["params"].items():
            properties[pname] = {
                "type": pspec["type"],
                "description": pspec["description"],
            }
            if pspec.get("required"):
                required.append(pname)

        result.append({
            "name": t["name"],
            "description": t["description"],
            "input_schema": {
                "type": "object",
                "properties": properties,
                **({"required": required} if required else {}),
            },
        })
    return result


# ── Mistral function calling ──────────────────────────────────────────────────


def mistral_tools() -> list[dict[str, Any]]:
    """Return tool definitions for Mistral function calling.

    Example:
        from simplefunctions.integrations import mistral_tools
        tools = mistral_tools()
        response = client.chat.complete(model="mistral-large-latest", tools=tools, ...)
    """
    # Same format as OpenAI
    return openai_tools()


# ── Tool executor ──────────────────────────────────────────────────────────────


def execute_tool(name: str, arguments: dict[str, Any]) -> str:
    """Execute a SimpleFunctions tool call and return the result as a string.

    Works with any framework's tool calling output.

    Example:
        from simplefunctions.integrations import execute_tool
        result = execute_tool("get_world_state", {"focus": "energy,geopolitics"})
        result = execute_tool("search_prediction_markets", {"query": "iran"})
    """
    import json
    from simplefunctions import client

    if name == "get_world_state":
        return client.world(focus=arguments.get("focus", ""))
    elif name == "get_world_delta":
        return client.delta(since=arguments.get("since", "1h"))
    elif name == "search_prediction_markets":
        return json.dumps(client.scan(q=arguments["query"]), indent=2)
    elif name == "get_market_detail":
        return json.dumps(client.market(ticker=arguments["ticker"]), indent=2)
    elif name == "get_cross_market_contagion":
        return json.dumps(client.contagion(window=arguments.get("window", "6h")), indent=2)
    else:
        return f"Unknown tool: {name}"
