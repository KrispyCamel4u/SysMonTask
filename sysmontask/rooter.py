

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
            # commands.append(["pkexec env DISPLAY={0} XAUTHORITY={1}".format(os.environ.get("DISPLAY"),os.environ.get("XAUTHORITY"))] + args)
            commands.append(["pkexec env DISPLAY=:1 XAUTHORITY=/run/user/1000/gdm/Xauthority"] + args)
            # pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY
            commands.append(["gksudo"] + args)
            commands.append(["kdesudo"] + args)

    commands.append(["sudo"] + args)
    

    for args in commands:
        try:
            # os.execl'p(args[0].split()[0], *args)
            os.system('pkexec env DISPLAY=:1 XAUTHORITY=/run/user/1000/gdm/Xauthority /usr/bin/python3 /home/neeraj/projects/task_manager/sysmontask/sysmontask/sysmontask.py')
            exit()
        except OSError as e:
            if e.errno != errno.ENOENT or args[0] == "sudo":
                raise
        # env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY