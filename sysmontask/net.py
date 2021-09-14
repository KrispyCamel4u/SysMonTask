from gi.repository import Gtk as g
import psutil as ps
from time import time
from os import popen
import json

try:
    from gi_composites import GtkTemplate
except ImportError:
    from sysmontask.gi_composites import GtkTemplate


if __name__=='sysmontask.net':
    from sysmontask.sysmontask import files_dir
    from sysmontask.gproc import byte_to_human
else:
    from sysmontask import files_dir
    from gproc import byte_to_human

@GtkTemplate(ui=files_dir+'/net.glade')
class networkWidget(g.ScrolledWindow):
    """
    A net tab widget(top level box with all childs fields) which is made by the gtk template.
    """
    # Required else you would need to specify the full module
    # name in mywidget.ui (__main__+MyWidget)
    __gtype_name__ = 'networkWidget'

    # Declaring/Fetching/Assigning the required childs(name in the template should be the same as used here)
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
    net_mac_addr_label_value= GtkTemplate.Child()
    netVendorLabelValue=GtkTemplate.Child()

    net_recv_color_descriptor= GtkTemplate.Child()
    net_send_color_descriptor= GtkTemplate.Child()

    # Alternative way to specify multiple widgets
    #label1, entry = GtkTemplate.Child.widgets(2)

    def __init__(self):
        """Constructing the Net Widget."""
        super(g.ScrolledWindow, self).__init__()

        # This must occur *after* you initialize your base
        self.init_template()
        # For the scaling of maximum value on the graph
        self.netmxScalingFactor=1
        # The main class self
        self.secondself=None

    def givedata(self,secondself,index):
        """
        Method to pass the data to the class(local) object from outside class. And assign them to the local class variables.

        Parameters
        ----------
        secondself : the main class reference(the main global self) which will be calling this function.
        index : index of the net adaptors from the list
        """
        # Receive(Donwload) and Send(Upload) speeds passing to the this class variables
        self.netRecSpeedArray=secondself.netReceiveArray[index]
        self.netSendSpeedArray=secondself.netSendArray[index]
        self.secondself=secondself

    @GtkTemplate.Callback
    def on_netDrawArea_draw(self,dr,cr):
        """
        Function Binding(for draw signal) for network speeds drawing area.

        This function draw the Network's Receive and Send speed curves upon called by the queue of request generated in
        the main *updator* function.

        Parameters
        ----------
        dr : the widget on which to draw the graph
        cr : the cairo surface object
        """
        # Default line width
        cr.set_line_width(2)

        # Color Pofile setup
        color=self.secondself.color_profile['network'][0]
        rectangle_color=self.secondself.color_profile['network'][1]

        self.net_recv_color_descriptor.set_markup(f'<span size="20000" foreground="{"#%02x%02x%02x" % (int(color[0]*255), int(color[1]*255), int(color[2]*255))}">|</span>')
        self.net_send_color_descriptor.set_markup(f'<span size="20000" foreground="{"#%02x%02x%02x" % (int(color[0]*255), int(color[1]*255), int(color[2]*255))}">¦</span>')

        # Get the allocated widht and height
        w=self.netdrawarea.get_allocated_width()
        h=self.netdrawarea.get_allocated_height()

        # Speed step in KB/s is the step in which the maximum speed(vertical scale) will adjust for dynamic speeds, i.e, in multiples
        # of this step.
        speedstep=250*1024          #250KB/s
        # The maximum read or write speeds in the buffer
        maximumcurrentspeed=max(max(self.netRecSpeedArray),max(self.netSendSpeedArray))
        # The current maximum scale speed
        currentscalespeed=self.netmxScalingFactor*speedstep

        # vertical scale adjustment calculation, i.e, new maximum scale speed
        while(currentscalespeed<maximumcurrentspeed):
            self.netmxScalingFactor+=1
            currentscalespeed=self.netmxScalingFactor*speedstep
        while(currentscalespeed-speedstep>maximumcurrentspeed and self.netmxScalingFactor>1):
            self.netmxScalingFactor-=1
            currentscalespeed=self.netmxScalingFactor*speedstep

        # Setting new maximum scale label
        self.netspeedscalelabelvalue.set_text(byte_to_human(currentscalespeed))

        # vertical scaling factor(step)
        scalingfactor=h/currentscalespeed

        # creating outer rectangle
        # cr.set_source_rgba(.458,.141,.141,1)    # Color of thr rectanlge
        cr.set_source_rgba(*rectangle_color,1)
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.stroke()

        # creating grid lines
        verticalGap=int(h/10)
        horzontalGap=int(w/10)
        for i in range(1,10):
            # cr.set_source_rgba(.58,.196,.196,1)  #for changing the glid line color
            cr.set_source_rgba(*color,1)
            cr.set_line_width(0.5)
            cr.move_to(0,i*verticalGap)
            cr.line_to(w,i*verticalGap)

            cr.move_to(i*horzontalGap,0)
            cr.line_to(i*horzontalGap,h)
            cr.stroke()
        cr.stroke()

        # Horzontal step size
        stepsize=w/99.0

        #print("in draw stepsize",stepsize)
        # for i in range(0,99):
        #     # not effcient way to fill the bars (drawing)
        #     cr.set_source_rgba(.709,.164,.164,.2)  #for changing the fill color
        #     cr.move_to(i*stepsize,scalingfactor*(currentscalespeed-self.netRecSpeedArray[i])+2)
        #     cr.line_to((i+1)*stepsize,scalingfactor*(currentscalespeed-self.netRecSpeedArray[i+1])+2)
        #     cr.line_to((i+1)*stepsize,h)
        #     cr.line_to(i*stepsize,h)
        #     cr.move_to(i*stepsize,scalingfactor*(currentscalespeed-self.netRecSpeedArray[i])+2)
        #     cr.fill()
        #     cr.stroke()

        #     # for outer line read speed
        #     cr.set_line_width(1.5)
        #     cr.set_source_rgba(.709,.164,.164,1) #for changing the outer line color
        #     cr.move_to(i*stepsize,scalingfactor*(currentscalespeed-self.netRecSpeedArray[i])+2)
        #     cr.line_to((i+1)*stepsize,scalingfactor*(currentscalespeed-self.netRecSpeedArray[i+1])+2)
        #     cr.stroke()

        #     #for write
        #     cr.set_source_rgba(1,.313,.313,.2)  #for changing the fill color
        #     cr.move_to(i*stepsize,scalingfactor*(currentscalespeed-self.netSendSpeedArray[i])+2)
        #     cr.line_to((i+1)*stepsize,scalingfactor*(currentscalespeed-self.netSendSpeedArray[i+1])+2)
        #     cr.line_to((i+1)*stepsize,h)
        #     cr.line_to(i*stepsize,h)
        #     cr.move_to(i*stepsize,scalingfactor*(currentscalespeed-self.netSendSpeedArray[i])+2)
        #     cr.fill()
        #     cr.stroke()

        #     # cr.set_dash([5.0])
        #     cr.set_source_rgba(1,.313,.313,1) #for changing the outer line color
        #     cr.move_to(i*stepsize,scalingfactor*(currentscalespeed-self.netSendSpeedArray[i])+2)
        #     cr.line_to((i+1)*stepsize,scalingfactor*(currentscalespeed-self.netSendSpeedArray[i+1])+2)
        #     cr.stroke()

        ## Receive ##
        # Drawing the curve
        # cr.set_source_rgba(.709,.164,.164,1) #for changing the outer line color
        cr.set_source_rgba(*color,1)
        cr.set_line_width(1.5)
        cr.move_to(0,scalingfactor*(currentscalespeed-self.netRecSpeedArray[0])+2)
        for i in range(0,99):
            cr.line_to((i+1)*stepsize,scalingfactor*(currentscalespeed-self.netRecSpeedArray[i+1])+2)
        cr.stroke_preserve()

        # Filling the curve from inside with solid color, the curve(shape) should be a closed then only it can be filled
        # cr.set_source_rgba(.709,.164,.164,.2)  #for changing the fill color
        cr.set_source_rgba(*color,0.2)
        cr.line_to(w,h)
        cr.line_to(0,h)
        cr.move_to(0,scalingfactor*(currentscalespeed-self.netRecSpeedArray[0])+2)
        cr.fill()
        cr.stroke()

        ## Send ##
        # Drawing the curve's outer line
        # cr.set_source_rgba(1,.313,.313,1) #for changing the outer line color
        cr.set_source_rgba(*color,1)
        cr.move_to(0,scalingfactor*(currentscalespeed-self.netSendSpeedArray[0])+2)
        cr.set_line_width(1.5)
        cr.set_dash([3.0 ,3.0])
        for i in range(0,99):
            cr.line_to((i+1)*stepsize,scalingfactor*(currentscalespeed-self.netSendSpeedArray[i+1])+2)
        cr.stroke_preserve()

        # Filling the curve from inside with solid color, the curve(shape) should be a closed then only it can be filled
        # cr.set_source_rgba(1,.313,.313,.2)  #for changing the fill color
        cr.set_source_rgba(*color,0.2)
        cr.line_to(w,h)
        cr.line_to(0,h)
        cr.move_to(0,scalingfactor*(currentscalespeed-self.netSendSpeedArray[0])+2)
        cr.fill()
        cr.stroke()

        return False


def netinit(self):
    """
    Function for initilization of the Network Components.
    """
    # Declaring list for holding the names of net adaptors
    self.netNameList :list =[]

    # Getting the adaptor status and find and store ones which are active
    temp :dict(network_name,tuple(isup,duplex,speed,mtu))=ps.net_if_stats()
    for name in temp:
        if name !='lo' and temp[name][0]==True:
            self.netNameList.append(name)

    # If NIC list is not empty
    if len(self.netNameList)!=0:
        self.netWidgetList={}
        self.netstate1=[]
        self.netReceiveArray=[]
        self.netSendArray=[]
        self.numOfNets=len(self.netNameList)   #number of internet adapters
        # print(self.numOfNets)

        try:
            # For finding the product name and vendor
            p=popen("lshw -c network -json")
            netinfo=json.loads(p.read())    # netinfo is a List of dictionary
            p.close()
        except:
            print("lshw not found")

        for i in range(0,self.numOfNets):
            self.netWidgetList[i]=networkWidget()
            self.performanceStack.add_titled(self.netWidgetList[i],f'page{self.stack_counter}','Network'+str(i))
            # For lookup devices and its assigned stack page numbers
            self.device_stack_page_lookup[self.netNameList[i]]=self.stack_counter
            self.stack_counter+=1
            self.netWidgetList[i].nettextlabel.set_text(self.netNameList[i])
            try:
                for item in netinfo:
                    if item["logicalname"]==self.netNameList[i]:
                        if "product" in item:
                            self.netWidgetList[i].netinfolabel.set_text(item["product"])    ###change for the name
                        if "vendor" in item:
                            self.netWidgetList[i].netVendorLabelValue.set_text(item["vendor"])
                        break
            except Exception as e:
                print(f"Error in getting Product/Vendor {e}")

            nettemp=ps.net_io_counters(pernic=True)
            self.nett1=time()
            for adpts in nettemp:
                if adpts==self.netNameList[i]:
                    self.netstate1.append(nettemp[adpts])

            # mac addr
            nettemp=ps.net_if_addrs()
            for entry in nettemp[self.netNameList[i]]:
                if entry.family==17:   #17 for AF_PACKET
                    self.netWidgetList[i].net_mac_addr_label_value.set_text(str(entry.address))

            self.netReceiveArray.append([0]*100)
            self.netSendArray.append([0]*100)

            self.netWidgetList[i].givedata(self,i)
            # print('give dat')
    else:
        print("Net:No active network adapter found")
        self.numOfNets=0


def netUpdate(self):
    """
    Function to periodically update Network's statistics.
    """
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
            bytesendpersec=(self.netDiff[i][0]/timenetDiff)           ##default in KB
            byterecpersec=(self.netDiff[i][1]/timenetDiff)
            totalbyterec=nettemp[self.netNameList[i]][1]           ##default in KB
            totalbytesent=nettemp[self.netNameList[i]][0]

            ## total received
            self.netWidgetList[i].nettotalreclabelvalue.set_text(byte_to_human(totalbyterec,persec=False))

            ## total bytes sent
            self.netWidgetList[i].nettotalsentlabelvalue.set_text(byte_to_human(totalbytesent,persec=False))

            ## send per sec (uploading speed)
            self.bytesendpersecString.append(byte_to_human(bytesendpersec))
            self.netWidgetList[i].netsendlabelvalue.set_text(self.bytesendpersecString[i])

            ## received per sec (downloading speed)
            self.byterecpersecString.append(byte_to_human(byterecpersec))
            self.netWidgetList[i].netreclabelvalue.set_text(self.byterecpersecString[i])

            if self.update_graph_direction:
                self.netReceiveArray[i].pop(0)
                self.netReceiveArray[i].append(byterecpersec)         ## in KBs

                self.netSendArray[i].pop(0)
                self.netSendArray[i].append(bytesendpersec)
            else:
                self.netReceiveArray[i].pop()
                self.netReceiveArray[i].insert(0,byterecpersec)         ## in KBs

                self.netSendArray[i].pop()
                self.netSendArray[i].insert(0,bytesendpersec)

            self.netWidgetList[i].givedata(self,i)

            self.netWidgetList[i].net4addrlablevalue.set_text(nettempaddr[self.netNameList[i]][0][1])
            try:
                self.netWidgetList[i].net6addrlabelvalue.set_text(nettempaddr[self.netNameList[i]][1][1])
            except Exception:
                pass
        except Exception as e:
            print(f'some error in net update: {e}')



    self.netstate1=self.netstate2
    #print(self.nett2-self.nett1)
    self.nett1=self.nett2