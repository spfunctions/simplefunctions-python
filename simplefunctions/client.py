import requests

DEFAULT_BASE = "https://simplefunctions.dev"
DEFAULT_TIMEOUT = 15

class PredictionMarketClient:
    def __init__(self, api_key=None, base_url=None, timeout=None):
        self.base = (base_url or DEFAULT_BASE).rstrip("/")
        self.api_key = api_key
        self.timeout = timeout or DEFAULT_TIMEOUT

    def _get(self, path, params=None):
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        url = f"{self.base}{path}"
        r = requests.get(url, params=params, headers=headers, timeout=self.timeout)
        r.raise_for_status()
        ct = r.headers.get("content-type", "")
        return r.json() if "json" in ct else r.text

    def world(self, format="json"):
        return self._get("/api/agent/world", {"format": format})

    def index(self, history=False):
        params = {}
        if history:
            params["history"] = "true"
        return self._get("/api/public/index", params)

    def edges(self):
        return self._get("/api/edges")

    def market(self, ticker, depth=False):
        params = {}
        if depth:
            params["depth"] = "true"
        return self._get(f"/api/public/market/{ticker}", params)

    def delta(self, since=None):
        params = {"format": "json"}
        if since:
            params["since"] = since
        return self._get("/api/agent/world/delta", params)
