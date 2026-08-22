
from learned_graph16.models import PathTemplate

def default_path_templates():
    return [
      PathTemplate("fast_only",["fast"],1.0,320,0.0),
      PathTemplate("fast_tool",["fast","tool"],1.4,520,0.0),
      PathTemplate("memory_balanced",["memory","balanced"],3.3,760,0.0),
      PathTemplate("balanced_tool",["balanced","tool"],3.6,920,.15),
      PathTemplate("balanced_reasoning",["balanced","reasoning"],11.5,2150,.35),
      PathTemplate("memory_balanced_reasoning",["memory","balanced","reasoning"],11.8,2200,.45),
    ]
