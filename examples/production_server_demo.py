
from production.adaptive_engine import AdaptiveTopoSpaceEngine
e=AdaptiveTopoSpaceEngine()
result=e.optimize_adaptive("debug auth",[
 {"id":"auth","tokens":2000,"utility":.9,"distance":.1,"score":.9,"drift":.05},
 {"id":"old","tokens":5000,"utility":.1,"distance":.8,"score":.1,"drift":.7},
],[],[],uncertainty=.2,complexity=.3,cost_pressure=.8)
print(result)
