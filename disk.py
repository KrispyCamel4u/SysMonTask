#!/usr/bin/env python3
# import gi
# gi.require_version("Gtk", "3.24")

from gi.repository import Gtk as g
import os,re,psutil as ps,math,time,cairo
from gi_composites import GtkTemplate


@GtkTemplate(ui='disk.glade')
class diskTabWidget(g.ScrolledWindow):

    # Required else you would need to specify the full module
    # name in mywidget.ui (__main__+MyWidget)
    __gtype_name__ = 'diskTabWidget'
    
    disktextlabel= GtkTemplate.Child()
    diskinfolabel = GtkTemplate.Child()
    diskdrawarea1=GtkTemplate.Child()
    diskdrawarea2=GtkTemplate.Child()
    disktextlabel=GtkTemplate.Child()
    diskactivelabelvalue=GtkTemplate.Child()
    diskreadlabelvalue=GtkTemplate.Child()
    diskwritelabelvalue=GtkTemplate.Child()
    diskcurrenspeedlabelvalue=GtkTemplate.Child()

    # Alternative way to specify multiple widgets
    #label1, entry = GtkTemplate.Child.widgets(2)

    def __init__(self):
        super(g.ScrolledWindow, self).__init__()
        
        # This must occur *after* you initialize your base
        self.init_template()
        self.diskmxfactor=1             #for the scaling of maximum value on the graph

    def givedata(self,secondself,index):
        self.diskactiveArray=secondself.diskActiveArray[index]
        self.diskreadArray=secondself.diskReadArray[index]
        self.diskwriteArray=secondself.diskWriteArray[index]
        

    @GtkTemplate.Callback
    def on_diskDrawArea2_draw(self,dr,cr):

        cr.set_line_width(2)

        w=self.diskdrawarea2.get_allocated_width()
        h=self.diskdrawarea2.get_allocated_height()

        speedstep=100
        maximumcurrentspeed=max(max(self.diskreadArray),max(self.diskwriteArray))
        currentscalespeed=self.diskmxfactor*speedstep
        if(currentscalespeed<maximumcurrentspeed):
            while(currentscalespeed<maximumcurrentspeed):
                self.diskmxfactor+=1
                currentscalespeed=self.diskmxfactor*speedstep
        else:
            while(currentscalespeed>maximumcurrentspeed+speedstep and self.diskmxfactor>1):
                self.diskmxfactor-=1
                currentscalespeed=self.diskmxfactor*speedstep
        
        self.diskcurrenspeedlabelvalue.set_text(str(currentscalespeed)+'MB')

        scalingfactor=h/currentscalespeed
        #creating outer rectangle
        cr.set_source_rgba(.109,.670,.0588,1)
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.stroke()
        # creating grid lines
        verticalGap=int(h/10)
        horzontalGap=int(w/10)
        for i in range(1,10):
            cr.set_source_rgba(.109,.670,.0588,1) #for changing the outer line color
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
            cr.set_source_rgba(.431,1,.04,0.25)  #for changing the fill color
            cr.move_to(i*stepsize,scalingfactor*(currentscalespeed-self.diskreadArray[i])+2)
            cr.line_to((i+1)*stepsize,scalingfactor*(currentscalespeed-self.diskreadArray[i+1])+2)
            cr.line_to((i+1)*stepsize,h)
            cr.line_to(i*stepsize,h)
            cr.move_to(i*stepsize,scalingfactor*(currentscalespeed-self.diskreadArray[i])+2)
            cr.fill()
            cr.stroke()

            # for outer line read speed
            cr.set_line_width(1.5)
            cr.set_source_rgba(.109,.670,.0588,1) #for changing the outer line color
            cr.move_to(i*stepsize,scalingfactor*(currentscalespeed-self.diskreadArray[i])+2)
            cr.line_to((i+1)*stepsize,scalingfactor*(currentscalespeed-self.diskreadArray[i+1])+2)
            cr.stroke()

            #for write
            cr.set_source_rgba(.207,.941,.682,0.3)  #for changing the fill color
            cr.move_to(i*stepsize,scalingfactor*(currentscalespeed-self.diskwriteArray[i])+2)
            cr.line_to((i+1)*stepsize,scalingfactor*(currentscalespeed-self.diskwriteArray[i+1])+2)
            cr.line_to((i+1)*stepsize,h)
            cr.line_to(i*stepsize,h)
            cr.move_to(i*stepsize,scalingfactor*(currentscalespeed-self.diskwriteArray[i])+2)
            cr.fill()
            cr.stroke()

            #cr.set_dash([1.0])
            cr.set_source_rgba(.207,.941,.682,1) #for changing the outer line color
            cr.move_to(i*stepsize,scalingfactor*(currentscalespeed-self.diskwriteArray[i])+2)
            cr.line_to((i+1)*stepsize,scalingfactor*(currentscalespeed-self.diskwriteArray[i+1])+2)
            cr.stroke()


        return False

    @GtkTemplate.Callback
    def on_diskDrawArea1_draw(self,dr,cr):

        cr.set_line_width(2)

        w=self.diskdrawarea1.get_allocated_width()
        h=self.diskdrawarea1.get_allocated_height()

        scalingfactor=h/100.0
        #creating outer rectangle
        cr.set_source_rgba(.109,.670,.0588,1)
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.stroke()
        # creating grid lines
        verticalGap=int(h/10)
        horzontalGap=int(w/10)
        for i in range(1,10):
            cr.set_source_rgba(.109,.670,.0588,1) #for changing the outer line color
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
            cr.set_source_rgba(.431,1,.04,0.25)  #for changing the fill color
            cr.move_to(i*stepsize,scalingfactor*(100-self.diskactiveArray[i])+2)
            cr.line_to((i+1)*stepsize,scalingfactor*(100-self.diskactiveArray[i+1])+2)
            cr.line_to((i+1)*stepsize,h)
            cr.line_to(i*stepsize,h)
            cr.move_to(i*stepsize,scalingfactor*(100-self.diskactiveArray[i])+2)

            cr.fill()
            cr.stroke()
            # for outer line
            cr.set_line_width(1.5)
            cr.set_source_rgba(.109,.670,.0588,1) #for changing the outer line color
            cr.move_to(i*stepsize,scalingfactor*(100-self.diskactiveArray[i])+2)
            cr.line_to((i+1)*stepsize,scalingfactor*(100-self.diskactiveArray[i+1])+2)
            cr.stroke()


        return False        

def diskinit(self):

    self.disklist=[]
    self.disksize=[]
    try:
        p=os.popen('lsblk -d -o NAME,SIZE')
        partitions=p.readlines()
        p.close()
        for parts in partitions:
            tempparts=parts.split()
            if 'loop' not in tempparts[0] and 'NAME' not in  tempparts[0]:
                self.disklist.append(tempparts[0])
                self.disksize.append(tempparts[1])
                print(tempparts[0])
    except:
        print("Failed to get Disks")
        pass

    self.diskWidgetList={}
    self.diskstate1=[]
    self.diskActiveArray=[]
    self.diskReadArray=[]
    self.diskWriteArray=[]
    self.numOfDisks=len(self.disklist)
    for i in range(0,self.numOfDisks):
        self.diskWidgetList[i]=diskTabWidget()
        self.performanceStack.add_titled(self.diskWidgetList[i],'diskStack'+str(i),'Disk'+str(i))
        self.diskWidgetList[i].disktextlabel.set_text(self.disklist[i])
        self.diskWidgetList[i].diskinfolabel.set_text(self.disksize[i])
        disktemp=ps.disk_io_counters(perdisk=True)
        self.diskt1=time.time()
        for drives in disktemp:
            if drives==self.disklist[i]:
               self.diskstate1.append(disktemp[drives])


        self.diskActiveArray.append([0]*100)
        self.diskReadArray.append([0]*100)
        self.diskWriteArray.append([0]*100)

        self.diskWidgetList[i].givedata(self,i)
    
    
                
    
def diskTabUpdate(self):
    disktemp=ps.disk_io_counters(perdisk=True)
    self.diskt2=time.time()##
    timediskDiff=self.diskt2-self.diskt1
    self.diskstate2=[]
    for i in range(0,self.numOfDisks):
        self.diskstate2.append(disktemp[self.disklist[i]])
        
    self.diskDiff=[]    
    self.diskActiveString=[]
    for i in range(0,self.numOfDisks):
        self.diskDiff.append([x2-x1 for x1,x2 in zip(self.diskstate1[i],self.diskstate2[i])])
        
        self.diskActiveString.append(str(int(self.diskDiff[i][8]/10))+'%')
        self.diskWidgetList[i].diskactivelabelvalue.set_text(self.diskActiveString[i])
        self.diskWidgetList[i].diskreadlabelvalue.set_text("{:.1f}".format(self.diskDiff[i][2]/1000000)+'MB')
        self.diskWidgetList[i].diskwritelabelvalue.set_text("{:.1f}".format(self.diskDiff[i][3]/1000000)+'MB')

        self.diskActiveArray[i].pop()
        self.diskActiveArray[i].insert(0,(self.diskDiff[i][8])/(10*timediskDiff))##

        self.diskReadArray[i].pop()
        self.diskReadArray[i].insert(0,self.diskDiff[i][2]/((timediskDiff)*1000000))

        self.diskWriteArray[i].pop()
        self.diskWriteArray[i].insert(0,self.diskDiff[i][3]/((timediskDiff)*1000000))

        self.diskWidgetList[i].givedata(self,i)


    self.diskstate1=self.diskstate2
    #print(self.diskt2-self.diskt1)
    self.diskt1=self.diskt2
    




    
    

