
from benchmarking.models import BenchmarkTask,RunRecord
from benchmarking.harness import ABBenchmarkHarness
from benchmarking.statistics import bootstrap_ci
from benchmarking.report import marketing_claim
from adapters.deterministic_ab import DeterministicABAdapter

def test_ab_harness():
 tasks=[BenchmarkTask("a","x","coding")]
 s=ABBenchmarkHarness(DeterministicABAdapter(),10).run(tasks)
 assert len(s["records"])==20
 assert s["metrics"]["input_tokens"]["reduction_pct_mean"]>20

def test_bootstrap_ci():
 lo,hi=bootstrap_ci([1,2,3,4,5],samples=200)
 assert lo<=3<=hi

def test_claim_guardrail():
 s={
   "metrics":{"input_tokens":{"reduction_pct_ci95":(30,40)}},
   "success":{"delta_pp_ci95":(-1,1)}
 }
 r=marketing_claim(s,-2,"input_tokens")
 assert r["eligible"] is True
