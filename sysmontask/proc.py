from gi.repository import Gtk as g , GLib as go,GdkPixbuf,Wnck, Gio
import psutil as ps,cairo,time
import re,os,signal
from math import pow

mibdevider=pow(2,20)
screen=Wnck.Screen.get_default()
icon_theme=g.IconTheme().get_default()
icon_theme.append_search_path('/usr/share/')
theme_icon_list=icon_theme.list_icons(None)
gio_apps=Gio.AppInfo.get_all()
# for app in Gio.AppInfo.get_all():
#     exetuable=app.get_executable()
#     if exetuable:
#         gio_apps[exetuable.split('/')[-1]]=app.get_icon()
#     else:
#         gio_apps[]=app.get_icon()
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
    multiplier=1
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

def row_selected(self,selection):
    try:
        model,row=selection.get_selected()
        self.selected_process_pid=model[row][0]
    except:
        print('error in row selections')

def kill_process(self,widget):
    # try:
    print('keller on the way',self.selected_process_pid)
    dialog=confirmation_popup(self.Window,self)
    response=dialog.run()
    if response==g.ResponseType.OK:
        print('killing',self.selected_process_pid)
        os.kill(self.selected_process_pid,signal.SIGTERM)
    dialog.destroy()
    time.sleep(0.1)
    procUpdate(self)
    # dialog=g.Dialog('Confirmation',self.Window,g.DialogFlags.MODAL,(g.STOCK_CANCEL,g.ResponseType.CANCEL,
    #    g.STOCK_OK,g.ResponseType.OK))
    # dialog.vbox.add(g.Label('hello'))
    # dialog.show_all()
    # res=dialog.run()
    # print(res)
    # dialog.destroy()
    # except:
    #     print('some error in killing')

class confirmation_popup(g.Dialog):
    def __init__(self,parentWindow,parent):
       g.Dialog.__init__(self,'Confirmation',parentWindow,g.DialogFlags.MODAL,(g.STOCK_CANCEL,g.ResponseType.CANCEL,
       g.STOCK_OK,g.ResponseType.OK))
       self.set_border_width(20)
       content_area=self.get_content_area() 
       content_area.add(g.Label('Are you sure you want to kill the process?\nPid:{0} Name:{1}'.format(parent.selected_process_pid,parent.processList[parent.selected_process_pid].name())))
       self.show_all()

def icon_finder(process):
    global gio_apps
    pname=process.name()
    pid=process.pid
    default_icon=icon_theme.load_icon('application-x-executable', 16, 0)

    if pname=='sh':
        pname='bash'
    
    # 2nd pref using Gio.AppInfo
    for app in gio_apps:
        app_name=re.sub(' ','-',app.get_display_name())
        gicon=app.get_icon()

        if gicon and gicon.to_string()=='application-x-executable':
            continue

        if re.search(pname,app_name,re.IGNORECASE) and gicon:  
            # print('1st',pname)      
            return icon_theme.lookup_by_gicon(gicon,16,g.IconLookupFlags.FORCE_SIZE).load_icon()

        app_name=re.sub('','\.desktop',app.get_id())
        app_name=re.sub('\.','-',app_name)       
        if re.search(pname,app_name,re.IGNORECASE) and gicon:
            # print('2st',pname) 
            return icon_theme.lookup_by_gicon(gicon,16,g.IconLookupFlags.FORCE_SIZE).load_icon()

        app_name=app.get_commandline()
        if app_name:
            if re.search(pname,app_name,re.IGNORECASE) and gicon:
                # print('3st',pname,app_name) 
                return icon_theme.lookup_by_gicon(gicon,16,g.IconLookupFlags.FORCE_SIZE).load_icon()
    
    # 1st pref using icon theme
    r=re.compile(pname,re.IGNORECASE)
    matchlist = list(filter(r.match, theme_icon_list))
    if len(matchlist)!=0:
        # print(pname,' ','convention')
        return icon_theme.load_icon(matchlist[0], 16, 0)


    # 3rd pref using Wnck module to get the active screen
    screen.force_update()
    for win in screen.get_windows():
        # print(win.get_name()
        
        if pid==win.get_pid() or re.search(pname,win.get_name(),re.IGNORECASE):
            return win.get_icon().scale_simple(20,20,2)

    # 4th pref using regex to search *name*
    r=re.compile(".*{}.*".format(pname),re.IGNORECASE)
    matchlist = list(filter(r.match, theme_icon_list))
    if len(matchlist)!=0:
        return icon_theme.load_icon(matchlist[0], 16, 0)

    # last prefs
    return default_icon
    
def column_button_press(self,treeview,event):
    if event.button==3:
        # path = treeview.get_path_at_pos(event.x,event.y)
        self.column_select_popover.popup(None, None, None, None, 0, g.get_current_event_time())
        # print("right click registered")

def column_header_selection(self,widget):
    id=int(widget.get_name())
    if widget.get_active():
        self.columnList[id].set_visible(True)
    else:
        self.columnList[id].set_visible(False)

# def show_menu(self):
#     # i1 = g.MenuItem("Item 1")
#     i1=g.CheckMenuItem(label='hello')
#     self.popMenu.append(i1)
#     i2 = g.MenuItem("Item 2")
#     self.popMenu.append(i2)
#     self.popMenu.show_all()
#     self.popMenu.popup(None, None, None, None, 0, g.get_current_event_time())
#     print("Done")

def searcher(self,sprocs,root):
    childlist=sprocs.children()
    if(sprocs.name()!='systemd'): 
        self.processChildList[sprocs.pid]=[]

    if len(childlist)==0:
        return 
    else:
        try:
            for procs in childlist:
                if (root!=None) or ('/libexec/' not in "".join(procs.cmdline()) and 'daemon' not in "".join(procs.cmdline()) and 'dbus' not in "".join(procs.cmdline()) ):
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
                    ,mem_util,'0 KB/s','0 KB/s','0 KB/s','0 KB/s',procs.username()," ".join(procs.cmdline()),icon_finder(procs)])
                    self.processTreeIterList[procs.pid]=itr
                    self.processList[procs.pid]=procs
                    self.procDiskprev[procs.pid]=[0,0]
                    self.procT1[procs.pid]=0
                else:
                    itr=None
                searcher(self,procs,itr)
        except:
            print('some error in searcher')

def procInit(self):
    # self.processTree=self.builder.get_object('processtree')
    
    self.processTree=g.TreeView()
    self.process_tab_box.add(self.processTree)
    self.process_tab_box.show_all()
    self.processTree_background=self.builder.get_object('processtreeBackground')
    self.process_kill_button=self.builder.get_object('processKillButton')
    self.process_kill_button.connect('clicked',self.kill_process)

    # self.data=[['chrome',30,50,0,1],['firefox',10,20,0,2],['sysmon',1,0,3,1]]
    self.processTreeStore=g.TreeStore(int,str,str,str,str,str,str,str,str,str,str,str,GdkPixbuf.Pixbuf)
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

        if(procs.username()!='root'):
            if procs.name()=='systemd':
                self.systemdId=pi
                break

    self.processSystemd=ps.Process(self.systemdId)
    searcher(self,self.processSystemd,None)
    
    self.processTree.set_model(self.processTreeStore)
    self.column_header_list=['pid','Name','rCPU','CPU','rMemory','Memory','rDiskRead','DiskRead','rDiskWrite','DiskWrite','Owner','Command']

    self.column_select_popover_check_buttons={}
    self.column_select_popover=g.Menu()
    # self.column_select_popover=g.Popover()
    # self.vbox=g.Box(orientation=g.Orientation.VERTICAL)
    # self.column_select_popover.add(self.vbox)

    for i,col in enumerate(self.column_header_list):
        renderer=g.CellRendererText()
        if col=='Command':
            renderer.props.wrap_width=-1
        if col=='Name':
            icon_renderer=g.CellRendererPixbuf()
            column=g.TreeViewColumn(col)
            column.pack_start(icon_renderer,False)
            column.add_attribute(icon_renderer,'pixbuf',12)
            column.pack_start(renderer,False)
            column.add_attribute(renderer,'text',1)
        else:
            column=g.TreeViewColumn(col,renderer,text=i)
        

        column.set_sort_column_id(i)
        column.set_resizable(True)
        column.set_reorderable(True)
        column.set_expand(True)
        column.set_alignment(0)
        column.set_sort_indicator(True)
        
        self.processTree.append_column(column)
        self.columnList[i]=column

        popover_check_button=g.CheckMenuItem(label=col)
        popover_check_button.set_name(str(i))
        popover_check_button.connect('toggled',self.column_header_selection)
        popover_check_button.set_active(True)
        self.column_select_popover.append(popover_check_button)
        self.column_select_popover_check_buttons[i]=popover_check_button

        if i!=1:   
            self.processTreeStore.set_sort_func(i,sorting_func,None)

    self.column_select_popover.show_all()

    selected_row=self.processTree.get_selection()
    selected_row.connect("changed",self.row_selected)
    # print("error occured in selecting row")

    self.processTree.connect('button-press-event',self.column_button_press)
    # self.processTree.connect(popover=self.column_select_popover)

    # self.columnList['rDiskRead'].set_visible(False)
    # self.columnList['rDiskWrite'].set_visible(False)
    # self.columnList[6].set_visible(False)
    # self.columnList[8].set_visible(False)
    self.column_select_popover_check_buttons[6].set_active(False)
    self.column_select_popover_check_buttons[8].set_active(False)

def procUpdate(self):
    pids=ps.pids()
    # new process appending
    for pi in pids:
        if pi not in self.processList and pi>self.systemdId:
            # print('my process')
            try:
                proc=ps.Process(pi)
                if '/libexec/' not in "".join(proc.cmdline()) and 'daemon' not in "".join(proc.cmdline()) and 'dbus' not in "".join(proc.cmdline()) :
                    parents_processess=proc.parents()
                    if self.processSystemd in parents_processess:
                        for parent in parents_processess:
                            cpu_percent=proc.cpu_percent()/ps.cpu_count()
                            cpu_percent="{:.1f}".format(cpu_percent)+' %'
                            mem_info=proc.memory_info()
                            mem_util=(mem_info[0]-mem_info[2])/mibdevider
                            mem_util='{:.1f}'.format(mem_util)+' MiB'
                            if parent.pid in self.processList:
                                itr=self.processTreeStore.append(self.processTreeIterList[parent.pid],[proc.pid,proc.name(),
                                cpu_percent,cpu_percent,mem_util,mem_util,'0 KB/s','0 KB/s','0 KB/s','0 KB/s',proc.username()
                                ," ".join(proc.cmdline()),icon_finder(proc)])
                                self.processTreeIterList[pi]=itr
                                self.processList[pi]=proc
                                self.processChildList[parent.pid].append(pi)
                                self.processChildList[pi]=[]

                                self.procDiskprev[pi]=[0,0]     ##
                                self.procT1[pi]=0
                                print('appending',pi)
                                break
                            elif '/libexec/' not in "".join(parent.cmdline()) and 'daemon' not in "".join(parent.cmdline()) and 'dbus' not in "".join(parent.cmdline()):
                                itr=self.processTreeStore.append(None,[proc.pid,proc.name(),
                                cpu_percent,cpu_percent,mem_util,mem_util,'0 KB/s','0 KB/s','0 KB/s','0 KB/s',proc.username()
                                ," ".join(proc.cmdline()),icon_finder(proc)])
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

    self.columnList[3].set_title('{0} %\nCPU'.format(self.cpuUtil))
    self.columnList[2].set_title('{0} %\nrCPU'.format(self.cpuUtil))
    self.columnList[4].set_title('{0} %\nrMemory'.format(self.memPercent))
    self.columnList[5].set_title('{0} %\nMemory'.format(self.memPercent))
    
    ## Total disk io for all disks
    diskio=ps.disk_io_counters()
    diskTotalT2=time.time()
    totalrspeed=(diskio[2]-self.diskTotalState1[0])/(diskTotalT2-self.diskTotalT1)
    totalwspeed=(diskio[3]-self.diskTotalState1[1])/(diskTotalT2-self.diskTotalT1)

    self.columnList[7].set_title('{0}\nDiskRead'.format(byte_to_human(totalrspeed)))
    self.columnList[9].set_title('{0}\nDiskWrite'.format(byte_to_human(totalwspeed)))

    self.diskTotalState1=diskio[2:4]
    self.diskTotalT1=diskTotalT2

    return True

    
                