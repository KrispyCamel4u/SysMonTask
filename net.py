from gi.repository import Gtk as g
import psutil as ps,cairo
from time import time
from gi_composites import GtkTemplate
from os import popen

from sysmontask import files_dir

@GtkTemplate(ui=files_dir+'/net.glade')
class networkWidget(g.ScrolledWindow):

    # Required else you would need to specify the full module
    # name in mywidget.ui (__main__+MyWidget)
    __gtype_name__ = 'networkWidget'
    
    nettextlabel= GtkTemplate.Child()
    netinfolabel= GtkTemplate.Child()
    netdrawarea=GtkTemplate.Child()
    netspeedscalelabelvalue= GtkTemplate.Child()
    netreclabelvalue= GtkTemplate.Child()
    nettotalreclabelvalue= GtkTemplate.Child()
    netsendlabelvalue= GtkTemplate.Child()
    nettotalsentlabelvalue= GtkTemplate.Child()
    net4addrlablevalue= GtkTemplate.Child()
    net6addrlabelvalue= GtkTemplate.Child()
    

    # Alternative way to specify multiple widgets
    #label1, entry = GtkTemplate.Child.widgets(2)

    def __init__(self):
        super(g.ScrolledWindow, self).__init__()
        
        # This must occur *after* you initialize your base
        self.init_template()
        self.netmxScalingFactor=1   #for the scaling of maximum value on the graph

    def givedata(self,secondself,index):
        self.netRecSpeedArray=secondself.netReceiveArray[index]
        self.netSendSpeedArray=secondself.netSendArray[index]

    @GtkTemplate.Callback
    def on_netDrawArea_draw(self,dr,cr):

        cr.set_line_width(2)

        w=self.netdrawarea.get_allocated_width()
        h=self.netdrawarea.get_allocated_height()

        speedstep=250          #500KB/s
        maximumcurrentspeed=max(max(self.netRecSpeedArray),max(self.netSendSpeedArray))
        currentscalespeed=self.netmxScalingFactor*speedstep
        while(currentscalespeed<maximumcurrentspeed):
            self.netmxScalingFactor+=1
            currentscalespeed=self.netmxScalingFactor*speedstep
        while(currentscalespeed>maximumcurrentspeed and self.netmxScalingFactor>1):
            self.netmxScalingFactor-=1
            currentscalespeed=self.netmxScalingFactor*speedstep
        
        if(currentscalespeed>=1000):
            suffix='MB/s'
            netscalefactor=1000
        else:
            suffix='KB/s'
            netscalefactor=1
        
        self.netspeedscalelabelvalue.set_text(str(currentscalespeed/netscalefactor)+suffix)

        scalingfactor=h/currentscalespeed
        #creating outer rectangle
        cr.set_source_rgba(.458,.141,.141,1)
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.stroke()
        # creating grid lines
        verticalGap=int(h/10)
        horzontalGap=int(w/10)
        for i in range(1,10):
            cr.set_source_rgba(.58,.196,.196,1)  #for changing the outer line color
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
            cr.set_source_rgba(.709,.164,.164,.2)  #for changing the fill color
            cr.move_to(i*stepsize,scalingfactor*(currentscalespeed-self.netRecSpeedArray[i])+2)
            cr.line_to((i+1)*stepsize,scalingfactor*(currentscalespeed-self.netRecSpeedArray[i+1])+2)
            cr.line_to((i+1)*stepsize,h)
            cr.line_to(i*stepsize,h)
            cr.move_to(i*stepsize,scalingfactor*(currentscalespeed-self.netRecSpeedArray[i])+2)
            cr.fill()
            cr.stroke()

            # for outer line read speed
            cr.set_line_width(1.5)
            cr.set_source_rgba(.709,.164,.164,1) #for changing the outer line color
            cr.move_to(i*stepsize,scalingfactor*(currentscalespeed-self.netRecSpeedArray[i])+2)
            cr.line_to((i+1)*stepsize,scalingfactor*(currentscalespeed-self.netRecSpeedArray[i+1])+2)
            cr.stroke()

            #for write
            cr.set_source_rgba(1,.313,.313,.2)  #for changing the fill color
            cr.move_to(i*stepsize,scalingfactor*(currentscalespeed-self.netSendSpeedArray[i])+2)
            cr.line_to((i+1)*stepsize,scalingfactor*(currentscalespeed-self.netSendSpeedArray[i+1])+2)
            cr.line_to((i+1)*stepsize,h)
            cr.line_to(i*stepsize,h)
            cr.move_to(i*stepsize,scalingfactor*(currentscalespeed-self.netSendSpeedArray[i])+2)
            cr.fill()
            cr.stroke()

            # cr.set_dash([5.0])
            cr.set_source_rgba(1,.313,.313,1) #for changing the outer line color
            cr.move_to(i*stepsize,scalingfactor*(currentscalespeed-self.netSendSpeedArray[i])+2)
            cr.line_to((i+1)*stepsize,scalingfactor*(currentscalespeed-self.netSendSpeedArray[i+1])+2)
            cr.stroke()


        return False


def netinit(self):

    self.netNameList=[]
    temp=ps.net_if_stats()
    for name in temp:
        if name !='lo' and temp[name][0]==True:
            self.netNameList.append(name)
            # print('working ')
    # print(self.netNameList)

    if len(self.netNameList)!=0:
        self.netWidgetList={}
        self.netstate1=[]
        self.netReceiveArray=[]
        self.netSendArray=[]
        self.numOfNets=len(self.netNameList)   #number of internet adapters
        # print(self.numOfNets)

        for i in range(0,self.numOfNets):
            self.netWidgetList[i]=networkWidget()
            self.performanceStack.add_titled(self.netWidgetList[i],'netStack'+str(i),'Network'+str(i))
            self.netWidgetList[i].nettextlabel.set_text(self.netNameList[i])
            ##self.netWidgetList[i].netinfolabel.set_text(self.netsize[i])                       ###change for the name
            nettemp=ps.net_io_counters(pernic=True)
            self.nett1=time()
            for adpts in nettemp:
                if adpts==self.netNameList[i]:
                    self.netstate1.append(nettemp[adpts])

            self.netReceiveArray.append([0]*100)
            self.netSendArray.append([0]*100)

            self.netWidgetList[i].givedata(self,i)
            # print('give dat')
    else:
        print("Net:No active network adapter found")
    
    

def netUpdate(self):
    nettemp=ps.net_io_counters(pernic=True)
    nettempaddr=ps.net_if_addrs()
    self.nett2=time()##
    timenetDiff=self.nett2-self.nett1
    self.netstate2=[]
    self.byterecpersecString=[]
    self.bytesendpersecString=[]
    for i in range(0,self.numOfNets):
        try:
            self.netstate2.append(nettemp[self.netNameList[i]])
        except:
            pass

    self.netDiff=[]
    for i in range(0,self.numOfNets):
        try:
            self.netDiff.append([x2-x1 for x1,x2 in zip(self.netstate1[i],self.netstate2[i])])
            bytesendpersec=(self.netDiff[i][0]/timenetDiff)/1000           ##default in KB
            byterecpersec=(self.netDiff[i][1]/timenetDiff)/1000  
            totalbyterec=nettemp[self.netNameList[i]][1]/1000            ##default in KB
            totalbytesent=nettemp[self.netNameList[i]][0]/1000

            ## total received
            if totalbyterec > 1000:   ###MB
                if totalbyterec > 1000000:    ##GB
                    netscalefactor=1000000
                    suffix='GB'
                else:
                    netscalefactor=1000
                    suffix='MB'
            else:
                netscalefactor=1
                suffix='KB'
        
            self.netWidgetList[i].nettotalreclabelvalue.set_text("{:.1f}".format(totalbyterec/netscalefactor)+suffix)

            ## total bytes sent
            if totalbytesent > 1000:   ###MB
                if totalbyterec > 1000000:    ##GB
                    netscalefactor=1000000
                    suffix='GB'
                else:
                    netscalefactor=1000
                    suffix='MB'
            else:
                netscalefactor=1
                suffix='KB'
            self.netWidgetList[i].nettotalsentlabelvalue.set_text("{:.1f}".format(totalbytesent/netscalefactor)+suffix)

            ## send per sec (uploading speed)
            if bytesendpersec > 1000:   ###MB
                netscalefactor=1000
                suffix='MB/s'
            else:
                netscalefactor=1
                suffix='KB/s'
            self.bytesendpersecString.append("{:.1f}".format(bytesendpersec/netscalefactor)+suffix)
            self.netWidgetList[i].netsendlabelvalue.set_text(self.bytesendpersecString[i])

            ## received per sec (downloading speed)
            if byterecpersec > 1000:   ###MB
                netscalefactor=1000
                suffix='MB/s'
            else:
                netscalefactor=1
                suffix='KB/s'
            self.byterecpersecString.append("{:.1f}".format(byterecpersec/netscalefactor)+suffix)
            self.netWidgetList[i].netreclabelvalue.set_text(self.byterecpersecString[i])

            self.netReceiveArray[i].pop()
            self.netReceiveArray[i].insert(0,byterecpersec)         ## in KBs

            self.netSendArray[i].pop()
            self.netSendArray[i].insert(0,bytesendpersec)

            self.netWidgetList[i].givedata(self,i)

            self.netWidgetList[i].net4addrlablevalue.set_text(nettempaddr[self.netNameList[i]][0][1])
            self.netWidgetList[i].net6addrlabelvalue.set_text(nettempaddr[self.netNameList[i]][1][1])
        except:
            pass


    self.netstate1=self.netstate2
    #print(self.nett2-self.nett1)
    self.nett1=self.nett2