
from general_geometry.aggregators import *
from general_geometry.views import ViewValue
from general_geometry.classes import DistanceClass
from general_geometry.engine import GeneralizedGeometryEngine
from general_geometry.profiles import hierarchical_agent_profile
from general_geometry.metric_field import ChainDistance
def test_lp_special_case():assert abs(WeightedLp(2).aggregate([3,4],[1,1])-5)<1e-9
def test_cheb_weighted():assert WeightedChebyshev().aggregate([.9,.5],[.2,1])==.5
def test_nested_constraint_sensitive():
 a=hierarchical_agent_profile();safe=a.aggregate([.1,.2,.1,0,0,.2,.1]);bad=a.aggregate([.1,.2,.1,1,0,.2,.1]);assert bad>safe
def test_concave():assert 0<ConcaveReshape(WeightedLp(1)).aggregate([.5,.5])<1
def test_owa_axioms():assert OrderedWeightedAverage([.6,.3,.1]).validate_axioms()
def test_guarantee_downgrade():
 e=GeneralizedGeometryEngine(WeightedLp(2));r=e.distance([ViewValue("a",.1),ViewValue("b",.2,distance_class=DistanceClass.RAW)])
 assert r["class"]=="raw" and "planning" not in r["guarantees"]
def test_chain():
 vals={("a","b"):1,("b","a"):1,("b","c"):1,("c","b"):1,("a","c"):4,("c","a"):4}
 assert ChainDistance().shortest(["a","b","c"],lambda x,y:vals[(x,y)],"a","c")==2
