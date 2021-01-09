import os,time,re
import psutil as ps
import math
"""
d1=ps.net_io_counters(pernic=True)['wlo1'][1]
for i in range(1,100):
    d2=ps.net_io_counters(pernic=True)['wlo1'][1]
    print(d2-d1) 
    time.sleep(1) 
    d1=d2  
"""
d=ps.net_if_addrs()
print(d)