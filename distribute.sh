#!/bin/bash
rm -rf build/
rm -rf dist/
rm -rf nestingnote.egg-info/
rm -f nestingnote.spec
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*

