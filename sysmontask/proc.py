from gi.repository import Gtk as g , GLib as go
import psutil as ps,cairo,time
from math import pow
mibdevider=pow(2,20)
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
                mem_util='{:.1f}'.format(mem_util)+' MB'
                itr=self.processTreeStore.append(root,[procs.pid,procs.name(),cpu_percent,cpu_percent,mem_util
                ,mem_util,'0 MB/s','0 MB/s',procs.username()," ".join(procs.cmdline())])
                self.processTreeIterList[procs.pid]=itr
                self.processList[procs.pid]=procs
                self.procDiskprev[procs.pid]=[0,0]
            else:
                itr=None
            searcher(self,procs,itr)

def procInit(self):
    self.processTree=self.builder.get_object('processtree')

    # self.data=[['chrome',30,50,0,1],['firefox',10,20,0,2],['sysmon',1,0,3,1]]
    self.processTreeStore=g.TreeStore(int,str,str,str,str,str,str,str,str,str)
    # self.processTreeStore=self.builder.get_object('processTreeStore')

    # for data in self.data:
    #     self.processTreeStore.append(None,data)
    pids=ps.pids()

    # self.di={}
    self.procDiskprev={}
    self.processList={}
    self.processTreeIterList={}
    self.processChildList={}
    for pi in pids:
        procs=ps.Process(pi)

        if(procs.username()=='neeraj'):
            if procs.name()=='systemd':
                self.systemdId=pi
                break

    self.processSystemd=ps.Process(self.systemdId)
    searcher(self,self.processSystemd,None)
    
    self.processTree.set_model(self.processTreeStore)


    for i,col in enumerate(['pid','Name','rCPU','CPU','rMemory','Memory','rDisk','Disk','Network','command']):
        renderer=g.CellRendererText()

        column=g.TreeViewColumn(col,renderer,text=i)
        column.set_sort_column_id(i)
        column.set_resizable(True)
        column.set_reorderable(True)
        column.set_expand(True)
        column.set_alignment(0)
        column.set_sort_indicator(True)
        self.processTree.append_column(column)
        
    self.procT1=0

# def childremover(self, pid):
#     temp=self.processChildList[pid]
#     self.processChildList.pop(pid)
#     for childId in temp:
#         if childId in self.processList:
#             self.processList.pop(childId)
#         if childId in self.processTreeIterList:
#             self.processTreeIterList.pop(childId)
#         childremover(self,childId)

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
                        mem_util='{:.1f}'.format(mem_util)+' MB'
                        if parent.pid in self.processList:
                            itr=self.processTreeStore.append(self.processTreeIterList[parent.pid],[proc.pid,proc.name(),
                            cpu_percent,cpu_percent,mem_util,mem_util,'0 MB/s','0 MB/s',proc.username()," ".join(proc.cmdline())])
                            self.processTreeIterList[pi]=itr
                            self.processList[pi]=proc
                            self.processChildList[parent.pid].append(pi)
                            self.processChildList[pi]=[]
                            self.procDiskprev[pi]=[0,0]   ##
                            print('appending',pi)
                            break
                        elif '/libexec/' not in "".join(parent.cmdline()) and 'daemon' not in "".join(parent.cmdline()) and parent.username()=='neeraj':
                            itr=self.processTreeStore.append(None,[proc.pid,proc.name(),
                            cpu_percent,cpu_percent,mem_util,mem_util,'0 MB/s','0 MB/s',proc.username()," ".join(proc.cmdline())])
                            self.processTreeIterList[pi]=itr
                            self.processList[pi]=proc
                            self.processChildList[pi]=[]
                            self.procDiskprev[pi]=[0,0]  ##
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
                mem_util='{:.1f}'.format(mem_util)+' MB'
                # prev=float(self.processTreeStore.get_value(self.processTreeIterList[pidds],6)[:-5])
                currArray=self.processList[pidds].io_counters()[2:4]
                self.procT2=time.time()
                sp=max((currArray[0]-self.procDiskprev[pidds][0]),(currArray[1]-self.procDiskprev[pidds][1]))/(self.procT2-self.procT1)
                rwspeed="{:.1f} MB/s".format(sp)
                if self.processList[pidds].name()=='nautilus':
                    print(currArray,self.procDiskprev[pidds],sp,self.procT2-self.procT1)
                self.processTreeStore.set(itr,2,cpu_percent,3,cpu_percent,4,mem_util,5,mem_util,6,rwspeed,7,rwspeed)
                self.procDiskprev[pidds]=currArray[:]
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
            self.processTreeStore.set(self.processTreeIterList[pid],4,"{:.1f}".format(rmem_util+mem_util)+' MB')

    self.procT1=self.procT2
    return True

    
                