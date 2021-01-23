#!/usr/bin/env python3
#import gi
#gi.require_version("Gtk", "3.24")

from gi.repository import Gtk as g , GObject as go
import psutil as ps,cairo
import os,re

from mem import *
from sidepane import *
from disk import *
from net import *
from gpu import *

class myclass:
    flag=0      #flag for the updator 
    resizerflag=0
    def __init__(self,passs):
        self.passs=passs
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

        self.gladefile="taskManager.glade"
        self.builder=g.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)
        self.Window=self.builder.get_object("main_window")
        self.quit=self.builder.get_object("quit")
        self.quit.connect('activate',self.on_quit_activate)
        
        self.performanceStack=self.builder.get_object('performancestack')


        self.sidepaneBox=self.builder.get_object('sidepanebox')

        self.memoryinitalisation()
        self.diskinitialisation()
        self.netinitialisation()
        self.gpuinitialisation()


        # for about dialog 
        self.aboutdialog=self.builder.get_object("aboutdialog")
        # for notebook
        self.notebook=self.builder.get_object('notebook')
        #self.on_notebook_switch_page(self.notebook,'',0)

        #drawing area for cpu
        self.cpuDrawArea=self.builder.get_object('cpudrawarea')
        self.cpuUtilArray=[0]*100   #cpu util array

        
        self.timeinterval=850     #time interval in mili

        # timer binding 
        self.timehandler=go.timeout_add(self.timeinterval,self.updater)

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



        self.sidepaneinitialisation()

        #time.sleep(2)
        self.Window.show()

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
        
        # g.main_quit()
        # os.system('runuser -l root -c "python3 taskmanager.py" &')
        self.diskinitialisation()
        self.netinitialisation()
        self.gpuinitialisation()
        self.sidepaneinitialisation()
    
    # method to show the about dialog
    def on_about_activate(self,menuitem,data=None):
        print("aboutdialog opening")
        self.response=self.aboutdialog.run()
        self.aboutdialog.hide()
        print("aboutdialog closed")
    
    def resizer(self,item,data=None):
        if(myclass.resizerflag==0):
            print('hello')
            self.Window.set_size_request(-1,-1)
            myclass.resizerflag+=1

    def updatespeed_on_activate(self,menuitem,data=None):
        print("update speed")
        update_speed=g.Buildable.get_name(menuitem)
        if(update_speed=='low'):
            go.source_remove(self.timehandler)
            self.timehandler=go.timeout_add(1400,self.updater)
        elif(update_speed=='normal'):
            go.source_remove(self.timehandler)
            self.timehandler=go.timeout_add(850,self.updater)
        elif(update_speed=='high'):
            go.source_remove(self.timehandler)
            self.timehandler=go.timeout_add(500,self.updater)
        elif(update_speed=='paused'):
            go.source_remove(self.timehandler)
            self.timehandler=go.timeout_add(1000000000,self.updater)

    # method for notebook switcher
    #def on_notebook_switch_page(self,notebook,page,page_num,data=None):

    # button click method
    def on_button_clicked(self,widget):
        print(widget.get_property('label'),"clicked")

    ## repeatedily called out fucntion
    def updater(self):
        
        self.speed=ps.cpu_freq()

        if(not myclass.flag):
            myclass.flag=1
            #print("in if")
            try:
                ## for the first time only to get the name of the cpu
                p=os.popen('cat /proc/cpuinfo |grep -m1 "model name"')
                self.cpuname=p.read().split(':')[1].split('\n')[0]
                #print(self.cpuname)                                          # cpu name
                self.cpuInfoLabel.set_text(self.cpuname)
                self.cpuInfoLabel.set_valign(g.Align.CENTER)
                p.close()
            except:
                print("Failed to get model information")

            self.cpuCoreLabelValue.set_text(str(ps.cpu_count(logical=False)))

            self.cpuLogicalLabelValue.set_text(str(ps.cpu_count()))
            try:
                p=os.popen('lscpu|grep -i -E "(vt-x)|(amd-v)"')
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
                p=os.popen('lscpu|grep -i -m1 "L1d cache"')
                self.cpuL1LabelValue.set_text(re.sub("[\s]","",p.read().split(':')[1]))
                p.close()
                
                p=os.popen('lscpu|grep -i -m1 "L2 cache"')
                self.cpuL2LabelValue.set_text(re.sub('[\s]','',p.read().split(':')[1]))
                p.close()

                p=os.popen('lscpu|grep -i "L3 cache"')
                self.cpuL3LabelValue.set_text(re.sub('[\s]','',p.read().split(':')[1]))
                p.close()
            except:
                print("Failed to get Cache information")

            self.cpuMxSpeedLabelValue.set_text('{:.2f}'.format(self.speed[2]/1000)+' GHz')

            return True

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
            p=os.popen("ps axms|wc -l")
            self.cpuThreadsLabelValue.set_text(re.sub('[\s]','',p.read()))
            p.close()
        except:
            print("Failed to get Threads")
            pass
        
        try:
            #cpu package temp
            self.cpuTempLabelValue.set_text(str(int(ps.sensors_temperatures()['coretemp'][0][1])))
            # cpu fan speed
        except:
            pass
        self.cpuSidePaneLabelValue.set_text(cpuUtilString+' '+cpuSpeedstring)

        self.memoryTab()
        self.disktabUpdate()
        if len(self.netNameList)!=0:
            # print('dismis')
            self.netTabUpdate() 
        if(self.isNvidiagpu==1):
            self.gpuTabUpdate()

        self.sidepaneUpdate()

        ## cpu utilisation graph
        self.cpuUtilArray.pop()
        self.cpuUtilArray.insert(0,self.cpuUtil)
        g.Widget.queue_draw(self.cpuDrawArea)
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
        for i in range(0,99):
            # not effcient way to fill the bars (drawing)
            cr.set_source_rgba(.815,.419,1.0,0.2)   #for changing the fill color
            cr.move_to(i*stepsize,scalingfactor*(self.memTotal-self.memUsedArray1[i]))
            cr.line_to((i+1)*stepsize,scalingfactor*(self.memTotal-self.memUsedArray1[i+1]))
            cr.line_to((i+1)*stepsize,h)
            cr.line_to(i*stepsize,h)
            cr.move_to(i*stepsize,scalingfactor*(self.memTotal-self.memUsedArray1[i]))

            cr.fill()
            cr.stroke()
            # for outer line
            cr.set_line_width(1.5)
            cr.set_source_rgba(.627,.196,.788,1) #for changing the outer line color
            cr.move_to(i*stepsize,scalingfactor*(self.memTotal-self.memUsedArray1[i]))
            cr.line_to((i+1)*stepsize,scalingfactor*(self.memTotal-self.memUsedArray1[i+1]))
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
        cr.stroke()
        
        stepsize=w/99.0
        #print("in draw stepsize",stepsize)
        for i in range(0,99):
            # not effcient way to fill the bars (drawing)
            cr.set_source_rgba(.588,.823,.98,0.25)   #for changing the fill color
            cr.move_to(i*stepsize,scalingfactor*(100-self.cpuUtilArray[i]))
            cr.line_to((i+1)*stepsize,scalingfactor*(100-self.cpuUtilArray[i+1]))
            cr.line_to((i+1)*stepsize,h)
            cr.line_to(i*stepsize,h)
            cr.move_to(i*stepsize,scalingfactor*(100-self.cpuUtilArray[i]))

            cr.fill()
            cr.stroke()
            # for outer line
            cr.set_line_width(1.5)
            cr.set_source_rgba(.384,.749,1.0,1) #for changing the outer line color
            cr.move_to(i*stepsize,scalingfactor*(100-self.cpuUtilArray[i]))
            cr.line_to((i+1)*stepsize,scalingfactor*(100-self.cpuUtilArray[i+1]))
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
        for i in range(0,99):
            # not effcient way to fill the bars (drawing)
            cr.set_source_rgba(.588,.823,.98,0.25)   #for changing the fill color
            cr.move_to(i*stepsize,scalingfactor*(100-self.cpuUtilArray[i]))
            cr.line_to((i+1)*stepsize,scalingfactor*(100-self.cpuUtilArray[i+1]))
            cr.line_to((i+1)*stepsize,h)
            cr.line_to(i*stepsize,h)
            cr.move_to(i*stepsize,scalingfactor*(100-self.cpuUtilArray[i]))

            cr.fill()
            cr.stroke()
            # for outer line
            cr.set_line_width(1.5)
            cr.set_source_rgba(.384,.749,1.0,1) #for changing the outer line color
            cr.move_to(i*stepsize,scalingfactor*(100-self.cpuUtilArray[i]))
            cr.line_to((i+1)*stepsize,scalingfactor*(100-self.cpuUtilArray[i+1]))
            cr.stroke()


        return False

    def on_memSidePaneDrawArea_draw(self,dr,cr):
        #print("tyoe",g.Buildable.get_name(dr))
        cr.set_line_width(2)

        w=self.cpuSidePaneDrawArea.get_allocated_width()
        h=self.cpuSidePaneDrawArea.get_allocated_height()
        scalingfactor=h/self.memTotal
        #creating outer rectangle
        cr.set_source_rgba(.380,.102,.509,1)  ##need tochange the color
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.stroke()
        
        stepsize=w/99.0
        #print("in draw stepsize",stepsize)
        for i in range(0,99):
            # not effcient way to fill the bars (drawing)
            cr.set_source_rgba(.815,.419,1.0,0.2)   #for changing the fill color
            cr.move_to(i*stepsize,scalingfactor*(self.memTotal-self.memUsedArray1[i]))
            cr.line_to((i+1)*stepsize,scalingfactor*(self.memTotal-self.memUsedArray1[i+1]))
            cr.line_to((i+1)*stepsize,h)
            cr.line_to(i*stepsize,h)
            cr.move_to(i*stepsize,scalingfactor*(self.memTotal-self.memUsedArray1[i]))

            cr.fill()
            cr.stroke()
            # for outer line
            cr.set_line_width(1.5)
            cr.set_source_rgba(.627,.196,.788,1) #for changing the outer line color
            cr.move_to(i*stepsize,scalingfactor*(self.memTotal-self.memUsedArray1[i]))
            cr.line_to((i+1)*stepsize,scalingfactor*(self.memTotal-self.memUsedArray1[i+1]))
            cr.stroke()


        return False




if __name__=="__main__":
    p=os.popen('zenity --password')
    passs=p.readline()[:-1]    
    p.close()
    passs=re.sub(' ','\ ',passs)
    main=myclass(passs)
    g.main()
