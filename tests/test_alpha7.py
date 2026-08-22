
from pathlib import Path
from consensus_topology.proposal import TopologyProposal
from consensus_topology.runtime import TopologicalMultiAgentConsensusRuntime
ROOT=Path(__file__).resolve().parents[1]
def p(a,c,conf=.9,u=.9,d=.1,e=.9):return TopologyProposal(a,"t",c,"tool",conf,u,d,e)
def test_consensus():
 r=TopologicalMultiAgentConsensusRuntime();o=r.resolve("t",[p("a","x"),p("b","x"),p("c","y",.6,.6,.4,.6)])
 assert o["decision"]["winner"]=="x"
def test_exploration_on_single_support():
 r=TopologicalMultiAgentConsensusRuntime();o=r.resolve("t",[p("a","x")]);assert o["decision"]["status"]=="needs_exploration"
def test_diversity_support():
 r=TopologicalMultiAgentConsensusRuntime();o=r.resolve("t",[p("a","x"),p("b","x"),p("c","y")])
 assert o["ranking"][0]["support"]>=2
def test_visual():
 assert "customElements.define" in (ROOT/"web-sdk/consensus-topology.js").read_text()
