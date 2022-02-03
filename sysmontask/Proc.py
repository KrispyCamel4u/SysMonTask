from gi.repository.GLib import file_get_contents
import psutil as ps
from os.path import isfile, exists

from Log import Log,staticVar

logger=staticVar.logger

class ProcInfo(ps.Process):
    """Information for a single process."""
    # has_cgroups=None
    __slots__ = ['cmdLine','tooltip','pname','ppId','uId','startTime']

    def __init__(self,pid):
        super().__init__(pid)
        logger.debug("ProcInfo---->")

        self.cmdLine=self.cmdline()
        self.tooltip=" ".join(self.cmdLine)
        self.pname=self.name()
        self.ppId=self.ppid()
        self.uId=self.uids()
        self.startTime=self.create_time()
        self.cgroups=self.get_proc_cgroups_info()

        logger.debug("ProcInfo<----")

    # def is_cgroups_enabled(self):
    #     """ To check if cgroups are enabled on the platform. """
    #     logger.debug("---->")

    #     if isfile("/proc/cgroups"):
    #         logger.info("cgroups: ok<---")
    #         return True
    #     logger.debug("<----")
    #     return False


    def get_proc_cgroups_info(self):
        """ Get the cgroups information for the process."""
        logger.debug("---->")

        if not isfile("/proc/cgroups"):     # can be removed and use the static var
            logger.info("cgroups: Not found<---")
            return None

        state,val=file_get_contents(f"/proc/{self.pid}/cgroup")
        if state:
            return val
        return None

        logger.debug("<----")


class ProcList:
    """Class for holding the ALL processes info."""
    def __init__():
        logger.debug("---->")



        logger.debug("<----")