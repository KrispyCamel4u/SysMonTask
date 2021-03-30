 
def on_plot_dialog_quit(widget):
    print("plot dialog quit")
    widget.destroy()

def plot_log(self,filename):
    try:
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_gtk3agg import (
            FigureCanvasGTK3Agg as FigureCanvas)
        from matplotlib.backends.backend_gtk3 import (
            NavigationToolbar2GTK3 as NavigationToolbar)
        from matplotlib.figure import Figure
        from gi.repository import Gtk as g
    except ImportError:
        print("matplotlib not found")
        return
    data=[[],[],[],[],[],[]]
    try:
        with open(filename) as ifile:
            ifile.readline()
            for line in ifile.readlines():
                line=line.split(',')
                for i,k in enumerate(line):
                    k=k.split()
                    if "%" in k[1]:
                        data[i].append(float(k[0]))
                    elif "M" in k[1]:
                        data[i].append(float(k[0]))
                    elif "K" in k[1]:
                        data[i].append(float(k[0])/1024)
                    elif "G" in k[1]:
                        data[i].append(float(k[0])*1024)
        
        step=5
        navg=range(2,len(data[0])-2)
        n=range(1,len(data[0])+1)
        avg=[[],[]] 
        
        avg[0]=[sum(data[0][i-2:i+3])/step for i in range(2,len(data[0])-2) ]
        avg[1]=[sum(data[1][i-2:i+3])/step for i in range(2,len(data[1])-2) ]

        fig, axs = plt.subplots(3, 2)

        fig.tight_layout()
        plt.sca(axs[0][0])
        plt.ylabel('rCPU [%]')
        plt.xlabel('Sample Number')
        axs[0][0].plot(n, data[0])
        axs[0][0].plot(navg, avg[0])
        axs[0][0].legend(['Normal',"Average"])

        plt.sca(axs[0][1])
        plt.ylabel('CPU %')
        plt.xlabel('Sample Number')
        axs[0][1].plot(n, data[1])
        axs[0][1].plot(navg, avg[1])
        axs[0][1].legend(['Normal',"Average"])
        
        plt.sca(axs[1][0])
        plt.ylabel('rMemory [MiB]')
        plt.xlabel('Sample Number')
        plt.plot(n, data[2])
        plt.sca(axs[1][1])
        plt.ylabel('Memory [MiB]')
        plt.xlabel('Sample Number')
        plt.plot(n, data[3])

        plt.sca(axs[2][0])
        plt.ylabel('DiskRead [MiB/s]')
        plt.xlabel('Sample Number')
        plt.plot(n, data[4])
        plt.sca(axs[2][1])
        plt.ylabel('DiskWrite [MiB/s]')
        plt.xlabel('Sample Number')
        plt.plot(n, data[5])

        plot_dialog=g.Window(title="SysMonTask Log Plot")
        plot_dialog.set_default_size(650,500)
        plot_box=g.VBox()
        plot_dialog.add(plot_box)

        swxx=g.ScrolledWindow()
        plot_box.pack_start(swxx, True, True, 0)
        canvas = FigureCanvas(fig)
        swxx.add(canvas)

        # Create toolbar
        toolbar = NavigationToolbar(canvas, plot_dialog)
        plot_box.pack_start(toolbar, False, False, 0)

        plot_dialog.connect("destroy",on_plot_dialog_quit)
        
        swxx.show_all()
        plot_dialog.show_all()
    except:
        print("error can't plot")

    
# plot_log("/home/neeraj/sysmontask_log/code.csv")