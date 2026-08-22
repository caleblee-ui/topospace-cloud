
from enum import Enum
class DistanceClass(str,Enum):
 METRIC="metric";PSEUDOMETRIC="pseudometric";QUASIMETRIC="quasi_metric";RAW="raw"
GUARANTEES={
 "metric":{"ranking","neighborhood","stability","constraint","dedup","chain_distance","planning","filtration"},
 "pseudometric":{"ranking","neighborhood","stability","constraint","dedup","chain_distance","planning","filtration"},
 "quasi_metric":{"ranking","neighborhood","stability","constraint","chain_distance"},
 "raw":{"ranking","neighborhood","stability","constraint"}}
def combined_class(classes):
 xs={DistanceClass(x) for x in classes}
 if DistanceClass.RAW in xs:return DistanceClass.RAW
 if DistanceClass.QUASIMETRIC in xs:return DistanceClass.QUASIMETRIC
 if DistanceClass.PSEUDOMETRIC in xs:return DistanceClass.PSEUDOMETRIC
 return DistanceClass.METRIC
