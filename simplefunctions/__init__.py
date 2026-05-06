"""
SimpleFunctions Python client.

Preview client for the SimpleFunctions HTTP/Data API. Public read endpoints
require no venue trading credentials. Install from PyPI as simplefunctions-ai
and import as simplefunctions.

CLI remains the primary local surface:

    npm i -g @spfunctions/cli
    sf describe --all --json

https://simplefunctions.dev
"""

from simplefunctions.client import PredictionMarketClient

_default = PredictionMarketClient()

def world(format="json"):
    return _default.world(format=format)

def index(history=False):
    return _default.index(history=history)

def edges():
    return _default.edges()

def market(ticker, depth=False):
    return _default.market(ticker, depth=depth)

def delta(since=None):
    return _default.delta(since=since)

__version__ = "0.2.1"

__all__ = ["PredictionMarketClient", "world", "index", "edges", "market", "delta"]
