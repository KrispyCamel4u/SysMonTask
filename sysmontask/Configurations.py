
from Log import Log, staticVar

logger = staticVar.logger

class Configurations:
    """
    It holds the configurations for the SysMonTask.
    """
    __slots__=[
    "proc_update_interval",
    "graph_update_interval",
    "disk_update_interval",
    "colors",
    "network_unit_in_bits",
    "network_total_unit_in_bits"
    ]
    def __init__(self,settings=None):
        if settings:
            self.proc_update_interval=settings.get_int("proc-update-interval")
        else:
            self.proc_update_interval=None
            self.graph_update_interval=None
            self.disk_update_interval=None
            self.colors=None
            self.network_unit_in_bits=None
            self.network_total_unit_in_bits=None