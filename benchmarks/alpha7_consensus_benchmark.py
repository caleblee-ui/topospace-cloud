
from pathlib import Path
import sys,random,json,statistics
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from consensus_topology.proposal import TopologyProposal
from consensus_topology.runtime import TopologicalMultiAgentConsensusRuntime
rng=random.Random(1729);single=[];cons=[]
for run in range(500):
 truth="best";props=[]
 for a in range(5):
  # independent noisy agents: best usually good, distractor sometimes looks better locally
  bc=max(0,min(1,rng.gauss(.82,.14)));dc=max(0,min(1,rng.gauss(.58,.22)))
  bu=max(0,min(1,rng.gauss(.84,.12)));du=max(0,min(1,rng.gauss(.55,.2)))
  bd=max(.01,min(1,rng.gauss(.15,.08)));dd=max(.01,min(1,rng.gauss(.42,.2)))
  be=max(0,min(1,rng.gauss(.86,.1)));de=max(0,min(1,rng.gauss(.5,.2)))
  props += [TopologyProposal(f"a{a}","t","best","tool",bc,bu,bd,be),
            TopologyProposal(f"a{a}","t","distractor","tool",dc,du,dd,de)]
 # baseline: first agent's own best score using same non-diversity components
 def local_score(p):return .30*p.confidence+.25*p.utility+.20*(1-p.distance)+.13*p.evidence
 first=[x for x in props if x.agent_id=="a0"];single.append(1 if max(first,key=local_score).candidate_id==truth else 0)
 o=TopologicalMultiAgentConsensusRuntime().resolve("t",props)
 cons.append(1 if o["decision"]["winner"]==truth else 0)
out={"runs":500,"single_agent_accuracy":statistics.mean(single),"consensus_accuracy":statistics.mean(cons),"gain_pp":100*(statistics.mean(cons)-statistics.mean(single)),"note":"Synthetic independent-noise benchmark; not external multi-agent accuracy evidence."}
print(json.dumps(out,indent=2));assert out["consensus_accuracy"]>.95 and out["consensus_accuracy"]>out["single_agent_accuracy"]
Path("results/alpha7_consensus_benchmark.json").write_text(json.dumps(out,indent=2))
