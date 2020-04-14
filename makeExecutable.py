#!/usr/bin/python3
import PyInstaller.__main__
from os import path
import platform

PyInstaller.__main__.run([
    '--name=nestingnote',
    '--onefile',
    '--console',
    '--specpath=dist',
    '--distpath={}'.format(path.join('executable', platform.system())),
#    '--icon={}'.format(path.join('dolly.ico')),
    path.join('nestingnote', '__main__.py'),
])
