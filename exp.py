import os,time,re
import psutil as ps
import math
temp=ps.disk_io_counters(perdisk=True)['nvme0n1']
time.sleep(1)
for i in range(0,1000):
    temp2=ps.disk_io_counters(perdisk=True)['nvme0n1']
    diff=[x2-x1 for x1,x2 in zip(temp,temp2)]
    print(diff)
    print('her')
    temp=temp2
    time.sleep(1)







