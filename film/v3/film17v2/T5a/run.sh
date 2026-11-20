#!/bin/bash
cd "$(dirname "$0")"; python3 render_t5a.py range 1039 1210 >> render.log 2>&1
