

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
            commands.append(["pkexec env DISPLAY=:1 XAUTHORITY=/run/user/1000/gdm/Xauthority"] + args)
            commands.append(["gksudo"] + args)
            commands.append(["kdesudo"] + args)

    commands.append(["sudo"] + args)

    for args in commands:
        try:
            print(args[0],args)
            os.execlp('pkexec', *args)
        except OSError as e:
            if e.errno != errno.ENOENT or args[0] == "sudo":
                raise
        # env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY