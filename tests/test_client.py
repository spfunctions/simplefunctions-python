from simplefunctions import world, index, edges, delta

def test_world():
    state = world()
    assert "index" in state
    assert state["index"]["uncertainty"] >= 0

def test_index():
    idx = index()
    assert 0 <= idx["uncertainty"] <= 100
    assert -1 <= idx["momentum"] <= 1

def test_edges():
    result = edges()
    assert "edges" in result

def test_delta():
    result = delta()
    assert "from" in result or "markdown" in result
