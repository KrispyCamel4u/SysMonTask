#!/usr/bin/env python3
############ container missing error in some distro #############
from gi import require_version
require_version("Gtk", "3.0")
require_version("Wnck", "3.0")
###############################################################
try:
    from rooter import theme_agent
except ImportError:
    from sysmontask.rooter import theme_agent

theme_agent()
import os

with open("{}/.sysmontask".format(os.environ.get("HOME")),'w+') as ofile:
    ofile.write('0')

from gi.repository import Gtk as g , GLib as go,Gio
import psutil as ps

print(ps.__version__)
if( not ps.__version__>='5.7.2'):
    print('warning[critical]: psutil>=5.7.2 needed(system-wide)')

try:
    # for running as main file 
    files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../glade_files")
    icon_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../icons")
    from cpu import *
    from mem import *
    from sidepane import *
    from disk import *
    from net import *
    from gpu import *
    from filter_prefs import *
    from gproc import *
    # from log_plotter import *
    
except:
    # for module level through  apt install comment it if running as main file
    files_dir="/usr/share/sysmontask/glade_files"
    icon_file='/usr/share/sysmontask/icons'
    from sysmontask.cpu import *
    from sysmontask.mem import *
    from sysmontask.sidepane import *
    from sysmontask.disk import *
    from sysmontask.net import *
    from sysmontask.gpu import *
    from sysmontask.filter_prefs import *
    from sysmontask.gproc import *
    # from sysmontask.log_plotter import *

class whatsnew_notice_dialog(g.Dialog):
    """ Class for What's New Dialog"""
    def __init__(self,parentWindow,parent):
        """Initialize the Dialog"""
        g.Dialog.__init__(self,"What's New",parentWindow,g.DialogFlags.MODAL)
        self.set_border_width(20)
        content_area=self.get_content_area()
        label=g.Label()
        label.set_markup(
        """
        <b><span size='20000'>New Feature #v1.3.9 </span></b>
          * <b><big>Filter Dialog</big></b>
              Can be accessed through : view->filter
              User can define his/her own filtering words to exclude the unwanted processes.
              Filter Dialog follow <b><big>strict semantic and formating rules</big></b> for adding a new entry.
              For more information of rules and filter dialog, visit: 
              <big><a href='https://github.com/KrispyCamel4u/SysMonTask/blob/master/DOCS.md#filter-dialog-view-filter'>https://github.com/KrispyCamel4u/SysMonTask/blob/master/DOCS.md</a></big>
          * <b><big>Process Log Record</big></b>(at lower right corner in process tab)
          * <b><big>Log plotter</big></b>(Tools->Log_plot)
          * Bug fixes, optimisation and support for all desktop enviornments.
        """ 
        )
        content_area.add(label)
        self.show_all()

class myclass:
    flag=0      #flag for the updator
    resizerflag=0
    def __init__(self):
        import time
        stt=time.time()
        self.settings=Gio.Settings.new('com.github.camelneeraj.sysmontask')
        
        myclass.cpuInit=cpuInit
        myclass.cpuUpdate=cpuUpdate

        myclass.memoryinitalisation=memorytabinit
        myclass.memoryTab=memoryTabUpdate

        myclass.sidepaneinitialisation=sidepaneinit
        myclass.sidepaneUpdate=sidePaneUpdate

        myclass.diskinitialisation=diskinit
        myclass.disktabUpdate=diskTabUpdate

        myclass.netinitialisation=netinit
        myclass.netTabUpdate=netUpdate

        myclass.gpuinitialisation=gpuinit
        myclass.gpuTabUpdate=gpuUpdate

        myclass.procinitialisation=procInit
        myclass.procUpdate=procUpdate
        myclass.row_selected=row_selected
        myclass.kill_process=kill_process
        myclass.column_button_press=column_button_press
        myclass.column_header_selection=column_header_selection

        myclass.filter_init=filter_init

        self.builder=g.Builder()
        self.builder.add_from_file(files_dir+"/sysmontask.glade")
        self.builder.connect_signals(self)
        self.Window=self.builder.get_object("main_window")
        self.quit=self.builder.get_object("quit")
        self.quit.connect('activate',self.on_quit_activate)

        self.Window.set_icon_from_file(icon_file+'/SysMonTask.png')

        self.performanceStack=self.builder.get_object('performancestack')
        self.process_tab_box=self.builder.get_object('process_tab_box')

        self.sidepaneBox=self.builder.get_object('sidepanebox')

        self.stack_counter=2  # for sidepane clicking and naming of stack pages

        self.cpuInit()
        self.memoryinitalisation()
        self.diskinitialisation()
        self.netinitialisation()
        self.gpuinitialisation()
        self.filter_init()
        self.procinitialisation()

        # for about dialog 
        self.aboutdialog=self.builder.get_object("aboutdialog")
        # for notebook
        self.notebook=self.builder.get_object('notebook')
        self.notebook.set_current_page(self.settings.get_int('current-tab'))
        #self.on_notebook_switch_page(self.notebook,'',0)

        #drawing area for cpu
        self.cpuDrawArea=self.builder.get_object('cpudrawarea')
        self.cpuUtilArray=[0]*100   #cpu util array
        self.cpu_logical_cores=ps.cpu_count()
        self.cpu_logical_cores_util_arrays=[]

        temp=ps.cpu_percent(percpu=True)
        for i in range(self.cpu_logical_cores):
            self.cpu_logical_cores_util_arrays.append([0]*99)
            self.cpu_logical_cores_util_arrays[i].append(temp[i])

        self.logical_cpu_grid=self.builder.get_object('logical_grid_area')

        self.timeinterval=850     #time interval in mili

        # timer binding 
        self.timehandler=go.timeout_add(self.timeinterval,self.updater)
        self.Processtimehandler=go.timeout_add(2000,self.procUpdate)

        # update direction
        self.update_dir_right=self.builder.get_object('update_right')
        self.update_dir_left=self.builder.get_object('update_left')
        self.update_dir_left.connect('toggled',self.on_set_left_update)
        self.update_dir_right.connect('toggled',self.on_set_right_update)
        self.update_graph_direction=1  #newer on right by default
        self.update_dir_right.set_active(True)
        
        # update speed
        self.update_speed_low=self.builder.get_object('low')
        self.update_speed_normal=self.builder.get_object('normal')
        self.update_speed_high=self.builder.get_object('high')
        self.update_speed_paused=self.builder.get_object('paused')

        self.update_speed_low.connect('toggled',self.on_update_speed_change)
        self.update_speed_normal.connect('toggled',self.on_update_speed_change)
        self.update_speed_high.connect('toggled',self.on_update_speed_change)
        self.update_speed_paused.connect('toggled',self.on_update_speed_change)
        
        self.update_speed_normal.set_active(True)
        self.one_time=0

        ## filter dialog 
        self.filter_button=self.builder.get_object("filter_button")
        self.filter_button.connect("activate",self.on_filter_dialog_activate)

        self.current_stack='page0'
        self.sidepaneinitialisation()

        #time.sleep(2)p
        self.Window.show()
        print("total window",time.time()-stt)
        position=self.settings.get_value('window-position')
        self.Window.move(position[0],position[1])
        size=self.settings.get_value('window-size')
        self.Window.resize(size[0],size[1])

        self.log_plot=self.builder.get_object("log_plot")  # connect through glade on_log_plot_activate

        ## whatsnew dialog
        if self.settings.get_int("one-time-whatsnew"):
            dialog=whatsnew_notice_dialog(self.Window,self)
            dialog.run()
            dialog.destroy()
            self.settings.set_int("one-time-whatsnew",0)

    def on_log_plot_activate(self,widget):
        file_dialog=g.FileChooserDialog(title="Select Log File",parent=self.Window,action=g.FileChooserAction.OPEN,\
            buttons=("Cancel", g.ResponseType.CANCEL,"Open", g.ResponseType.OK))
        file_dialog.set_current_folder(os.path.join(os.environ.get("HOME"),"sysmontask_log"))

        response=file_dialog.run()
        if response==g.ResponseType.OK:
            filename=file_dialog.get_filename()
            print("file choosen",filename)
            file_dialog.destroy()
            os.system(f"python3 {os.path.join(os.path.abspath(os.path.dirname(__file__)),'log_plotter.py')} {filename} &")
            # plot_log(filename)
            
            # print("plot plot")
        else:
            print("didnt choose")
            file_dialog.destroy()
                 

    def on_menu_whatsnew(self,widget):
        dialog=whatsnew_notice_dialog(self.Window,self)
        response=dialog.run()
        dialog.destroy()

    def on_set_left_update(self,widget):
        if widget.get_active():
            self.update_dir_right.set_active(False)
            self.update_graph_direction=0  #0 means newer on left 1 means newer on right

            self.cpuUtilArray.reverse()
            for i in range(self.cpu_logical_cores):
                self.cpu_logical_cores_util_arrays[i].reverse()

            self.memUsedArray1.reverse()

            for i in range(self.numOfDisks):
                self.diskActiveArray[i].reverse()
                self.diskReadArray[i].reverse()
                self.diskWriteArray[i].reverse()

            for i in range(self.numOfNets):
                self.netSendArray[i].reverse()
                self.netReceiveArray[i].reverse()

            self.gpuUtilArray.reverse()
            self.gpuVramArray.reverse()
            self.gpuEncodingArray.reverse()
            self.gpuDecodingArray.reverse()

        print('update Dir left',widget.get_active())

    def on_set_right_update(self,widget):
        if widget.get_active():
            self.update_dir_left.set_active(False)
            self.update_graph_direction=1  #0 means newer on left 1 means newer on right

            self.cpuUtilArray.reverse()
            for i in range(self.cpu_logical_cores):
                self.cpu_logical_cores_util_arrays[i].reverse()

            self.memUsedArray1.reverse()

            for i in range(self.numOfDisks):
                self.diskActiveArray[i].reverse()
                self.diskReadArray[i].reverse()
                self.diskWriteArray[i].reverse()

            for i in range(self.numOfNets):
                self.netSendArray[i].reverse()
                self.netReceiveArray[i].reverse()
            
            self.gpuUtilArray.reverse()
            self.gpuVramArray.reverse()
            self.gpuEncodingArray.reverse()
            self.gpuDecodingArray.reverse()
            
        print('update Dir right',widget.get_active())

    def on_main_window_destroy(self,widget,data=None):
        print("print with cancel")
        # print(self.Window.get_position())
        self.settings.set_value('window-position',go.Variant("(ii)",self.Window.get_position()))
        self.settings.set_value('window-size',go.Variant("(ii)",self.Window.get_size()))
        # print(object.get_position(),self.settings.get_value('window-size'))
        self.settings.set_int('current-tab',self.notebook.get_current_page())
        # print(self.settings.get_value('process-filter'))

        l=[]
        for i,row in enumerate(self.filter_list_store):
            l.append([])
            l[i]+=[str(row[0]),row[1],str(row[2]),str(row[3])]
        self.settings.set_value('process-filter',go.Variant('aas',l))

        if self.log_file:
            self.log_file.close()

        g.main_quit()

    def on_quit_activate(self,menuitem,data=None):
        print("quit from menu",g.Buildable.get_name(menuitem))
        self.on_main_window_destroy(menuitem)

    def on_refresh_activate(self,menuitem,data=None):
        print("refreshing")
        print(self.current_stack)
        self.stack_counter=2
        if(self.isNvidiagpu==1):
            g.Widget.destroy(self.gpuWidget)
            g.Widget.destroy(self.gpuSidePaneWidget)
        for i in range(0,self.numOfDisks):
            g.Widget.destroy(self.diskWidgetList[i])
            g.Widget.destroy(self.diskSidepaneWidgetList[i])
        for i in range(self.numOfNets):
            g.Widget.destroy(self.netWidgetList[i])
            g.Widget.destroy(self.netSidepaneWidgetList[i])
        g.Widget.destroy(self.processTree)
        self.processTreeStore.clear()
        
        # g.main_quit()
        self.procinitialisation()
        self.diskinitialisation()
        self.netinitialisation()
        self.gpuinitialisation()
        self.sidepaneinitialisation()
        print(self.current_stack)
        self.performanceStack.set_visible_child_name(self.current_stack)
    
    # method to show the about dialog
    def on_about_activate(self,menuitem,data=None):
        print("aboutdialog opening")
        # self.aboutdialog.set_icon_from_file('/usr/share/sysmontask/icons/SysMonTask.png')
        self.response=self.aboutdialog.run()
        self.aboutdialog.hide()
        print("aboutdialog closed")
    
    def on_filter_dialog_activate(self,dialog,data=None):
        self.filter_dialog.run()
        # self.filter_dialog.show()
        self.filter_entry.delete_text(0,-1)
        print("hiding")
        self.filter_dialog.hide()

    def resizer(self,item,data=None):
        if(myclass.resizerflag==0):
            print('hello')
            self.Window.set_size_request(-1,-1)
            myclass.resizerflag+=1


    def on_update_speed_change(self,widget):
        if widget.get_active():
            update_speed=g.Buildable.get_name(widget)
            if(update_speed=='low'):
                print("update speed to low")
                go.source_remove(self.timehandler)
                self.timehandler=go.timeout_add(1400,self.updater)
                go.source_remove(self.Processtimehandler)
                self.Processtimehandler=go.timeout_add(2000,self.procUpdate)
                self.update_speed_normal.set_active(False)
                self.update_speed_high.set_active(False)
                self.update_speed_paused.set_active(False)

            elif(update_speed=='normal'):
                print("update speed to normal")
                go.source_remove(self.timehandler)
                self.timehandler=go.timeout_add(850,self.updater)
                go.source_remove(self.Processtimehandler)
                self.Processtimehandler=go.timeout_add(2000,self.procUpdate)
                self.update_speed_low.set_active(False)
                self.update_speed_high.set_active(False)
                self.update_speed_paused.set_active(False)

            elif(update_speed=='high'):
                print("update speed to high")
                go.source_remove(self.timehandler)
                self.timehandler=go.timeout_add(500,self.updater)
                go.source_remove(self.Processtimehandler)
                self.Processtimehandler=go.timeout_add(2000,self.procUpdate)
                self.update_speed_normal.set_active(False)
                self.update_speed_low.set_active(False)
                self.update_speed_paused.set_active(False)

            elif(update_speed=='paused'):
                print("update speed to paused")
                go.source_remove(self.timehandler)
                go.source_remove(self.Processtimehandler)
                # self.timehandler=go.timeout_add(1000000000,self.updater)
                self.Processtimehandler=go.timeout_add(100000000,self.procUpdate)
                self.update_speed_normal.set_active(False)
                self.update_speed_high.set_active(False)
                self.update_speed_low.set_active(False)

    # method for notebook switcher
    #def on_notebook_switch_page(self,notebook,page,page_num,data=None):

    # button click method
    # def on_button_clicked(self,widget):
    #     print(widget.get_property('label'),"clicked")

    ## repeatedily called out fucntion
    def updater(self):
        
        ## updating 
        self.cpuUpdate()
        self.memoryTab()
        self.disktabUpdate()
        if len(self.netNameList)!=0:
            self.netTabUpdate() 
        if(self.isNvidiagpu==1):
            self.gpuTabUpdate()
        self.sidepaneUpdate()
        
        ## drawing queue
        g.Widget.queue_draw(self.cpuDrawArea)

        for i in range(self.cpu_logical_cores):
            g.Widget.queue_draw(self.cpu_logical_cores_draw_areas[i])

        g.Widget.queue_draw(self.memDrawArea1)
        g.Widget.queue_draw(self.memDrawArea2)
        for i in range(0,self.numOfDisks):
            g.Widget.queue_draw(self.diskWidgetList[i].diskdrawarea1)
            g.Widget.queue_draw(self.diskWidgetList[i].diskdrawarea2)

        for i in range(0,self.numOfNets):
            g.Widget.queue_draw(self.netWidgetList[i].netdrawarea)

        if(self.isNvidiagpu==1):
            g.Widget.queue_draw(self.gpuWidget.gpuutildrawarea)
            g.Widget.queue_draw(self.gpuWidget.gpuvramdrawarea)
            g.Widget.queue_draw(self.gpuWidget.gpuencodingdrawarea)
            g.Widget.queue_draw(self.gpuWidget.gpudecodingdrawarea)


        ##  sidepane  
        g.Widget.queue_draw(self.cpuSidePaneDrawArea)
        g.Widget.queue_draw(self.memSidePaneDrawArea)
        for i in range(0,self.numOfDisks):
            g.Widget.queue_draw(self.diskSidepaneWidgetList[i].disksidepanedrawarea)
        for i in range(self.numOfNets):
            g.Widget.queue_draw(self.netSidepaneWidgetList[i].netsidepanedrawarea)
        if(self.isNvidiagpu==1):
            g.Widget.queue_draw(self.gpuSidePaneWidget.gpusidepanedrawarea)


        return True

    def on_cpu_logical_drawing(self,draw_area_widget,cr):
        cr.set_line_width(2)
        logical_cpu_id=int(draw_area_widget.get_name())
        cpu_logical_util_array=self.cpu_logical_cores_util_arrays[logical_cpu_id]
        w=draw_area_widget.get_allocated_width()
        h=draw_area_widget.get_allocated_height()
        
        scalingfactor=h/100.0
        #creating outer rectangle
        cr.set_source_rgba(0,.454,.878,1)
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.stroke()
        # creating grid lines
        verticalGap=int(h/10)
        horzontalGap=int(w/10)
        for i in range(1,10):
            cr.set_source_rgba(.384,.749,1.0,1) #for changing the outer line color
            cr.set_line_width(0.5)
            cr.move_to(0,i*verticalGap)
            cr.line_to(w,i*verticalGap)

            cr.move_to(i*horzontalGap,0)
            cr.line_to(i*horzontalGap,h)
            cr.stroke()
        cr.stroke()
        
        stepsize=w/99.0

        # for i in range(0,99):
        #     # not effcient way to fill the bars (drawing)
        #     cr.set_source_rgba(.588,.823,.98,0.25)   #for changing the fill color
        #     cr.move_to(i*stepsize,scalingfactor*(100-cpu_logical_util_array[i]))
        #     cr.line_to((i+1)*stepsize,scalingfactor*(100-cpu_logical_util_array[i+1]))
        #     cr.line_to((i+1)*stepsize,h)
        #     cr.line_to(i*stepsize,h)
        #     cr.move_to(i*stepsize,scalingfactor*(100-cpu_logical_util_array[i]))

        #     cr.fill()
        #     cr.stroke()
        #     # for outer line
        #     cr.set_line_width(1.5)
        #     cr.set_source_rgba(.384,.749,1.0,1) #for changing the outer line color
        #     cr.move_to(i*stepsize,scalingfactor*(100-cpu_logical_util_array[i]))
        #     cr.line_to((i+1)*stepsize,scalingfactor*(100-cpu_logical_util_array[i+1]))
        #     cr.stroke()

        # cr.set_source_rgba(.588,.823,.98,0.25)   #for changing the fill color
        cr.set_source_rgba(.384,.749,1.0,1)
        cr.move_to(0,scalingfactor*(100-cpu_logical_util_array[0]))
        for i in range(0,99):
            cr.set_line_width(1.5)
            cr.line_to((i+1)*stepsize,scalingfactor*(100-cpu_logical_util_array[i+1]))
        cr.stroke_preserve()
        cr.set_source_rgba(.588,.823,.98,0.25)
        cr.line_to(w,h)
        cr.line_to(0,h)
        cr.move_to(0,scalingfactor*(100-cpu_logical_util_array[0]))
        cr.fill()
        cr.stroke()

        return False

    def on_memDrawArea1_draw(self,dr,cr):
        #print("memdraw1")
        cr.set_line_width(2)

        w=self.memDrawArea1.get_allocated_width()
        h=self.memDrawArea1.get_allocated_height()
        scalingfactor=h/self.memTotal
        #creating outer rectangle
        cr.set_source_rgba(.380,.102,.509,1)  ##need tochange the color
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.stroke()
        # creating grid lines
        verticalGap=int(h/10)
        horzontalGap=int(w/10)
        for i in range(1,10):
            cr.set_source_rgba(.815,.419,1.0,1) #for changing the outer line color
            cr.set_line_width(0.5)
            cr.move_to(0,i*verticalGap)
            cr.line_to(w,i*verticalGap)

            cr.move_to(i*horzontalGap,0)
            cr.line_to(i*horzontalGap,h)
        cr.stroke()
        
        stepsize=w/99.0
        #print("in draw stepsize",stepsize)
        # for i in range(0,99):
        #     # not effcient way to fill the bars (drawing)
        #     cr.set_source_rgba(.815,.419,1.0,0.2)   #for changing the fill color
        #     cr.move_to(i*stepsize,scalingfactor*(self.memTotal-self.memUsedArray1[i]))
        #     cr.line_to((i+1)*stepsize,scalingfactor*(self.memTotal-self.memUsedArray1[i+1]))
        #     cr.line_to((i+1)*stepsize,h)
        #     cr.line_to(i*stepsize,h)
        #     cr.move_to(i*stepsize,scalingfactor*(self.memTotal-self.memUsedArray1[i]))

        #     cr.fill()
        #     cr.stroke()
        #     # for outer line
        #     cr.set_line_width(1.5)
        #     cr.set_source_rgba(.627,.196,.788,1) #for changing the outer line color
        #     cr.move_to(i*stepsize,scalingfactor*(self.memTotal-self.memUsedArray1[i]))
        #     cr.line_to((i+1)*stepsize,scalingfactor*(self.memTotal-self.memUsedArray1[i+1]))
        #     cr.stroke()

        # efficient way to fill
        cr.set_source_rgba(.627,.196,.788,1) #for changing the outer line color
        cr.set_line_width(1.5)
        cr.move_to(0,scalingfactor*(self.memTotal-self.memUsedArray1[0]))
        for i in range(0,99):
            cr.line_to((i+1)*stepsize,scalingfactor*(self.memTotal-self.memUsedArray1[i+1]))
        cr.stroke_preserve()

        cr.set_source_rgba(.815,.419,1.0,0.2)   #for changing the fill color
        cr.line_to(w,h)
        cr.line_to(0,h)
        cr.move_to(0,scalingfactor*(self.memTotal-self.memUsedArray1[0]))
        cr.fill()
        cr.stroke()


        return False

    def on_memDrawArea2_draw(self,dr,cr):
        #print("memdraw2")
        cr.set_line_width(2)

        w=self.memDrawArea2.get_allocated_width()
        h=self.memDrawArea2.get_allocated_height()
        scalingfactor=int(w/self.memTotal)

        #print("in draw stepsize",stepsize)
        cr.set_source_rgba(.815,.419,1.0,0.25)   #for changing the fill color
        cr.set_line_width(2)
        cr.rectangle(0,0,scalingfactor*self.usedd,h)
        cr.fill()
        cr.stroke()
        cr.set_source_rgba(.815,.419,1.0,1)
        cr.set_line_width(2)
        cr.move_to(scalingfactor*self.usedd,0)
        cr.line_to(scalingfactor*self.usedd,h)
        cr.stroke()

        cr.set_source_rgba(.815,.419,1.0,0.1)   #for changing the fill color
        cr.set_line_width(2)
        cr.rectangle(scalingfactor*(self.usedd),0,scalingfactor*(self.memAvailable-self.memFree),h)
        cr.fill()
        cr.stroke()
        cr.set_source_rgba(.815,.419,1.0,.7)   #for changing the fill color
        cr.set_line_width(2)
        cr.move_to(scalingfactor*(self.usedd+self.memAvailable-self.memFree),0)
        cr.line_to(scalingfactor*(self.usedd+self.memAvailable-self.memFree),h)
        cr.stroke()

        cr.set_source_rgba(.815,.419,1.0,0.2)   #for changing the fill color
        cr.set_line_width(2)
        cr.rectangle(scalingfactor*(self.usedd+self.memAvailable-self.memFree),0,scalingfactor*self.memFree,h)
        cr.stroke()

        #creating outer rectangle
        cr.set_source_rgba(.380,.102,.509,1)  ##need tochange the color
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.stroke()
        

        return False
    
    ## method for drawing
    def on_cpuDrawArea_draw(self,dr,cr):
        #print("idsaf")
        cr.set_line_width(2)

        w=self.cpuDrawArea.get_allocated_width()
        h=self.cpuDrawArea.get_allocated_height()
        scalingfactor=h/100.0
        #creating outer rectangle
        cr.set_source_rgba(0,.454,.878,1)
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.stroke()
        # creating grid lines
        verticalGap=int(h/10)
        horzontalGap=int(w/10)
        for i in range(1,10):
            cr.set_source_rgba(.384,.749,1.0,1) #for changing the outer line color
            cr.set_line_width(0.5)
            cr.move_to(0,i*verticalGap)
            cr.line_to(w,i*verticalGap)

            cr.move_to(i*horzontalGap,0)
            cr.line_to(i*horzontalGap,h)
        cr.stroke()
        
        stepsize=w/99.0

        # for i in range(0,99):
        #     # not effcient way to fill the bars (drawing)
        #     cr.set_source_rgba(.588,.823,.98,0.25)   #for changing the fill color
        #     cr.move_to(i*stepsize,scalingfactor*(100-self.cpuUtilArray[i]))
        #     cr.line_to((i+1)*stepsize,scalingfactor*(100-self.cpuUtilArray[i+1]))
        #     cr.line_to((i+1)*stepsize,h)
        #     cr.line_to(i*stepsize,h)
        #     cr.move_to(i*stepsize,scalingfactor*(100-self.cpuUtilArray[i]))

        #     cr.fill()
        #     cr.stroke()
        #     # for outer line
        #     cr.set_line_width(1.5)
        #     cr.set_source_rgba(.384,.749,1.0,1) #for changing the outer line color
        #     cr.move_to(i*stepsize,scalingfactor*(100-self.cpuUtilArray[i]))
        #     cr.line_to((i+1)*stepsize,scalingfactor*(100-self.cpuUtilArray[i+1]))
        #     cr.stroke()

        cr.set_source_rgba(.384,.749,1.0,1) #for changing the outer line color
        cr.set_line_width(1.5)
        cr.move_to(0,scalingfactor*(100-self.cpuUtilArray[0]))
        for i in range(0,99):
            cr.line_to((i+1)*stepsize,scalingfactor*(100-self.cpuUtilArray[i+1]))
        cr.stroke_preserve()

        cr.set_source_rgba(.588,.823,.98,0.25)   #for changing the fill color
        cr.line_to(w,h)
        cr.line_to(0,h)
        cr.move_to(0,scalingfactor*(100-self.cpuUtilArray[0]))
        cr.fill()
        cr.stroke()
        
        return False
        
        #side pane cpu draw
    
    def on_cpuSidePaneDrawArea_draw(self,dr,cr):
        #print("cpu sidepane draw")
        cr.set_line_width(2)

        w=self.cpuSidePaneDrawArea.get_allocated_width()
        h=self.cpuSidePaneDrawArea.get_allocated_height()
        scalingfactor=h/100.0
        #creating outer rectangle
        cr.set_source_rgba(0,.454,.878,1)
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.stroke()
        
        
        stepsize=w/99.0
        #print("in draw stepsize",stepsize)
        # for i in range(0,99):
        #     # not effcient way to fill the bars (drawing)
        #     cr.set_source_rgba(.588,.823,.98,0.25)   #for changing the fill color
        #     cr.move_to(i*stepsize,scalingfactor*(100-self.cpuUtilArray[i]))
        #     cr.line_to((i+1)*stepsize,scalingfactor*(100-self.cpuUtilArray[i+1]))
        #     cr.line_to((i+1)*stepsize,h)
        #     cr.line_to(i*stepsize,h)
        #     cr.move_to(i*stepsize,scalingfactor*(100-self.cpuUtilArray[i]))

        #     cr.fill()
        #     cr.stroke()
        #     # for outer line
        #     cr.set_line_width(1.5)
        #     cr.set_source_rgba(.384,.749,1.0,1) #for changing the outer line color
        #     cr.move_to(i*stepsize,scalingfactor*(100-self.cpuUtilArray[i]))
        #     cr.line_to((i+1)*stepsize,scalingfactor*(100-self.cpuUtilArray[i+1]))
        #     cr.stroke()

        # efficient way to fill
        cr.set_line_width(1.5)
        cr.set_source_rgba(.384,.749,1.0,1) #for changing the outer line color
        cr.move_to(0,scalingfactor*(100-self.cpuUtilArray[0]))
        for i in range(0,99):
            cr.line_to((i+1)*stepsize,scalingfactor*(100-self.cpuUtilArray[i+1]))
        cr.stroke_preserve()

        cr.set_source_rgba(.588,.823,.98,0.25)   #for changing the fill color
        cr.line_to(w,h)
        cr.line_to(0,h)
        cr.move_to(0,scalingfactor*(100-self.cpuUtilArray[0]))
        cr.fill()
        cr.stroke()

        return False

    def on_memSidePaneDrawArea_draw(self,dr,cr):
        #print("tyoe",g.Buildable.get_name(dr))
        cr.set_line_width(2)

        w=self.memSidePaneDrawArea.get_allocated_width()
        h=self.memSidePaneDrawArea.get_allocated_height()
        scalingfactor=h/self.memTotal
        #creating outer rectangle
        cr.set_source_rgba(.380,.102,.509,1)  ##need tochange the color
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.stroke()
        
        stepsize=w/99.0
        #print("in draw stepsize",stepsize)
        # for i in range(0,99):
        #     # not effcient way to fill the bars (drawing)
        #     cr.set_source_rgba(.815,.419,1.0,0.2)   #for changing the fill color
        #     cr.move_to(i*stepsize,scalingfactor*(self.memTotal-self.memUsedArray1[i]))
        #     cr.line_to((i+1)*stepsize,scalingfactor*(self.memTotal-self.memUsedArray1[i+1]))
        #     cr.line_to((i+1)*stepsize,h)
        #     cr.line_to(i*stepsize,h)
        #     cr.move_to(i*stepsize,scalingfactor*(self.memTotal-self.memUsedArray1[i]))

        #     cr.fill()
        #     cr.stroke()
        #     # for outer line
        #     cr.set_line_width(1.5)
        #     cr.set_source_rgba(.627,.196,.788,1) #for changing the outer line color
        #     cr.move_to(i*stepsize,scalingfactor*(self.memTotal-self.memUsedArray1[i]))
        #     cr.line_to((i+1)*stepsize,scalingfactor*(self.memTotal-self.memUsedArray1[i+1]))
        #     cr.stroke()

        # efficient way to fill
        cr.set_source_rgba(.627,.196,.788,1) #for changing the outer line color
        cr.set_line_width(1.5)
        cr.move_to(0,scalingfactor*(self.memTotal-self.memUsedArray1[0]))
        for i in range(0,99):
            cr.line_to((i+1)*stepsize,scalingfactor*(self.memTotal-self.memUsedArray1[i+1]))
        cr.stroke_preserve()

        cr.set_source_rgba(.815,.419,1.0,0.2)   #for changing the fill color
        cr.line_to(w,h)
        cr.line_to(0,h)
        cr.move_to(0,scalingfactor*(self.memTotal-self.memUsedArray1[0]))
        cr.fill()
        cr.stroke()

        return False



def start():
    main=myclass()
    g.main()

# import cProfile
    
if __name__=="__main__":
    # cProfile.run("start()")
    start()

# def uninstall():
#     os.system('sudo {0}/uninstall_for_pip.sh'.format(os.path.dirname(os.path.abspath(__file__))))
