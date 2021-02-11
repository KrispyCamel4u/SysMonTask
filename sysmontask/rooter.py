

import errno
import os
import sys

def getPrivilege(graphical=True):

    if os.getuid() == 0 :
        return

    args = [sys.executable] + sys.argv
    commands = []

    if graphical:
        if sys.platform.startswith("linux"):
            commands.append(["pkexec env DISPLAY={0} XAUTHORITY={1}".format(os.environ.get("DISPLAY"),os.environ.get("XAUTHORITY"))] + args)
            commands.append(["gksudo"] + args)
            commands.append(["kdesudo"] + args)

    commands.append(["sudo"] + args)
    

    for args in commands:
        try:
            os.execlp(args[0].split()[0], *args)
        except OSError as e:
            if e.errno != errno.ENOENT or args[0] == "sudo":
                raise
        # env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY