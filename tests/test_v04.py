from runtime.workspace import WorkspaceRegistry
from runtime.events import EventBus
from runtime.telemetry import Telemetry
from index.embeddings import HashEmbeddingProvider
from index.ann import ANNIndex
def test_workspace_isolation():
 r=WorkspaceRegistry();assert r.create('t1','w') is not r.create('t2','w')
def test_embedding_ann():
 e=HashEmbeddingProvider(64);i=ANNIndex(64);i.build([('auth',e.embed('oauth authentication token')),('css',e.embed('layout typography'))]);assert i.query(e.embed('oauth authentication token'),1)[0][0]=='auth'
def test_event_telemetry():
 assert EventBus().publish('state.changed','w',{}).event=='state.changed';t=Telemetry();t.count('requests');assert t.snapshot()['counters']['requests']==1
