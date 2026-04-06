import json
import sys
from simplefunctions.client import PredictionMarketClient

client = PredictionMarketClient()

def cmd_world():
    fmt = "json" if "--json" in sys.argv else "markdown"
    result = client.world(format=fmt)
    print(json.dumps(result, indent=2) if isinstance(result, dict) else result)

def cmd_index():
    result = client.index()
    if "--json" in sys.argv:
        print(json.dumps(result, indent=2))
    else:
        print(f"Uncertainty:  {result['uncertainty']}/100")
        print(f"Geopolitical: {result['geopolitical']}/100")
        m = result['momentum']
        print(f"Momentum:     {'+' if m > 0 else ''}{m}")
        print(f"Activity:     {result['activity']}/100")

def cmd_edges():
    result = client.edges()
    if "--json" in sys.argv:
        print(json.dumps(result, indent=2))
    else:
        for e in result.get("edges", []):
            d = "▲" if e.get("direction") == "yes" else "▼"
            print(f"{d} {e.get('executableEdge', '?')}c  {e.get('title', '?')}")

def cmd_market():
    if len(sys.argv) < 2:
        print("Usage: sf-market <TICKER>"); sys.exit(1)
    ticker = sys.argv[1]
    result = client.market(ticker, depth="--depth" in sys.argv)
    print(json.dumps(result, indent=2))

def cmd_delta():
    since = None
    for a in sys.argv[1:]:
        if not a.startswith("--"):
            since = a; break
    result = client.delta(since=since)
    if isinstance(result, dict) and "markdown" in result:
        print(result["markdown"])
    else:
        print(json.dumps(result, indent=2) if isinstance(result, dict) else result)
