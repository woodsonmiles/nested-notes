#!/usr/bin/python3
import PyInstaller.__main__
from os import path

PyInstaller.__main__.run([
    '--name=nestingnote',
    '--onefile',
    '--console',
    '--icon=nestingdoll.ico',
    path.join('nestingnote', '__main__.py'),
])