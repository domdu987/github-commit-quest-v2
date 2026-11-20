#!/bin/bash
cd "$(dirname "$0")"; python3 render_t5a.py range $1 $2 >> render_$1.log 2>&1
