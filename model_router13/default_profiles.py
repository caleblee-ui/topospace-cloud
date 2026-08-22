
from model_router13.models import ModelProfile

def default_profiles():
    return [
      ModelProfile("fast",quality=.72,latency_ms=350,input_cost_per_1k=.08,output_cost_per_1k=.20,tool_affinity=.55,reasoning_affinity=.25,max_context=64000),
      ModelProfile("balanced",quality=.86,latency_ms=700,input_cost_per_1k=.30,output_cost_per_1k=.90,tool_affinity=.75,reasoning_affinity=.60,max_context=128000),
      ModelProfile("reasoning",quality=.94,latency_ms=1500,input_cost_per_1k=1.20,output_cost_per_1k=4.00,tool_affinity=.82,reasoning_affinity=.95,max_context=200000)
    ]
