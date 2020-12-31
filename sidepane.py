from gi.repository import Gtk as g , GObject as go, Gdk
import os,cairo,re,psutil as ps

from mem import *

def sidepaneinit(self):
    print("initialisating sidepane")
    self.cpuSidePaneLabelValue=self.builder.get_object('cpusidepanelabelvalue')
    self.cpuSidePaneDrawArea=self.builder.get_object('cpusidepanedrawarea')

