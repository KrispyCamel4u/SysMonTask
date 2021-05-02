from gi.repository import Gtk as g , GLib as go,Gio,Gdk
import cairo
from os import popen
from re import sub
import os
import psutil as ps

def cpuInit(self):
    print('cpuInit')
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
    
    self.speed=ps.cpu_freq()
    self.cpuMxSpeedLabelValue.set_text('{:.2f} GHz'.format(self.speed[2]/1000))
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


def cpuUpdate(self):
    self.speed=ps.cpu_freq()

    #print("setting speed")
    cpuSpeedstring="{:.2f} Ghz".format(self.speed[0]/1000)
    self.cpuSpeedLabelValue.set_text(cpuSpeedstring)
    #print("speed setting done")

    self.cpuUtil=ps.cpu_percent() ## % of the time is is working
    
    #print("setting utilisation")
    cpuUtilString="{0}%".format(int(self.cpuUtil))
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
        else:
            try:
                fan_list = ps.sensors_fans()
                cpu_temp = cpuTempByFanMatching(temperatures_list, fan_list)
                self.cpuTempLabelValue.set_text('{0} °C'.format(int(cpu_temp.current)))
            except:
                pass

        # cpu fan speed
    except:
        pass
    self.cpuSidePaneLabelValue.set_text(f'{cpuUtilString} {cpuSpeedstring}')

    ## cpu utilisation graph
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


def cpuTempByFanMatching(sensors_temp, sensors_fan):
    temp_keys = list(sensors_temp.keys())
    fan_keys = list(sensors_fan.keys())

    # Detect first fan key which matches temperature key
    try:
       sensor_name = helperMatchFirstKey(temp_keys, fan_keys)
    except NameError:
       raise NameError("Cannot identify cpu sensor")

    # Return first temperature
    temps = sensors_temp[sensor_name]
    return temps[0]


def helperMatchFirstKey(temp_keys, fan_keys):
    for fan_name in fan_keys:
        for temp_name in temp_keys:
            if fan_name == temp_name:
                return temp_name
    raise NameError("No matching fan and temperature name found!")
