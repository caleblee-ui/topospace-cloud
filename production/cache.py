
from collections import OrderedDict
class LRUCache:
    def __init__(self,maxsize=2048): self.maxsize=maxsize; self.data=OrderedDict()
    def get(self,key):
        if key not in self.data:return None
        self.data.move_to_end(key);return self.data[key]
    def put(self,key,value):
        self.data[key]=value;self.data.move_to_end(key)
        while len(self.data)>self.maxsize:self.data.popitem(last=False)
    def clear(self):self.data.clear()
