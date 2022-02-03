from gi.repository import Gtk as gtk,Gdk as gdk,GLib as glib

from Log import Log,staticVar

logger=staticVar.logger

def cb_column_header_clicked(col,event,data):
    """ Callback whenver the column header is clicked.

    Args:
        col (Gtk.TreeViewColumn): Column
        event (Gdk.EventButton): which mouse button is pressed
        data (Gtk.Menu): header_menu
    """
    logger.debug("---->")
    
    if event.button==gdk.BUTTON_SECONDARY:
        logger.info("showing column popup menu")
        data.popup_at_pointer(event)
        logger.debug("<---")
        return True ## Why
    logger.debug("<----")
    return False  ## why returning?

def smt_tree_view_get_column_from_id(proc_tree,sort_id):
    """ Returns the column with sort id as sort_id

    Args:
        proc_tree (Gtk.TreeView): the tree view
        sort_id (int): id for the column
    """
    for col in proc_tree.get_columns():
        if col.get_sort_column_id()==sort_id:
            return col


def smt_tree_view_load_saved_state(tree_view):
    """ Loads the saved state of the TreeView from the settings.

    Args:
        tree_view (Gtk.TreeView): proctree (TreeView for the processes)
    """
    logger.debug("---->")

    model=tree_view.get_model()
    sort_col=tree_view.settings.get_int("sort-col")
    sort_type=tree_view.settings.get_int("sort-order")
    model.set_sort_column_id(sort_col,sort_type)

    if tree_view.store_column_order:
        header_menu=gtk.Menu()
        columns=tree_view.get_columns()

        for col in columns:
            sort_id=col.get_sort_column_id()
            if sort_id in tree_view.excluded_columns:
                col.set_visible(False)
                continue

            #### Creating the popup menu for the column header ####
            button=col.get_button()
            button.connect("button-press-event",cb_column_header_clicked,header_menu)

            check_item=gtk.CheckMenuItem(label=col.get_title())
            col.bind_property("visible",check_item,"active",1 | 2) #BIDIRECTIONAL | SYNC
            header_menu.append(check_item)

            col.set_fixed_width(tree_view.settings.get_int(f"col-{sort_id}-width"))
            col.set_min_width(30)   ## need to check if needed

            col.set_visible(tree_view.settings.get_boolean(f"col-{sort_id}-visible"))

        header_menu.show_all()

        #### Arranging the columns in order ####
        col_order=tree_view.settings.get_value("columns-order")
        last=None
        for i in col_order:
            col=smt_tree_view_get_column_from_id(tree_view,i)
            if col and col!=last:   ## need to check the second condition
                tree_view.move_column_after(col,last)
                last=col
    
    logger.debug("<----")

def smt_tree_view_save_state(tree_view):
    """ save the state of the TreeView to the settings.

    Args:
        tree_view (Gtk.TreeView): proctree (TreeView for the processes)
    """
    logger.debug("---->")

    tree_view.settings.delay()
    
    model=tree_view.get_model()
    sort_id,sort_type=model.get_sort_column_id()

    if sort_id !=None and sort_type != None:
        logger.info(f"setting sort-col {sort_id} and sort-order {sort_type}")
        tree_view.settings.set_int("sort-col",sort_id)
        tree_view.settings.set_int("sort-order",sort_type)
    
    if tree_view.store_column_order:
        cols=tree_view.get_columns()
        order=[ i.get_sort_column_id() for i in cols ]
        logger.info(f"Column Order: {order}")
        tree_view.settings.set_value("columns-order",glib.Variant("ai",order))

    tree_view.settings.apply()

    logger.debug("<----")

class SmtTreeview(gtk.TreeView):
    """ Class to wrap the Gtk.TreeView for extra variables. """
    __slots__ =[
        "settings",
        "store_column_order",
        "excluded_columns",
        "process_menu"
    ]
    def __init__(self,setting,store_col_order):
        """Constructor for Class"""
        logger.debug("---->")

        super().__init__()
        self.settings=setting
        self.store_column_order=store_col_order
        self.excluded_columns=[]
        self.process_menu=None

        logger.debug("<----")
