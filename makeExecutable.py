#!/usr/bin/python3
import PyInstaller.__main__
from os import path
import platform


#    '--specpath=dist',
PyInstaller.__main__.run([
    '--name=nestingnote',
    '--onefile',
    '--console',
    '--distpath={}'.format(path.join('executable', platform.system())),
    '--icon=doll.ico',
    path.join('nestingnote', '__main__.py'),
])
