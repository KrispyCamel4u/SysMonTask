from gi.repository import Gtk as g,GdkPixbuf,Wnck, Gio
import psutil as ps
from time import time,sleep,ctime
import re,os,signal,sys
from math import pow
from csv import writer

try:
    from filter_prefs import filter_process_matching_func
except ImportError:
    from sysmontask.filter_prefs import filter_process_matching_func

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

####### added for python<=3.7
def reversed_process(procdi):
    if sys.version_info >= (3, 8):
        return reversed(procdi)
    else:
        return reversed(list(procdi.keys()))

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

def sorting_func(model, row1, row2, sort_id):
    # sort_column, _ = model.get_sort_column_id()
    sort_column=sort_id
    val1 = model.get_value(row1, sort_column)
    val2 = model.get_value(row2, sort_column)
    multiplier=1
    # if val1=='NA' or val2=="NA":
    #     return 1
    if val1=='NA':
        val1='0 0'
    if val2=='NA':
        val2='0 0'
    if not isinstance(val1,int):
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
        return 1
    elif val1==val2:
        return 0
    else:
        return -1

def row_selected(self,selection):
    try:
        model,row=selection.get_selected()
        self.selected_process_pid=model[row][0]
    except:
        self.selected_process_pid=0
        print('error in row selections')

previous_killed_process_id=0
def kill_process(self,widget):
    # self.processTreeStore.remove(self.processTreeIterList[1690])
    # itr=self.processTreeStore.iter_children(self.processTreeIterList[1679])
    global previous_killed_process_id
    if self.selected_process_pid:
        print('killer on the way',self.selected_process_pid)
        dialog=confirmation_popup(self.Window,self)
        response=dialog.run()
        if response==g.ResponseType.OK:
            print('killing',self.selected_process_pid)
            try:
                if previous_killed_process_id==self.selected_process_pid:
                    os.kill(self.selected_process_pid,signal.SIGKILL)
                else:
                    os.kill(self.selected_process_pid,signal.SIGTERM)
                # os.kill(self.selected_process_pid,signal.SIGKILL)
            except:
                if previous_killed_process_id==self.selected_process_pid:
                    os.system('pkexec {1}/proc-kill.sh {0} 1'.format(self.selected_process_pid,os.path.dirname(os.path.abspath(__file__))))
                else:
                    os.system('pkexec {1}/proc-kill.sh {0} 0'.format(self.selected_process_pid,os.path.dirname(os.path.abspath(__file__))))
                # os.system('pkexec {1}/proc-kill.sh {0}'.format(self.selected_process_pid,os.path.dirname(os.path.abspath(__file__))))
            previous_killed_process_id=self.selected_process_pid

            dialog.destroy()
            sleep(0.1)
            procUpdate(self)
        else:
            dialog.destroy()

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
    """Confirmation Before Killing The Process"""
    def __init__(self,parentWindow,parent):
       g.Dialog.__init__(self,'Confirmation',parentWindow,g.DialogFlags.MODAL,(g.STOCK_CANCEL,g.ResponseType.CANCEL,
       g.STOCK_OK,g.ResponseType.OK))
       self.set_border_width(20)
       content_area=self.get_content_area()
       content_area.add(g.Label('Are you sure you want to kill the process?\nPid:{0} Name:{1}'.format(parent.selected_process_pid,parent.processList[parent.selected_process_pid].name())))
       self.show_all()

def icon_finder(process):
    # global gio_apps
    pname=process.name()
    pid=process.pid
    default_icon=icon_theme.load_icon('application-x-executable', 16, 0)

    if pname=='sh' or pname=='zsh':
        pname='bash'

    # 2nd pref using Gio.AppInfo
    for app in gio_apps:
        app_name=re.sub(' ','-',app.get_display_name())
        gicon=app.get_icon()

        if gicon and gicon.to_string()=='application-x-executable':
            continue

        if re.search(pname,app_name,re.IGNORECASE) and gicon:
            # print('1st',pname)
            temp=icon_theme.lookup_by_gicon(gicon,16,g.IconLookupFlags.FORCE_SIZE)
            if temp:
                return temp.load_icon()

        app_name=re.sub(r'','\.desktop',app.get_id())
        app_name=re.sub(r'\.','-',app_name)
        if re.search(pname,app_name,re.IGNORECASE) and gicon:
            # print('2st',pname)
            temp=icon_theme.lookup_by_gicon(gicon,16,g.IconLookupFlags.FORCE_SIZE)
            if temp:
                return temp.load_icon()

        app_name=app.get_commandline()
        if app_name:
            if re.search(pname,app_name,re.IGNORECASE) and gicon:
                # print('3st',pname,app_name)
                temp=icon_theme.lookup_by_gicon(gicon,16,g.IconLookupFlags.FORCE_SIZE)
                if temp:
                    return temp.load_icon()

    # 1st pref using icon theme
    r=re.compile(pname,re.IGNORECASE)
    matchlist = list(filter(r.match, theme_icon_list))
    if len(matchlist)!=0:
        # print(pname,' ','convention')
        return icon_theme.load_icon(matchlist[0], 16, 0)


    # 3rd pref using Wnck module to get the active screen
    if screen:
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
    idd=int(widget.get_name())
    if widget.get_active():
        self.columnList[idd].set_visible(True)
    else:
        self.columnList[idd].set_visible(False)

def on_start_interactive_search(widget):
    print('interactive search')

def interactive_search(model, column, key, iter,tree):
    tree.expand_row(model.get_path(iter),False)
    # self.processTree.expand_all()
    if key in model[iter][1] or key in model[iter][13]:
        print("found",key)
        return False
    model[iter][15]=False
    prev=model.iter_previous(iter)
    if prev:
        tree.collapse_row(model.get_path(prev))
    return True

def refresh_tree_filter(widget,self):
    """Apply filtering to results"""
    search_query = widget.get_text().lower()
    if search_query == "":
        self.processTreeStore.foreach(reset_row, True,self)
        # if self.EXPAND_BY_DEFAULT:
        # self.processTree.expand_all()
        # else:
        # self.processTree.collapse_all()
    else:
        self.matched_iters=[]
        self.processTreeStore.foreach(reset_row, False,self)
        self.processTreeStore.foreach(show_matches, search_query,self)
        self.processTree.expand_all()


    self.filter_model.refilter()

def reset_row(model, path, iter, make_visible,self):
    """Reset some row attributes independent of row hierarchy"""
    model.set_value(iter, self.COL_VISIBLE, make_visible)

def make_path_visible(model, iter,self):
    """Make a row and its ancestors visible"""
    while iter:
        self.processTreeStore.set_value(iter, self.COL_VISIBLE, True)
        # self.processTree.expand_row(self.processTreeStore.get_path(iter),False)
        iter = model.iter_parent(iter)

def make_subtree_visible(model, iter,self):
    """Make descendants of a row visible"""
    # self.processTree.collapse_row(model.get_path(iter))
    for i in range(model.iter_n_children(iter)):
        subtree = model.iter_nth_child(iter, i)
        if model.get_value(subtree, self.COL_VISIBLE):
            # Subtree already visible
            continue
        model.set_value(subtree, self.COL_VISIBLE, True)
        # print("sdfsa")
        make_subtree_visible(model, subtree,self)

def show_matches(model, path, iter, search_query,self):
    text_name = model.get_value(iter, self.COL_NAME).lower()
    text_command=model.get_value(iter, self.COL_COMMAND).lower()
    if search_query in text_name or search_query in text_command:
        # Propagate visibility change up
        make_path_visible(model, iter,self)
        # Propagate visibility change down
        # self.processTree.expand_all()
        make_subtree_visible(model, iter,self)
        self.matched_iters.append(iter)
        return

# def show_menu(self):
#     # i1 = g.MenuItem("Item 1")
#     i1=g.CheckMenuItem(label='hello')
#     self.popMenu.append(i1)
#     i2 = g.MenuItem("Item 2")
#     self.popMenu.append(i2)
#     self.popMenu.show_all()
#     self.popMenu.popup(None, None, None, None, 0, g.get_current_event_time())
#     print("Done")

def searcher(self,sysproc):
    childlist=sysproc.children()
    for procs in childlist:
        if procs.pid not in self.black_list:
            self.processChildList[procs.pid]=[]
            try:
                cpu_percent=procs.cpu_percent()
                mem_info=procs.memory_info()
            except Exception as e:
                print(f"process error in searcher: {e}")
                continue

            cpu_percent="{:.1f} %".format(cpu_percent)


            rss='{:.1f} MiB'.format(mem_info[0]/mibdevider) #resident memory in string
            shared='{:.1f} MiB'.format(mem_info[2]/mibdevider) #shared memory in string
            mem_util=(mem_info[0]-mem_info[2])/mibdevider
            mem_util='{:.1f} MiB'.format(mem_util)
            try:
                pitr=self.processTreeStore.append(None,[procs.pid,procs.name(),cpu_percent,cpu_percent,mem_util
                ,mem_util,'0 KB/s','0 KB/s','0 KB/s','0 KB/s',rss,shared,procs.username()," ".join(procs.cmdline()),
                icon_finder(procs),True])
            except Exception as e:
                print(f"process appending error in searcher: {e}")
                continue

            self.processTreeIterList[procs.pid]=pitr
            self.processList[procs.pid]=procs
            self.procDiskprev[procs.pid]=[0,0]
            self.procT1[procs.pid]=0
            # self.processTree.expand_row(self.processTreeStore.get_path(pitr),False)

            for cprocs in procs.children():
                if cprocs.pid not in self.black_list:
                    try:
                        cpu_percent=cprocs.cpu_percent()
                        mem_info=cprocs.memory_info()
                    except Exception as e:
                        print(f"process error in child searcher: {e}")
                        continue

                    cpu_percent="{:.1f} %".format(cpu_percent)


                    rss='{:.1f} MiB'.format(mem_info[0]/mibdevider) #resident memory in string
                    shared='{:.1f} MiB'.format(mem_info[2]/mibdevider) #shared memory in string
                    mem_util=(mem_info[0]-mem_info[2])/mibdevider
                    mem_util='{:.1f} MiB'.format(mem_util)
                    try:
                        itr=self.processTreeStore.append(pitr,[cprocs.pid,cprocs.name(),cpu_percent,cpu_percent,mem_util
                        ,mem_util,'0 KB/s','0 KB/s','0 KB/s','0 KB/s',rss,shared,cprocs.username()," ".join(cprocs.cmdline()),
                        icon_finder(cprocs),True])
                    except Exception as e:
                        print(f"process appending error in child searcher: {e}")
                        continue

                    self.processChildList[cprocs.pid]=[]
                    self.processChildList[procs.pid].append(cprocs.pid)

                    self.processTreeIterList[cprocs.pid]=itr
                    self.processList[cprocs.pid]=cprocs
                    self.procDiskprev[cprocs.pid]=[0,0]
                    self.procT1[cprocs.pid]=0

def appending(self,pids,cpu_count):

    # new process appending
    # st=time()
    pids=list(pids)
    pids.sort()
    for pi in pids:
        if pi not in self.processList and pi>1:  # and pi>self.systemdId changed for mutliple user
            # print('my process')
            try:
                try:
                    proc=ps.Process(pi)
                except Exception as e:
                    print(f'process error in appending: {e}')
                    continue
                # if proc in self.blacklist: #or proc in (self.process_cinnamon+self.process_terminal_server):
                #     continue
                # cmdline="".join(proc.cmdline())
                if proc.pid in self.black_list:
                    continue
                parents_processess=proc.parents()
                appended=False
                if self.processSystemd in parents_processess:
                    filter_process_matching_func(self,proc)
                    # print(pi)
                    if pi in self.black_list:
                        continue


                    for parent in parents_processess:
                        # print(parent)
                        if parent.pid in self.processList:
                            # print(parent.pid)
                            try:
                                cpu_percent=proc.cpu_percent()/cpu_count
                                mem_info=proc.memory_info()
                            except Exception as e:
                                print(f'value get error in appending: {e}')
                                break

                            cpu_percent="{:.1f} %".format(cpu_percent)

                            rss='{:.1f} MiB'.format(mem_info[0]/mibdevider)
                            shared='{:.1f} MiB'.format(mem_info[2]/mibdevider)
                            mem_util=(mem_info[0]-mem_info[2])/mibdevider
                            mem_util='{:.1f} MiB'.format(mem_util)

                            itr=self.processTreeStore.append(self.processTreeIterList[parent.pid],[proc.pid,proc.name(),
                            cpu_percent,cpu_percent,mem_util,mem_util,'0 KB/s','0 KB/s','0 KB/s','0 KB/s',rss,shared,proc.username()
                            ," ".join(proc.cmdline()),icon_finder(proc),True])
                            self.processTreeIterList[pi]=itr
                            self.processList[pi]=proc
                            self.processChildList[parent.pid].append(pi)
                            self.processChildList[pi]=[]

                            self.procDiskprev[pi]=[0,0]     ##
                            self.procT1[pi]=0
                            appended=True
                            print('appending',pi)
                            break
                    if not appended:
                        try:
                            cpu_percent=proc.cpu_percent()/cpu_count
                            mem_info=proc.memory_info()
                        except Exception as e:
                            print(f'value get error in appending: {e}')
                            break

                        cpu_percent="{:.1f} %".format(cpu_percent)

                        rss='{:.1f} MiB'.format(mem_info[0]/mibdevider)
                        shared='{:.1f} MiB'.format(mem_info[2]/mibdevider)
                        mem_util=(mem_info[0]-mem_info[2])/mibdevider
                        mem_util='{:.1f} MiB'.format(mem_util)

                        itr=self.processTreeStore.append(None,[proc.pid,proc.name(),
                        cpu_percent,cpu_percent,mem_util,mem_util,'0 KB/s','0 KB/s','0 KB/s','0 KB/s',rss,shared,proc.username()
                        ," ".join(proc.cmdline()),icon_finder(proc),True])
                        self.processTreeIterList[pi]=itr
                        self.processList[pi]=proc
                        self.processChildList[pi]=[]

                        self.procDiskprev[pi]=[0,0]  ##
                        self.procT1[pi]=0
                        print('appending',pi)

                    # print('before child arranging')
                    for child in proc.children(True):
                        if child.pid in self.processList:
                            # print('bef rem')
                            process_pop(self,child.pid,self.processTreeIterList[child.pid])
                            # print('rem')
            except Exception as e:
                print(f'some error in appending: {e}')
    if self.append_signal>0:
        self.append_signal-=1

    # print("append time",time()-st)

def on_record_button_toggle(widget,self):
    wname=widget.get_name()
    try:
        log_path=os.path.join(os.environ.get("HOME"),"sysmontask_log")
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        if widget.get_active():
            if wname=="record_start":
                if self.selected_process_pid:
                    self.record_start=True
                    self.log_file_name=f'{self.processList[self.selected_process_pid].name()}_{ctime().replace(" ","_")}.csv'
                    self.log_file=open(f'{log_path}/{self.log_file_name}', 'w+',newline='')
                    self.log_file_writer=writer(self.log_file)
                    self.log_file_writer.writerow(['rCPU','CPU','rMemory','Memory','DiskRead','DiskWrite'])
                    self.log_pid=self.selected_process_pid
                    widget.set_tooltip_text(f"Recording: {self.log_pid},{self.processList[self.log_pid].name()}")
                    print("record start")
            elif wname=="record_pause":
                self.record_pause=True
                if self.log_file:
                    self.log_file.close()

                widget.set_tooltip_text("Paused")
                print("record pause")
        else:
            if wname=="record_start":
                self.record_start=False
                self.log_file.close()
                self.log_pid=0
                widget.set_tooltip_text("Start Recording")
            elif wname=="record_pause":
                self.record_pause=False
                print("record_pause false")
                if self.log_pid:

                    self.log_file=open(f'{log_path}/{self.log_file_name}', 'a+',newline='')
                    self.log_file_writer=writer(self.log_file)
                widget.set_tooltip_text("Pause Recording")
    except :
        print("error while recording")
        self.process_record_pause.set_active(False)
        self.process_record_start.set_active(False)

def procInit(self):
    # self.processTree=self.builder.get_object('processtree')

    self.COL_NAME,self.COL_COMMAND,self.COL_VISIBLE=1,13,15

    self.processTree=g.TreeView()
    self.process_tab_box.add(self.processTree)
    self.process_tab_box.show_all()
    self.processTree_background=self.builder.get_object('processtreeBackground')
    self.process_kill_button=self.builder.get_object('processKillButton')
    self.process_kill_button.connect('clicked',self.kill_process)

    # self.processTree.connect("start-interactive-search",on_start_interactive_search)
    # self.processTree.set_search_equal_func(interactive_search,self.processTree)
    self.process_tree_search_entry=self.builder.get_object("process_search_entry")
    self.process_tree_search_entry.connect("changed",refresh_tree_filter,self)

    self.processTree.set_search_entry(self.process_tree_search_entry)
    self.processTree.set_enable_tree_lines(True)

    ## process record
    self.record_start,self.record_pause=False,False
    self.log_file=None

    self.process_record_start=self.builder.get_object("process_record_start")
    self.process_record_pause=self.builder.get_object("process_record_pause")

    self.process_record_start.connect("toggled",on_record_button_toggle,self)
    self.process_record_pause.connect("toggled",on_record_button_toggle,self)

    # Diabling them until a process is selected
    self.process_record_start.set_sensitive(False)
    self.process_record_pause.set_sensitive(False)
    self.process_kill_button.set_sensitive(False)

    #                                 0   1   2   3   4   5   6   7   8   9   10   11  12  13       14
    self.processTreeStore=g.TreeStore(int,str,str,str,str,str,str,str,str,str,str,str,str,str,GdkPixbuf.Pixbuf,bool)
    self.filter_model=self.processTreeStore.filter_new()
    self.filter_model.set_visible_column(15)
    self.filter_sort_model=g.TreeModelSort(self.filter_model)

    #treestore->sort_model->filter_model
    # self.filter_sort_model=g.TreeModelSort(self.processTreeStore)
    # self.filter_model=self.filter_sort_model.filter_new()
    # self.filter_model.set_visible_column(15)


    # self.di={}
    self.procDiskprev,self.processList,self.processTreeIterList,self.processChildList,self.columnList\
       ,self.procT1 ={},{},{},{},{},{}
    self.old_pids=[]

    ### total disk io counter calculation are done in proc.py
    self.diskTotalT1=0
    diskio=ps.disk_io_counters()
    self.diskTotalState1=[diskio[2],diskio[3]]

    self.systemdId=1
    self.selected_process_pid=0
    self.processSystemd=ps.Process(1)

    self.blacklist=[]

    searcher(self,self.processSystemd)

    # self.processTree.set_model(self.processTreeStore)
    self.processTree.set_model(self.filter_sort_model)
    #                          0    1       2      3        4       5           6       7           8               9           10              11      12       13
    self.column_header_list=['pid','Name','rCPU','CPU','rMemory','Memory','rDiskRead','DiskRead','rDiskWrite','DiskWrite','Resident\nMemory','Shared','Owner','Command']

    self.column_select_popover_check_buttons={}
    self.column_header_labels=[]
    self.column_select_popover=g.Menu()

    for i,col in enumerate(self.column_header_list):
        renderer=g.CellRendererText()
        # renderer.props.wrap_width=500
        # if col=='Command':
        #     renderer.props.wrap_width=1
        if col=='Name':
            icon_renderer=g.CellRendererPixbuf()
            column=g.TreeViewColumn(col)
            column.pack_start(icon_renderer,False)
            column.add_attribute(icon_renderer,'pixbuf',14)
            column.pack_start(renderer,False)
            column.add_attribute(renderer,'text',1)

        else:
            column=g.TreeViewColumn(col,renderer,text=i)

        ## forcing the column header to have the widget to get the button
        label = g.Label(col)
        label.show()
        self.column_header_labels.append(label)
        column.set_widget(label)

        widget = column.get_widget()
        while not isinstance(widget, g.Button):
            widget = widget.get_parent()
        widget.connect('button-press-event',self.column_button_press)

        column.set_sort_column_id(i)
        column.set_resizable(True)
        column.set_reorderable(True)
        column.set_expand(True)
        # column.set_alignment(0)
        column.set_sort_indicator(True)
        # Setting the minimum width so that the column wont move with each update of values
        column.set_min_width(90)

        self.processTree.append_column(column)
        self.columnList[i]=column

        popover_check_button=g.CheckMenuItem(label=col)
        popover_check_button.set_name(str(i))
        popover_check_button.connect('toggled',self.column_header_selection)
        popover_check_button.set_active(True)
        self.column_select_popover.append(popover_check_button)
        self.column_select_popover_check_buttons[i]=popover_check_button

        # if i not in [1,6,7,8,9]:
        if not (i==1 or i==12 or i==13) :
            # self.filter_sort_model.set_sort_column_id(i,1)
            self.filter_sort_model.set_sort_func(i,sorting_func,i)
            # self.filter_model.set_sort_func(i,sorting_func,None)

    self.column_select_popover.show_all()

    selected_row=self.processTree.get_selection()
    selected_row.connect("changed",self.row_selected)

    # self.processTree.connect('button-press-event',self.column_button_press)
    # self.processTree.connect(popover=self.column_select_popover)

    self.column_select_popover_check_buttons[6].set_active(False)
    self.column_select_popover_check_buttons[8].set_active(False)
    self.column_select_popover_check_buttons[10].set_active(False)
    self.column_select_popover_check_buttons[11].set_active(False)

    # self.kproc_set=set(ps.Process(2).children(True))

def child_remover(self,procId,itr):
    for child in self.processChildList[procId]:
        child_remover(self,child,self.processTreeIterList[child])
    self.processChildList.pop(procId)
    self.processTreeIterList.pop(procId)
    self.processTreeStore.remove(itr)
    self.processList.pop(procId)

def process_pop(self,pidds,itr):
    # self.processTreeStore.remove(itr)
    # self.processList.pop(pidds)
    # self.processTreeIterList.pop(pidds)

    self.procDiskprev.pop(pidds)
    child_remover(self,pidds,itr)
    tempchi=self.processChildList.copy()
    for key in tempchi:
        if pidds in self.processChildList[key]:
            self.processChildList[key].remove(pidds)
            # self.processTreeIterList.pop(pidds)

def procUpdate(self,header=True):

    if self.selected_process_pid==0:
        self.process_record_start.set_sensitive(False)
        self.process_record_pause.set_sensitive(False)
        self.process_kill_button.set_sensitive(False)
    else:
        self.process_record_start.set_sensitive(True)
        self.process_record_pause.set_sensitive(True)
        self.process_kill_button.set_sensitive(True)

    # stt=time()
    cpu_count=ps.cpu_count()

    pids=set(ps.pids())
    # pids=list(set(pids)-self.kproc_set)
    # print(list(pids))
    if self.old_pids!=pids or self.append_signal:
        appending(self,pids,cpu_count)

    # st=time()
    # updating
    # print('before update')
    tempdi=self.processList.copy()
    pids=set(pids)
    for pidds in reversed_process(tempdi):

        itr=self.processTreeIterList[pidds]
        if pidds in self.black_list:
            # print("before pop1")
            process_pop(self,pidds,itr)
            continue
        try:
            if pidds not in pids:

                process_pop(self,pidds,itr)

                print('poping',pidds)
            else:
                # ut=time()
                try:
                    cpu_percent=self.processList[pidds].cpu_percent()/cpu_count
                    mem_info=self.processList[pidds].memory_info()
                except Exception:
                    process_pop(self,pidds,itr)
                    continue
                # print("time2",time()-ut)

                cpu_percent="{:.1f} %".format(cpu_percent)

                rss='{:.1f} MiB'.format(mem_info[0]/mibdevider)
                shared='{:.1f} MiB'.format(mem_info[2]/mibdevider)
                mem_util=(mem_info[0]-mem_info[2])/mibdevider
                mem_util='{:.1f} MiB'.format(mem_util)

                # prev=float(self.processTreeStore.get_value(self.processTreeIterList[pidds],6)[:-5])

                ########## added for running as non-root
                # ut=time()
                try:
                    currArray=self.processList[pidds].io_counters()[2:4]
                    procT2=time()
                    wspeed=(currArray[1]-self.procDiskprev[pidds][1])/(procT2-self.procT1[pidds])
                    wspeed=byte_to_human(wspeed)
                    rspeed=(currArray[0]-self.procDiskprev[pidds][0])/(procT2-self.procT1[pidds])
                    rspeed=byte_to_human(rspeed)
                except:
                    wspeed='NA'
                    rspeed='NA'
                # print('before tree store',pidds)

                self.processTreeStore.set(itr,2,cpu_percent,3,cpu_percent,4,mem_util,5,mem_util,6,'0',7,rspeed,8,'0',9,wspeed,10,rss,11,shared)

                try:
                    self.procDiskprev[pidds]=currArray[:]
                    self.procT1[pidds]=procT2
                except:
                    pass
                # print("time4",time()-ut)
        except Exception as e:
            print(f'error in process updating: {e}')

    # print("updating time",time()-st)
    # st=time()
    # print(self.processChildList)
    #recursive calculations
    for pid in reversed_process(self.processChildList):
        # print(pid)
        rcpu_percent=0
        rmem_util=0
        try:
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
                self.processTreeStore.set(self.processTreeIterList[pid],2,"{:.1f} %".format(rcpu_percent+cpu_percent))
                mem_util=self.processTreeStore.get_value(self.processTreeIterList[pid],5)
                mem_util=float(mem_util[:-3])
                self.processTreeStore.set(self.processTreeIterList[pid],4,"{:.1f} MiB".format(rmem_util+mem_util))
        except Exception as e:
            print(f"problem in recursive calculations: {e}")

    # print("recursive time",time()-st)
    # st=time()

    self.column_header_labels[3].set_text('{0} %\nCPU'.format(self.cpuUtil))
    self.column_header_labels[2].set_text('{0} %\nrCPU'.format(self.cpuUtil))
    self.column_header_labels[4].set_text('{0} %\nrMemory'.format(self.memPercent))
    self.column_header_labels[5].set_text('{0} %\nMemory'.format(self.memPercent))

    ## Total disk io for all disks
    diskio=ps.disk_io_counters()
    diskTotalT2=time()
    totalrspeed=(diskio[2]-self.diskTotalState1[0])/(diskTotalT2-self.diskTotalT1)
    totalwspeed=(diskio[3]-self.diskTotalState1[1])/(diskTotalT2-self.diskTotalT1)

    self.column_header_labels[7].set_text('{0}\nDiskRead'.format(byte_to_human(totalrspeed)))
    self.column_header_labels[9].set_text('{0}\nDiskWrite'.format(byte_to_human(totalwspeed)))

    self.diskTotalState1=diskio[2:4]
    self.diskTotalT1=diskTotalT2

    if self.record_start and not self.record_pause:
        try:
            if self.log_pid in self.processList:
                row=self.processTreeStore[self.processTreeIterList[self.log_pid]]
                self.log_file_writer.writerow(row[2:6]+[row[7],row[9]])
            else:
                self.process_record_start.set_active(False)
        except Exception as e:
            print(f"Log write error: {e}")

    self.old_pids=pids.copy()

    # print("header time",time()-st)
    # print("total time",time()-stt)

    return True



