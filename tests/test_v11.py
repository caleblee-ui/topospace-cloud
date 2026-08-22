
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_release_files_exist():
    for p in ["pyproject.toml","LICENSE","CONTRIBUTING.md","SECURITY.md","web-sdk/topospace-graph-v1.1.js","npm/package.json"]:
        assert (ROOT/p).exists()

def test_web_sdk_features_present():
    text=(ROOT/"web-sdk/topospace-graph-v1.1.js").read_text()
    for token in ["layoutForce","clusterByType","animateFiltration","edgeTypes","ring"]:
        assert token in text
