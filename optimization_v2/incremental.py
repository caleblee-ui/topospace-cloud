
class IncrementalNeighborhood:
    """Updates only affected neighborhoods when candidate distances change."""
    def __init__(self,epsilon=.3):
        self.epsilon=float(epsilon);self.points={};self.neighbors={}

    def upsert(self,point_id,distance):
        self.points[point_id]=float(distance)
        affected=[]
        for pid,d in self.points.items():
            near=abs(d-float(distance))<=self.epsilon
            self.neighbors.setdefault(pid,set())
            self.neighbors.setdefault(point_id,set())
            if near:
                self.neighbors[pid].add(point_id);self.neighbors[point_id].add(pid)
            else:
                self.neighbors[pid].discard(point_id);self.neighbors[point_id].discard(pid)
            if near:affected.append(pid)
        return sorted(set(affected))

    def get(self,point_id):
        return sorted(self.neighbors.get(point_id,set())-{point_id})
