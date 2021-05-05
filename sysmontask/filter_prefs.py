from gi.repository import Gtk as g, GLib as go
import psutil as ps
import re

if __name__=='sysmontask.filter_prefs':
    from sysmontask.sysmontask import files_dir
else:
    from sysmontask import files_dir

def on_filter_toggled(widget,path,self):
    # print(widget.get_active())
    self.filter_list_store[path][0]= not self.filter_list_store[path][0]

def on_filter_regex_toggled(widget,path,self):
    # print(widget.get_active())
    # print("regex",self.filter_list_store[path][3])
    self.filter_list_store[path][3]= not self.filter_list_store[path][3]

def on_activate_filter_entry(entry,self):
    print('filter entry')
    textt=entry.get_text()
    if not textt.isspace():
        textt=textt.strip()
        if textt[-1]==';':
            textt=textt[:-1]
        text=textt.split(';')
        print(text)

        for line in text:
            ent=''
            if line.count(',')==0:
                if ':' in line:
                    line,depth=line.split(':')
                    if not depth:
                        depth=-1
                    depth=int(depth)
                else:
                    line=line.split(':')[0]
                    depth=-1
                line=line.strip()
                for i,row in enumerate(self.filter_list_store):
                    if line==row[1]:
                        return
                    elif line in row[1] and depth<row[2]:
                        self.filter_list_store[i]=False
                self.filter_list_store.append([True,line,depth,False])
            elif line.count(',')==2:
                if ':' in line:
                    line,depth=line.split(':')
                    if not depth:
                        depth=-1
                    depth=int(depth)
                else:
                    line=line.split(':')[0]
                    depth=-1
                ttline=line.split(',')
                ttline[0]=ttline[0].strip()
                ttline[1]=ttline[1].strip()
                ttline[2]=ttline[2].strip()
                for row in self.filter_list_store:
                    matched=0
                    temp=row[1].split(',')
                    if len(temp)==1:
                        if temp[0] in line and depth<row[2]:
                            return
                        continue
                    if ttline[0]==temp[0]:
                        matched+=1
                    if ttline[1]==temp[1]:
                        matched+=1
                    if ttline[2]==temp[2]:
                        matched+=1
                    if matched==3:
                        return

                for i in ttline:
                    print(i)
                    ent+=i.strip()+','
                self.filter_list_store.append([True,ent[:-1],depth,False])
                # self.filter_list_store_iter[ent[:-1]]=iter
    entry.delete_text(0,-1)

def on_filter_add_button_activate(button,self):
    print('sdf')
    on_activate_filter_entry(self.filter_entry,self)

def filter_row_selected(selection,self):
    # print(selection.get_tree_iter())
    # try:
    # model,row=selection.get_selected()
    _,row=selection.get_selected()
    # print('hell')
    # print(model,row)
    self.selected_filter_row=row
    # selected_=model[model.get_path(row)]
    # self.=model[model.get_path(row)]
    # print("sdfsd",selected)
    # model.remove(row)
    # except:
    #     print('error in row selections')

def on_filter_delete_button_activate(button,self):
    print('delete button')
    if self.filter_list_store[self.filter_list_store.get_path(self.selected_filter_row)][1]!=',root,':
        self.filter_list_store.remove(self.selected_filter_row)

def put_in_black_list(self,proc,depth):
    childlist=proc.children()
    if depth==0:
        return
    for child in childlist:
        put_in_black_list(self,child,depth-1)
    # if proc.pid not in self.temp_black_list:
    self.temp_black_list.append(proc.pid)

def put_process_in_black_list(self,proc,depth):
    childlist=proc.children()
    if depth==0:
        return
    for child in childlist:
        put_in_black_list(self,child,depth-1)
    # if proc.pid not in self.temp_black_list:
    self.black_list.add(proc.pid)

def filter_process_matching_func(self,proc):
    self.temp_black_list=[]
    try:
        if proc.pid not in self.temp_black_list:
            for row in self.filter_list_store:
                cnt=row[1].count(',')
                if not row[0]:
                    continue
                if cnt==0:
                    if not row[3]:
                        if (row[1] in proc.name()) or (row[1] in proc.username()) or (row[1] in " ".join(proc.cmdline())):
                            put_process_in_black_list(self,proc,row[2])
                    else:
                        if re.search(row[1],proc.name()) or re.search(row[1],proc.username()) or re.search(row[1]," ".join(proc.cmdline())):
                            put_process_in_black_list(self,proc,row[2])
                elif cnt==2:
                    if not row[3]:
                        temp=row[1].split(',')
                        need_match=0
                        match=0
                        for i,txt in enumerate(temp):
                            if txt:
                                need_match+=1
                                if i==0:
                                    if txt in proc.name():
                                        match+=1

                                elif i==1:
                                    if txt in proc.username():
                                        match+=1

                                elif i==2:
                                    if txt in " ".join(proc.cmdline()):
                                        match+=1

                        if need_match==match:
                            put_process_in_black_list(self,proc,row[2])

                    else:
                        temp=row[1].split(',')
                        need_match=0
                        match=0
                        for i,txt in enumerate(temp):
                            if txt:
                                need_match+=1
                                if i==0:
                                    if re.search(txt,proc.name()):
                                        match+=1

                                elif i==1:
                                    if re.search(txt,proc.username()):
                                        match+=1

                                elif i==2:
                                    if re.search(txt," ".join(proc.cmdline())):
                                        match+=1

                        if need_match==match:
                            put_process_in_black_list(self,proc,row[2])
    except ps.NoSuchProcess:
        print("process error in filter matching func")

def filter_list_sorting_func(model, row1, row2,self):
    sort_column, _ = model.get_sort_column_id()
    val1 = model.get_value(row1, sort_column)
    val2 = model.get_value(row2, sort_column)
    if val1==-1:
        val1=1000
    if val2==-1:
        val2=1000

    if val1<val2:
        return 1
    elif val1==val2:
        return 0
    else:
        return -1

def filter_matching_func(self):
    for proc in ps.Process(1).children(True):
        try:
            if proc.pid not in self.temp_black_list:
                for row in self.filter_list_store:
                    cnt=row[1].count(',')
                    if not row[0]:
                        continue
                    if cnt==0:
                        if not row[3]:
                            if (row[1] in proc.name()) or (row[1] in proc.username()) or (row[1] in " ".join(proc.cmdline())):
                                put_in_black_list(self,proc,row[2])
                        else:
                            if re.search(row[1],proc.name()) or re.search(row[1],proc.username()) or re.search(row[1]," ".join(proc.cmdline())):
                                put_in_black_list(self,proc,row[2])
                    elif cnt==2:
                        if not row[3]:
                            temp=row[1].split(',')
                            need_match=0
                            match=0
                            for i,txt in enumerate(temp):
                                if txt:
                                    need_match+=1
                                    if i==0:
                                        if txt in proc.name():
                                            match+=1

                                    elif i==1:
                                        if txt in proc.username():
                                            match+=1

                                    elif i==2:
                                        if txt in " ".join(proc.cmdline()):
                                            match+=1

                            if need_match==match:
                                put_in_black_list(self,proc,row[2])

                        else:
                            temp=row[1].split(',')
                            need_match=0
                            match=0
                            for i,txt in enumerate(temp):
                                if txt:
                                    need_match+=1
                                    if i==0:
                                        if re.search(txt,proc.name()):
                                            match+=1

                                    elif i==1:
                                        if re.search(txt,proc.username()):
                                            match+=1

                                    elif i==2:
                                        if re.search(txt," ".join(proc.cmdline())):
                                            match+=1

                            if need_match==match:
                                put_in_black_list(self,proc,row[2])
        except ps.NoSuchProcess:
            print("process error in filter matching func")

def on_filter_save_button_activate(button,self):
    print('save button')
    self.temp_black_list=[]

    filter_matching_func(self)

    self.black_list=set(self.temp_black_list.copy())
    l=[]
    for i,row in enumerate(self.filter_list_store):
        l.append([])
        l[i]+=[str(row[0]),row[1],str(row[2]),str(row[3])]
    self.settings.set_value('process-filter',go.Variant('aas',l))

    self.append_signal=3
    # print(self.black_list)
    # self.filter_dialog.hide()
    # self.filter_dialog.close()

def filter_init(self):
    self.filter_builder=g.Builder()
    self.filter_builder.add_from_file(files_dir+'/filter_dialog.glade')
    self.filter_dialog=self.filter_builder.get_object('filter_dialog')
    # self.filter_dialog.set_transient_for(self.Window)

    self.filter_entry=self.filter_builder.get_object("filter_entry")
    self.filter_entry.connect('activate',on_activate_filter_entry,self)

    self.filter_add_button=self.filter_builder.get_object("filter_add_button")
    self.filter_add_button.connect('clicked',on_filter_add_button_activate,self)

    self.filter_delete_button=self.filter_builder.get_object("filter_delete_button")
    self.filter_delete_button.connect('clicked',on_filter_delete_button_activate,self)

    self.filter_save_button=self.filter_builder.get_object("filter_save_button")
    self.filter_save_button.connect('clicked',on_filter_save_button_activate,self)

    self.filter_tree_view=self.filter_builder.get_object("filter_tree_view")

    # list store
    self.filter_list_store=g.ListStore(bool,str,int,bool)
    self.black_list=[]
    self.temp_black_list=[]
    self.append_signal=0

    # self.filter_list_store.append([False,'zqzqzqzq',0,False])
    self.saved_filter=[]
    for row in self.settings.get_value('process-filter'):
        temp=[bool(row[0]=="True"),row[1],int(row[2]),bool(row[3]=="True")]
        self.saved_filter.append(temp)
        self.filter_list_store.append(temp)

    self.filter_list_store_iter={}

    self.filter_tree_view.set_model(self.filter_list_store)

    self.filter_list_store.set_sort_column_id(2,g.SortType.ASCENDING)
    self.filter_list_store.set_sort_func(2,filter_list_sorting_func,self)

    for i,col in enumerate(['Status','Filter String','Depth','Regex']):

        if i==3 or i==0:
            toggle_renderer=g.CellRendererToggle()
            if i==0:
                toggle_renderer.connect ("toggled", on_filter_toggled,self)
            elif i==3:
                toggle_renderer.connect ("toggled", on_filter_regex_toggled,self)

            column=g.TreeViewColumn(col)
            column.pack_start(toggle_renderer,False)
            column.add_attribute(toggle_renderer,'active',i)
        else:
            renderer=g.CellRendererText()
            column=g.TreeViewColumn(col,renderer,text=i)

        column.set_resizable(True)
        # if i==2:
            # column.set_sort_column_id(i)


        # column.set_alignment(0)

        self.filter_tree_view.append_column(column)

    filter_selected_row=self.filter_tree_view.get_selection()
    filter_selected_row.connect("changed",filter_row_selected,self)
    # filter_matching_func(self,2)
    on_filter_save_button_activate(self.filter_save_button,self)

