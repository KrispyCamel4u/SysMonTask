from setuptools import setup, find_packages

def get_data_files():
    data_files = [('share/sysmontask/glade_files', ['glade_files/disk.glade','glade_files/diskSidepane.glade','glade_files/gpu.glade',
    'glade_files/gpuSidepane.glade','glade_files/net.glade','glade_files/netSidepane.glade','glade_files/sysmontask.glade']),
    ('share/sysmontask/icons',['icons/SysMonTask.png']),
    ('share/doc/sysmontask',['AUTHORS', 'README.md','LICENSE']),
    ('share/applications',['SysMonTask.desktop'])
    ]

    return data_files

setup(
    name='sysmontask',
    version='1.1.1',
    description='System Monitor With UI Like Windows',
    url='http://github.com/krispycamel4u',
    author='Neeraj Kumar',
    author_email='neerajjangra4u@gmail.com',
    license='BSD-3',
    include_package_data=True,
    data_files=get_data_files(),
    install_requires=['psutil >=5.8','pip','PyGObject'],
    packages=find_packages(),
    entry_points=dict(
        console_scripts=[
            'sysmontask=sysmontask.sysmontask:start',
            'sysmontask.set_default=sysmontask.theme_setter:set_theme_default',
            'sysmontask.set_light=sysmontask.theme_setter:set_theme_light',
            'sysmontask.set_dark=sysmontask.theme_setter:set_theme_dark']
    )
)