# import gi
# gi.require_version("Gtk", "3.24")

from gi.repository import Gtk as g,Gdk
try:
    from gi_composites import GtkTemplate
except ImportError:
    from sysmontask.gi_composites import GtkTemplate


if __name__=='sysmontask.sidepane':
    from sysmontask.sysmontask import files_dir, icon_file
else:
    from sysmontask import files_dir,icon_file

@GtkTemplate(ui=files_dir+'/diskSidepane.glade')
class diskSidepaneWidget(g.Box):

    # Required else you would need to specify the full module
    # name in mywidget.ui (__main__+MyWidget)
    __gtype_name__ = 'diskSidepaneWidget'

    disksidepanetextlabel= GtkTemplate.Child()
    disksidepanelabelvalue = GtkTemplate.Child()
    disksidepanedrawarea=GtkTemplate.Child()
    disk_switcher_button=GtkTemplate.Child()


    # Alternative way to specify multiple widgets
    #label1, entry = GtkTemplate.Child.widgets(2)

    def __init__(self):
        """Construct Disk Sidepane widget."""
        super(g.Box, self).__init__()

        # This must occur *after* you initialize your base
        self.init_template()

    def givedata(self,secondself,index):
        self.diskactiveArray=secondself.diskActiveArray[index]

    @GtkTemplate.Callback
    def on_diskSidepaneDrawArea_draw(self,dr,cr):
        cr.set_line_width(2)

        w=self.disksidepanedrawarea.get_allocated_width()
        h=self.disksidepanedrawarea.get_allocated_height()
        scalingfactor=h/100.0
        #creating outer rectangle
        cr.set_source_rgba(.109,.670,.0588,1)
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.stroke()


        stepsize=w/99.0
        #print("in draw stepsize",stepsize)
        # for i in range(0,99):
        #     # not effcient way to fill the bars (drawing)
        #     cr.set_source_rgba(.431,1,.04,0.25)  #for changing the fill color
        #     cr.move_to(i*stepsize,scalingfactor*(100-self.diskactiveArray[i])+2)
        #     cr.line_to((i+1)*stepsize,scalingfactor*(100-self.diskactiveArray[i+1])+2)
        #     cr.line_to((i+1)*stepsize,h)
        #     cr.line_to(i*stepsize,h)
        #     cr.move_to(i*stepsize,scalingfactor*(100-self.diskactiveArray[i])+2)

        #     cr.fill()
        #     cr.stroke()
        #     # for outer line
        #     cr.set_line_width(1.5)
        #     cr.set_source_rgba(.109,.670,.0588,1) #for changing the outer line color
        #     cr.move_to(i*stepsize,scalingfactor*(100-self.diskactiveArray[i])+2)
        #     cr.line_to((i+1)*stepsize,scalingfactor*(100-self.diskactiveArray[i+1])+2)
        #     cr.stroke()

        cr.set_source_rgba(.109,.670,.0588,1) #for changing the outer line color
        cr.set_line_width(1.5)
        cr.move_to(0,scalingfactor*(100-self.diskactiveArray[0])+2)
        for i in range(0,99):
            cr.line_to((i+1)*stepsize,scalingfactor*(100-self.diskactiveArray[i+1])+2)
        cr.stroke_preserve()

        cr.set_source_rgba(.431,1,.04,0.25)  #for changing the fill color
        cr.line_to(w,h)
        cr.line_to(0,h)
        cr.move_to(0,scalingfactor*(100-self.diskactiveArray[0])+2)
        cr.fill()
        cr.stroke()


        return False

@GtkTemplate(ui=files_dir+'/netSidepane.glade')
class netSidepaneWidget(g.Box):

    # Required else you would need to specify the full module
    # name in mywidget.ui (__main__+MyWidget)
    __gtype_name__ = 'netSidepaneWidget'

    netsidepanetextlabel= GtkTemplate.Child()
    netsidepanelabelvalue = GtkTemplate.Child()
    netsidepanedrawarea=GtkTemplate.Child()
    net_switcher_button=GtkTemplate.Child()



    # Alternative way to specify multiple widgets
    #label1, entry = GtkTemplate.Child.widgets(2)

    def __init__(self):
        """Construct Net Sidepane widget."""
        super(g.Box, self).__init__()

        # This must occur *after* you initialize your base
        self.init_template()
        self.netmxScalingFactor=1

    def givedata(self,secondself,index):
        self.netRecSpeedArray=secondself.netReceiveArray[index]
        self.netSendSpeedArray=secondself.netSendArray[index]

    @GtkTemplate.Callback
    def on_netSidepaneDrawArea_draw(self,dr,cr):
        cr.set_line_width(2)

        w=self.netsidepanedrawarea.get_allocated_width()
        h=self.netsidepanedrawarea.get_allocated_height()

        speedstep=250*1024          #250KB/s
        maximumcurrentspeed=max(max(self.netRecSpeedArray),max(self.netSendSpeedArray))
        currentscalespeed=self.netmxScalingFactor*speedstep
        while(currentscalespeed<maximumcurrentspeed):
            self.netmxScalingFactor+=1
            currentscalespeed=self.netmxScalingFactor*speedstep
        while(currentscalespeed>maximumcurrentspeed and self.netmxScalingFactor>1):
            self.netmxScalingFactor-=1
            currentscalespeed=self.netmxScalingFactor*speedstep


        scalingfactor=h/currentscalespeed
        #creating outer rectangle
        cr.set_source_rgba(.458,.141,.141,1)
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.stroke()


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

        #efficient receive speed drawing
        cr.set_source_rgba(.709,.164,.164,1) #for changing the outer line color
        cr.set_line_width(1.5)
        cr.move_to(0,scalingfactor*(currentscalespeed-self.netRecSpeedArray[0])+2)
        for i in range(0,99):
            cr.line_to((i+1)*stepsize,scalingfactor*(currentscalespeed-self.netRecSpeedArray[i+1])+2)
        cr.stroke_preserve()

        cr.set_source_rgba(.709,.164,.164,.2)  #for changing the fill color
        cr.line_to(w,h)
        cr.line_to(0,h)
        cr.move_to(0,scalingfactor*(currentscalespeed-self.netRecSpeedArray[0])+2)
        cr.fill()
        cr.stroke()

        #efficient drawing for send
        cr.set_source_rgba(1,.313,.313,1) #for changing the outer line color
        cr.move_to(0,scalingfactor*(currentscalespeed-self.netSendSpeedArray[0])+2)
        cr.set_line_width(1.5)
        for i in range(0,99):
            cr.line_to((i+1)*stepsize,scalingfactor*(currentscalespeed-self.netSendSpeedArray[i+1])+2)
        cr.stroke_preserve()

        cr.set_source_rgba(1,.313,.313,.2)  #for changing the fill color
        cr.line_to(w,h)
        cr.line_to(0,h)
        cr.move_to(0,scalingfactor*(currentscalespeed-self.netSendSpeedArray[0])+2)
        cr.fill()
        cr.stroke()

        return False

@GtkTemplate(ui=files_dir+'/gpuSidepane.glade')
class gpuSidepaneWidget(g.Box):

    # Required else you would need to specify the full module
    # name in mywidget.ui (__main__+MyWidget)
    __gtype_name__ = 'gpuSidepaneWidget'

    gpusidepanetextlabel= GtkTemplate.Child()
    gpusidepanelabelvalue = GtkTemplate.Child()
    gpusidepanedrawarea=GtkTemplate.Child()
    gpu_switcher_button=GtkTemplate.Child()



    # Alternative way to specify multiple widgets
    #label1, entry = GtkTemplate.Child.widgets(2)

    def __init__(self):
        """Construct GPU Sidepane widget."""
        super(g.Box, self).__init__()

        # This must occur *after* you initialize your base
        self.init_template()

    def givedata(self,secondself):
        self.gpuutilArray=secondself.gpuUtilArray

    @GtkTemplate.Callback
    def gpuSidepaneDrawArea_draw(self,dr,cr):
        cr.set_line_width(2)

        w=self.gpusidepanedrawarea.get_allocated_width()
        h=self.gpusidepanedrawarea.get_allocated_height()
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
        #     cr.move_to(i*stepsize,scalingfactor*(100-self.gpuutilArray[i])+2)
        #     cr.line_to((i+1)*stepsize,scalingfactor*(100-self.gpuutilArray[i+1])+2)
        #     cr.line_to((i+1)*stepsize,h)
        #     cr.line_to(i*stepsize,h)
        #     cr.move_to(i*stepsize,scalingfactor*(100-self.gpuutilArray[i])+2)

        #     cr.fill()
        #     cr.stroke()
        #     # for outer line
        #     cr.set_line_width(1.5)
        #     cr.set_source_rgba(.384,.749,1.0,1) #for changing the outer line color
        #     cr.move_to(i*stepsize,scalingfactor*(100-self.gpuutilArray[i])+2)
        #     cr.line_to((i+1)*stepsize,scalingfactor*(100-self.gpuutilArray[i+1])+2)
        #     cr.stroke()

        cr.set_line_width(1.5)
        cr.set_source_rgba(.384,.749,1.0,1) #for changing the outer line color
        cr.move_to(0,scalingfactor*(100-self.gpuutilArray[0]))
        for i in range(0,99):
            cr.line_to((i+1)*stepsize,scalingfactor*(100-self.gpuutilArray[i+1]))
        cr.stroke_preserve()

        cr.set_source_rgba(.588,.823,.98,0.25)   #for changing the fill color
        cr.line_to(w,h)
        cr.line_to(0,h)
        cr.move_to(0,scalingfactor*(100-self.gpuutilArray[0]))
        cr.fill()
        cr.stroke()


        return False

# def on_switcher_clicked(button,stack,curr_stack):
#     if not button.get_name()==stack.get_visible_child_name():
#         stack.set_visible_child_name(button.get_name())
#         curr_stack=button.get_name()

def on_switcher_clicked(button,event,stack,self):
    if event.type==Gdk.EventType.BUTTON_PRESS:
        if event.button==1:
            if not button.get_name()==stack.get_visible_child_name():
                stack.set_visible_child_name(button.get_name())
                self.current_stack=int(button.get_name()[4:])
        elif event.button==3:
            self.right_clicked_stack_switcher_button_num=int(button.get_name()[4:])
            show_popover(self)
            # print("right click")

def show_popover(self):
    self.stack_popover_menu.popup(None, None, None, None, 0, g.get_current_event_time())

def color_chooser(widget,self):
    c_dialog=g.ColorChooserDialog(title="Choose Color",parent=self.Window)
    response=c_dialog.run()
    print(response)
    if response==g.ResponseType.OK:
        color=c_dialog.get_rgba()
        c_dialog.destroy()
    else: c_dialog.destroy();return

def hide_devices_callback(widget,self):
    self.device_menu_items[self.right_clicked_stack_switcher_button_num].set_active(False)

def hide_devices(button_num,self):
    if len(self.hidden_stack_page_numbers)>=self.stack_counter-1 and button_num not in self.hidden_stack_page_numbers:
        self.device_menu_items[button_num].set_active(True);return
    self.stack_switcher_buttons[button_num].hide()

    if button_num not in self.hidden_stack_page_numbers:self.hidden_stack_page_numbers.append(button_num)

    if self.current_stack== button_num:
        i=button_num+1
        print(i,self.stack_counter,self.current_stack)
        while(i!=button_num):
            print(i)
            if i==self.stack_counter:i=0
            if i not in self.hidden_stack_page_numbers:
                self.performanceStack.set_visible_child_name(f'page{i}'); self.current_stack=i; break
            i+=1


def show_devices(button_num,self):
    if button_num in self.hidden_stack_page_numbers:
        self.stack_switcher_buttons[button_num].show()
        self.hidden_stack_page_numbers.remove(button_num)

def device_show_hide_menu_callback(widget,self):
    if widget.get_active():
        show_devices(self.device_stack_page_lookup[widget.get_name()],self)
    else:
        hide_devices(self.device_stack_page_lookup[widget.get_name()],self)
    print(self.hidden_stack_page_numbers)

def feature_setup(self):

    self.default_colors :dict(device,rgb)={
        'cpu':(.384,.749,1.0),
        'memory':(.627,.196,.788,1),
        'disk':(),
        'network':(),
        'gpu':()
    }

    # popup menu for right click
    self.stack_popover_menu=g.Menu()
    popover_item=g.ImageMenuItem("Change color")
    img=g.Image()
    img.set_from_file(f"{icon_file}/choose_color.png")
    popover_item.set_image(img)
    popover_item.set_always_show_image(True)
    popover_item.connect('activate',color_chooser,self)
    self.stack_popover_menu.append(popover_item)

    img=g.Image()
    popover_item=g.ImageMenuItem("Hide")
    img.set_from_file(f"{icon_file}/hide.png")
    popover_item.set_image(img)
    popover_item.set_always_show_image(True)
    popover_item.connect('activate',hide_devices_callback,self)
    self.stack_popover_menu.append(popover_item)

    self.stack_popover_menu.show_all()


def sidepaneinit(self):
    print("initialisating sidepane")

    self.default_colors :dict(device,rgb)={
        'cpu':(.384,.749,1.0),
        'memory':(.627,.196,.788,1),
        'disk':(),
        'network':(),
        'gpu':()
    }
    self.graph_colors={}


    # lookup for stack page switcher button
    self.stack_switcher_buttons={}

    button_counter=0 # button name counter

    self.cpuSidePaneLabelValue=self.builder.get_object('cpusidepanelabelvalue')
    self.cpuSidePaneDrawArea=self.builder.get_object('cpusidepanedrawarea')
    cpu_switcher_button=self.builder.get_object("cpu_switcher_button")
    cpu_switcher_button.connect('button-press-event',on_switcher_clicked,self.performanceStack,self)
    cpu_switcher_button.set_name(f'page{button_counter}')
    self.stack_switcher_buttons[button_counter]=cpu_switcher_button
    button_counter+=1

    self.memSidePaneLabelValue=self.builder.get_object('memsidepanelabelvalue')
    self.memSidePaneDrawArea=self.builder.get_object('memsidepanedrawarea')
    mem_switcher_button=self.builder.get_object("mem_switcher_button")
    mem_switcher_button.connect('button-press-event',on_switcher_clicked,self.performanceStack,self)
    mem_switcher_button.set_name(f'page{button_counter}')
    self.stack_switcher_buttons[button_counter]=mem_switcher_button
    button_counter+=1

    self.diskSidepaneWidgetList={}
    for i in range(0,self.numOfDisks):
        self.diskSidepaneWidgetList[i]=diskSidepaneWidget()
        self.sidepaneBox.pack_start(self.diskSidepaneWidgetList[i],True,True,0)
        self.diskSidepaneWidgetList[i].disksidepanetextlabel.set_text(self.disklist[i])
        self.diskSidepaneWidgetList[i].givedata(self,i)

        self.diskSidepaneWidgetList[i].disk_switcher_button.connect('button-press-event',on_switcher_clicked,self.performanceStack,self)
        self.diskSidepaneWidgetList[i].disk_switcher_button.set_name(f'page{button_counter}')
        self.stack_switcher_buttons[button_counter]=self.diskSidepaneWidgetList[i].disk_switcher_button
        button_counter+=1

    if len(self.netNameList)!=0:
        self.netSidepaneWidgetList={}
        for i in range(0,self.numOfNets):
            self.netSidepaneWidgetList[i]=netSidepaneWidget()
            self.sidepaneBox.pack_start(self.netSidepaneWidgetList[i],True,True,0)
            self.netSidepaneWidgetList[i].netsidepanetextlabel.set_text(self.netNameList[i])
            self.netSidepaneWidgetList[i].givedata(self,i)

            self.netSidepaneWidgetList[i].net_switcher_button.connect('button-press-event',on_switcher_clicked,self.performanceStack,self)
            self.netSidepaneWidgetList[i].net_switcher_button.set_name(f'page{button_counter}')
            self.stack_switcher_buttons[button_counter]=self.netSidepaneWidgetList[i].net_switcher_button
            button_counter+=1

    if(self.isNvidiagpu==1):
        self.gpuSidePaneWidget=gpuSidepaneWidget()
        self.sidepaneBox.pack_start(self.gpuSidePaneWidget,True,True,0)
        self.gpuSidePaneWidget.gpusidepanetextlabel.set_text(f'{self.gpuName.split()[-2]}{self.gpuName.split()[-1]}')
        self.gpuSidePaneWidget.givedata(self)

        ## unknown signal bug fixed
        self.gpuSidePaneWidget.gpu_switcher_button.connect('button-press-event',on_switcher_clicked,self.performanceStack,self)
        self.gpuSidePaneWidget.gpu_switcher_button.set_name(f'page{button_counter}')
        self.stack_switcher_buttons[button_counter]=self.gpuSidePaneWidget.gpu_switcher_button
        button_counter+=1

    for i in self.hidden_stack_page_numbers:
        hide_devices(i, self)


def sidePaneUpdate(self):
    self.memSidePaneLabelValue.set_text(f'{self.usedd}/{self.memTotal} GiB\n{self.memPercent} %')

    ##disk sidepane
    for i in range(0,self.numOfDisks):
        try:
            self.diskSidepaneWidgetList[i].disksidepanelabelvalue.set_text(self.diskActiveString[i])

            self.diskSidepaneWidgetList[i].givedata(self,i)
        except Exception as e:
            print(f"some error in disksidepane update {e}")

    # net sidepane
    if(len(self.netNameList)!=0):
        for i in range(0,self.numOfNets):
            try:
                self.netSidepaneWidgetList[i].netsidepanelabelvalue.set_text(f'R:{self.byterecpersecString[i]}\nS:{self.bytesendpersecString[i]}')

                self.diskSidepaneWidgetList[i].givedata(self,i)
            except Exception as e:
                print(f"some error in netsidepane update {e}")

    if(self.isNvidiagpu==1):
        try:
            self.gpuSidePaneWidget.gpusidepanelabelvalue.set_text(self.gpuutil)
            self.gpuSidePaneWidget.givedata(self)
        except Exception as e:
            print(f"some error in gpusidepane update {e}")