
from pathlib import Path
import tempfile
from performance.incremental_neighborhood import IncrementalNeighborhood
from performance.delta import TopologyDelta
from performance.topology_delta_runtime import TopologyDeltaRuntime
from indexing.sharded import ShardedObjectIndex
from performance.vectorized import weighted_lp_batch
from cache.persistent_cache import PersistentCache

def test_incremental_neighborhood():
 n=IncrementalNeighborhood(epsilon=.3)
 assert [x["id"] for x in n.rebuild([{"id":"a","distance":.1,"score":.9,"drift":.1},{"id":"b","distance":.7,"score":.9,"drift":.1}])]==["a"]
 n.apply_delta(updated=[{"id":"b","distance":.2,"score":.9,"drift":.1}])
 assert set(n.members)=={"a","b"}

def test_delta_runtime():
 r=TopologyDeltaRuntime();r.bootstrap([{"id":"a","distance":.1,"score":.9,"drift":.1}],[])
 o=r.apply(TopologyDelta(added_nodes=[{"id":"b","distance":.2,"score":.8,"drift":.1}],added_edges=[("a","b",.1)]))
 assert o["nodes"]==2 and o["edges"]==1

def test_sharded_index():
 s=ShardedObjectIndex(8);s.put("x",1);assert s.get("x")==1 and len(s)==1

def test_weighted_lp_batch():
 o=weighted_lp_batch([0,0],[[3,4],[0,1]],[1,1],2)
 assert round(o[0],5)==5 and round(o[1],5)==1

def test_persistent_cache():
 with tempfile.TemporaryDirectory() as d:
  c=PersistentCache(Path(d)/"c.db");c.put("x",{"a":1});assert c.get("x")["a"]==1
