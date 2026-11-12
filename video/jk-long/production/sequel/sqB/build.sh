#!/bin/bash
# build.sh: assemble the episode template from parts and build the HyperFrames project
cd "$(dirname "$0")"
cat head.part sigcard.part helpers0.part ../cm.part shots*.part foot.part > ep.tmpl.html && python3 make.py
