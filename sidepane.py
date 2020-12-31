from gi.repository import Gtk as g , GObject as go, Gdk
import os,cairo,re,psutil as ps

from mem import *

def sidepaneinit(self):
    print("initialisating sidepane")
    self.cpuSidePaneLabelValue=self.builder.get_object('cpusidepanelabelvalue')
    self.cpuSidePaneDrawArea=self.builder.get_object('cpusidepanedrawarea')

    self.memSidePaneLabelValue=self.builder.get_object('memsidepanelabelvalue')
    self.memSidePaneDrawArea=self.builder.get_object('memsidepanedrawarea')

def sidePaneUpdate(self):
    self.memSidePaneLabelValue.set_text(str(self.usedd)+'/'+str(self.memTotal)+" GiB\n"+str(self.memPercent)+' %')