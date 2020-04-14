#!/bin/bash
rm -rf build/
rm -rf dist/
rm -rf nestingnote.egg-info/
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*

