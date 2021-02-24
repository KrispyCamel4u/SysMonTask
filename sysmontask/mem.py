#!/usr/bin/env python3
# import gi
# gi.require_version("Gtk", "3.24")

from gi.repository import Gtk as g 
import re,psutil as ps,cairo
from os import popen
from math import pow

def memorytabinit(self):
    print("memory tab initialising")
    self.memInfoLabel=self.builder.get_object('meminfolabel')
    self.memInUseLabelValue=self.builder.get_object('meminuselabelvalue')
    self.memAvailableLabelValue=self.builder.get_object('memavailablelabelvalue')
    self.memBuffersLabelValue=self.builder.get_object('membufferslabelvalue')
    self.memCachedLabelValue=self.builder.get_object('memcachedlabelvalue')
    self.memSwapLabelValue=self.builder.get_object('memswaplabelvalue')

    self.memSpeedLabelValue=self.builder.get_object('memspeedlabelvalue')
    self.memSlotLabelValue=self.builder.get_object('memslotlabelvalue')
    self.memFormLabelValue=self.builder.get_object('memformlabelvalue')
    self.memCourruptedLabelValue=self.builder.get_object('memreservedlabelvalue')

    self.memDrawArea1=self.builder.get_object('memdrawarea1')
    self.memUsedArray1=[0]*100   #mem used array

    self.memDrawArea2=self.builder.get_object('memdrawarea2')

    self.memTotal=round(ps.virtual_memory()[0]/pow(2,30),1)  # in GiBs
    # self.memTotalInMiB=self.memTotal*pow(2,10)
    self.memInfoLabel.set_text(str(self.memTotal)+'GiB')

    try:
        # p=popen('echo '+self.passs+ '| sudo -S dmidecode -t memory|grep -E -i "memory speed"')
        p=popen('dmidecode -t memory|grep -E -i "memory speed"')
        dmidecodetemp=p.readlines()
        p.close()
        memspeed=100000000
        memusedslots=0
        for line in dmidecodetemp:
            line=line.split(':')[1]
            line=re.split('[\s]',line)[1]
            try:
                if(memspeed>int(line)):
                    memspeed=int(line)
                memusedslots+=1
            except:
                pass
            
        self.memSpeedLabelValue.set_text(str(memspeed)+' MHz')
        self.memSlotLabelValue.set_text(str(memusedslots)+' of '+str(len(dmidecodetemp)))
    except:
        print("Failed to get Memory speed")
        pass

    try:
        # p=popen('echo '+self.passs+'| sudo -S dmidecode -t memory|grep -E -m1 -i "form factor"')
        p=popen('dmidecode -t memory|grep -E -m1 -i "form factor"')
        self.memFormLabelValue.set_text(re.sub('\s','',p.read().split(':')[1]))
        p.close()
    except:
        print("Failed to get Memory Form Factor")
        pass

    try:
        p=popen('cat /proc/meminfo | grep -E -i "corrupted"')
        tempcourrupted=p.read().split(':')[1]
        p.close()
        self.memCourruptedLabelValue.set_text(re.sub('\s','',tempcourrupted))
    except:
        print("Failed to get Corrupted Memory")
        pass

def memoryTabUpdate(self):
    memory=ps.virtual_memory()
    self.usedd=round((memory[0]-memory[1])/pow(2,30),1)      
    self.memAvailable=round(memory[1]/pow(2,30),1)
    self.memFree=round(memory[4]/pow(2,30),1)
    
    self.memPercent=memory[2]

    self.memInUseLabelValue.set_text(str(self.usedd)+' GiB')
    self.memAvailableLabelValue.set_text(str(self.memAvailable)+' GiB')
    self.memBuffersLabelValue.set_text(str(round(memory[7]/pow(2,30),1))+' GiB')
    self.memCachedLabelValue.set_text(str(round(memory[8]/pow(2,30),1))+' GiB')

    swapmemory=ps.swap_memory()
    self.memSwapLabelValue.set_text(str(round(swapmemory[1]/pow(2,30),1))+'/'+str(round(swapmemory[0]/pow(2,30),1))+' GiB')

    ## for graph update direction 1 new on right 0 new on left
    if self.update_graph_direction:
        self.memUsedArray1.pop(0)
        self.memUsedArray1.append(self.usedd)
    else:
        self.memUsedArray1.pop()
        self.memUsedArray1.insert(0,self.usedd)


