
from cloud21.bootstrap import build_service
from cloud21.asgi import ProductionASGI
service=build_service()
app=ProductionASGI(service)
