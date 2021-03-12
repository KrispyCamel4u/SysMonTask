import os
file_path=os.path.dirname(os.path.abspath(__file__))
pathh=os.path.join(file_path,'../usr/share')
if not os.path.exists('/usr/share/applications/SysMonTask.desktop'):
    os.system("pkexec {0}/move.sh {1} {0}".format(file_path,pathh))
    print("copying done")