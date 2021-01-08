# import gi
# gi.require_version("Gtk", "3.24")

from gi.repository import Gtk as g,cairo
from gi_composites import GtkTemplate


@GtkTemplate(ui='diskSidepane.glade')
class diskSidepaneWidget(g.Box):

    # Required else you would need to specify the full module
    # name in mywidget.ui (__main__+MyWidget)
    __gtype_name__ = 'diskSidepaneWidget'
    
    disksidepanetextlabel= GtkTemplate.Child()
    disksidepanelabelvalue = GtkTemplate.Child()
    disksidepanedrawarea=GtkTemplate.Child()


    # Alternative way to specify multiple widgets
    #label1, entry = GtkTemplate.Child.widgets(2)

    def __init__(self):
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


def sidepaneinit(self):
    print("initialisating sidepane")
    self.cpuSidePaneLabelValue=self.builder.get_object('cpusidepanelabelvalue')
    self.cpuSidePaneDrawArea=self.builder.get_object('cpusidepanedrawarea')

    self.memSidePaneLabelValue=self.builder.get_object('memsidepanelabelvalue')
    self.memSidePaneDrawArea=self.builder.get_object('memsidepanedrawarea')

    self.diskSidepaneWidgetList={}
    for i in range(0,self.numOfDisks):
        self.diskSidepaneWidgetList[i]=diskSidepaneWidget()
        self.sidepaneBox.pack_start(self.diskSidepaneWidgetList[i],True,True,0)
        self.diskSidepaneWidgetList[i].disksidepanetextlabel.set_text(self.disklist[i])
        self.diskSidepaneWidgetList[i].givedata(self,i)


def sidePaneUpdate(self):
    self.memSidePaneLabelValue.set_text(str(self.usedd)+'/'+str(self.memTotal)+" GiB\n"+str(self.memPercent)+' %')
    
    for i in range(0,self.numOfDisks):
        self.diskSidepaneWidgetList[i].disksidepanelabelvalue.set_text(self.diskActiveString[i])

        self.diskSidepaneWidgetList[i].givedata(self,i)