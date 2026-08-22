
from pathlib import Path
import sys,subprocess,time,json,statistics,urllib.request,os
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime_sdk.client.python import TopoSpaceClient

root=Path(__file__).resolve().parents[1]
proc=subprocess.Popen([sys.executable,"-m","runtime_server.app"],cwd=root,
                      stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,
                      env={**os.environ,"PORT":"8791"})
try:
    ready=False
    for _ in range(60):
        try:
            with urllib.request.urlopen("http://127.0.0.1:8791/healthz",timeout=.2) as r:
                if r.status==200:
                    ready=True
                    break
        except Exception:
            time.sleep(.1)
    if not ready:
        err=proc.stderr.read().decode(errors="ignore") if proc.stderr else ""
        raise RuntimeError("runtime_server_not_ready: "+err[-2000:])

    c=TopoSpaceClient("http://127.0.0.1:8791",tenant_id="bench",agent_id="agent")
    lat=[]
    for i in range(500):
        t=f"t{i}";s=time.perf_counter()
        c.task_start(t)
        c.before_model(t,prompt="x")
        c.after_model(t,answer="y")
        c.before_tool(t,tool_id="tool")
        c.after_tool(t,tool_id="tool",success=True,reward=.9)
        c.task_complete(t,success=True)
        lat.append((time.perf_counter()-s)*1000)
    snap=c.http.snapshot()
    out={
      "runs":500,
      "mean_remote_lifecycle_ms":statistics.mean(lat),
      "p95_remote_lifecycle_ms":sorted(lat)[int(.95*len(lat))-1],
      "tasks_recorded":len(snap["tasks"]),
      "note":"Localhost HTTP runtime benchmark; excludes real network, LLM, tool and external storage latency."
    }
    print(json.dumps(out,indent=2))
    assert out["tasks_recorded"]==500 and out["p95_remote_lifecycle_ms"]<50
    Path("results/beta1_runtime_server_benchmark.json").write_text(json.dumps(out,indent=2))
finally:
    proc.terminate()
    try:proc.wait(timeout=3)
    except Exception:proc.kill()
