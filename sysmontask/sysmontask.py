#!/usr/bin/env python3
# import builtins
import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk as gtk, GLib as glib,Gio as gio

from Log import Log,staticVar

import sys
#### just for now Need to handle command line also ####
if "--" in sys.argv[-1]:
    logDict={
        'DEBUG':10,
        'INFO':20,
        'WARNING':30,
        'ERROR':40,
        'CRTICAL':50
    }
    logLevel=sys.argv[-1][2:]
    Log.LEVEL=logDict[logLevel.upper()]
else:
    Log.LEVEL=40 ## logging.ERROR
logger=staticVar.logger=Log.getLogger("SMT")

from Configurations import Configurations
from Dialogs import HelpDial
from PrettyProcTable import PrettyProcTable
from ConfigBind import *
from WinCreater import *

VERSION="2.0.0"
# import traceback
# def who_am_i():
#    stack = traceback.extract_stack()
#    filename, codeline, funcName, text = stack[-2]

#    return funcName

# def DEBUG_DECORATOR(func):

#     def inner(*args, **kwargs):
#         logger.debug(f"{func.__name__} ------>")

#         func(*args, **kwargs)

#         logger.debug(f"{func.__name__} <------")

#     return inner


class SmtApplication(gtk.Application):
    """
    Sysmontask Application class inheriting from the Gtk.Application.
    """
    data_dir="/home/neeraj/projects/task_manager/sysmontask/data" # need to change it.

    __slots__=[
        'main_window',
        "settings",
        "config",
        "notebook",
        "search_entry",
        "tree",
        "top_of_tree",
        ]

    def __init__(self,*args,**kwargs):
        logger.debug(f"---->")

        super().__init__(*args,
        application_id="com.github.camelneeraj.sysmontask",
        flags=gio.ApplicationFlags.FLAGS_NONE,
        **kwargs
        )
        glib.set_application_name("SysMonTask")

        # self.window=gtk.ApplicationWindow(application=self,title="SysMonTask")
        self.main_window=None
        self.settings=gio.Settings.new("com.github.camelneeraj.sysmontask")
        self.config=Configurations()
        self.notebook=None
        self.search_entry=None
        self.tree=None
        self.top_of_tree=None
        self.last_vscroll_max=0    #need to check these two
        self.last_vscroll_value=0
        self.treeView_selection=None


        logger.debug(f"<----")

    def do_startup(self):
        """
        It does the startup of the application. Will be called right after constructor is called.
        """
        logger.debug(f"---->")

        gtk.Application.do_startup(self)

        ## load resources will see it.

        #### Creating the Actions and adding them to the application. ####
        action=gio.SimpleAction.new("quit",None)
        action.connect("activate",self.on_quit_activate)
        self.add_action(action)

        action=gio.SimpleAction.new("help",None)
        action.connect("activate",self.on_help_activate)
        self.add_action(action)

        action=gio.SimpleAction.new("about",None)
        action.connect("activate",self.on_about_activate)
        self.add_action(action)

        ## More action need to added. ##
        ## preference in file menu



        ####### add accelerator #######
        self.set_accels_for_action("app.help",["F1"])
        self.set_accels_for_action("app.quit",["<Primary>q"])
        self.set_accels_for_action("win.show-hierarchy",["<Primary>h"])

        ####### Load Settings ######
        self.load_settings()

        #### prettytable ####
        self.prettyProcTable=PrettyProcTable()

        #### Create Main Window ####
        create_main_window(self)
        self.main_window.set_default_icon_name("com.github.SysMonTask")

        self.set_accels_for_action("win.refresh",["<Primary>r"])

        logger.debug(f"<----")


    def do_activate(self):
        """
        Called when the application is ready.
        """
        logger.debug(f"SmtApplication::do_activate ------>")
        # gtk.Application.do_activate(self)
        self.main_window.present()
        logger.debug(f"SmtApplication::do_activate <------")


    def do_command_line(self):
        """
        For handling the command line options.
        """
        logger.debug(f"SmtApplication::do_command_line ------>")

        logger.debug(f"SmtApplication::do_command_line <------")

    def do_shutdown(self):
        """
        Do the shutdown tasks.
        """
        logger.debug(f"SmtApplication::do_shutdown ------>")
        self.save_config()
        gtk.Application.do_shutdown(self)
        
        #### Application Quit ####
        self.quit()

        logger.debug(f"SmtApplication::do_shutdown <------")

    def on_quit_activate(self,action,data):
        """
        On closing the application.
        """
        logger.debug(f"SmtApplication::on_quit_activate ------>")

        self.do_shutdown()

        logger.debug(f"SmtApplication::on_quit_activate <------")

    def on_help_activate(self,action,data):
        """
        On Help.
        """
        logger.debug(f"SmtApplication::on_help_activate ------>")

        helpDial=HelpDial()

        logger.debug(f"SmtApplication::on_help_activate <------")


    def on_about_activate(self,action,data):
        """
        On About.
        """
        logger.debug(f"---->")

        author=["Neeraj Kumar aka camel.neeraj"]
        documentor=["Neeraj Kumar aka camel.neeraj"]
        artist=["Neeraj Kumar aka camel.neeraj"]

        logger.info("Creating the About Dialog")
        aboutDialog=gtk.AboutDialog(self.main_window,
            name="SysMonTask",
            comments="A Windows Like Task Manager, offering simple and higher control on system monitoring.",
            version=VERSION,
            authors=author,
            documenters=documentor,
            artists=artist,
            website="https://github.com/KrispyCamel4u/SysMonTask",
            copyright="Copyright © 2021-2022 Neeraj Kumar",
            license_type=gtk.License.BSD_3,
            logo_icon_name="com.github.SysMonTask"
        )
        logger.info("Showing About Dialog")
        # aboutDialog.show()
        if aboutDialog.run()==-4:
            aboutDialog.destroy()

        logger.debug(f"<----")

    def load_settings(self):
        """
        Loads the Settings from the gsetting schemas.
        """
        logger.debug(f"SmtApplication::load_settings ------>")

        #### Get the Configs from the settings ####
        # self.config.network_unit_in_bits=self.settings.get_boolean("network-in-bits")
        # self.settings.connect("changed::network-in-bits",cb_network_in_bits_changed,self)
        
        #### update Interval ####
        self.settings.connect("changed::proc-update-interval",cb_proc_update_interval_changed,app)

        #### Time window ####

        #### color information ####
        logger.debug(f"SmtApplication::load_settings <------")

    def save_config(self):
        """
        Save the configuration of the application.
        """
        logger.debug(f"SmtApplication::save_config ------>")

        self.settings.set_value("window-state",glib.Variant("(iiii)",self.main_window.get_size()+self.main_window.get_position()))
        self.settings.set_boolean("maximized",self.main_window.is_maximized())

        logger.debug(f"SmtApplication::save_config <-----")


if __name__=="__main__":
    app=SmtApplication()
    app.run()