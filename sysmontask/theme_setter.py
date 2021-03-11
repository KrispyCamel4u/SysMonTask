import os,glob
dir_path=os.path.dirname(os.path.abspath(__file__))
# dir_path='.'
themes_available=glob.glob('/usr/share/themes/*')
light_themes=[]
dark_themes=[]
for theme in themes_available:
    theme_name=theme.split('/')[-1]
    if 'dark' in theme_name or 'black' in theme_name:
        dark_themes.append(theme_name)
    else:
        light_themes.append(theme_name)

def set_theme_default():    
    try:
        os.system('cp {0}/rooter_default.py {0}/rooter.py'.format(dir_path))
        print('Setting to default: Done:)')
    except:
        print("Failed to set Theme:( \nRun with sudo(root privileges) is required.")

    
def set_theme_light():
    try:
        for index,theme in enumerate(light_themes):
            print(index,':',theme)

        index=int(input('Index for Corresponding Theme that you want to apply?:'))
        with open(dir_path+'/rooter.py') as ifile:
            original_rooter=ifile.readlines()
        with open(dir_path+'/rooter.py','w') as ofile:
            for line in original_rooter:
                if 'return 0' in line:
                    continue
                if 'os.system(' in line:
                    # ofile.write("    os.system('pkexec env GTK_THEME={0} DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY '+' '.join(args))\n".format(light_themes[index]))
                    ofile.write("    os.system('GTK_THEME={0} sysmontask')\n".format(light_themes[index]))
                else:
                    ofile.write(line)
        print('Setting of Light Theme Done:)')
    except:
        print("Failed to set Theme:( \nRun with sudo(root privileges) is required.")

def set_theme_dark():
    try:
        for index,theme in enumerate(dark_themes):
            print(index,':',theme)
        index=int(input('Index for Corresponding Theme that you want to apply?:'))
        with open(dir_path+'/rooter.py') as ifile:
            original_rooter=ifile.readlines()
        with open(dir_path+'/rooter.py','w') as ofile:
            for line in original_rooter:
                if 'return 0' in line:
                    continue
                if 'os.system(' in line:
                    # ofile.write("    os.system('pkexec env GTK_THEME={0} DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY '+' '.join(args))\n".format(light_themes[index]))
                    ofile.write("    os.system('GTK_THEME={0} sysmontask')\n".format(dark_themes[index]))
                else:
                    ofile.write(line)
        print('Setting of Dark Theme Done:)')
    except:
        print("Failed to set Theme:( \nRun with sudo(root privileges) is required.")