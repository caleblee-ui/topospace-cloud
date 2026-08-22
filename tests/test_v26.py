
from pathlib import Path
from torusdb.memory_backend import InMemoryTorusBackend
from torusdb.models import MemoryRecord
from torusdb.bridge import TorusTopoMemoryBridge
from mcp.topospace_memory_tools import TOOLS

ROOT=Path(__file__).resolve().parents[1]

def test_torus_memory_bridge():
    b=InMemoryTorusBackend()
    b.upsert(MemoryRecord("auth","oauth auth design",importance=.9,tokens=100,distance=.1))
    b.upsert(MemoryRecord("css","frontend layout",importance=.2,tokens=100,distance=.8))
    r=TorusTopoMemoryBridge(b).recall("oauth auth",limit=10,max_return=5)
    assert r["memories"][0]["id"]=="auth"
    assert all(x["id"]!="css" for x in r["memories"])

def test_ciphertext_is_opaque():
    b=InMemoryTorusBackend();b.upsert(MemoryRecord("x",ciphertext="ENC",metadata={"kind":"secret"},importance=.8,distance=.1))
    x=b.get("x");assert x.ciphertext=="ENC" and x.content is None

def test_mcp_tools_present():
    names={x["name"] for x in TOOLS}
    assert {"topospace_memory_recall","topospace_memory_remember","topospace_memory_forget"}.issubset(names)

def test_skill_package_exists():
    assert (ROOT/"skills/topospace-memory/SKILL.md").exists()
    assert (ROOT/"agents/openai.yaml").exists()

def test_visualization_assets_exist():
    js=(ROOT/"web-sdk/torus-memory-graph.js").read_text()
    html=(ROOT/"studio-web/v2.6-torus-memory.html").read_text()
    assert "customElements.define" in js and "TorusMemoryGraphSDK.mount" in html
