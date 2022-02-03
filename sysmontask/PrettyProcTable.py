from gi.repository import Gdk as gdk, Wnck, GLib as glib,Gio as gio,GdkPixbuf, Gtk as gtk

from Log import Log,staticVar

APP_ICON_SIZE=16

logger=staticVar.logger

class PrettyProcTable:
    """Class to decorate the process table with Icons."""
    def __init__(self):
        logger.debug("---->")
        #### if wnck and gdk_windowing_x11
        wnckScreen=Wnck.Screen.get_default()
        if wnckScreen:
            logger.info("Wnck Screen: OK")
            wnckScreen.connect("application_opened",self.__on_application_opened)
            wnckScreen.connect("application_closed",self.__on_application_closed)

        #### caching Gio.AppInfo for applications ####
        self.gio_apps: Mapping[str,Gio.AppInfo]={}

        #### Icons lookup for pid ####
        self.procIcons: Mapping[int,GdkPixbuf]={}

        #### Gio.FileMonitor for data dirs path ####
        self.monitors: Mapping[str,Gio.FileMonitor]={}

        system_data_dir=glib.get_system_data_dirs()
        for dirPath in system_data_dir:
            dirPath+="/applications"
            monitor=gio.File.new_for_path(dirPath).monitor_directory(gio.FileMonitorFlags.WATCH_MOVES,None)
            monitor.set_rate_limit(2000)    #### 2 sec

            monitor.connect("changed",self.__on_fileMonitor_change_event)
            self.monitors[dirPath]=monitor

        self.__gio_app_cache_init()

        logger.debug("<----")

    def set_icon(self):
        """For setting the icon for the process."""
        logger.debug("---->")


        logger.debug("<----")

    def __on_fileMonitor_change_event(self,file,newFile,event):
        logger.debug("---->")

        self.__gio_app_cache_init()

        logger.debug("<----")

    def __gio_app_cache_init(self):
        """Cache the application(Gio.AppInfo), to map it with executable name."""
        logger.debug("---->")

        self.gio_apps.clear() ## miight need change ###

        apps=gio.AppInfo.get_all()
        for app in apps:
            exe=app.get_executable()
            if not exe=="sh" and not exe=="env":
                self.gio_apps[exe]=app

        logger.debug("<----")

    def __on_application_opened(self,screen,app):
        """Callback when a new application on the screen is opened."""
        logger.debug("---->")

        pid=app.get_pid()
        if not pid:
            logger.info(f"[BAD]: PID:{pid} for {app.get_name()}")
            logger.debug("<----")
            return
        # icon_name=app.get_icon_name().split()[-1] ### because name are like
        # logger.info(f"ICON NAME {icon_name}")
        # try:
        #     icon=gtk.IconTheme.load_icon(gtk.IconTheme.get_default(),icon_name,APP_ICON_SIZE,gtk.IconLookupFlags.USE_BUILTIN)
        # except Exception as e:
        #     logger.error(f"[BAD]: IconTheme.load_icon() for {app.get_name()}\n\t\tmsg:{e}")
        #     icon=None

        # if not icon:
        #     logger.info(f"Icon NONE")
        logger.info(f"Getting Icon from wnck for : {app.get_name()}")
        icon=app.get_icon().scale_simple(APP_ICON_SIZE,APP_ICON_SIZE,GdkPixbuf.InterpType.BILINEAR)

        if not icon:
            logger.info(f"[Failed] Wnck Icon not found for {app.get_name()}")
            logger.debug("<---")
            return

        ## Need to add some register_application ##
        self.procIcons[pid]=icon

        logger.debug("<----")

    def __on_application_closed(self,screen,app):
        """Callback when a application is closed."""
        logger.debug("---->")

        pid=app.get_pid()
        if not pid:
            logger.info(f"PID:{pid} for {app.get_name()}")
            return

        ## unregister_application ##
        self.procIcons.pop(pid)
        logger.info(f"{app.get_name()},{pid} deleted from procIcons")

        logger.debug("<----")
