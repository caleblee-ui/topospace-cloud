
import hashlib,json,time
class SemanticDecisionCache:
    def __init__(self,ttl=60):self.ttl=ttl;self.rows={}
    def key(self,request):
        raw=json.dumps({"messages":request.messages,"model":request.model,"state":request.state},sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()
    def get(self,key):
        row=self.rows.get(key)
        if not row:return None
        if time.time()-row[0]>self.ttl:self.rows.pop(key,None);return None
        return row[1]
    def put(self,key,value):self.rows[key]=(time.time(),value)
