import os
# import sys

def theme_agent():
    return 0
    if os.path.exists("{}/.sysmontask".format(os.environ.get("HOME"))):
        with open("{}/.sysmontask".format(os.environ.get("HOME")),'r') as ifile:
            if ifile.read()=='1':
                return
    else:
        with open("{}/.sysmontask".format(os.environ.get("HOME")),'w+') as ofile:
            pass
    with open("{}/.sysmontask".format(os.environ.get("HOME")),'w') as ofile:
        ofile.write('1')
    # args = [sys.executable] +sys.argv
    # args = ['env GTK_THEME=Yaru-light']+sys.argv
    print('In rooter')
    # os.system ('pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY '+' '.join(args))
    # os.system ('echo '+passs+ '| sudo -S ' + ' '.join(args))
    os.system("")
    exit()
    # print(args)