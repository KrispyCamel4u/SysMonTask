from gi.repository import Gtk as gtk, GLib as glib,Gio as gio, Gdk as gdk

from Log import Log, staticVar
from ProcTable import proctable_new

logger = staticVar.logger

def create_proc_view(app,builder):
    logger.debug("---->")

    proctree=proctable_new(app)
    scrolled_window=builder.get_object("proc-scrolled-window")
    scrolled_window.add(proctree)

    #### process popup menu which is poped up on right click on process ####
    process_popup_menu=gtk.Menu.new_from_model(builder.get_object("process-popup-menu"))
    proctree.process_menu=process_popup_menu

    process_popup_menu.attach_to_widget(app.main_window)

    #### search entry  related things

    logger.debug("<----")

def smt_add_simple_action(obj,action_name,signal_name,callback,state=None,data=None,paramtype=None):
    logger.debug("---->")
    if state !=None:
        action=gio.SimpleAction.new_stateful(action_name,paramtype,state)
        print(state)
    else:
        action=gio.SimpleAction.new(action_name,None)
    action.connect(signal_name,callback,data)
    obj.add_action(action)
    logger.debug("<----")

# def add_simple_action_stateful(obj,action_name,signal_name,callback,state,data):
#     action=gio.SimpleAction.new_stateful(action_name,None,state)
#     action.connect(signal_name,callback,data)
#     obj.add_action(action)

def cb_show_hierarchy_state_change(action,new_state,app):
    """ Set the State fo the Show Hierarchy Action """
    logger.debug("---->")

    app.settings.set_value("show-hierarchy", new_state)
    action.set_state(new_state)
    
    logger.debug("<----")

def cb_show_whose_processes_state_change(action,new_state,app):
    logger.debug("---->")

    app.settings.set_value("show-whose-processes", new_state)
    # action.set_state(new_state)

    logger.debug("---->")

def on_activate_radio(action,param,data):
    logger.debug("---->")

    action.change_state(param)

    logger.debug("<----")

def on_activate_toggle(action,param,data):
    logger.debug("---->")

    action.change_state(glib.Variant.new_boolean(not action.get_state()))

    logger.debug("<----")

def cb_notebook_switch_page(notebook,page,page_num,app):
    """ Callback when the notebook page(Process, Resources tab) is changed """
    logger.debug("---->")

    if page_num == 0: # Processes Page
        # protable_update(app)
        # proctable_thaw(app)
        app.search_entry.show()

        # update_sensitivity(app)
    else:
        # proctable_freeze(app)
        app.search_entry.hide()
        # update_sensitivity(app)
    

    logger.debug("<----")

# can callee caller can be changed
def update_page_activities(app):
    """ Function for setting things up for a page change """
    notebook=app.notebook
    page_num=notebook.get_current_page()
    cb_notebook_switch_page(notebook,notebook.get_nth_page(page_num),page_num,app)

def cb_main_window_state_change(main_window_widget,event,app):
    """ Callback to handle the window state change such as minimise or below other windows"""
    logger.debug("---->")

    current_page=app.notebook.get_current_page()
    logger.info(f"Current page is {current_page}")
    if event.new_window_state & gdk.WindowState.WITHDRAWN or \
        event.new_window_state & gdk.WindowState.ICONIFIED or \
        event.new_window_state & gdk.WindowState.BELOW:
        logger.info(f"EVENT matched")
        if current_page == 0:
            # proctable_freeze(app)
            pass
    else:
        logger.info("EVENT unmatched")
        if current_page == 0:
            # proctable_update(app)
            # proctable_thaw(app)
            pass
            
def on_activate_refresh(action,param,app):
    """ Callback when refresh is done """
    logger.debug("---->")
    # proctable_update(app)
    logger.debug("<----")

def create_main_window(app):
    """ Creates the Main Window and Process and Resources Tab """
    logger.debug("---->")
    builder=gtk.Builder.new_from_file("/home/neeraj/projects/task_manager/sysmontask/data/interface.ui")
    # builder.connect_signals(app)
    main_window=builder.get_object("main_window")
    main_window.set_application(app)
    # main_window.set_name("sysmontask")

    #### Menu Bar ####
    builder.add_from_file("/home/neeraj/projects/task_manager/sysmontask/data/menus.ui")  ## need to make it for resources
    # menubar = builder.get_object('menubar')
    app.set_menubar(builder.get_object('menubar'))
    main_window.set_show_menubar(True)
    # app.set_menubar(builder.get_object('menubar2'))
    # fileMenu=builder.get_object("file-menu")
    # fileMenu.remove(1)
    # fileMenu.append("quit","app.quit")

    app.main_window=main_window

    #### Getting the size and position of the window ####
    window_state=app.settings.get_value("window-state")  ## width,height,xpos, ypos
    width,height,xpos,ypos=window_state[0],window_state[1],window_state[2],window_state[3]

    #### Display and Physical monitor, where app should be shown ####
    display=gdk.Display.get_default()
    monitor=display.get_monitor_at_point(xpos,ypos)
    if not monitor:
        monitor=display.get_monitor(0) ## maybe get_primary_monitor()
    monitor_geometry=monitor.get_geometry()

    CLAMP=lambda a,low, high: high if(a>high) else low if(a<low) else a
    width  = CLAMP (width, 50, monitor_geometry.width)
    height = CLAMP (height, 50, monitor_geometry.height)
    xpos   = CLAMP (xpos, 0, monitor_geometry.width - width)
    ypos   = CLAMP (ypos, 0, monitor_geometry.height - height)


    #### Setting window size and postioning it. ####
    main_window.set_default_size(width,height)
    main_window.move(xpos,ypos)

    if app.settings.get_boolean("maximized"):
        main_window.maximize()


    #### Search entry and killer buttonm ####
    app.search_entry=builder.get_object("proc-search-entry")

    #### action entries to windows ####
    # smt_add_simple_action(main_window,"show-hierarchy","change-state",cb_show_hierarchy_state_change,glib.Variant.new_boolean(False),app)
    # smt_add_simple_action(main_window,"show-whose-processes","change-state",cb_show_whose_processes_state_change,glib.Variant.new_string("user"),app,glib.VariantType.new("s"))

    action_entries=[
        ("show-whose-processes", on_activate_radio, "s", "'user'", cb_show_whose_processes_state_change ),
        ("show-hierarchy", on_activate_toggle, None, "false", cb_show_hierarchy_state_change ),
        ( "refresh", on_activate_refresh, None, None, None )
    ]

    main_window.add_action_entries(action_entries,app)


    #### Setting the visuals(color science) to use ####
    screen=main_window.get_screen()
    visual=screen.get_rgba_visual()

    if visual:
        main_window.set_visual(visual)

    ## could I move it to the constructor?
    app.notebook=notebook=builder.get_object("main-notebook")

    #### creating/initialising the process tab ####
    create_proc_view(app,builder)

    app.settings.bind("current-tab",notebook,"page",gio.SettingsBindFlags.DEFAULT)
    notebook.connect("switch-page",cb_notebook_switch_page,app)

    # main_window.connect("delete-event",cb_notebook_delete_event,app) #need it?

    main_window.connect("window-state-event",cb_main_window_state_change,app)

    #### action map 
    action=main_window.lookup_action("show-hierarchy")
    action.change_state(app.settings.get_value("show-hierarchy"))

    action=main_window.lookup_action("show-whose-processes")
    action.change_state(app.settings.get_value("show-whose-processes"))

    update_page_activities(app)         # changing things depending on which tab we are on

    main_window.show()
    logger.debug("<----")