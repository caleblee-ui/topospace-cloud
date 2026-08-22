
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from benchmarking.models import BenchmarkTask
from benchmarking.harness import ABBenchmarkHarness
from benchmarking.report import marketing_claim
from adapters.deterministic_ab import DeterministicABAdapter

def main():
 tasks=[
  BenchmarkTask("coding-1","Fix authentication bug","coding"),
  BenchmarkTask("tool-1","Complete tool workflow","tool-use"),
  BenchmarkTask("long-1","Solve long-running agent task","long-horizon"),
  BenchmarkTask("multi-1","Coordinate multiple agents","multi-agent"),
 ]
 summary=ABBenchmarkHarness(DeterministicABAdapter(),repeats=20).run(tasks)
 summary["claim_input"]=marketing_claim(summary,-2.0,"input_tokens")
 summary["claim_cost"]=marketing_claim(summary,-2.0,"cost_usd")
 summary["provenance"]="synthetic deterministic A/B harness; replace adapter with real model/task runners before marketing use"
 print(json.dumps(summary["metrics"],indent=2))
 print(json.dumps(summary["success"],indent=2))
 print(json.dumps(summary["claim_input"],indent=2))
 assert summary["metrics"]["input_tokens"]["reduction_pct_mean"]>30
 assert summary["success"]["delta_pp_mean"]>=-5
 Path("results/v17_ab_summary.json").write_text(json.dumps(summary,indent=2))
if __name__=="__main__":main()
