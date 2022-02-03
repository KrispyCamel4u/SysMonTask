class HelpDial():
    """
    Help Dialog to show Doc from Github.
    """
    help_win=None
    def __init__(self):
        #### We only allow one Help Window ####
        if not HelpDial.help_win:
            from gi.repository import WebKit2 as Webkit,Gtk as gtk
            HelpDial.help_win = gtk.Window()
            HelpDial.help_win.connect("destroy",self.on_help_dial_destroy)
            HelpDial.help_win.set_default_size(800,600)

            scrollwindow=gtk.ScrolledWindow()

            webview = Webkit.WebView()
            webview.load_uri("https://github.com/KrispyCamel4u/SysMonTask/blob/v2.0.0/DOCS.md")
            set=webview.get_settings()
            # set.set_enable_back_forward_navigation_gestures(True)
            # set.set_enable_offline_web_application_cache(True)

            scrollwindow.add(webview)

            header=gtk.HeaderBar()
            header.set_show_close_button(True)

            #### Backword in history button ####
            button=gtk.Button()
            button.add(gtk.Arrow(gtk.ArrowType.LEFT))
            button.connect("clicked",self.go_backword,webview)
            header.pack_start(button)

            #### Forward In History Button ####
            button=gtk.Button()
            button.add(gtk.Arrow(gtk.ArrowType.RIGHT))
            button.connect("clicked",self.go_forward,webview)
            header.pack_start(button)

            header.props.title="SysMonTask Help"

            HelpDial.help_win.set_titlebar(header)

            HelpDial.help_win.add(scrollwindow)
            HelpDial.help_win.show_all()

    def on_help_dial_destroy(self,widget):
        """
        On closing the Help Window.
        """
        HelpDial.help_win=None

    def go_backword(self,widget,webview):
        """ Go back in history.

        Args:
            widget (gtk.Button): Button which gets clicked.
            webview (WebKit2.WebView): Web View which shows the content.
        """
        webview.go_back()

    def go_forward(self,widget,webview):
        """ Go Forward in history.

        Args:
            widget (gtk.Button): Button which gets clicked.
            webview (WebKit2.WebView): Web View which shows the content.
        """
        webview.go_forward()