"""
HTTP client for SimpleFunctions API.

All public endpoints require no authentication.
Authenticated endpoints (thesis, trading) require an API key from
https://simplefunctions.dev/dashboard/keys
"""

from __future__ import annotations

from typing import Any, Optional
import requests

BASE_URL = "https://simplefunctions.dev"

_session: Optional[requests.Session] = None


def _get_session() -> requests.Session:
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers["User-Agent"] = "simplefunctions-python/0.1.0"
    return _session


def _get(path: str, params: Optional[dict[str, Any]] = None) -> requests.Response:
    resp = _get_session().get(f"{BASE_URL}{path}", params=params, timeout=30)
    resp.raise_for_status()
    return resp


# ── World State ────────────────────────────────────────────────────────────────


def world(
    focus: str = "",
    format: str = "markdown",
) -> str:
    """Real-time world model for AI agents.

    Returns ~800 tokens covering geopolitics, economy, energy, elections,
    crypto, tech. Anchor contracts (recession, Fed, Iran invasion) always
    present. Calibrated by prediction markets — real money at risk.

    Args:
        focus: Comma-separated topics for deeper coverage. Same token budget,
               concentrated on fewer topics. Options: geopolitics, economy,
               energy, elections, crypto, tech.
        format: "markdown" (default, optimized for LLM context) or "json".

    Returns:
        Markdown string (default) or JSON string.

    Example:
        >>> from simplefunctions import world
        >>> print(world())                           # full panorama
        >>> print(world(focus="energy,geopolitics"))  # deeper on 2 topics
        >>> data = world(format="json")               # structured JSON
    """
    params: dict[str, str] = {}
    if focus:
        params["focus"] = focus
    if format != "markdown":
        params["format"] = format
    return _get("/api/agent/world", params or None).text


def delta(since: str = "1h", format: str = "markdown") -> str:
    """Incremental world state update — only what changed.

    Returns ~30-50 tokens instead of 800. For agents in long-running
    sessions that need periodic world awareness refresh.

    Args:
        since: Relative ("30m", "1h", "6h", "24h") or ISO timestamp.
        format: "markdown" or "json".

    Example:
        >>> from simplefunctions import delta
        >>> print(delta(since="1h"))   # what changed in the last hour
        >>> print(delta(since="6h"))   # last 6 hours
    """
    params: dict[str, str] = {"since": since}
    if format != "markdown":
        params["format"] = format
    return _get("/api/agent/world/delta", params).text


# ── Market Data ────────────────────────────────────────────────────────────────


def scan(q: str, venue: str = "", limit: int = 20) -> dict[str, Any]:
    """Search prediction markets across Kalshi + Polymarket.

    Returns prices, spreads, volumes with relevance ranking.

    Args:
        q: Natural language query, e.g. "iran oil", "fed rate cut", "bitcoin".
        venue: Filter by venue: "kalshi" or "polymarket". Empty for both.
        limit: Max results (default 20, max 50).

    Example:
        >>> from simplefunctions import scan
        >>> results = scan("recession")
        >>> for m in results["markets"][:5]:
        ...     print(f"{m['title']}: {m['price']}c")
    """
    params: dict[str, Any] = {"q": q, "limit": limit}
    if venue:
        params["venue"] = venue
    return _get("/api/public/scan", params).json()


def market(ticker: str, depth: bool = False) -> dict[str, Any]:
    """Complete market profile for a single contract.

    Price, bid/ask, spread, volume, status, description.
    Optional 5-level orderbook depth.

    Args:
        ticker: Kalshi ticker (e.g. "KXIRANINVASION") or Polymarket conditionId.
        depth: Include 5-level orderbook (default False).

    Example:
        >>> from simplefunctions import market
        >>> m = market("KXRECESSION-26DEC31", depth=True)
        >>> print(f"Price: {m['price']}c, Spread: {m['spread']}c")
    """
    params: dict[str, Any] = {}
    if depth:
        params["depth"] = "true"
    return _get(f"/api/public/market/{ticker}", params or None).json()


def contagion(window: str = "6h") -> dict[str, Any]:
    """Cross-market anomaly detection.

    When market A moves, which causally connected markets SHOULD move
    but haven't? The gap is a potential edge.

    Args:
        window: Lookback window: "1h", "6h", "24h", "3d".

    Example:
        >>> from simplefunctions import contagion
        >>> data = contagion(window="24h")
        >>> for signal in data["signals"][:3]:
        ...     print(f"Trigger: {signal['trigger']['ticker']} → {len(signal['lagging'])} lagging")
    """
    return _get("/api/public/contagion", {"window": window}).json()


def index(history: bool = False) -> dict[str, Any]:
    """SF Prediction Market Index.

    Uncertainty (0-100), Geopolitical Risk (0-100), Momentum (-1 to +1),
    Activity (0-100). Computed from 548 orderbook-tracked tickers.

    Args:
        history: Include 24h hourly trajectory (default False).

    Example:
        >>> from simplefunctions import index
        >>> idx = index()
        >>> print(f"Geo Risk: {idx['geopolitical']}/100")
    """
    params: dict[str, Any] = {}
    if history:
        params["history"] = "true"
    return _get("/api/public/index", params or None).json()


def query(q: str, mode: str = "full", depth: bool = False) -> dict[str, Any]:
    """Ask any question about future events or probabilities.

    Returns live contract prices from Kalshi + Polymarket, X/Twitter
    sentiment, traditional market prices, and an LLM-synthesized answer.

    Args:
        q: Natural language query.
        mode: "full" (LLM synthesis, default) or "raw" (data only, fastest).
        depth: Include orderbook depth for top markets.

    Example:
        >>> from simplefunctions import query
        >>> result = query("fed rate cut probability 2026")
        >>> print(result["answer"])
    """
    params: dict[str, Any] = {"q": q, "mode": mode}
    if depth:
        params["depth"] = "true"
    return _get("/api/public/query", params).json()


def edges() -> dict[str, Any]:
    """Aggregated edges across all public theses.

    Sorted by |adjustedEdge|. Each edge = model price vs market price.

    Example:
        >>> from simplefunctions import edges
        >>> for e in edges()["edges"][:5]:
        ...     print(f"{e['title']}: {e['edge']}c edge")
    """
    return _get("/api/edges").json()


def context(compact: bool = False, q: str = "") -> dict[str, Any]:
    """Global market intelligence snapshot.

    Top edges, price movers, highlights, traditional markets.

    Args:
        compact: Edges + highlights + traditional only.
        q: Filter by keyword.
    """
    params: dict[str, Any] = {}
    if compact:
        params["compact"] = "true"
    if q:
        params["q"] = q
    return _get("/api/public/context", params or None).json()


def briefing(topic: str, window: str = "24h") -> dict[str, Any]:
    """Daily topic briefing: what changed, key movers, X sentiment, outlook.

    Args:
        topic: One of: iran, oil, fed, economy, elections, crypto, china,
               ukraine, tech, climate.
        window: Time window (default "24h").
    """
    return _get("/api/public/briefing", {"topic": topic, "window": window}).json()


def diff(
    tickers: str = "",
    topic: str = "",
    window: str = "24h",
) -> dict[str, Any]:
    """Market derivatives: price/volume/spread deltas over time.

    Detects divergence signals (volume spike + flat price, liquidity exit).

    Args:
        tickers: Comma-separated tickers.
        topic: Or use topic to auto-resolve tickers.
        window: Time window (default "24h").
    """
    params: dict[str, Any] = {"window": window}
    if tickers:
        params["tickers"] = tickers
    if topic:
        params["topic"] = topic
    return _get("/api/public/diff", params).json()


def changes(
    since: str = "",
    q: str = "",
    type: str = "",
) -> dict[str, Any]:
    """Server-side detected price moves, new contracts, settlements.

    Args:
        since: ISO timestamp (default: 1h ago).
        q: Filter by keyword.
        type: "price_move", "new_contract", or "removed_contract".
    """
    params: dict[str, Any] = {}
    if since:
        params["since"] = since
    if q:
        params["q"] = q
    if type:
        params["type"] = type
    return _get("/api/changes", params or None).json()
