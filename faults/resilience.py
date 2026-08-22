
class ResilienceHarness:
    def run(self,fn,iterations=100):
        ok=errors=0
        for i in range(iterations):
            try: fn(i);ok+=1
            except Exception: errors+=1
        return {"iterations":iterations,"ok":ok,"errors":errors,"error_rate":errors/max(1,iterations)}
