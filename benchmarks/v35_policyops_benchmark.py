
from pathlib import Path
import sys,json,random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from policyops.champion import ChampionChallenger,PolicyCandidate
from policyops.rollback import AutomaticRollback
from policyops.drift import ConceptDriftDetector

champ=PolicyCandidate("balanced",12,.42,.95,.08,500)
chall=PolicyCandidate("efficient",7,.49,.945,.09,180)
promotion=ChampionChallenger().evaluate(champ,chall)

rollback=AutomaticRollback().check(
 {"success_rate":.95,"error_rate":.02,"p95_ms":100},
 {"success_rate":.89,"error_rate":.11,"p95_ms":145}
)

rng=random.Random(7)
ref=[min(1,max(0,rng.gauss(.25,.08))) for _ in range(500)]
cur=[min(1,max(0,rng.gauss(.62,.10))) for _ in range(500)]
drift=ConceptDriftDetector().detect(ref,cur)

out={"promotion":promotion,"rollback":rollback,"concept_drift":drift}
print(json.dumps(out,indent=2))
assert promotion["promote"] is True
assert rollback["rollback"] is True
assert drift["drift"] is True
Path("results/v35_policyops_benchmark.json").write_text(json.dumps(out,indent=2))
