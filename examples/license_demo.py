
import time
from customer.license import License,LicenseManager
m=LicenseManager("dev-secret")
token=m.issue(License("acme","enterprise",time.time()+3600,10,20,["torusdb","multiagent"]))
print(m.verify(token))
