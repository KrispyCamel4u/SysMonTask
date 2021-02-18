import errno
import os
import sys

def getPrivilege(graphical=True):

    if os.getuid() == 0 :
        print('acquired root permission')
        return

    args = [sys.executable] + sys.argv
    os.system('pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY '+' '.join(args))
    exit()
    # print(args)
