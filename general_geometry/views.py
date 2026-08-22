
from dataclasses import dataclass
from general_geometry.classes import DistanceClass
@dataclass
class ViewValue:
 name:str;value:float;weight:float=1.0;distance_class:DistanceClass=DistanceClass.METRIC;group:str="default"
