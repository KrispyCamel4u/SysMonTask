from gi.repository import Gtk as g , GLib as go
import psutil as ps,cairo,time
from math import pow
mibdevider=pow(2,20)

def byte_to_human(value,persec=True):
    if value > 1024:   ###KiB
        if value > 1048576:    ##MiB
            if value> 1073741824:
                if value>1073741824*1024:
                    scalefactor=1073741824*1024
                    suffix='TiB'
                else:
                    scalefactor=1073741824
                    suffix='GiB'
            else:
                scalefactor=1048576
                suffix='MiB'
        else:
            scalefactor=1024
            suffix='KiB'
    else:
        if persec:
            return "{:.1f} ".format(0)+'KiB/s'
        return "{:.1f} ".format(0)+'KiB'

    if persec:
        suffix+='/s'
    return "{:.1f} ".format(value/scalefactor)+suffix

def sorting_func(model, row1, row2, user_data):
    sort_column, _ = model.get_sort_column_id()
    val1 = model.get_value(row1, sort_column)
    val2 = model.get_value(row2, sort_column)
    if not type(val1)==int:
        temp1=val1.split()
        val1 = float(temp1[0])
        if 'K' in temp1[1]:
            multiplier=1024
        elif 'M' in temp1[1]:
            multiplier=1048576
        elif 'G' in temp1[1]:
            multiplier=1073741824
        elif 'T' in temp1[1]:
            multiplier=1073741824*1024
        val1*=multiplier

        temp2=val2.split()
        val2 = float(temp2[0])
        if 'K' in temp2[1]:
            multiplier=1024
        elif 'M' in temp2[1]:
            multiplier=1048576
        elif 'G' in temp2[1]:
            multiplier=1073741824
        elif 'T' in temp1[1]:
            multiplier=1073741824*1024
        val2*=multiplier
    if val1<val2:
        return -1
    elif val1==val2:
        return 0
    else:
        return 1

def searcher(self,sprocs,root):
    childlist=sprocs.children()
    if(sprocs.name()!='systemd'): 
        self.processChildList[sprocs.pid]=[]

    if len(childlist)==0:
        return 
    else:
        for procs in childlist:
            if (root!=None) or ('/libexec/' not in "".join(procs.cmdline()) and 'daemon' not in "".join(procs.cmdline()) and procs.username()=='neeraj'):
                # if(sprocs.name()=='systemd'):
                #     if(len(procs.children())!=0):
                #         print(procs.name())
                #         root=self.processTreeStore.append(None,[0,'name',0,0,0,'name','name'])
                if(sprocs.name()!='systemd'):
                    # print(sprocs.name()) 
                    # print(sprocs.pid,' ',procs.pid)
                    self.processChildList[sprocs.pid].append(procs.pid)

                cpu_percent=procs.cpu_percent()
                mem_info=procs.memory_info()
                cpu_percent="{:.1f}".format(cpu_percent)+' %'
                mem_util=(mem_info[0]-mem_info[2])/mibdevider
                mem_util='{:.1f}'.format(mem_util)+' MiB'
                itr=self.processTreeStore.append(root,[procs.pid,procs.name(),cpu_percent,cpu_percent,mem_util
                ,mem_util,'0 KB/s','0 KB/s','0 KB/s','0 KB/s',procs.username()," ".join(procs.cmdline())])
                self.processTreeIterList[procs.pid]=itr
                self.processList[procs.pid]=procs
                self.procDiskprev[procs.pid]=[0,0]
                self.procT1[procs.pid]=0
            else:
                itr=None
            searcher(self,procs,itr)

def procInit(self):
    self.processTree=self.builder.get_object('processtree')

    # self.data=[['chrome',30,50,0,1],['firefox',10,20,0,2],['sysmon',1,0,3,1]]
    self.processTreeStore=g.TreeStore(int,str,str,str,str,str,str,str,str,str,str,str)
    # self.processTreeStore=self.builder.get_object('processTreeStore')

    # for data in self.data:
    #     self.processTreeStore.append(None,data)

    # self.processTreeStore.set_sort_func(4,sorting_func,None)

    pids=ps.pids()

    # self.di={}
    self.procDiskprev={}
    self.processList={}
    self.processTreeIterList={}
    self.processChildList={}
    self.columnList={}
    self.procT1={}

    ### total disk io counter calculation are done in proc.py
    self.diskTotalT1=0
    diskio=ps.disk_io_counters()
    self.diskTotalState1=[diskio[2],diskio[3]]

    for pi in pids:
        procs=ps.Process(pi)

        if(procs.username()=='neeraj'):
            if procs.name()=='systemd':
                self.systemdId=pi
                break

    self.processSystemd=ps.Process(self.systemdId)
    searcher(self,self.processSystemd,None)
    
    self.processTree.set_model(self.processTreeStore)


    for i,col in enumerate(['pid','Name','rCPU','CPU','rMemory','Memory','rDiskRead','DiskRead','rDiskWrite','DiskWrite','Owner','command']):
        renderer=g.CellRendererText()
        column=g.TreeViewColumn(col,renderer,text=i)
        column.set_sort_column_id(i)
        column.set_resizable(True)
        column.set_reorderable(True)
        column.set_expand(True)
        column.set_alignment(0)
        column.set_sort_indicator(True)
        self.processTree.append_column(column)
        self.columnList[col]=column   
        self.processTreeStore.set_sort_func(i,sorting_func,None)

    self.columnList['rDiskRead'].set_visible(False)
    self.columnList['rDiskWrite'].set_visible(False)

def procUpdate(self):
    pids=ps.pids()
    # new process appending
    for pi in pids:
        if pi not in self.processList and pi>self.systemdId:
            # print('my process')
            try:
                proc=ps.Process(pi)
                if '/libexec/' not in "".join(proc.cmdline()) and 'daemon' not in "".join(proc.cmdline()) and proc.username()=='neeraj':
                    for parent in proc.parents():
                        cpu_percent=proc.cpu_percent()/ps.cpu_count()
                        cpu_percent="{:.1f}".format(cpu_percent)+' %'
                        mem_info=proc.memory_info()
                        mem_util=(mem_info[0]-mem_info[2])/mibdevider
                        mem_util='{:.1f}'.format(mem_util)+' MiB'
                        if parent.pid in self.processList:
                            itr=self.processTreeStore.append(self.processTreeIterList[parent.pid],[proc.pid,proc.name(),
                            cpu_percent,cpu_percent,mem_util,mem_util,'0 KB/s','0 KB/s','0 KB/s','0 KB/s',proc.username()," ".join(proc.cmdline())])
                            self.processTreeIterList[pi]=itr
                            self.processList[pi]=proc
                            self.processChildList[parent.pid].append(pi)
                            self.processChildList[pi]=[]

                            self.procDiskprev[pi]=[0,0]     ##
                            self.procT1[pi]=0
                            print('appending',pi)
                            break
                        elif '/libexec/' not in "".join(parent.cmdline()) and 'daemon' not in "".join(parent.cmdline()) and parent.username()=='neeraj':
                            itr=self.processTreeStore.append(None,[proc.pid,proc.name(),
                            cpu_percent,cpu_percent,mem_util,mem_util,'0 KB/s','0 KB/s','0 KB/s','0 KB/s',proc.username()," ".join(proc.cmdline())])
                            self.processTreeIterList[pi]=itr
                            self.processList[pi]=proc
                            self.processChildList[pi]=[]

                            self.procDiskprev[pi]=[0,0]  ##
                            self.procT1[pi]=0
                            print('appending',pi)
                            break
            except:
                print('some error in appending')

    # updating 
    tempdi=self.processList.copy()
    for pidds in reversed(tempdi):
        itr=self.processTreeIterList[pidds]
        try:
            if pidds not in pids:
                # childremover(self,pidds)
                self.processTreeStore.remove(itr)
                self.processList.pop(pidds)
                self.processTreeIterList.pop(pidds)
                tempchi=self.processChildList.copy()

                self.procDiskprev.pop(pidds)
                for key in tempchi:
                    if key==pidds:
                        self.processChildList.pop(pidds)
                    else:
                        if pidds in self.processChildList[key]:
                            self.processChildList[key].remove(pidds)
                            
                print('poping',pidds)
            else:
                cpu_percent=self.processList[pidds].cpu_percent()/ps.cpu_count()
                cpu_percent="{:.1f}".format(cpu_percent)+' %'
                mem_info=self.processList[pidds].memory_info()
                mem_util=(mem_info[0]-mem_info[2])/mibdevider
                mem_util='{:.1f}'.format(mem_util)+' MiB'
                # prev=float(self.processTreeStore.get_value(self.processTreeIterList[pidds],6)[:-5])
                
                currArray=self.processList[pidds].io_counters()[2:4]
                procT2=time.time()
                wspeed=(currArray[1]-self.procDiskprev[pidds][1])/(procT2-self.procT1[pidds])
                wspeed=byte_to_human(wspeed)
                rspeed=(currArray[0]-self.procDiskprev[pidds][0])/(procT2-self.procT1[pidds])
                rspeed=byte_to_human(rspeed)

                self.processTreeStore.set(itr,2,cpu_percent,3,cpu_percent,4,mem_util,5,mem_util,6,rspeed,7,rspeed,8,wspeed,9,wspeed)

                self.procDiskprev[pidds]=currArray[:]
                self.procT1[pidds]=procT2
        except:
            print('error in process updating')

    # print(self.processChildList)
    for pid in reversed(self.processChildList):
        # print(pid)
        rcpu_percent=0
        rmem_util=0
        for childId in self.processChildList[pid]:
            cpu_percent=self.processTreeStore.get_value(self.processTreeIterList[childId],2)
            cpu_percent=float(cpu_percent[:-2])
            mem_util=self.processTreeStore.get_value(self.processTreeIterList[childId],4)
            mem_util=float(mem_util[:-3])
            # self.processTreeStore.set(self.processTreeIterList[childId],2,cpu_percent)
            rcpu_percent+=cpu_percent
            rmem_util+=mem_util
        if pid in self.processTreeIterList:
            cpu_percent=self.processTreeStore.get_value(self.processTreeIterList[pid],3)
            cpu_percent=float(cpu_percent[:-2])
            self.processTreeStore.set(self.processTreeIterList[pid],2,"{:.1f}".format(rcpu_percent+cpu_percent)+' %')
            mem_util=self.processTreeStore.get_value(self.processTreeIterList[pid],5)
            mem_util=float(mem_util[:-3])
            self.processTreeStore.set(self.processTreeIterList[pid],4,"{:.1f}".format(rmem_util+mem_util)+' MiB')

    self.columnList['CPU'].set_title('{0} %\nCPU'.format(self.cpuUtil))
    self.columnList['rCPU'].set_title('{0} %\nrCPU'.format(self.cpuUtil))
    self.columnList['rMemory'].set_title('{0} %\nrMemory'.format(self.memPercent))
    self.columnList['Memory'].set_title('{0} %\nMemory'.format(self.memPercent))
    
    ## Total disk io for all disks
    diskio=ps.disk_io_counters()
    diskTotalT2=time.time()
    totalrspeed=(diskio[2]-self.diskTotalState1[0])/(diskTotalT2-self.diskTotalT1)
    totalwspeed=(diskio[3]-self.diskTotalState1[1])/(diskTotalT2-self.diskTotalT1)

    self.columnList['DiskRead'].set_title('{0}\nDiskRead'.format(byte_to_human(totalrspeed)))
    self.columnList['DiskWrite'].set_title('{0}\nDiskWrite'.format(byte_to_human(totalwspeed)))

    self.diskTotalState1=diskio[2:4]
    self.diskTotalT1=diskTotalT2

    return True

    
                