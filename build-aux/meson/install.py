from setuptools import setup

setup(
    name='sysmontask',
    data_files=get_data_files(),
    entry_points=dict(
        console_scripts=[
            'sysmontask=sysmontask.sysmontask:start',
            'sysmontask.set_default=sysmontask.theme_setter:set_theme_default',
            'sysmontask.set_light=sysmontask.theme_setter:set_theme_light',
            'sysmontask.set_dark=sysmontask.theme_setter:set_theme_dark']
    )
)
