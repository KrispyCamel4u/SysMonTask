#!/usr/bin/env python3
# import gi
# gi.require_version("Gtk", "3.24")

from gi.repository import Gtk as g,Gdk
import psutil as ps
from time import time
from os import popen

# Importing neccessary files
try:
    from gi_composites import GtkTemplate
except ImportError:
    from sysmontask.gi_composites import GtkTemplate

if __name__=='sysmontask.disk':
    from sysmontask.sysmontask import files_dir
    from sysmontask.gproc import sorting_func,byte_to_human
else:
    from sysmontask import files_dir
    from gproc import sorting_func,byte_to_human

@GtkTemplate(ui=files_dir+'/disk.glade')
class diskTabWidget(g.ScrolledWindow):
    """
    A disk tab widget(top level box with all childs fields) which is made by the gtk template.
    """

    # Required else you would need to specify the full module
    # name in mywidget.ui (__main__+MyWidget)
    __gtype_name__ = 'diskTabWidget'

    # Declaring/Fetching/Assigning the required childs(name in the template should be the same as used here)
    disktextlabel= GtkTemplate.Child()
    diskinfolabel = GtkTemplate.Child()
    diskdrawarea1=GtkTemplate.Child()
    diskdrawarea2=GtkTemplate.Child()
    disktextlabel=GtkTemplate.Child()
    diskactivelabelvalue=GtkTemplate.Child()
    diskreadlabelvalue=GtkTemplate.Child()
    diskwritelabelvalue=GtkTemplate.Child()
    diskcurrenspeedlabelvalue=GtkTemplate.Child()
    diskUsagesTreeView=GtkTemplate.Child()

    disk_read_color_descriptor= GtkTemplate.Child()
    disk_write_color_descriptor= GtkTemplate.Child()

    # Alternative way to specify multiple widgets
    #label1, entry = GtkTemplate.Child.widgets(2)

    def __init__(self):
        """Constructing the Disk Widget."""
        super(g.ScrolledWindow, self).__init__()

        # This must occur *after* you initialize your base
        self.init_template()
        # For the scaling of maximum value on the graph
        self.diskmxfactor=1
        self.secondself=None # main class

    def givedata(self,secondself,index):
        """
        Method to pass the data to the class object from outside. And assign them to the local class variables.

        Parameters
        ----------
        secondself : the main class reference(the main self) which will be calling this function.
        index : index of the disk from several disks
        """
        self.diskactiveArray=secondself.diskActiveArray[index]
        self.diskreadArray=secondself.diskReadArray[index]
        self.diskwriteArray=secondself.diskWriteArray[index]
        self.secondself=secondself

    @GtkTemplate.Callback
    def on_diskDrawArea1_draw(self,dr,cr):
        """
        Function Binding(for draw signal) for Disk Utilisation draw area.

        This function draw the Disk's Utilisation curves upons called by the queue of request in the updator
        function.

        Parameters
        ----------
        dr : the widget on which to draw the graph
        cr : the cairo surface object
        """
        cr.set_line_width(2)

        # Color Pofile setup
        color=self.secondself.color_profile['disk'][0]
        rectangle_color=self.secondself.color_profile['disk'][1]

        # Get the allocated width and height
        w=self.diskdrawarea1.get_allocated_width()
        h=self.diskdrawarea1.get_allocated_height()

        # Vertical step size
        scalingfactor=h/100.0

        #creating outer rectangle
        # cr.set_source_rgba(.109,.670,.0588,1)
        cr.set_source_rgba(*rectangle_color,1)
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.stroke()

        # creating grid lines
        verticalGap=int(h/10)
        horzontalGap=int(w/10)
        for i in range(1,10):
            # cr.set_source_rgba(.109,.670,.0588,1) #for changing the outer line color
            cr.set_source_rgba(*color,1)
            cr.set_line_width(0.5)
            cr.move_to(0,i*verticalGap)
            cr.line_to(w,i*verticalGap)

            cr.move_to(i*horzontalGap,0)
            cr.line_to(i*horzontalGap,h)
            cr.stroke()
        cr.stroke()

        # Horizontal step size
        stepsize=w/99.0

        # Drawing the outer lines for the curve
        # cr.set_source_rgba(.109,.670,.0588,1) #for changing the outer line color
        cr.set_source_rgba(*color,1)
        cr.set_line_width(1.5)
        cr.move_to(0,scalingfactor*(100-self.diskactiveArray[0])+2)
        for i in range(0,99):
            cr.line_to((i+1)*stepsize,scalingfactor*(100-self.diskactiveArray[i+1])+2)
        cr.stroke_preserve()

        # Filling the curve
        # cr.set_source_rgba(.431,1,.04,0.25)  #for changing the fill color
        cr.set_source_rgba(*color,0.25)
        cr.line_to(w,h)
        cr.line_to(0,h)
        cr.move_to(0,scalingfactor*(100-self.diskactiveArray[0])+2)
        cr.fill()
        cr.stroke()

        return False

    @GtkTemplate.Callback
    def on_diskDrawArea2_draw(self,dr,cr):
        """
        Function Binding(for draw signal) for disk speed draw area.

        This function draw the Disk's Read and Write speed curves upon called by the queue of request generated in the
        main updator function.

        Parameters
        ----------
        dr : the widget on which to draw the graph
        cr : the cairo surface object
        """
        cr.set_line_width(2)

        # Color Pofile setup
        color=self.secondself.color_profile['disk'][0]
        rectangle_color=self.secondself.color_profile['disk'][1]

        self.disk_read_color_descriptor.set_markup(f'<span size="20000" foreground="{"#%02x%02x%02x" % (int(color[0]*255), int(color[1]*255), int(color[2]*255))}">|</span>')
        self.disk_write_color_descriptor.set_markup(f'<span size="20000" foreground="{"#%02x%02x%02x" % (int(color[0]*255), int(color[1]*255), int(color[2]*255))}">¦</span>')

        # Get the allocated widht and height
        w=self.diskdrawarea2.get_allocated_width()
        h=self.diskdrawarea2.get_allocated_height()

        # Speed step in MB/s is the step in which the maximum speed(vertical scale) will adjust for dynamic speeds, i.e, in multiples
        # of this step.
        speedstep=50
        # The maximum read or write speeds in the buffer
        maximumcurrentspeed=max(max(self.diskreadArray),max(self.diskwriteArray))
        # The current maximum scale speed
        currentscalespeed=self.diskmxfactor*speedstep

        # vertical scale adjustment calculation, i.e, new maximum scale speed
        if(currentscalespeed<maximumcurrentspeed):
            while(currentscalespeed<maximumcurrentspeed):
                self.diskmxfactor+=1
                currentscalespeed=self.diskmxfactor*speedstep
        else:
            while(currentscalespeed>maximumcurrentspeed+speedstep and self.diskmxfactor>1):
                self.diskmxfactor-=1
                currentscalespeed=self.diskmxfactor*speedstep

        # Setting new maximum scale label
        self.diskcurrenspeedlabelvalue.set_text(str(currentscalespeed)+'MB/s')

        # vertical scaling factor(step)
        scalingfactor=h/currentscalespeed

        #creating outer rectangle
        # cr.set_source_rgba(.109,.670,.0588,1)
        cr.set_source_rgba(*rectangle_color,1)
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.stroke()

        # creating grid lines
        verticalGap=int(h/10)
        horzontalGap=int(w/10)
        for i in range(1,10):
            # cr.set_source_rgba(.109,.670,.0588,1) #for changing the grid line color
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

        ## Read Speed ##
        # Drawing the curve line
        # cr.set_source_rgba(.109,.670,.0588,1) #for changing the outer line color
        cr.set_source_rgba(*color,1)
        cr.set_line_width(1.5)
        cr.move_to(0,scalingfactor*(currentscalespeed-self.diskreadArray[0])+2)
        for i in range(0,99):
            cr.line_to((i+1)*stepsize,scalingfactor*(currentscalespeed-self.diskreadArray[i+1])+2)
        cr.stroke_preserve()

        # Filling the curve with solid color, the curve(shape) should be a closed then only it can be filled
        # cr.set_source_rgba(.431,1,.04,0.25)  #for changing the fill color
        cr.set_source_rgba(*color,0.2)
        cr.line_to(w,h)
        cr.line_to(0,h)
        cr.move_to(0,scalingfactor*(currentscalespeed-self.diskreadArray[i])+2)
        cr.fill()
        cr.stroke()

        ## Write Speed ##
        # Drawing the outer lines for the curve
        # cr.set_source_rgba(.207,.941,.682,1) #for changing the outer line color
        cr.set_source_rgba(*color,1)
        cr.set_line_width(1.5)
        cr.move_to(0,scalingfactor*(currentscalespeed-self.diskwriteArray[0])+2)
        # Dash line configuration
        cr.set_dash([3.0,3.0])
        for i in range(0,99):
            cr.line_to((i+1)*stepsize,scalingfactor*(currentscalespeed-self.diskwriteArray[i+1])+2)
        cr.stroke_preserve()

        # Filling the curve
        # cr.set_source_rgba(.207,.941,.682,0.3)  #for changing the fill color
        cr.set_source_rgba(*color,0.2)
        cr.line_to(w,h)
        cr.line_to(0,h)
        cr.move_to(0,scalingfactor*(currentscalespeed-self.diskwriteArray[0])+2)
        cr.fill()
        cr.stroke()

        return False



def diskinit(self):
    """
    Initilization of the Disk Components.
    """
    # Declaring the lists to hold the name and size of the disks.
    self.disklist=[]
    self.disksize=[]

    # Getting the name and size of the disks using shell command,(excluding zrams)
    try:
        p=popen('lsblk -d | grep -e ^NAME -e disk')
        partitions=p.readlines()
        p.close()
        for parts in partitions:
            tempparts=parts.split()
            if 'NAME' not in  tempparts[0] and 'zram' not in tempparts[0]:
                self.disklist.append(tempparts[0])
                self.disksize.append(tempparts[3])
                print(tempparts[0])
    except Exception as e:
        print(f"Failed to get Disks: {e}")

    # Declaring the Lists and dictionary for data holding
    self.diskWidgetList={}
    self.diskstate1=[]
    self.diskActiveArray=[]
    self.diskReadArray=[]
    self.diskWriteArray=[]
    self.numOfDisks=len(self.disklist)

    # For partition information
    self.diskPartitions={}
    self.diskListStores={}
    self.diskListStoreItrs={}
    partitions=ps.disk_partitions()

    # for scanning each
    for i in range(0,self.numOfDisks):
        # Creating a disk tab widget
        self.diskWidgetList[i]=diskTabWidget()
        # Adding to the stack
        self.performanceStack.add_titled(self.diskWidgetList[i],f'page{self.stack_counter}','Disk'+str(i))
        # For lookup devices and its assigned page number
        self.device_stack_page_lookup[self.disklist[i]]=self.stack_counter
        # Incrementing the stack counter to be used for side pane
        self.stack_counter+=1
        # Setting the labels for a disk at index i
        self.diskWidgetList[i].disktextlabel.set_text(self.disklist[i])
        self.diskWidgetList[i].diskinfolabel.set_text(self.disksize[i])
        # Getting th I/O of disk
        disktemp=ps.disk_io_counters(perdisk=True)
        # Time for the previous data
        self.diskt1=time()
        # Storing the state1 of the different disks
        for drives in disktemp:
            if drives==self.disklist[i]:
               self.diskstate1.append(disktemp[drives])

        # partition info
        self.diskPartitions[i]=[]
        for part in partitions:
            if self.disklist[i] in part[0]:
                self.diskPartitions[i]+=[part]

        # ListStore for treeview of disk storage
        self.diskListStores[i]=g.ListStore(str,str,str,str,str,int,bool)
        self.diskListStoreItrs[i]=[]    # list of iterators for each row for a disk
        # Storing the values in the list stores
        for part in self.diskPartitions[i]:
            temp=ps.disk_usage(part[1])
            itr=self.diskListStores[i].append([part[0],part[1],part[2],byte_to_human(temp[0],persec=False),byte_to_human(temp[1],persec=False),temp[3],False])
            self.diskListStoreItrs[i].append(itr)

        # setting the model(liststore) for the treeview
        self.diskWidgetList[i].diskUsagesTreeView.set_model(self.diskListStores[i])

        # Iterating for making each column in the disk treeview
        for k,col in enumerate(['Device','MountPoint','Type','Total','Used']):
            # Text renderer
            renderer=g.CellRendererText()
            # Creating a column and assigning additional properties based on type
            if col=='Used':
                column=g.TreeViewColumn(col)
                progRenderer=g.CellRendererProgress()
                # progRenderer.props.text='50%'
                # progRenderer.props.fraction=0.5
                column.pack_start(renderer,False)
                column.add_attribute(renderer,"text",4)
                column.pack_start(progRenderer,False)
                column.add_attribute(progRenderer,"value",5)
                # column=g.TreeViewColumn(col,progRenderer,value=5,inverted=6)

            else:
                column=g.TreeViewColumn(col,renderer,text=k)

            # Making each column sortable, resizable, and reorderable
            column.set_sort_column_id(k)
            column.set_resizable(True)
            column.set_reorderable(True)
            # column.set_expand(True)
            column.set_alignment(0)
            column.set_sort_indicator(True)
            # Appending the column to the disk treestore
            self.diskWidgetList[i].diskUsagesTreeView.append_column(column)

            # self.processTreeStore.set_sort_func(i,sorting_func,None)

        # Setting the custom sorting fucntion for the column 3(used column)
        self.diskListStores[i].set_sort_func(3,sorting_func,3)

        # data holding arrays
        self.diskActiveArray.append([0]*100)
        self.diskReadArray.append([0]*100)
        self.diskWriteArray.append([0]*100)

        # Providing the data to the disktab widget class
        self.diskWidgetList[i].givedata(self,i)



def diskTabUpdate(self):
    """
    Function to periodically update DISKs statistics.
    """
    # getting the disk I/O and the current time
    disktemp :dict(read_count,write_count,read_bytes,write_bytes,read_time,write_time,mrc,wrc,busy_time)=ps.disk_io_counters(perdisk=True)
    self.diskt2=time()##

    # Time elapsed from the previous update
    timediskDiff=self.diskt2-self.diskt1

    # Array for current state
    self.diskstate2=[]

    # Updating the disk storage tree view(partitions)
    for i in range(0,self.numOfDisks):
        try:
            # New disk I/O state
            self.diskstate2.append(disktemp[self.disklist[i]])

            for j,part in enumerate(self.diskPartitions[i]):
                temp=ps.disk_usage(part[1])
                self.diskListStores[i].set(self.diskListStoreItrs[i][j],3,byte_to_human(temp[0],persec=False),4,byte_to_human(temp[1],persec=False),5,temp[3])
        except Exception as e:
            print(f"error in diskliststore: {e}")

    # list to store the difference between the previous and the current disk state and to hold the disk active(utilisation)
    self.diskActiveString=[]

    for i in range(0,self.numOfDisks):
        try:
            # Calclulating the difference between current and previous disk state
            diskDiff :list =[self.diskstate2[i].read_bytes-self.diskstate1[i].read_bytes\
                ,self.diskstate2[i].write_bytes-self.diskstate1[i].write_bytes\
                ,self.diskstate2[i].busy_time-self.diskstate1[i].busy_time]

            # Disk active(utilisation) percentage
            active_percetage=int(diskDiff[2]/(10*timediskDiff))
            if active_percetage>100: active_percetage=100
            self.diskActiveString.append(f'{active_percetage}%')

            # Setting the info labels , 1024*1024=1048576 for MiB coversion
            self.diskWidgetList[i].diskactivelabelvalue.set_text(self.diskActiveString[i])
            self.diskWidgetList[i].diskreadlabelvalue.set_text("{:.1f} MiB/s".format(diskDiff[0]/(timediskDiff*1048576)))
            self.diskWidgetList[i].diskwritelabelvalue.set_text("{:.1f} MiB/s".format(diskDiff[1]/(timediskDiff*1048576)))

            # updating the sample data holding array depending upon the direction 1: newer on right
            if self.update_graph_direction:
                self.diskActiveArray[i].pop(0)
                self.diskActiveArray[i].append((diskDiff[2])/(10*timediskDiff))##

                self.diskReadArray[i].pop(0)
                self.diskReadArray[i].append(diskDiff[0]/(timediskDiff*1048576))

                self.diskWriteArray[i].pop(0)
                self.diskWriteArray[i].append(diskDiff[1]/(timediskDiff*1048576))
            else:
                self.diskActiveArray[i].pop()
                self.diskActiveArray[i].insert(0,(diskDiff[2])/(10*timediskDiff))##

                self.diskReadArray[i].pop()
                self.diskReadArray[i].insert(0,diskDiff[0]/((timediskDiff)*1048576))

                self.diskWriteArray[i].pop()
                self.diskWriteArray[i].insert(0,diskDiff[1]/((timediskDiff)*1048576))

            # passing data to the disk tab widget class
            self.diskWidgetList[i].givedata(self,i)
        except Exception as e:
            print(f'error in  disk update: {e}')

    # assigning the previous state/time to the current one
    self.diskstate1=self.diskstate2
    self.diskt1=self.diskt2








