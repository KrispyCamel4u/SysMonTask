from setuptools import setup, find_packages
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

def get_data_files():
    data_files = [('/usr/share/sysmontask/glade_files', ['glade_files/disk.glade','glade_files/diskSidepane.glade','glade_files/gpu.glade',
    'glade_files/gpuSidepane.glade','glade_files/net.glade','glade_files/netSidepane.glade','glade_files/sysmontask.glade','glade_files/filter_dialog.glade']),
    ('/usr/share/sysmontask/icons',['icons/SysMonTask.png','icons/choose_color.png','icons/hide.png','icons/reset-color.png','icons/show.png']),
    ('/usr/share/doc/sysmontask',['AUTHORS', 'README.md','LICENSE']),
    ('/usr/share/applications',['SysMonTask.desktop']),
    ('/usr/share/glib-2.0/schemas',['com.github.camelneeraj.sysmontask.gschema.xml'])
    ]

    return data_files

setup(
    name='sysmontask',
    version='1.x.x',
    description='System Monitor With UI Like Windows',
    url='https://github.com/KrispyCamel4u/SysMonTask',
    author='Neeraj Kumar',
    author_email='neerajjangra4u@gmail.com',
    license='BSD-3',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        'Topic :: System :: Monitoring',
    ],
    include_package_data=True,
    data_files=get_data_files(),
    install_requires=['psutil>=5.7.2','PyGObject','pycairo'],
    packages=find_packages(),
    entry_points=dict(
        console_scripts=[
            'sysmontask=sysmontask.sysmontask:start',
            'sysmontask.set_default=sysmontask.theme_setter:set_theme_default',
            'sysmontask.set_light=sysmontask.theme_setter:set_theme_light',
            'sysmontask.set_dark=sysmontask.theme_setter:set_theme_dark']
    )
)

os.system("sudo glib-compile-schemas /usr/share/glib-2.0/schemas")
print("gschema Compiled")