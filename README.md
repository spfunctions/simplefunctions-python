# SimpleFunctions Python Client

Preview Python client for the SimpleFunctions HTTP/Data API.

The PyPI distribution name is `simplefunctions-ai`. The import package remains `simplefunctions`.

```bash
pip install simplefunctions-ai
```

```python
from simplefunctions import world, index, edges, market

state = world()
print(state["index"]["uncertainty"])

idx = index()
print(f"Uncertainty: {idx['uncertainty']}/100")

for edge in edges().get("edges", [])[:3]:
    print(edge.get("title"), edge.get("executableEdge"))

detail = market("KXRECESSION-26DEC31", depth=True)
print(detail)
```

## What this package is

- A lightweight Python client over public SimpleFunctions endpoints.
- A notebook and research-pipeline entry point for prediction-market world state.
- A small set of console scripts for quick reads.

## What this package is not

- It is not the canonical SimpleFunctions SDK yet.
- It is not the execution runtime.
- It is not the primary product surface.

The primary local surface is the `sf` CLI from npm:

```bash
npm i -g @spfunctions/cli
sf describe --all --json
sf world --json
```

Use the HTTP/Data API when you need a network-native surface from Python. Use MCP only when your host specifically requires MCP.

## Client Class

```python
from simplefunctions import PredictionMarketClient

client = PredictionMarketClient(api_key="sf_live_...")
state = client.world(format="json")
```

## Console Scripts

```bash
sf-world
sf-index
sf-edges
sf-market KXFED
sf-delta 1h
```

Public read endpoints require no venue trading credentials. Authenticated execution and portfolio workflows belong in the CLI/API surfaces with explicit permission gates.

## Links

- PyPI: https://pypi.org/project/simplefunctions-ai/
- CLI: https://simplefunctions.dev/cli
- API docs: https://docs.simplefunctions.dev/api-reference/overview
- World endpoint: https://simplefunctions.dev/api/agent/world
- Public package catalog: https://simplefunctions.dev/opensource

## License

MIT - [SimpleFunctions](https://simplefunctions.dev)
