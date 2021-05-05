
from gi import  require_version
require_version("Gtk","3.0")
from gi.repository import Gtk as g

def fun(filename):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not found")
        not_found=g.Dialog(title="Can't Plot",parent=None,flags=g.DialogFlags.MODAL)
        content=not_found.get_content_area()
        label=g.Label()
        label.set_markup(
            """
         <b><big>matplotlib(python3-matplotlib) not found </big></b>.
         Please install using pip or package manager.
            """
        )
        content.add(label)
        label.show()
        not_found.show_all()
        not_found.run()
        not_found.destroy()
        return

    data=[[],[],[],[],[],[]]
    try:
        with open(filename) as ifile:
            ifile.readline()
            for line in ifile.readlines():
                line=line.split(',')
                for i,k in enumerate(line):
                    if "NA" in k:
                        data[i].append(0)
                        continue
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
        fig.canvas.set_window_title(f"Log_plot: {filename}")

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
        plt.show()
    except Exception as e:
        print(f"error can't plot: {e}")
        can_not_plot=g.Dialog(title="Can't Plot",parent=None,flags=g.DialogFlags.MODAL)
        content=can_not_plot.get_content_area()
        label=g.Label()
        label.set_markup(
            """
         <b><big>Error Encountered While Plotting.</big></b>
          "<b>.csv</b>" type files required, check if the selected file
          is of correct type and not currupted.
            """
        )
        content.add(label)
        label.show()
        can_not_plot.show_all()
        can_not_plot.run()
        can_not_plot.destroy()

# def on_plot_dialog_quit(widget,FigureCanvas,plt,NavigationToolbar):
#     print("plot dialog quit")
#     widget.destroy()

# def plot_log(filename):
#     try:
#         import matplotlib.pyplot as plt
#         from matplotlib.backends.backend_gtk3agg import (
#             FigureCanvasGTK3Agg as FigureCanvas)
#         from matplotlib.backends.backend_gtk3 import (
#             NavigationToolbar2GTK3 as NavigationToolbar)
#         # from matplotlib.figure import Figure
#         # raise ImportError

#     except ImportError:
#         print("matplotlib not found")
#         not_found=g.Dialog(title="Can't Plot",parent=None,flags=g.DialogFlags.MODAL)
#         content=not_found.get_content_area()
#         label=g.Label()
#         label.set_markup(
#             """
#          <b><big>matplotlib(python3-matplotlib) not found </big></b>.
#          Please install using pip or package manager.
#             """
#         )
#         content.add(label)
#         label.show()
#         not_found.show_all()
#         r=not_found.run()
#         not_found.destroy()
#         return

#     data=[[],[],[],[],[],[]]
#     try:
#         with open(filename) as ifile:
#             ifile.readline()
#             for line in ifile.readlines():
#                 line=line.split(',')
#                 for i,k in enumerate(line):
#                     k=k.split()
#                     if "%" in k[1]:
#                         data[i].append(float(k[0]))
#                     elif "M" in k[1]:
#                         data[i].append(float(k[0]))
#                     elif "K" in k[1]:
#                         data[i].append(float(k[0])/1024)
#                     elif "G" in k[1]:
#                         data[i].append(float(k[0])*1024)

#         step=5
#         navg=range(2,len(data[0])-2)
#         n=range(1,len(data[0])+1)
#         avg=[[],[]]

#         avg[0]=[sum(data[0][i-2:i+3])/step for i in range(2,len(data[0])-2) ]
#         avg[1]=[sum(data[1][i-2:i+3])/step for i in range(2,len(data[1])-2) ]

#         fig, axs = plt.subplots(3, 2)

#         fig.tight_layout()
#         plt.sca(axs[0][0])
#         plt.ylabel('rCPU [%]')
#         plt.xlabel('Sample Number')
#         axs[0][0].plot(n, data[0])
#         axs[0][0].plot(navg, avg[0])
#         axs[0][0].legend(['Normal',"Average"])

#         plt.sca(axs[0][1])
#         plt.ylabel('CPU %')
#         plt.xlabel('Sample Number')
#         axs[0][1].plot(n, data[1])
#         axs[0][1].plot(navg, avg[1])
#         axs[0][1].legend(['Normal',"Average"])

#         plt.sca(axs[1][0])
#         plt.ylabel('rMemory [MiB]')
#         plt.xlabel('Sample Number')
#         plt.plot(n, data[2])
#         plt.sca(axs[1][1])
#         plt.ylabel('Memory [MiB]')
#         plt.xlabel('Sample Number')
#         plt.plot(n, data[3])

#         plt.sca(axs[2][0])
#         plt.ylabel('DiskRead [MiB/s]')
#         plt.xlabel('Sample Number')
#         plt.plot(n, data[4])
#         plt.sca(axs[2][1])
#         plt.ylabel('DiskWrite [MiB/s]')
#         plt.xlabel('Sample Number')
#         plt.plot(n, data[5])

#         plot_dialog=g.Window(title="SysMonTask Log Plot")
#         plot_dialog.set_default_size(650,500)
#         plot_box=g.VBox()
#         plot_dialog.add(plot_box)

#         swxx=g.ScrolledWindow()
#         plot_box.pack_start(swxx, True, True, 0)
#         canvas = FigureCanvas(fig)
#         swxx.add(canvas)

#         # Create toolbar
#         toolbar = NavigationToolbar(canvas, plot_dialog)
#         plot_box.pack_start(toolbar, False, False, 0)

#         plot_dialog.connect("destroy",on_plot_dialog_quit,FigureCanvas,plt,NavigationToolbar)

#         swxx.show_all()
#         plot_dialog.show_all()
#         # fig.clf()
#         # gc.collect()

#     except Exception as e:
#         print(f"error can't plot: {e}")
#         can_not_plot=g.Dialog(title="Can't Plot",parent=None,flags=g.DialogFlags.MODAL)
#         content=can_not_plot.get_content_area()
#         label=g.Label()
#         label.set_markup(
#             """
#          <b><big>Error Encountered While Plotting.</big></b>
#           "<b>.csv</b>" type files required, check if the selected file
#           is correct and not currupted.
#             """
#         )
#         content.add(label)
#         label.show()
#         can_not_plot.show_all()
#         r=can_not_plot.run()
#         can_not_plot.destroy()


# plot_log("/home/neeraj/sysmontask_log/code.csv")
import sys
fun(sys.argv[1])