
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from production.adaptive_engine import AdaptiveTopoSpaceEngine

context=[
 {"id":"task","tokens":900,"utility":1,"distance":0,"score":1,"drift":0},
 {"id":"auth","tokens":5200,"utility":.95,"distance":.10,"score":.94,"drift":.05},
 {"id":"oauth","tokens":4800,"utility":.90,"distance":.14,"score":.88,"drift":.08},
 {"id":"tests","tokens":4100,"utility":.82,"distance":.22,"score":.80,"drift":.05},
 {"id":"logs","tokens":7600,"utility":.45,"distance":.31,"score":.48,"drift":.20},
 {"id":"docs","tokens":5500,"utility":.34,"distance":.42,"score":.38,"drift":.18},
 {"id":"frontend","tokens":6800,"utility":.10,"distance":.72,"score":.14,"drift":.55},
 {"id":"old","tokens":9300,"utility":.08,"distance":.81,"score":.12,"drift":.70},
]
agents=[
 {"id":"coding","capabilities":["code"],"score":.94,"reliability":.96,"cost":.2,"risk":.08},
 {"id":"security","capabilities":["security"],"score":.90,"reliability":.97,"cost":.2,"risk":.05},
 {"id":"test","capabilities":["test"],"score":.86,"reliability":.96,"cost":.18,"risk":.05},
]
e=AdaptiveTopoSpaceEngine()
raw=sum(x["tokens"] for x in context)
scenarios={}
for name,kwargs in {
 "easy_cost_sensitive":{"uncertainty":.15,"drift":.05,"previous_success":True,"cost_pressure":.9,"complexity":.2},
 "normal":{"uncertainty":.35,"drift":.15,"previous_success":True,"cost_pressure":.5,"complexity":.5},
 "hard_uncertain":{"uncertainty":.82,"drift":.45,"previous_success":False,"cost_pressure":.2,"complexity":.85},
}.items():
 r=e.optimize_adaptive("Fix OAuth vulnerability",context,agents,["code","security","test"],**kwargs)
 scenarios[name]={
   "raw_tokens":raw,"context_tokens":r["context_tokens"],
   "reduction_pct":100*(1-r["context_tokens"]/raw),
   "kept":[x["id"] for x in r["context"]],
   "adaptive":r["adaptive"],"quality_expansion":r["expanded_for_quality"]
 }
print(json.dumps(scenarios,indent=2))
assert scenarios["easy_cost_sensitive"]["context_tokens"] <= scenarios["hard_uncertain"]["context_tokens"]
assert scenarios["hard_uncertain"]["quality_expansion"] is True
Path("results/v20_adaptive_benchmark.json").write_text(json.dumps(scenarios,indent=2))
