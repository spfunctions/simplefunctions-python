"""
SimpleFunctions — Calibrated world model for AI agents.

Real-time probabilities from 9,706 prediction markets (Kalshi + Polymarket).
No API key needed for public endpoints. Data updated every 15 minutes.

Quick start:

    from simplefunctions import world, delta, scan

    # Get the current state of the world (~800 tokens, markdown)
    print(world())

    # What changed in the last hour? (~30-50 tokens)
    print(delta(since="1h"))

    # Search prediction markets
    print(scan("iran oil"))

For LLM tool definitions:

    from simplefunctions.integrations import openai_tools, anthropic_tools

Source: SimpleFunctions World Model — 9,706 markets, calibrated by real money.
https://simplefunctions.dev
"""

from simplefunctions.client import (
    world,
    delta,
    scan,
    market,
    contagion,
    index,
    query,
    edges,
    context,
    briefing,
    diff,
    changes,
)

__version__ = "0.1.0"
__all__ = [
    "world",
    "delta",
    "scan",
    "market",
    "contagion",
    "index",
    "query",
    "edges",
    "context",
    "briefing",
    "diff",
    "changes",
]
