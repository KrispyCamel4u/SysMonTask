#!/usr/bin/env python3
############ container missing error in some distro #############
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Wnck", "3.0")
###############################################################
try:
    from rooter import *
except:
    from sysmontask.rooter import *
getPrivilege()
with open("{}/.sysmontask".format(os.environ.get("HOME")),'w') as ofile:
    ofile.write('0')

from gi.repository import Gtk as g , GLib as go
import cairo
from os import popen
from re import sub
import os
import psutil as ps

if( not ps.__version__>='5.7.3'):
    print('warning[critical]: psutil>=5.7.3 needed(system-wide)')


try:
    # for running as main file 
    files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../glade_files")
    icon_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../icons")
    from mem import *
    from sidepane import *
    from disk import *
    from net import *
    from gpu import *
    from proc import *
except:
    # for module level through  apt install comment it if running as main file
    files_dir="/usr/share/sysmontask/glade_files"
    icon_file='/usr/share/sysmontask/icons'
    from sysmontask.mem import *
    from sysmontask.sidepane import *
    from sysmontask.disk import *
    from sysmontask.net import *
    from sysmontask.gpu import *
    from sysmontask.proc import *

class myclass:
    flag=0      #flag for the updator 
    resizerflag=0
    def __init__(self):
        # self.passs=passs
        myclass.memoryinitalisation=memorytabinit
        myclass.memoryTab=memoryTabUpdate
        #myclass.memDrawFunc1=on_memDrawArea1_draw
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

        self.gladefile=files_dir+"/sysmontask.glade"
        self.builder=g.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)
        self.Window=self.builder.get_object("main_window")
        self.quit=self.builder.get_object("quit")
        self.quit.connect('activate',self.on_quit_activate)

        self.Window.set_icon_from_file(icon_file+'/SysMonTask.png')

        self.performanceStack=self.builder.get_object('performancestack')
        self.process_tab_box=self.builder.get_object('process_tab_box')

        self.sidepaneBox=self.builder.get_object('sidepanebox')
        self.memoryinitalisation()
        self.diskinitialisation()
        self.netinitialisation()
        self.gpuinitialisation()
        self.procinitialisation()

        # for about dialog 
        self.aboutdialog=self.builder.get_object("aboutdialog")
        # for notebook
        self.notebook=self.builder.get_object('notebook')
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

        ## cpu draw tab labels
        self.cpuInfoLabel=self.builder.get_object('cpuinfolabel')
        ## cpu utilisation label
        self.cpuUtilLabelValue=self.builder.get_object('cpuutilisation')
        # cpu speed
        self.cpuSpeedLabelValue=self.builder.get_object('cpuspeed')
        # processes
        self.cpuProcessesLabelValue=self.builder.get_object('cpuprocesses')
        self.cpuThreadsLabelValue=self.builder.get_object('cputhreads')
        
        ## other cpu info
        self.cpuCoreLabelValue=self.builder.get_object('cpucoreslablevalue')
        self.cpuLogicalLabelValue=self.builder.get_object('cpulogicallabelvalue')
        self.cpuVirtualisationLabelValue=self.builder.get_object('cpuvirtualisationlabelvalue')
        self.cpuL1LabelValue=self.builder.get_object('cpul1labelvalue')
        self.cpuL2LabelValue=self.builder.get_object('cpul2labelvalue')
        self.cpuL3LabelValue=self.builder.get_object('cpul3labelvalue')
        self.cpuTempLabelValue=self.builder.get_object('cputemplabelvalue')
        self.cpuFanSpeedLabelValue=self.builder.get_object('cpufanspeedlabelvalue')
        self.cpuMxSpeedLabelValue=self.builder.get_object('cpumxspeedlabelvalue')

        self.update_dir_right=self.builder.get_object('update_right')
        self.update_dir_left=self.builder.get_object('update_left')
        self.update_dir_left.connect('toggled',self.on_set_left_update)
        self.update_dir_right.connect('toggled',self.on_set_right_update)
        self.update_graph_direction=1  #newer on right by default
        self.update_dir_right.set_active(True)
        
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
        

        self.sidepaneinitialisation()

        #time.sleep(2)p
        self.Window.show()
    
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

    def on_main_window_destroy(self,object,data=None):
        print("print with cancel")
        g.main_quit()

    def on_quit_activate(self,menuitem,data=None):
        print("quit from menu",g.Buildable.get_name(menuitem))
        g.main_quit()

    def on_refresh_activate(self,menuitem,data=None):
        print("refreshing")
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
    
    # method to show the about dialog
    def on_about_activate(self,menuitem,data=None):
        print("aboutdialog opening")
        # self.aboutdialog.set_icon_from_file('/usr/share/sysmontask/icons/SysMonTask.png')
        self.response=self.aboutdialog.run()
        self.aboutdialog.hide()
        print("aboutdialog closed")
    
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
                self.update_speed_normal.set_active(False)
                self.update_speed_high.set_active(False)
                self.update_speed_paused.set_active(False)

            elif(update_speed=='normal'):
                print("update speed to normal")
                go.source_remove(self.timehandler)
                self.timehandler=go.timeout_add(850,self.updater)
                self.update_speed_low.set_active(False)
                self.update_speed_high.set_active(False)
                self.update_speed_paused.set_active(False)

            elif(update_speed=='high'):
                print("update speed to high")
                go.source_remove(self.timehandler)
                self.timehandler=go.timeout_add(500,self.updater)
                self.update_speed_normal.set_active(False)
                self.update_speed_low.set_active(False)
                self.update_speed_paused.set_active(False)

            elif(update_speed=='paused'):
                print("update speed to paused")
                go.source_remove(self.timehandler)
                self.timehandler=go.timeout_add(1000000000,self.updater)
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
        
        self.speed=ps.cpu_freq()

        if(not myclass.flag):
            myclass.flag=1
            #print("in if")
            try:
                ## for the first time only to get the name of the cpu
                p=popen('cat /proc/cpuinfo |grep -m1 "model name"')
                self.cpuname=p.read().split(':')[1].split('\n')[0]
                #print(self.cpuname)                                          # cpu name
                self.cpuInfoLabel.set_text(self.cpuname)
                self.cpuInfoLabel.set_valign(g.Align.CENTER)
                p.close()
            except:
                print("Failed to get model information")

            self.cpuCoreLabelValue.set_text(str(ps.cpu_count(logical=False)))
            self.cpuLogicalLabelValue.set_text(str(self.cpu_logical_cores))
            try:
                p=popen('lscpu|grep -i -E "(vt-x)|(amd-v)"')
                temp=p.read()
                if temp:
                    temptext="Enabled"
                else:
                    temptext="Disabled"
                self.cpuVirtualisationLabelValue.set_text(temptext)
                p.close()
            except:
                print("Failed to get Virtualisation information")

            try:
                p=popen('lscpu|grep -i -m1 "L1d cache"')
                self.cpuL1LabelValue.set_text(sub("[\s]","",p.read().split(':')[1]))
                p.close()
                
                p=popen('lscpu|grep -i -m1 "L2 cache"')
                self.cpuL2LabelValue.set_text(sub('[\s]','',p.read().split(':')[1]))
                p.close()

                p=popen('lscpu|grep -i "L3 cache"')
                self.cpuL3LabelValue.set_text(sub('[\s]','',p.read().split(':')[1]))
                p.close()
            except:
                print("Failed to get Cache information")

            self.cpuMxSpeedLabelValue.set_text('{:.2f}'.format(self.speed[2]/1000)+' GHz')
            self.num_of_column_per_row={
                1:1,
                2:2,
                3:3,
                4:2,
                5:3,
                6:3,
                7:4,
                8:4,
                9:3,
                10:5,
                11:4,
                12:4,
                13:5,
                14:5,
                15:5,
                16:4,
                17:5,
                18:5,
                19:5,
                20:5,
                21:6,
                22:6,
                23:6,
                24:6,
                25:7,
                26:7,
                27:7,
                28:7,
                29:8,
                30:8,
                31:8,
                32:8
            }

            ## logical
            self.cpu_logical_cores_draw_areas=[]
            row,column=0,0
            for cpu_index in range(self.cpu_logical_cores):
                draw_area=g.DrawingArea()
                draw_area.set_name(str(cpu_index))
                self.cpu_logical_cores_draw_areas.append(draw_area)
                # draw_area=g.Button(label="begin{0}".format(cpu_index))
                if column < self.num_of_column_per_row[self.cpu_logical_cores]:
                    self.logical_cpu_grid.attach(draw_area,column,row,1,1)
                    column+=1
                else:
                    column=0
                    row+=1
                    self.logical_cpu_grid.attach(draw_area,column,row,1,1)
                    column+=1
                draw_area.connect('draw',self.on_cpu_logical_drawing)

            self.logical_cpu_grid.show_all()

            # return True

        #print("setting speed")
        cpuSpeedstring="{:.2f}".format(self.speed[0]/1000)+' Ghz'
        self.cpuSpeedLabelValue.set_text(cpuSpeedstring)
        #print("speed setting done")

        self.cpuUtil=ps.cpu_percent() ## % of the time is is working
        #print(self.cpuUtil)
        
        #print("setting utilisation")
        cpuUtilString=str(int(self.cpuUtil))+'%'
        self.cpuUtilLabelValue.set_text(cpuUtilString)
        #print('setting utilisation done')

        #print("setting number of processes and threads")
        self.cpuProcessesLabelValue.set_text(str(len(ps.pids())))
        try:
            p=popen("ps axms|wc -l")
            self.cpuThreadsLabelValue.set_text(sub('[\s]','',p.read()))
            p.close()
        except:
            print("Failed to get Threads")
            pass
        
        try:
            #cpu package temp
            temperatures_list=ps.sensors_temperatures()
            if 'coretemp' in temperatures_list:
                self.cpuTempLabelValue.set_text(str(int(temperatures_list['coretemp'][0][1]))+' °C')
            elif 'k10temp' in temperatures_list:
                for lis in temperatures_list:
                    if lis.label=='Tdie':
                        self.cpuTempLabelValue.set_text(str(int(lis.current))+' °C')
                        break

            # cpu fan speed
        except:
            pass
        self.cpuSidePaneLabelValue.set_text(cpuUtilString+' '+cpuSpeedstring)

        

        ## updating 
        ## cpu utilisation graph
        if self.update_graph_direction:
            self.cpuUtilArray.pop(0)
            self.cpuUtilArray.append(self.cpuUtil)
        else:
            self.cpuUtilArray.pop()
            self.cpuUtilArray.insert(0,self.cpuUtil)

        temp=ps.cpu_percent(percpu=True)
        direction=self.update_graph_direction
        for i in range(self.cpu_logical_cores):
            if direction:
                self.cpu_logical_cores_util_arrays[i].pop(0)
                self.cpu_logical_cores_util_arrays[i].append(temp[i])
            else:
                self.cpu_logical_cores_util_arrays[i].pop()
                self.cpu_logical_cores_util_arrays[i].insert(0,temp[i])

        self.memoryTab()
        self.disktabUpdate()
        if len(self.netNameList)!=0:
            # print('dismis')
            self.netTabUpdate() 
        if(self.isNvidiagpu==1):
            self.gpuTabUpdate()

        self.sidepaneUpdate()

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

    
if __name__=="__main__":
    main=myclass()
    g.main()
