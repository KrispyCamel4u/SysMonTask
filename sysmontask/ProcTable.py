from gi.repository import Gtk as gtk, GLib as glib,Gio as gio, Gdk as gdk, GdkPixbuf
from re import compile

from Log import Log,staticVar
from TreeView import SmtTreeview,smt_tree_view_load_saved_state,smt_tree_view_save_state
from Util import *

logger=staticVar.logger

COL_NAME=0
COL_PID=1
COL_USER=2
COL_STATUS=3
COL_CPU_TIME=4
COL_CPU=5
COL_RCPU=6
COL_MEM=7
COL_RMEM=8
COL_VMSIZE=9
COL_MEMRES=10
COL_MEMSHARED=11
COL_START_TIME=12
COL_CMDL=13
COL_NICE=14
COL_CGROUP=15
COL_OWNER=16
COL_DISK_READ=17
COL_DISK_READ_TOTAL=18
COL_DISK_WRITE=19
COL_DISK_WRITE_TOTAL=20
COL_PRIORITY=21
COL_WCHAN=22
COL_PIXBUFF=23
COL_PROCINFO=24
COL_TOOLTIP=25

def iter_matches_search_key(model,iter,search_text):
    logger.debug("---->")

    pid,name,user,cmdline=model.get(iter,
        COL_PID,
        COL_NAME,
        COL_USER,
        COL_CMDL
    )
    search_pattern="|".join(search_text.split(" |"))
    logger.info(f"search pattern: {search_pattern}")
    pat=compile(search_pattern)
    string=f"{pid} {name} {user} {cmdline}"
    if pat.search(string):
        logger.info(f"found match in string: {string}")
        logger.debug("<---")
        return True

    logger.debug("<----")
    return False

def process_visibility_function(model,iter,app):
    logger.debug("---->")

    if not app.search_entry:
        search_text=""
    else:
        search_text=app.search_entry.get_text()
    logger.info(f"search text: {search_text}")

    if not search_text:
        logger.debug("<---")
        return

    match=False
    if app.settings.get_object("show-hierarchy"):
        child=model.iter_children(iter)
        child_match=False
        while(child and not child_match):
            child_match=process_visibility_function(model, child, app)
            child=model.iter_next()
        match=child_match

        ## optimise this conditions
        if not match:
            match=iter_matches_search_key(model,iter,search_text)
        if match:
            logger.info(f"match found")
            tree_path=model.get_path(iter)
            app.tree.expand_to_path(tree_path)
            tree_path.free()
    else:
        match=iter_matches_search_key(model,iter,search_text)

    logger.info(f"MATCH VALUE: {match}")
    logger.debug("<----")
    return match

def save_col_state(settings,col):
    logger.debug("---->")

    col_id=col.get_sort_column_id()
    logger.info(f"Saving Column: {col_id}")
    settings.delay()
    settings.set_int(f"col-{col_id}-width",col.get_width())
    settings.set_boolean(f"col-{col_id}-visible",col.get_visible())
    settings.apply()
    staticVar.saved_column=None

    logger.debug("<----")
    return False

def cb_update_column_state(col,_,settings):
    logger.debug("---->")

    staticVar.current_column=col
    logger.info(f"col id {col.get_sort_column_id()}")
    if staticVar.saved_column != col:
        logger.info(f"delaying save for col: {col.get_sort_column_id()}")
        staticVar.saved_column=col
        glib.timeout_add_seconds(1,save_col_state,settings,col)

    logger.debug("<----")

def cb_refresh_icons(theme,app):
    """ Refreshes the Icons in the ProcTable.

    Args:
        theme (Gtk.IconTheme): Current Theme
        app (SmtApplication): The SmtApplication.
    """
    ## Will impliment it letter
    pass

def cb_row_selected(selection,app):
    """ Callback when the row is selected.

    Args:
        selection (Gtk.TreeSelection): treeView selection
        app (SmtApplication): The SmtApplication.
    """

    pass

    # update_sensitivity()

def cb_proctree_popup_menu(proc_tree,app):
    """ POPUP related?

    Args:
        widget (Gtk.TreeView): need to check more on it
        app (SmtApplication): Application class
    """
    logger.debug("---->")

    proc_tree.process_menu.popup_at_pointer(None)

    logger.debug("<----")
    

def cb_proctree_button_press(proc_tree,event,app):
    """ To handle when clicked on row """
    #### showing menu on right click(instead of checking event.button to right mouse click 
    # this one is preffered because of platform convention) ####
    if not event.triggers_context_menu():
        return False
    
    path=proc_tree.get_path_at_pos(event.x,event.y)
    if not path:
        return False
    
    selection=proc_tree.get_selection()
    if not selection.path_is_selected(path):
        # need to check why we are this mask check and select_path
        if not event.state & (gdk.ModifierType.SHIFT_MASK | gdk.ModifierType.CONTROL_MASK):
            selection.unselect_all()
        selection.select_path(path)

    proc_tree.process_menu.popup_at_pointer(event) ## NULL is given in reference code


def cb_proctree_save_state(_,app):
    logger.debug("---->")

    smt_tree_view_save_state(app.tree)
    
    logger.debug("<----")

def cb_proctree_destroy(proc_tree,app):
    logger.debug("---->")

    proc_tree.disconnect_by_func(cb_proctree_save_state)
    proc_tree.get_model().disconnect_by_func(cb_proctree_save_state)

    logger.debug("<----")

def cb_show_hierarchy_changed(settings,key,app):
    logger.debug("---->")

    action=app.main_window.lookup_action("show-hierarchy")
    action.set_state(settings.get_value("show-hierarchy"))

    logger.debug("<----")

def cb_show_whose_processes_changed(settings,key,app):
    logger.debug("---->")
    logger.debug("<----")

def proctable_new(app):
    logger.debug("---->")

    col_titles=[
        "Name",
        "PID",
        "User",
        "Status",
        "CPU Time",
        "% CPU",
        "% rCPU",
        "Memory",
        "rMemory",
        "Virtual Memory",
        "Resident Memory",
        "Shared Memory",
        "Started",
        "Command",
        "Nice",
        "Control Group",
        "Owner",
        "Disk Read",
        "Disk Read Total",
        "Disk Write",
        "Disk Write Total",
        "Priority",             ## need to check if I can get
        "Wating Channel",       ## need to check
    ]

    settings=app.settings.get_child("proctree")
    model=gtk.TreeStore(        ## .new in reference code
        str,                # Name
        int,                # PID
        str,                # User
        str,                # Status
        int,                # CPU Time
        float,              # % CPU
        float,              # % rCPU
        int,                # Memory,
        int,                # rMemory
        int,                # Virtual Memory
        int,                # Resident Memory
        int,                # Shared Memory
        int,                # Started
        str,                # Command
        int,                # Nice
        str,                # Cgroups
        str,                # Owner
        int,                # Disk Read
        int,                # Disk Read Total
        int,                # Disk Write
        int,                # Disk Write Total
        str,                # Priority
        str,                # Waiting Channel
        GdkPixbuf.Pixbuf,   # Icon
        object,             # ProcInfo
        str,                # Tooltip
    )

    #### Model for filtering ####
    model_filter=model.filter_new()
    model_filter.set_visible_func(process_visibility_function,data=app)

    #### Model for sorting the columns ####
    model_sort=gtk.TreeModelSort(model_filter)

    proctree=SmtTreeview(settings,True)
    proctree.set_model(model_sort)

    proctree.set_tooltip_column(COL_TOOLTIP)
    proctree.set_show_expanders(app.settings.get_boolean("show-hierarchy"))
    proctree.set_enable_search(False)
    #unref the model via del may be

    #### Adding the icon and name in the Name column ####
    column=gtk.TreeViewColumn()

    cell_renderer=gtk.CellRendererPixbuf()
    column.pack_start(cell_renderer,False)
    column.set_attributes(cell_renderer,pixbuf=COL_PIXBUFF)

    cell_renderer=gtk.CellRendererText()
    column.pack_start(cell_renderer,False)
    column.set_attributes(cell_renderer,text=COL_NAME)

    column.set_title(col_titles[0])     # Process Name column
    column.set_sort_column_id(COL_NAME)
    column.set_reorderable(True)
    column.set_resizable(True)
    column.set_sizing(gtk.TreeViewColumnSizing.FIXED)
    column.set_min_width(20)     # may be changed to 20 or may be removed

    proctree.append_column(column)
    column.connect("notify::fixed-width",cb_update_column_state,settings)
    column.connect("notify::visible",cb_update_column_state,settings)

    proctree.set_expander_column(column)  # can be changed to pid col
    column.set_expand(True)     # need to check it

    for i in range(COL_PID,COL_WCHAN):
        cell_renderer=gtk.CellRendererText()
        column=gtk.TreeViewColumn()
        column.pack_start(cell_renderer,False)
        column.set_title(col_titles[i])     # column Name
        column.set_sort_column_id(i)
        column.set_reorderable(True)
        column.set_resizable(True)

        # SORT indicator?

        #### Append and bind the column things
        proctree.append_column(column)
        column.connect("notify::fixed-width",cb_update_column_state,settings)
        column.connect("notify::visible",cb_update_column_state,settings)

        proctree.set_expander_column(column)  # can be changed to pid col
        column.set_expand(True)     # need to check it

        #### Data Function for cell data
        if COL_VMSIZE or COL_MEMRES or COL_MEMSHARED or COL_MEM or COL_RMEM:
            column.set_cell_data_func(cell_renderer,size_cell_data_func,i)
        elif COL_CPU or COL_RCPU:
            column.set_cell_data_func(cell_renderer,percent_cell_data_func,i)
        elif COL_CPU_TIME:
            column.set_cell_data_func(cell_renderer,duration_cell_data_func,i)
        elif COL_START_TIME:
            column.set_cell_data_func(cell_renderer,time_cell_data_func,i)
        elif COL_DISK_WRITE_TOTAL or COL_DISK_READ_TOTAL:   ## can be merged with memory
            column.set_cell_data_func(cell_renderer,size_cell_data_func,i)
        elif COL_DISK_WRITE or COL_DISK_READ:
            column.set_cell_data_func(cell_renderer,io_rate_cell_data_func,i)
        elif COL_PRIORITY:
            column.set_cell_data_func(cell_renderer,priority_cell_data_func,i)
        else:
            column.set_attributes(cell_renderer,"text",i)

        ### Leaving out tubular column switch

        #### Sorting #### Need to check if nice also has to added or not
        if  COL_VMSIZE or \
            COL_MEMRES or \
            COL_MEMSHARED or \
            COL_MEM or \
            COL_RMEM or \
            COL_CPU or \
            COL_RCPU or \
            COL_CPU_TIME or \
            COL_DISK_READ_TOTAL or \
            COL_DISK_WRITE_TOTAL or \
            COL_DISK_READ_CURRENT or \
            COL_DISK_WRITE_CURRENT or \
            COL_START_TIME:

            model_sort.set_sort_func(i,number_compare_func,i)
        elif COL_PRIORITY:
            model_sort.set_sort_func(i,priority_compare_func,COL_NICE)

        ### Leaving xalign

        #### sizing of columns ####
        column.set_sizing(gtk.TreeViewColumnSizing.FIXED)
        if COL_CMDL:
            column.set_min_width(150)
            column.set_expand(True)
        else:
            column.set_min_width(20)
            column.set_expand(False)

    if not is_cgroups_enabled():
        proctree.excluded_columns.append(COL_CGROUP)
    app.tree=proctree

    #### Loading the saved state of proctree ####
    smt_tree_view_load_saved_state(proctree)

    # theme=gtk.IconTheme.get_default()
    # theme.connect("changed",cb_refresh_icons,app)   ## can be skipped not an important for now

    selection=proctree.get_selection()
    app.treeView_selection=selection

    selection.set_mode(gtk.SelectionMode.MULTIPLE)  # Multiple line to be selected

    selection.connect("changed",cb_row_selected,app) ## Need to update the callback

    proctree.connect("popup_menu",cb_proctree_popup_menu,app)   ## Need to have one more look

    proctree.connect("button-press-event",cb_proctree_button_press,app) ## look again into it neeraj

    proctree.connect("destroy",cb_proctree_destroy,app)   

    proctree.connect("columns-changed",cb_proctree_save_state,app)

    model_sort.connect("sort-column-changed",cb_proctree_save_state,app)

    ## settings bindings for shows_whose_process and show_dependancies
    app.settings.connect("changed::show-hierarchy",cb_show_hierarchy_changed,app)    #need to look again
    app.settings.connect("changed::show-whose-processes",cb_show_whose_processes_changed,app)

    proctree.show()

    logger.debug("<----")
    return proctree