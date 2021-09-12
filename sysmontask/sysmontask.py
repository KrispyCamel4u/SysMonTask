#!/usr/bin/env python3
############ container missing error in some distro #############
from gi import require_version
require_version("Gtk", "3.0")
require_version("Wnck", "3.0")
###############################################################
try:
    from rooter import theme_agent
except ImportError:
    from sysmontask.rooter import theme_agent

theme_agent()
import os

with open("{}/.sysmontask".format(os.environ.get("HOME")),'w+') as ofile:
    ofile.write('0')

from gi.repository import Gtk as g , GLib as go,Gio,Gdk
import psutil as ps

print(ps.__version__)
if( not ps.__version__>='5.7.2'):
    print('warning[critical]: psutil>=5.7.2 needed(system-wide)')

""" Importing neccessary Files """
try:
    # for running as main file
    files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../glade_files")
    icon_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../icons")
    from cpu import *
    from mem import *
    from sidepane import *
    from disk import *
    from net import *
    from gpu import *
    from filter_prefs import *
    from gproc import *
    # from log_plotter import *

except ImportError:
    # for module level through  apt install comment it if running as main file
    files_dir="/usr/share/sysmontask/glade_files"
    icon_file='/usr/share/sysmontask/icons'
    from sysmontask.cpu import *
    from sysmontask.mem import *
    from sysmontask.sidepane import *
    from sysmontask.disk import *
    from sysmontask.net import *
    from sysmontask.gpu import *
    from sysmontask.filter_prefs import *
    from sysmontask.gproc import *
    # from sysmontask.log_plotter import *

VERSION_INT =2

class whatsnew_notice_dialog(g.Dialog):
    """ Class for What's New Dialog, inheriting the GtkDialog class."""

    def __init__(self,parentWindow,parent):
        """Initialize the Dialog."""
        g.Dialog.__init__(self,"What's New",parentWindow,g.DialogFlags.MODAL)
        self.set_border_width(20)
        content_area=self.get_content_area()
        label=g.Label()
        label.set_markup(
        """
        <b><span size='20000'>New Feature #v1.x.x </span></b>
          * <b><big>Color Customizations</big></b>
              Color for each devices can be changed.
          * <b><big>Hide/Show Devices</big></b>
              Now each device can be hide permanantly.
          * <b><big>Bug fixes and Small Visual Improvements</big></b>
              For details visit:<a href='https://github.com/KrispyCamel4u/SysMonTask'>https://github.com/KrispyCamel4u/SysMonTask/</a>
            -------------------------------------------------------------------------------------------------
            <b>Previous highlights</b>
            -------------------------------------------------------------------------------------------------
          * <b><big>Filter Dialog</big></b>
              Can be accessed through : view->filter
              User can define his/her own filtering words to exclude the unwanted processes.
              Filter Dialog follow <b><big>strict semantic and formating rules</big></b> for adding a new entry.
              For more information of rules and filter dialog, visit:
              <a href='https://github.com/KrispyCamel4u/SysMonTask/blob/master/DOCS.md#filter-dialog-view-filter'>https://github.com/KrispyCamel4u/SysMonTask/blob/master/DOCS.md</a>
          * <b><big>Process Log Record</big></b>(at lower right corner in process tab)
          * <b><big>Log plotter</big></b>(Tools->Log_plot)
          * Bug fixes, optimisation and support for all desktop enviornments.
        """
        )
        content_area.add(label)
        self.show_all()

class myclass:
    """ The main Class which manages everything"""

    flag=0      #flag for the updator
    resizerflag=0
    def __init__(self):
        """All components will be initialized here."""
        import time
        stt=time.time()

        # Object for fetcting the global setting saved by GLIB schema.
        self.settings=Gio.Settings.new('com.github.camelneeraj.sysmontask')

        # Load and Embed the CSS stylesheet
        style_provider = g.CssProvider()
        css = open(f'{os.path.dirname(os.path.abspath(__file__))}/style.css','rb') # rb needed for python 3 support
        css_data = css.read()
        css.close()

        style_provider.load_from_data(css_data)

        g.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,
            g.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        #Methods and variables defined in other files, making them into the class methods and variables.
        myclass.cpuInit=cpuInit
        myclass.cpuUpdate=cpuUpdate

        myclass.memoryinitalisation=memorytabinit
        myclass.memoryTab=memoryTabUpdate

        myclass.sidepaneinitialisation=sidepaneinit
        myclass.sidepaneUpdate=sidePaneUpdate

        myclass.diskinitialisation=diskinit
        myclass.disktabUpdate=diskTabUpdate

        myclass.netinitialisation=netinit
        myclass.netTabUpdate=netUpdate

        myclass.gpuinitialisation=gpuinit
        myclass.gpuTabUpdate=gpuUpdate

        myclass.procinitialisation=procInit
        myclass.procUpdate=procUpdate
        myclass.row_selected=row_selected
        myclass.kill_process=kill_process
        myclass.column_button_press=column_button_press
        myclass.column_header_selection=column_header_selection

        myclass.filter_init=filter_init

        #Creating the builder object and loading the glade(layout) file and connecting the signals.
        self.builder=g.Builder()
        self.builder.add_from_file(files_dir+"/sysmontask.glade")
        self.builder.connect_signals(self)

        #Creating Main Window object from the glade(layout) file
        self.Window=self.builder.get_object("main_window")

        #Quit button defined in glade(layout) file
        self.quit=self.builder.get_object("quit")
        self.quit.connect('activate',self.on_quit_activate)

        #Setting the icon for the window from the png image
        self.Window.set_icon_from_file(icon_file+'/SysMonTask.png')

        #The performance tab(only the right side the sidepane in not included) defined in glade(layout) file, which has the CPU, Memory etc. details.
        self.performanceStack=self.builder.get_object('performancestack')

        #Box which contains the process tree
        self.process_tab_box=self.builder.get_object('process_tab_box')

        #Sidepane box which will contain the side graphs and switches for stack
        self.sidepaneBox=self.builder.get_object('sidepanebox')

        #Number of stack pages(initialized to 2 for cpu and memory),for names of the button(which acts as the stack switcher) in the sidepane
        self.stack_counter=2
        # Variable which gives the name of the current stack page
        self.current_stack=0
        # global acessible variable which holds the hold the stack switcher button on which right click is done
        # self.right_clicked_stack_switcher_button='NA'
        # stack pages(devices) which are hidden
        self.device_stack_page_lookup={
            'cpu':0,
            'memory':1
        }

        #Initializing color profiles
        color_profile_initializer(self)

        #Initializing each component
        self.cpuInit()
        self.memoryinitalisation()
        self.diskinitialisation()
        self.netinitialisation()
        self.gpuinitialisation()
        self.filter_init()
        self.procinitialisation()

        # Getting about dialog from the file
        self.aboutdialog=self.builder.get_object("aboutdialog")

        # Notebook (top tabs for processes and performances)
        self.notebook=self.builder.get_object('notebook')
        # Fetching the active page number in the last session and setting current page to that
        self.notebook.set_current_page(self.settings.get_int('current-tab'))

        # If the current page is not processes tab than hide the search entry
        if self.notebook.get_current_page()!=0:
            self.process_tree_search_entry.hide()

        # Update time interval in miliseconds for performance tab
        default_time_interval=850

        # Timer binding
        self.timehandler=go.timeout_add(default_time_interval,self.updater)
        self.Processtimehandler=go.timeout_add(2000,self.procUpdate)    #for processes tab it is 2000 ms

        # Update-Direction initializing
        self.update_dir_right=self.builder.get_object('update_right')
        self.update_dir_left=self.builder.get_object('update_left')
        self.update_dir_left.connect('toggled',self.on_set_left_update)
        self.update_dir_right.connect('toggled',self.on_set_right_update)

        # Newer on right by default
        self.update_graph_direction=1
        self.update_dir_right.set_active(True)

        # Update-Speed object creation
        self.update_speed_low=self.builder.get_object('low')
        self.update_speed_normal=self.builder.get_object('normal')
        self.update_speed_high=self.builder.get_object('high')
        self.update_speed_paused=self.builder.get_object('paused')

        # Update-Speed signal connection
        self.update_speed_low.connect('toggled',self.on_update_speed_change)
        self.update_speed_normal.connect('toggled',self.on_update_speed_change)
        self.update_speed_high.connect('toggled',self.on_update_speed_change)
        self.update_speed_paused.connect('toggled',self.on_update_speed_change)

        # Update-Speed default to normal
        self.update_speed_normal.set_active(True)

        # self.one_time=0 #need to remove it

        # Associating the Filter Button(Filter in menu->View) with Filter dialog
        self.filter_button=self.builder.get_object("filter_button")
        self.filter_button.connect("activate",self.on_filter_dialog_activate)
        print("device",self.device_stack_page_lookup)

        # One time feature set/ right click popup menu initialization
        feature_setup(self)
        # Post setup/initialisation of things which needs to execute upon refresh
        self.post_init()
        # Initializing the sidepane at the last because it need every other module to get Initialized
        self.sidepaneinitialisation()

        # Show the Window
        self.Window.show()
        # Time taken to show the window
        print("total window",time.time()-stt)

        # Fetching the coordinate of the window when last time it was closed.
        position=self.settings.get_value('window-position')

        # Moving the Window to those coordinates
        self.Window.move(position[0],position[1])

        # Fetching and setting the window size used during the last time before window closing.
        size=self.settings.get_value('window-size')
        self.Window.resize(size[0],size[1])

        # Button for log_plot in menu->Tools
        self.log_plot=self.builder.get_object("log_plot")

        # On page change on notebook signal binding
        self.notebook.connect("switch-page",self.on_notebook_page_change)

        ## What's New dialog show only for the first time
        if (self.settings.get_int("version-int")!=VERSION_INT):
            dialog=whatsnew_notice_dialog(self.Window,self)
            dialog.run()
            dialog.destroy()
            self.settings.set_int("version-int",VERSION_INT)

    def post_init(self):
        # group lookup by device
        self.grouping_for_color_profile={
            'cpu':'cpu',
            'memory':'memory',
            }
        if self.isNvidiagpu:
            self.grouping_for_color_profile[self.gpuName]='gpu'
        for i in self.disklist:
            self.grouping_for_color_profile[i]='disk'
        for i in self.netNameList:
            self.grouping_for_color_profile[i]='network'

        # Reversing the lookup so to access via page numbers
        self.reverse_device_stack_page_lookup={}
        for key in self.device_stack_page_lookup:
            self.reverse_device_stack_page_lookup[self.device_stack_page_lookup[key]]=key

        # hidden page numbers
        self.hidden_stack_page_numbers=[]
        device_list=self.settings.get_value('hidden-device-list')
        for i in device_list:
            self.hidden_stack_page_numbers.append(self.device_stack_page_lookup[i])

        # Check Box Menu for hide/show devices
        # contains the menu items
        self.device_menu_items={}
        # show hide menu in view
        self.show_hide_menu=self.builder.get_object("devices_menu")
        sub_menu=g.Menu()
        self.show_hide_menu.set_submenu(sub_menu)

        for key in self.device_stack_page_lookup:
            value=self.device_stack_page_lookup[key]
            item=g.CheckMenuItem(label=key)
            item.set_name(key)
            if value not in self.hidden_stack_page_numbers: item.set_active(True)
            else: item.set_active(False)
            item.connect('toggled',device_show_hide_menu_callback,self)
            self.device_menu_items[value]=item
            sub_menu.append(item)
        sub_menu.show_all()


    def on_log_plot_activate(self,widget):
        """
        Function binding for menu->Tools->Log_Plot button.

        It executes the script to plot the data stored for a process in .CSV file
        at ~/sysmontask_log directory.

        Parameters
        ----------
        widget : the clicked button(menu log_plot button)
        """
        # Creating the file chooser dialog
        file_dialog=g.FileChooserDialog(title="Select Log File",parent=self.Window,action=g.FileChooserAction.OPEN,\
            buttons=("Cancel", g.ResponseType.CANCEL,"Open", g.ResponseType.OK))
        # Setting the current folder in file chooser dialog to ~/sysmontask_log
        file_dialog.set_current_folder(os.path.join(os.environ.get("HOME"),"sysmontask_log"))

        # Running the dialog
        response=file_dialog.run()

        # Conditional response behaviours
        if response==g.ResponseType.OK:
            filename=file_dialog.get_filename()
            print("file choosen",filename)
            file_dialog.destroy()

            # Executing the log_plotter.py script in backgound
            os.system(f"python3 {os.path.join(os.path.abspath(os.path.dirname(__file__)),'log_plotter.py')} {filename} &")
            # plot_log(filename)

            # print("plot plot")
        else:
            print("didnt choose")
            file_dialog.destroy()

    def on_notebook_page_change(self,object,page,page_num):
        """
        To detect a Page Change in GtkNotebook.
        The search entry in processes tab will be hidden if the page is not processes and unhidden when page corresponds to processes tab.

        Parameters
        ----------
        object : GtkNotebook widget
        page : new page object
        page_num : index corresponding to the new page
        """
        if page_num!=0:
            self.process_tree_search_entry.hide()
        else:
            self.process_tree_search_entry.show()

    def on_menu_whatsnew(self,widget):
        """
        Signal handler(on active)(binded in glade) for the What's New button in menu->Help

        Parameters
        ----------
        Widget : clicked button(What's New button)

        """
        dialog=whatsnew_notice_dialog(self.Window,self)
        dialog.run()
        dialog.destroy()

    def on_set_left_update(self,widget):
        """
        Function Binding (activate signal) of 'menu->Graph Direction->Newer on Left' button.
        Change the Update direction of the graphs to Left.

        Parameters
        ----------
        widget : Clicked button(newer on left)

        """

        # Reversing the corresponding arrays and setting the direction var
        if widget.get_active():
            self.update_dir_right.set_active(False)
            self.update_graph_direction=0  #0 means newer on left 1 means newer on right

            self.cpuUtilArray.reverse()
            for i in range(self.cpu_logical_cores):
                self.cpu_logical_cores_util_arrays[i].reverse()

            self.memUsedArray1.reverse()

            for i in range(self.numOfDisks):
                self.diskActiveArray[i].reverse()
                self.diskReadArray[i].reverse()
                self.diskWriteArray[i].reverse()

            for i in range(self.numOfNets):
                self.netSendArray[i].reverse()
                self.netReceiveArray[i].reverse()

            self.gpuUtilArray.reverse()
            self.gpuVramArray.reverse()
            self.gpuEncodingArray.reverse()
            self.gpuDecodingArray.reverse()

        print('update Dir left',widget.get_active())

    def on_set_right_update(self,widget):
        """
        Function Binding (activate signal) of 'menu->Graph Direction->Newer on Right' button.
        Change the Update direction of the graphs to Right.

        Parameters
        ----------
        widget : Clicked button(newer on right)

        """
        # Reversing the corresponding arrays and setting the direction var
        if widget.get_active():
            self.update_dir_left.set_active(False)
            self.update_graph_direction=1  #0 means newer on left 1 means newer on right

            self.cpuUtilArray.reverse()
            for i in range(self.cpu_logical_cores):
                self.cpu_logical_cores_util_arrays[i].reverse()

            self.memUsedArray1.reverse()

            for i in range(self.numOfDisks):
                self.diskActiveArray[i].reverse()
                self.diskReadArray[i].reverse()
                self.diskWriteArray[i].reverse()

            for i in range(self.numOfNets):
                self.netSendArray[i].reverse()
                self.netReceiveArray[i].reverse()

            self.gpuUtilArray.reverse()
            self.gpuVramArray.reverse()
            self.gpuEncodingArray.reverse()
            self.gpuDecodingArray.reverse()

        print('update Dir right',widget.get_active())

    def on_main_window_destroy(self,widget,data=None):
        """
        Function Binding(delete-event) (binded in glade) for the window close button.
        Settings are saved back to glib-schemas.
        Parameters
        ----------
        widget : main window
        data : optional data passed to the window

        """
        print("print with cancel")

        # Storing the the window size, coordinates and current page of the notebook
        # print(self.Window.get_position())
        self.settings.set_value('window-position',go.Variant("(ii)",self.Window.get_position()))
        self.settings.set_value('window-size',go.Variant("(ii)",self.Window.get_size()))
        # print(object.get_position(),self.settings.get_value('window-size'))
        self.settings.set_int('current-tab',self.notebook.get_current_page())
        # print(self.settings.get_value('process-filter'))

        # Storing the filter entries
        l=[]
        for i,row in enumerate(self.filter_list_store):
            l.append([])
            l[i]+=[str(row[0]),row[1],str(row[2]),str(row[3])]
        self.settings.set_value('process-filter',go.Variant('aas',l))

        # Storing the device names that user wants to be hidden
        l.clear()
        for i in self.hidden_stack_page_numbers:
            l.append(self.reverse_device_stack_page_lookup[i])
        self.settings.set_value('hidden-device-list',go.Variant('as',l))

        # Storing the color profile
        l.clear()
        for i in self.color_profile:
            l.append(self.color_profile[i][0])
        self.settings.set_value('color-profile',go.Variant('a(ddd)',l))
        # print("l during exit",l)

        # Closing the log file if any opened.
        if self.log_file:
            self.log_file.close()

        # Gtk Quit
        g.main_quit()

    def on_quit_activate(self,menuitem,data=None):
        """
        Function Binding(activate) (binded in glade) for the 'menu->File->quit' button.

        Parameters
        ----------
        menuitem : Clicked button(item in the menu)
        """
        print("quit from menu",g.Buildable.get_name(menuitem))
        self.on_main_window_destroy(menuitem)

    def on_refresh_activate(self,menuitem,data=None):
        """
        Function Binding for the 'menu->View->Refresh'.
        It force refreshes the app to accomodate any hardware change such as network change, USB drive plugged in/out etc.

        Parameters
        ----------
        menuitem : the refresh menu button
        data : optional user data
        """

        print("refreshing")

        permanent_hidden_devices=[]
        for i in self.hidden_stack_page_numbers:
            permanent_hidden_devices.append(self.reverse_device_stack_page_lookup[i])
        self.settings.set_value("hidden-device-list",go.Variant('as',permanent_hidden_devices))

        # print(self.current_stack)
        self.stack_counter=2

        # Destroying the all the except CPU and Memory
        if(self.isNvidiagpu==1):
            g.Widget.destroy(self.gpuWidget)
            g.Widget.destroy(self.gpuSidePaneWidget)
        for i in range(0,self.numOfDisks):
            g.Widget.destroy(self.diskWidgetList[i])
            g.Widget.destroy(self.diskSidepaneWidgetList[i])
        for i in range(self.numOfNets):
            g.Widget.destroy(self.netWidgetList[i])
            g.Widget.destroy(self.netSidepaneWidgetList[i])
        # g.Widget.destroy(self.processTree)

        # Clearing the process tree store
        # self.processTreeStore.clear()

        # Since after refresh some new device are added and removed
        self.device_stack_page_lookup={
            'cpu':0,
            'memory':1
        }

        # Reinitializing all destroyed components
        # self.procinitialisation()
        self.diskinitialisation()
        self.netinitialisation()
        self.gpuinitialisation()

        self.post_init()
        self.sidepaneinitialisation()
        # print(self.current_stack)

        # Again back to the stack which was before refreshing(can be wrong since it uses the index)
        self.performanceStack.set_visible_child_name(f'page{self.current_stack}')

    # method to show the about dialog
    def on_about_activate(self,menuitem,data=None):
        """
        Function Binding for menu->Help->About button.

        This function shows the about dialog.

        Parameters
        ----------
        menuitem : the clicked button(about button)
        data : optional user data
        """
        print("aboutdialog opening")
        # self.aboutdialog.set_icon_from_file('/usr/share/sysmontask/icons/SysMonTask.png')
        self.response=self.aboutdialog.run()
        self.aboutdialog.hide()
        print("aboutdialog closed")

    def on_filter_dialog_activate(self,widget,data=None):
        """
        Function Binding for menu->View->Filter.

        Activates the filter dialog and show it.

        Parameters
        ----------
        widget : the clicked buttonargs_desc
        data : optional user data
        """
        self.filter_dialog.run()
        # Delete the initial Text
        self.filter_entry.delete_text(0,-1) # (st,end)
        print(f"Hiding Filter Dialog")
        self.filter_dialog.hide()

    """..removed::v1.x.x """
    # def resizer(self,item,data=None):
    #     if(myclass.resizerflag==0):
    #         print('hello')
    #         self.Window.set_size_request(-1,-1)
    #         myclass.resizerflag+=1

    def on_update_speed_change(self,widget):
        """
        Function Binding for menu->View->Update Speed->{speed}.

        Changes the updating-speed at which the values are updated/fetched.

        Parameters
        ----------
        widget : the clicked check button
        """
        if widget.get_active():
            update_speed=g.Buildable.get_name(widget)
            if(update_speed=='low'):
                print("update speed to low")
                # Removing the time handler
                go.source_remove(self.timehandler)
                go.source_remove(self.Processtimehandler)

                # Assigning new time handler for updater methods
                self.timehandler=go.timeout_add(1400,self.updater)
                self.Processtimehandler=go.timeout_add(2000,self.procUpdate)

                # Setting the other button to false
                self.update_speed_normal.set_active(False)
                self.update_speed_high.set_active(False)
                self.update_speed_paused.set_active(False)

            elif(update_speed=='normal'):
                print("update speed to normal")
                go.source_remove(self.timehandler)
                self.timehandler=go.timeout_add(850,self.updater)
                go.source_remove(self.Processtimehandler)
                self.Processtimehandler=go.timeout_add(2000,self.procUpdate)
                self.update_speed_low.set_active(False)
                self.update_speed_high.set_active(False)
                self.update_speed_paused.set_active(False)

            elif(update_speed=='high'):
                print("update speed to high")
                go.source_remove(self.timehandler)
                self.timehandler=go.timeout_add(500,self.updater)
                go.source_remove(self.Processtimehandler)
                self.Processtimehandler=go.timeout_add(2000,self.procUpdate)
                self.update_speed_normal.set_active(False)
                self.update_speed_low.set_active(False)
                self.update_speed_paused.set_active(False)

            elif(update_speed=='paused'):
                print("update speed to paused")
                go.source_remove(self.timehandler)
                go.source_remove(self.Processtimehandler)
                # self.timehandler=go.timeout_add(1000000000,self.updater)
                self.Processtimehandler=go.timeout_add(100000000,self.procUpdate)
                self.update_speed_normal.set_active(False)
                self.update_speed_high.set_active(False)
                self.update_speed_low.set_active(False)


    ## repeatedily called out fucntion
    def updater(self):
        """
        Main Driver function to update all modules and components for performance tab.

        It gets executed periodically via timer associated(time handler).
        """
        # Calling update method for each component
        self.cpuUpdate()
        self.memoryTab()
        self.disktabUpdate()
        if len(self.netNameList)!=0:
            self.netTabUpdate()
        if(self.isNvidiagpu==1):
            self.gpuTabUpdate()
        self.sidepaneUpdate()

        # Calling drawing methods putting them into the queue to draw for each component.
        g.Widget.queue_draw(self.cpuDrawArea)

        for i in range(self.cpu_logical_cores):
            g.Widget.queue_draw(self.cpu_logical_cores_draw_areas[i])

        g.Widget.queue_draw(self.memDrawArea1)
        g.Widget.queue_draw(self.memDrawArea2)
        for i in range(0,self.numOfDisks):
            g.Widget.queue_draw(self.diskWidgetList[i].diskdrawarea1)
            g.Widget.queue_draw(self.diskWidgetList[i].diskdrawarea2)

        for i in range(0,self.numOfNets):
            g.Widget.queue_draw(self.netWidgetList[i].netdrawarea)

        if(self.isNvidiagpu==1):
            g.Widget.queue_draw(self.gpuWidget.gpuutildrawarea)
            g.Widget.queue_draw(self.gpuWidget.gpuvramdrawarea)
            g.Widget.queue_draw(self.gpuWidget.gpuencodingdrawarea)
            g.Widget.queue_draw(self.gpuWidget.gpudecodingdrawarea)


        ##  sidepane
        g.Widget.queue_draw(self.cpuSidePaneDrawArea)
        g.Widget.queue_draw(self.memSidePaneDrawArea)
        for i in range(0,self.numOfDisks):
            g.Widget.queue_draw(self.diskSidepaneWidgetList[i].disksidepanedrawarea)
        for i in range(self.numOfNets):
            g.Widget.queue_draw(self.netSidepaneWidgetList[i].netsidepanedrawarea)
        if(self.isNvidiagpu==1):
            g.Widget.queue_draw(self.gpuSidePaneWidget.gpusidepanedrawarea)

        # Returning True to run periodically
        return True

    def on_cpu_logical_drawing(self,draw_area_widget,cr):
        """
        Function Binding for draw signal by logical cpu drawing areas.
        This function draws the graphs for the logical cpu views.

        Parameters
        ----------
        draw_area_widget : the widget on which to draw the graph
        cr : the cairo surface object
        """

        color=self.color_profile['cpu'][0]
        rectangle_color=self.color_profile['cpu'][1]

        # Setting line width
        cr.set_line_width(2)
        # getting name and from it getting the id
        logical_cpu_id=int(draw_area_widget.get_name())
        cpu_logical_util_array=self.cpu_logical_cores_util_arrays[logical_cpu_id]

        # Get the allocated width and height
        w=draw_area_widget.get_allocated_width()
        h=draw_area_widget.get_allocated_height()

        # Scalling factor for the graphs
        scalingfactor=h/100.0

        #creating outer rectangle
        cr.set_source_rgba(*rectangle_color,1)
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.stroke()

        # creating grid lines
        verticalGap=int(h/10)
        horzontalGap=int(w/10)
        for i in range(1,10):
            cr.set_source_rgba(*color,1) #for changing the outer line color
            cr.set_line_width(0.5)
            cr.move_to(0,i*verticalGap)
            cr.line_to(w,i*verticalGap)

            cr.move_to(i*horzontalGap,0)
            cr.line_to(i*horzontalGap,h)
            cr.stroke()
        cr.stroke()

        stepsize=w/99.0
        # Drawing the outer line
        cr.set_source_rgba(*color,1) # Line Color
        cr.move_to(0,scalingfactor*(100-cpu_logical_util_array[0]))
        for i in range(0,99):
            cr.set_line_width(1.5)
            cr.line_to((i+1)*stepsize,scalingfactor*(100-cpu_logical_util_array[i+1]))
        cr.stroke_preserve()

        # Filling the Color inside the graph
        cr.set_source_rgba(*color,0.25)  #Fill Color
        cr.line_to(w,h)
        cr.line_to(0,h)
        cr.move_to(0,scalingfactor*(100-cpu_logical_util_array[0]))
        cr.fill()
        cr.stroke()

        # Return false to execute only once per request
        return False

    def on_memDrawArea1_draw(self,dr,cr):
        """
        Function Binding(for draw signal) for Memory Utilisation draw area.

        This function draw the Memory Utilisation graph.

        Parameters
        ----------
        dr : the widget on which to draw the graph
        cr : the cairo surface object
        """
        # Setting the line width
        cr.set_line_width(2)

        # Color Pofile setup
        color=self.color_profile['memory'][0]
        rectangle_color=self.color_profile['memory'][1]

        # Get the allocated width and height
        w=self.memDrawArea1.get_allocated_width()
        h=self.memDrawArea1.get_allocated_height()

        # Scalling factor for the graphs
        scalingfactor=h/self.memTotal

        #creating outer rectangle
        # cr.set_source_rgba(.380,.102,.509,1)  # Color for the Outer Rectangle
        cr.set_source_rgba(*rectangle_color,1)
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.stroke()

        # creating grid lines
        verticalGap=int(h/10)
        horzontalGap=int(w/10)
        for i in range(1,10):
            # cr.set_source_rgba(.815,.419,1.0,1) #for changing the outer line color
            cr.set_source_rgba(*color,1)
            cr.set_line_width(0.5)
            cr.move_to(0,i*verticalGap)
            cr.line_to(w,i*verticalGap)

            cr.move_to(i*horzontalGap,0)
            cr.line_to(i*horzontalGap,h)
        cr.stroke()

        stepsize=w/99.0

        # efficient way to Fill
        # Drawing the outer lines for the curve
        # cr.set_source_rgba(.627,.196,.788,1) #for changing the outer line color
        cr.set_source_rgba(*color,1)
        cr.set_line_width(1.5)
        cr.move_to(0,scalingfactor*(self.memTotal-self.memUsedArray1[0]))
        for i in range(0,99):
            cr.line_to((i+1)*stepsize,scalingfactor*(self.memTotal-self.memUsedArray1[i+1]))
        cr.stroke_preserve()

        # Filling the curve
        # cr.set_source_rgba(.815,.419,1.0,0.2)   #for changing the fill color
        cr.set_source_rgba(*color,0.2)
        cr.line_to(w,h)
        cr.line_to(0,h)
        cr.move_to(0,scalingfactor*(self.memTotal-self.memUsedArray1[0]))
        cr.fill()
        cr.stroke()

        return False

    def on_memDrawArea2_draw(self,dr,cr):
        """
        Function Binding(for draw signal) for Memory Composition draw area.

        This function draw the Memory Composition graph.

        Parameters
        ----------
        dr : the widget on which to draw the graph
        cr : the cairo surface object
        """

        # Setting the line width
        cr.set_line_width(2)

        # Color Pofile setup
        color=self.color_profile['memory'][0]
        rectangle_color=self.color_profile['memory'][1]

        # Get the allocated width and height to the drawing area widget
        w=self.memDrawArea2.get_allocated_width()
        h=self.memDrawArea2.get_allocated_height()

        scalingfactor=int(w/self.memTotal)

        # Drawing the used area rectangle
        # cr.set_source_rgba(.815,.419,1.0,0.25)   #for changing the fill color
        cr.set_source_rgba(*color,0.25)
        cr.set_line_width(2)
        cr.rectangle(0,0,scalingfactor*self.usedd,h)
        cr.fill()
        cr.stroke()

        # cr.set_source_rgba(.815,.419,1.0,1)
        cr.set_source_rgba(*color,1)
        cr.set_line_width(2)
        cr.move_to(scalingfactor*self.usedd,0)
        cr.line_to(scalingfactor*self.usedd,h)
        cr.stroke()

        # Buffered and Cached Memory composition
        # cr.set_source_rgba(.815,.419,1.0,0.1)   #for changing the fill color
        cr.set_source_rgba(*color,0.1)
        cr.set_line_width(2)
        cr.rectangle(scalingfactor*(self.usedd),0,scalingfactor*(self.memAvailable-self.memFree),h)
        cr.fill()
        cr.stroke()
        # cr.set_source_rgba(.815,.419,1.0,.7)   #for changing the fill color
        cr.set_source_rgba(*color,0.7)
        cr.set_line_width(2)
        cr.move_to(scalingfactor*(self.usedd+self.memAvailable-self.memFree),0)
        cr.line_to(scalingfactor*(self.usedd+self.memAvailable-self.memFree),h)
        cr.stroke()

        # Free Memory
        # cr.set_source_rgba(.815,.419,1.0,0.2)   #for changing the fill color
        cr.set_source_rgba(*color,0.2)
        cr.set_line_width(2)
        cr.rectangle(scalingfactor*(self.usedd+self.memAvailable-self.memFree),0,scalingfactor*self.memFree,h)
        cr.stroke()

        # # Creating outer rectangle
        # cr.set_source_rgba(.380,.102,.509,1)  ##need tochange the color
        cr.set_source_rgba(*rectangle_color,1)
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.stroke()

        return False

    ## method for drawing
    def on_cpuDrawArea_draw(self,dr,cr):
        """
        Function Binding(for draw signal) for CPU Utilisation draw area.

        This function draw the CPU Utilisation graph.

        Parameters
        ----------
        dr : the widget on which to draw the graph
        cr : the cairo surface object
        """
        cr.set_line_width(2)

        color=self.color_profile['cpu'][0]
        rectangle_color=self.color_profile['cpu'][1]
        # print("rectangle",rectangle_color)

        # Get the allocated widht and height to the drawing area
        w=self.cpuDrawArea.get_allocated_width()
        h=self.cpuDrawArea.get_allocated_height()

        scalingfactor=h/100.0

        # Creating outer rectangle
        # cr.set_source_rgba(0,.454,.878,1)
        cr.set_source_rgba(*rectangle_color,1)
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.stroke()

        # Creating grid lines
        verticalGap=int(h/10)
        horzontalGap=int(w/10)
        for i in range(1,10):
            # cr.set_source_rgba(.384,.749,1.0,1) #for changing the outer line color
            cr.set_source_rgba(*color,1)
            cr.set_line_width(0.5)
            cr.move_to(0,i*verticalGap)
            cr.line_to(w,i*verticalGap)

            cr.move_to(i*horzontalGap,0)
            cr.line_to(i*horzontalGap,h)
        cr.stroke()

        stepsize=w/99.0

        # Not efficient
        # for i in range(0,99):
        #     # not effcient way to fill the bars (drawing)
        #     cr.set_source_rgba(.588,.823,.98,0.25)   #for changing the fill color
        #     cr.move_to(i*stepsize,scalingfactor*(100-self.cpuUtilArray[i]))
        #     cr.line_to((i+1)*stepsize,scalingfactor*(100-self.cpuUtilArray[i+1]))
        #     cr.line_to((i+1)*stepsize,h)
        #     cr.line_to(i*stepsize,h)
        #     cr.move_to(i*stepsize,scalingfactor*(100-self.cpuUtilArray[i]))

        #     cr.fill()
        #     cr.stroke()
        #     # for outer line
        #     cr.set_line_width(1.5)
        #     cr.set_source_rgba(.384,.749,1.0,1) #for changing the outer line color
        #     cr.move_to(i*stepsize,scalingfactor*(100-self.cpuUtilArray[i]))
        #     cr.line_to((i+1)*stepsize,scalingfactor*(100-self.cpuUtilArray[i+1]))
        #     cr.stroke()

        # Efficient one
        # Outer lines for the curve
        # cr.set_source_rgba(.384,.749,1.0,1) #for changing the outer line color
        cr.set_source_rgba(*color,1)
        cr.set_line_width(1.5)
        cr.move_to(0,scalingfactor*(100-self.cpuUtilArray[0]))
        for i in range(0,99):
            cr.line_to((i+1)*stepsize,scalingfactor*(100-self.cpuUtilArray[i+1]))
        cr.stroke_preserve()

        # Filling the curve
        # cr.set_source_rgba(.588,.823,.98,0.25)   #for changing the fill color
        # cr.set_source_rgba(.384,.749,1.0,0.2) #for changing the outer line color
        cr.set_source_rgba(*color,0.2)
        cr.line_to(w,h)
        cr.line_to(0,h)
        cr.move_to(0,scalingfactor*(100-self.cpuUtilArray[0]))
        cr.fill()
        cr.stroke()

        return False

    #side pane cpu draw

    def on_cpuSidePaneDrawArea_draw(self,dr,cr):
        """
        Function Binding(for draw signal) for CPU Sidepane Utilisation draw area.

        This function draw the CPU Sidepane Utilisation graph.

        Parameters
        ----------
        dr : the widget on which to draw the graph
        cr : the cairo surface object
        """

        #print("cpu sidepane draw")
        cr.set_line_width(2)

        # Color Pofile setup
        color=self.color_profile['cpu'][0]
        rectangle_color=self.color_profile['cpu'][1]
        # Get the allocated widht and height of the draw area widget.
        w=self.cpuSidePaneDrawArea.get_allocated_width()
        h=self.cpuSidePaneDrawArea.get_allocated_height()

        scalingfactor=h/100.0

        # Creating outer rectangle
        cr.set_source_rgba(*rectangle_color,1)
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.stroke()

        stepsize=w/99.0

        # Drawing the outer lines for the curve
        cr.set_line_width(1.5)
        cr.set_source_rgba(*color,1) #for changing the outer line color
        cr.move_to(0,scalingfactor*(100-self.cpuUtilArray[0]))
        for i in range(0,99):
            cr.line_to((i+1)*stepsize,scalingfactor*(100-self.cpuUtilArray[i+1]))
        cr.stroke_preserve()

        # Filling the curve
        cr.set_source_rgba(*color,0.25)   #for changing the fill color
        cr.line_to(w,h)
        cr.line_to(0,h)
        cr.move_to(0,scalingfactor*(100-self.cpuUtilArray[0]))
        cr.fill()
        cr.stroke()

        return False

    def on_memSidePaneDrawArea_draw(self,dr,cr):
        """
        Function Binding(for draw signal) for Memory Sidepane Utilisation draw area.

        This function draw the Memory Sidepane Utilisation graph.

        Parameters
        ----------
        dr : the widget on which to draw the graph
        cr : the cairo surface object
        """
        cr.set_line_width(2)

        # Color Pofile setup
        color=self.color_profile['memory'][0]
        rectangle_color=self.color_profile['memory'][1]

        # Get the allocated widht and height of the drawing widget
        w=self.memSidePaneDrawArea.get_allocated_width()
        h=self.memSidePaneDrawArea.get_allocated_height()

        scalingfactor=h/self.memTotal

        #creating outer rectangle
        cr.set_source_rgba(*rectangle_color,1)  ##need tochange the color
        cr.set_line_width(3)
        cr.rectangle(0,0,w,h)
        cr.stroke()

        stepsize=w/99.0

        # Drawing the outer lines for the curve
        cr.set_source_rgba(*color,1) #for changing the outer line color
        cr.set_line_width(1.5)
        cr.move_to(0,scalingfactor*(self.memTotal-self.memUsedArray1[0]))
        for i in range(0,99):
            cr.line_to((i+1)*stepsize,scalingfactor*(self.memTotal-self.memUsedArray1[i+1]))
        cr.stroke_preserve()

        # Filling the curve
        cr.set_source_rgba(*color,0.2)   #for changing the fill color
        cr.line_to(w,h)
        cr.line_to(0,h)
        cr.move_to(0,scalingfactor*(self.memTotal-self.memUsedArray1[0]))
        cr.fill()
        cr.stroke()

        return False


def start():
    """
    Function to start the application.
    """
    main=myclass()
    g.main()

# import cProfile

if __name__=="__main__":
    # cProfile.run("start()")
    start()

# def uninstall():
#     os.system('sudo {0}/uninstall_for_pip.sh'.format(os.path.dirname(os.path.abspath(__file__))))
