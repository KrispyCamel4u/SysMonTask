import re,psutil as ps
from os import popen
from math import pow

def memorytabinit(self):
    """
    Initialisation of Memory components.
    """

    print("Memory Tab Initialising")

    # Fetching and assigning widgets from the glade file
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

    # Memory Utilisation Drawing area
    self.memDrawArea1=self.builder.get_object('memdrawarea1')
    self.memUsedArray1=[0]*100   #mem used array

    # Memory Composition Drawing area
    self.memDrawArea2=self.builder.get_object('memdrawarea2')

    # Total Memory
    self.memTotal=round(ps.virtual_memory()[0]/pow(2,30),1)  # in GiBs
    self.memInfoLabel.set_text(f'{self.memTotal}GiB')

    self.usedd,self.memAvailable,self.memFree=0,0,0

    # Memory Frequency and slot used, using shell
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

        if memspeed==100000000: self.memSpeedLabelValue.set_text(f'NA')
        else: self.memSpeedLabelValue.set_text(f'{memspeed} MHz')
        self.memSlotLabelValue.set_text(f'{memusedslots} of {len(dmidecodetemp)}')
    except:
        print("Failed to get Memory speed")

    # Memory Form factor using shell
    try:
        # p=popen('echo '+self.passs+'| sudo -S dmidecode -t memory|grep -E -m1 -i "form factor"')
        p=popen('dmidecode -t memory|grep -E -m1 -i "form factor"')
        self.memFormLabelValue.set_text(re.sub('\s','',p.read().split(':')[1]))
        p.close()
    except:
        print("Failed to get Memory Form Factor")

    # Getting the Corrupted memory info
    try:
        p=popen('cat /proc/meminfo | grep -E -i "corrupted"')
        tempcourrupted=p.read().split(':')[1]
        p.close()
        self.memCourruptedLabelValue.set_text(re.sub('\s','',tempcourrupted))
    except:
        print("Failed to get Corrupted Memory")

def memoryTabUpdate(self):
    """
    Function to periodically update Memory statistics.
    """
    # Conversion divider
    gibdivider=pow(2,30)

    # Getting memory information
    memory=ps.virtual_memory()
    self.usedd=round((memory[0]-memory[1])/gibdivider,1)
    self.memAvailable=round(memory[1]/gibdivider,1)
    self.memFree=round(memory[4]/gibdivider,1)
    self.memPercent=memory[2]

    # Setting the information labels
    self.memInUseLabelValue.set_text(f'{self.usedd} GiB')
    self.memAvailableLabelValue.set_text(f'{self.memAvailable} GiB')
    self.memBuffersLabelValue.set_text(f'{round(memory[7]/gibdivider,1)} GiB')
    self.memCachedLabelValue.set_text(f'{round(memory[8]/gibdivider,1)} GiB')

    # Getting and Setting the swap info
    swapmemory=ps.swap_memory()
    self.memSwapLabelValue.set_text(f'{round(swapmemory[1]/gibdivider,1)}/{round(swapmemory[0]/gibdivider,1)} GiB')

    ## for graph update direction 1 new on right 0 new on left
    if self.update_graph_direction:
        self.memUsedArray1.pop(0)
        self.memUsedArray1.append(self.usedd)
    else:
        self.memUsedArray1.pop()
        self.memUsedArray1.insert(0,self.usedd)


