
from telemetry.efficiency import RunMetrics,compare
base=RunMetrics(50000,4000,12,5,18000,.90,True)
optimized=RunMetrics(29000,3500,8,3,12500,.55,True)
print(compare(base,optimized))
