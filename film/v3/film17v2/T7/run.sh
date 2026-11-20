#!/bin/bash
cd "$(dirname "$0")"
until [ "$(ls frames/g_*.png 2>/dev/null | wc -l)" -ge 186 ]; do python3 render_T7.py 1689 1874 frames >> render.log 2>&1; sleep 5; done
