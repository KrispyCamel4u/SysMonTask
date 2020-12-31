#!/usr/bin/env python3
from gi.repository import Gtk as g , GObject as go, Gdk
import os,cairo,re,psutil as ps


class myclass:
    flag=0      #flag for the updator 

    def __init__(self):
        self.gladefile="taskManager.glade"
        self.builder=g.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)
        self.Window=self.builder.get_object("main_window")
        self.quit=self.builder.get_object("quit")
        self.quit.connect('activate',self.on_quit_activate)
        
        # for about dialog 
        self.aboutdialog=self.builder.get_object("aboutdialog")
        # for notebook
        self.notebook=self.builder.get_object('notebook')
        #self.on_notebook_switch_page(self.notebook,'',0)

        #drawing area for cpu
        self.cpuDrawArea=self.builder.get_object('cpudrawarea')
        self.cpuUtilArray=[0]*100   #cpu util array

        
        self.timeinterval=1000     #time interval in mili

        # timer binding 
        go.timeout_add(self.timeinterval,self.updater)

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
        
        self.expdraw=self.builder.get_object('expdraw')
        self.expdraw.connect("button-press-event",self.do_button_press_event)
        self.expdraw.set_events(self.expdraw.get_events() | Gdk.EventMask.BUTTON_PRESS_MASK)

        self.Window.show()

    def do_button_press_event(self,widget,event):
        print("hi its working")
        #g.Widget.queue_draw(self.expdraw)

    def on_expdraw_draw(self,dr,cr):
        w=self.cpuDrawArea.get_allocated_width()
        h=self.cpuDrawArea.get_allocated_height()
        #creating outer rectangle
        print('hel')
        cr.set_source_rgba(1,.607,1.0,1)
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.fill()
        cr.stroke()


        return False

    def on_main_window_destroy(self,object,data=None):
        print("print with cancel")
        g.main_quit()

    def on_quit_activate(self,menuitem,data=None):
        print("quit from menu",g.Buildable.get_name(menuitem))
        g.main_quit()

    # method to show the about dialog
    def on_about_activate(self,menuitem,data=None):
        print("aboutdialog opening")
        self.response=self.aboutdialog.run()
        self.aboutdialog.hide()
        print("aboutdialog closed")
    
    # method for notebook switcher
    #def on_notebook_switch_page(self,notebook,page,page_num,data=None):

    # button click method
    def on_button_clicked(self,widget):
        print(widget.get_property('label'),"clicked")

    ## repeatedily called out fucntion
    def updater(self):
        
        if(not myclass.flag):
            myclass.flag=1
            #print("in if")

            ## for the first time only to get the name of the cpu
            p=os.popen('cat /proc/cpuinfo |grep -m1 "model name"')
            self.cpuname=p.read().split(':')[1].split('\n')[0]
            #print(self.cpuname)                                          # cpu name
            self.cpuInfoLabel.set_text(self.cpuname)
            self.cpuInfoLabel.set_valign(g.Align.CENTER)
            p.close()

            self.cpuCoreLabelValue.set_text(str(ps.cpu_count(logical=False)))

            self.cpuLogicalLabelValue.set_text(str(ps.cpu_count()))

            p=os.popen('lscpu|grep -i -E "(vt-x)|(amd-v)"')
            temp=p.read()
            if temp:
                temptext="Enabled"
            else:
                temptext="Disabled"
            self.cpuVirtualisationLabelValue.set_text(temptext)
            p.close()
            
            p=os.popen('lscpu|grep -i -m1 "L1d cache"')
            self.cpuL1LabelValue.set_text(re.sub("[\s]","",p.read().split(':')[1]))
            p.close()
            
            p=os.popen('lscpu|grep -i -m1 "L2 cache"')
            self.cpuL2LabelValue.set_text(re.sub('[\s]','',p.read().split(':')[1]))
            p.close()

            p=os.popen('lscpu|grep -i "L3 cache"')
            self.cpuL3LabelValue.set_text(re.sub('[\s]','',p.read().split(':')[1]))
            p.close()

            return True

        #print("setting speed")
        self.speed=ps.cpu_freq()
        self.cpuSpeedLabelValue.set_text("{:.2f}".format(self.speed[0]/1000)+' Ghz')
        #print("speed setting done")

        self.cpuUtil=ps.cpu_percent() ## % of the time is is working
        #print(self.cpuUtil)
        
        #print("setting utilisation")
        self.cpuUtilLabelValue.set_text(str(int(self.cpuUtil))+' %')
        #print('setting utilisation done')

        #print("setting number of processes and threads")
        self.cpuProcessesLabelValue.set_text(str(len(ps.pids())))

        p=os.popen("ps axms|wc -l")
        self.cpuThreadsLabelValue.set_text(re.sub('[\s]','',p.read()))
        p.close()

        #cpu package temp
        self.cpuTempLabelValue.set_text(str(int(ps.sensors_temperatures()['coretemp'][0][1])))
        # cpu fan speed

        ## cpu utilisation graph
        self.cpuUtilArray.pop()
        self.cpuUtilArray.insert(0,self.cpuUtil)
        g.Widget.queue_draw(self.cpuDrawArea)
        return True

    ## method for drawing
    def on_cpuDrawArea_draw(self,dr,cr):
        cr.set_line_width(2)

        w=self.cpuDrawArea.get_allocated_width()
        h=self.cpuDrawArea.get_allocated_height()
        scalingfactor=h/100.0
        #creating outer rectangle
        cr.set_source_rgba(0,.607,1.0,1)
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
        


if __name__=="__main__":
    main=myclass()
    g.main()
