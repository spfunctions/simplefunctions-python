# simplefunctions-ai

Calibrated world model for AI agents. Real-time probabilities from 30,000+ prediction markets.

```bash
pip install simplefunctions-ai
```

```python
from simplefunctions import world, index, edges

state = world()
print(state['index']['uncertainty'])   # 35 (0-100)
print(state['regimeSummary'])          # "Risk-off: geo elevated..."

idx = index()
print(f"Uncertainty: {idx['uncertainty']}/100")

for e in edges()['edges'][:3]:
    print(f"{e['title']}: {e['executableEdge']}c edge")
```

## CLI
```bash
sf-world           # World state markdown
sf-index           # Uncertainty index
sf-edges           # Actionable edges
sf-market KXFED    # Market detail
sf-delta 1h        # Recent changes
```

## Client class
```python
from simplefunctions import PredictionMarketClient
client = PredictionMarketClient(api_key="sk-...")
state = client.world(format="json")
```

## License
MIT — [SimpleFunctions](https://simplefunctions.dev)
