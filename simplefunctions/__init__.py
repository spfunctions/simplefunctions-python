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

__all__ = ["PredictionMarketClient", "world", "index", "edges", "market", "delta"]
