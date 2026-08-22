
from pathlib import Path
import tempfile
from runtime.graph_store import GraphStore
from runtime.sse import SSEStream
from runtime.live_trace import LiveTraceBuffer

def test_graph_store():
    with tempfile.TemporaryDirectory() as d:
        g=GraphStore(Path(d)/"g.db")
        g.save("w1",1,{"nodes":[{"id":"a"}],"edges":[]})
        assert g.latest("w1")["seq"]==1
        assert len(g.history("w1"))==1

def test_sse_stream():
    b=LiveTraceBuffer(); f=b.push("graph","w1",[{"id":"a"}],[],{})
    s=SSEStream(b)
    assert s.poll(0)[0]["seq"]==1
    assert "event: topology" in s.encode(f)
