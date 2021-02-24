import errno
import os
import sys,re

def getPrivilege(graphical=True):

    if os.getuid() == 0 :
        print('acquired root permission')
        return

    p=os.popen('zenity --password')
    passs=p.readline()[:-1]    
    p.close()
    passs=re.sub(' ','\ ',passs)

    args = [sys.executable] + sys.argv
    # os.system ('pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY '+' '.join(args))
    os.system('echo '+passs+ '| sudo -S ' + ' '.join(args))
    exit()
    # print(args)
