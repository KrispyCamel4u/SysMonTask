from gi.repository import Gtk as g
from os import popen
from re import sub
import psutil as ps

def cpuInit(self):
    """
    Initialization of CPU components.
    """
    print('cpuInit')

    # Drawing area for cpu utilisation
    self.cpuDrawArea=self.builder.get_object('cpudrawarea')

    # CPU utilisation array of 100 samples
    self.cpuUtilArray=[0]*100

    # Finding the logical cores and declaring the list for storing the utilisation arrays
    self.cpu_logical_cores=ps.cpu_count()
    self.cpu_logical_cores_util_arrays=[]
    temp=ps.cpu_percent(percpu=True)
    for i in range(self.cpu_logical_cores):
        self.cpu_logical_cores_util_arrays.append([0]*100)
        self.cpu_logical_cores_util_arrays[i].append(temp[i])

    # Grid for containing the logical cpu utilization graphs
    self.logical_cpu_grid=self.builder.get_object('logical_grid_area')

    # Getting and assigning objects declared in the glade file
    ## cpu draw tab labels
    self.cpuInfoLabel=self.builder.get_object('cpuinfolabel')
    ## cpu utilisation label
    self.cpuUtilLabelValue=self.builder.get_object('cpuutilisation')
    # cpu speed label
    self.cpuSpeedLabelValue=self.builder.get_object('cpuspeed')
    # processes
    self.cpuProcessesLabelValue=self.builder.get_object('cpuprocesses')
    self.cpuThreadsLabelValue=self.builder.get_object('cputhreads')

    ## other cpu info objects
    self.cpuCoreLabelValue=self.builder.get_object('cpucoreslablevalue')
    self.cpuLogicalLabelValue=self.builder.get_object('cpulogicallabelvalue')
    self.cpuVirtualisationLabelValue=self.builder.get_object('cpuvirtualisationlabelvalue')
    self.cpuL1LabelValue=self.builder.get_object('cpul1labelvalue')
    self.cpuL2LabelValue=self.builder.get_object('cpul2labelvalue')
    self.cpuL3LabelValue=self.builder.get_object('cpul3labelvalue')
    self.cpuTempLabelValue=self.builder.get_object('cputemplabelvalue')
    self.cpuFanSpeedLabelValue=self.builder.get_object('cpufanspeedlabelvalue')
    self.cpuMxSpeedLabelValue=self.builder.get_object('cpumxspeedlabelvalue')

    try:
        ## for the first time only to get the name of the cpu
        p=popen('cat /proc/cpuinfo |grep -m1 "model name"')
        self.cpuname=p.read().split(':')[1].split('\n')[0]
        self.cpuInfoLabel.set_text(self.cpuname)
        self.cpuInfoLabel.set_valign(g.Align.CENTER)
        p.close()
    except:
        print("Failed to get model information")

    # Number of cores and logical cores available
    self.cpuCoreLabelValue.set_text(str(ps.cpu_count(logical=False)))
    self.cpuLogicalLabelValue.set_text(str(self.cpu_logical_cores))

    # Virtualisation Info
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

    # CPU Caches
    try:
        p=popen('lscpu|grep -i -m1 "L1d"')
        self.cpuL1LabelValue.set_text(sub("[\s]","",p.read().split(':')[1]))
        p.close()

        p=popen('lscpu|grep -i -m1 "L2"')
        self.cpuL2LabelValue.set_text(sub('[\s]','',p.read().split(':')[1]))
        p.close()

        p=popen('lscpu|grep -i "L3"')
        self.cpuL3LabelValue.set_text(sub('[\s]','',p.read().split(':')[1]))
        p.close()
    except:
        print("Failed to get Cache information")

    # CPU Frequency
    self.speed=ps.cpu_freq()
    self.cpuMxSpeedLabelValue.set_text('{:.2f} GHz'.format(self.speed[2]/1000))

    # Number fo drawing widgets to put in one column for different logical cpu counts
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
        32:8,
        34:7,
        36:9,
        38:8,
        40:8,
        42:7,
        48:8,
        50:10,
        64:8
    }

    ## logical
    self.cpu_logical_cores_draw_areas=[]
    row,column=0,0
    try:
        col_max=self.num_of_column_per_row[self.cpu_logical_cores]
    except Exception:
        col_max=10

    # Creating and Arranging the Logical CPU Drawing widgets to the grid format
    for cpu_index in range(self.cpu_logical_cores):
        draw_area=g.DrawingArea()
        draw_area.set_name(str(cpu_index))
        self.cpu_logical_cores_draw_areas.append(draw_area)
        # draw_area=g.Button(label="begin{0}".format(cpu_index))
        if column < col_max:
            self.logical_cpu_grid.attach(draw_area,column,row,1,1)
            column+=1
        else:
            column=0
            row+=1
            self.logical_cpu_grid.attach(draw_area,column,row,1,1)
            column+=1
        draw_area.connect('draw',self.on_cpu_logical_drawing)

    self.logical_cpu_grid.show_all()


def cpuUpdate(self):
    """
    Function to periodically update CPU statistics.
    """
    # CPU frequency
    self.speed=ps.cpu_freq()
    cpuSpeedstring="{:.2f} Ghz".format(self.speed[0]/1000)
    self.cpuSpeedLabelValue.set_text(cpuSpeedstring)

    # CPU Utilisation
    self.cpuUtil=ps.cpu_percent() ## % of the time is is working
    cpuUtilString="{0}%".format(int(self.cpuUtil))
    self.cpuUtilLabelValue.set_text(cpuUtilString)

    # Setting number of processes and threads")
    self.cpuProcessesLabelValue.set_text(str(len(ps.pids())))
    try:
        p=popen("ps axms|wc -l")
        self.cpuThreadsLabelValue.set_text(sub('[\s]','',p.read()))
        p.close()
    except:
        print("Failed to get Threads")

    try:
        #cpu package temp
        temperatures_list=ps.sensors_temperatures()
        if 'coretemp' in temperatures_list:
            self.cpuTempLabelValue.set_text('{0} °C'.format(int(temperatures_list['coretemp'][0][1])))

        ## amd cpu package temp
        elif 'k10temp' in temperatures_list:
            for lis in temperatures_list['k10temp']:
                if lis.label=='Tdie':
                    self.cpuTempLabelValue.set_text('{0} °C'.format(int(lis.current)))
                    break
        elif 'zenpower' in temperatures_list:
            for lis in temperatures_list['zenpower']:
                if lis.label=='Tdie':
                    self.cpuTempLabelValue.set_text('{0} °C'.format(int(lis.current)))
                    break

    except:
        pass

    # CPU SidePane utilization lable
    self.cpuSidePaneLabelValue.set_text(f'{cpuUtilString} {cpuSpeedstring}')

    ## cpu utilisation graph(aggregate and logical) data holding array updation depending on direction
    temp=ps.cpu_percent(percpu=True)
    if self.update_graph_direction:
        self.cpuUtilArray.pop(0)
        self.cpuUtilArray.append(self.cpuUtil)
        for i in range(self.cpu_logical_cores):
            self.cpu_logical_cores_util_arrays[i].pop(0)
            self.cpu_logical_cores_util_arrays[i].append(temp[i])
    else:
        self.cpuUtilArray.pop()
        self.cpuUtilArray.insert(0,self.cpuUtil)
        for i in range(self.cpu_logical_cores):
            self.cpu_logical_cores_util_arrays[i].pop()
            self.cpu_logical_cores_util_arrays[i].insert(0,temp[i])