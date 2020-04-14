#!/usr/bin/python3
import PyInstaller.__main__

PyInstaller.__main__.run([
    '--name=nestingnote',
    '--onefile',
    '--console',
    '--icon=nestingdoll.ico',
    os.path.join('nestingnote', '__main__.py'),
