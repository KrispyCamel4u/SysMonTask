from gi.repository import Gtk as gtk, GLib as glib,Gio as gio, Gdk as gdk, GdkPixbuf, Pango
from datetime import datetime
from os.path import isfile

from Log import Log, staticVar

def size_cell_data_func(col,renderer,model,iter,index):
    """ Function to format and display size kind of data to renderer

    Args:
        col (Gtk.TreeViewColumn): Column
        renderer (Gtk.CellRendererText): Text renderer
        model (Gtk.TreeModel): Abstract TreeModel store
        iter (Gtk.TreeIter): Iterator for Tree
        index (int): Column Index
    """
    value=model.get_value(iter,index)
    if value==0:
        renderer.props.text='N/A'
        renderer.props.style=Pango.Style.ITALIC
    else:
        renderer.props.text=glib.format_size_full(value,2)  ## IEC :power of 2 KiB MiB etc
        renderer.props.style=Pango.Style.NORMAL

def percent_cell_data_func(col,renderer,model,iter,index):
    """ Function to format and display percentage data to renderer

    Args:
        col (Gtk.TreeViewColumn): Column
        renderer (Gtk.CellRendererText): Text renderer
        model (Gtk.TreeModel): Abstract TreeModel store
        iter (Gtk.TreeIter): Iterator for Tree
        index (int): Column Index
    """
    renderer.props.text="{:.1f}".format(model.get_value(iter,index))

def duration_cell_data_func(col,renderer,model,iter,index):
    ## need to get back to it
    pass

def time_cell_data_func(col,renderer,model,iter,index):
    """ Function to format and display Time data to renderer

    Args:
        col (Gtk.TreeViewColumn): Column
        renderer (Gtk.CellRendererText): Text renderer
        model (Gtk.TreeModel): Abstract TreeModel store
        iter (Gtk.TreeIter): Iterator for Tree
        index (int): Column Index
    """
    renderer.props.text=str(datetime.fromtimestamp(model.get_value(iter,index)))

def io_rate_cell_data_func(col,renderer,model,iter,index):
    """ Function to format and display IO Rate data to renderer

    Args:
        col (Gtk.TreeViewColumn): Column
        renderer (Gtk.CellRendererText): Text renderer
        model (Gtk.TreeModel): Abstract TreeModel store
        iter (Gtk.TreeIter): Iterator for Tree
        index (int): Column Index
    """
    value=model.get_value(iter,index)
    if value==0:
        renderer.props.text='N/A'
        renderer.props.style=Pango.Style.ITALIC
    else:
        renderer.props.text=glib.format_size_full(value,2)  ## 2->IEC :power of 2 KiB MiB etc
        renderer.props.style=Pango.Style.NORMAL


def priority_cell_data_func(col,renderer,model,iter,index):
    """ Function to format and display priority data to renderer

    Args:
        col (Gtk.TreeViewColumn): Column
        renderer (Gtk.CellRendererText): Text renderer
        model (Gtk.TreeModel): Abstract TreeModel store
        iter (Gtk.TreeIter): Iterator for Tree
        index (int): Column Index
    """
    value=model.get_value(iter,index) ## it is nice value from which we will determine priority
    if value < -7:
        renderer.props.text='Very High'
    elif value < -2:
        renderer.props.text='High'
    elif value < 3:
        renderer.props.text='Normal'
    elif value < 8:
        renderer.props.text='Low'
    else:
        renderer.props.text='Very Low'

def number_compare_func(model, first, second, data):
    """ Helper function to compare the number

    Args:
        model (Gtk.TreeModel): Tree model(tree store)
        first (Gtk.TreeIter): Iterator pointing to first tree row
        second (Gtk.TreeIter): Iterator pointing to second tree row
        data (int): Column Index
    """
    size1=model.get_value(first,data)
    size2=model.get_value(second,data)

    if size1 < size2:
        return 1
    elif size2 < size1:
        return -1
    else:
        return 0

def priority_compare_func(model, first, second, data):
    """ Helper function to compare the priority

    Args:
        model (Gtk.TreeModel): Tree model(tree store)
        first (Gtk.TreeIter): Iterator pointing to first tree row
        second (Gtk.TreeIter): Iterator pointing to second tree row
        data (int): Column Index
    """
    val1=model.get_value(first,data)
    val2=model.get_value(second,data)
    return val1-val2    ## need to check how it works


def is_cgroups_enabled():
    if not isfile("/proc/cgroups"):     # can be removed and use the static var
        return False
    return True
