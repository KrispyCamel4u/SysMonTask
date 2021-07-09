import os,glob
dir_path=os.path.dirname(os.path.abspath(__file__))
# dir_path='.'
# Finding all the themes available on the system
themes_available :list =glob.glob('/usr/share/themes/*')

# variables of type list to store the names of light and dark themes_available
light_themes,dark_themes=[],[]

# Finding the dark and light themes
for theme in themes_available:
    theme_name=theme.split('/')[-1]
    if 'dark' in theme_name.lower() or 'black' in theme_name.lower():
        dark_themes.append(theme_name)
    else:
        light_themes.append(theme_name)

def set_theme_default():
    """
    In default mode, the system theme is applied. The rooter.py file content is replaced with rooter_default.py.
    """
    try:
        os.system('cp {0}/rooter_default.py {0}/rooter.py'.format(dir_path))
        print('Setting to default: Done:)')
    except Exception as e:
        print(f"Failed to set Theme:( \nRun with sudo(root privileges) is required.\nError: {e}")


def set_theme_light():
    """
    Force setting the light theme. The rooter.py file is modified with the theme name selected.
    """
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
    except Exception as e:
        print(f"Failed to set Theme:( \nRun with sudo(root privileges) is required.\nError: {e}")

def set_theme_dark():
    """
    Force setting the dark theme. The rooter.py file is modified with the theme name selected.
    """
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
    except Exception as e:
        print(f"Failed to set Theme:( \nRun with sudo(root privileges) is required.\nError: {e}")