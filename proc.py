import os,time,re
import psutil as ps
print(ps.sensors_fans())
#for i in range(0,50):
#    p=os.popen("cat /proc/cpuinfo | grep \"^[c]pu MHz\" | awk '{print $4}'")
#    speed=[int(float(x)) for x in p.read().split()]
#    print(speed)
#    p.close()
#    time.sleep(1)

#for i in range(1,100):
#    p=os.popen('head -1 /proc/stat')
#    s2=p.read().split()[1:]
#    p.close()
#    diff=[]
#    for x1,x2 in zip(s1,s2):
#       diff.append(int(x2)-int(x1))
#    print(diff)
#    print(sum(diff))
#    print((sum(diff)-diff[3])/8.0)
#    s1=s2
#    time.sleep(1)