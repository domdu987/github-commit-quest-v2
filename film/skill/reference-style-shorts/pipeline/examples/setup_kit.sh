#!/bin/sh
# setup_kit.sh : regenerate every cache a first render needs, in order, after scripts/bootstrap.py.
#   cd <PROJ> && sh examples/setup_kit.sh            (about 80 s on 4 cores; about 150 MB written)
# The skill ships code, not texture or sprite caches. Each step below is a no-op when its cache is current.
set -e
cd "$(dirname "$0")/.."
PROJ=$(pwd)
[ -n "$NODE_PATH" ] || NODE_PATH=$(npm root -g 2>/dev/null) && export NODE_PATH   # the node calls default to /opt/node22/lib/node_modules
node -e "require('playwright')" || { echo "playwright not found under NODE_PATH=$NODE_PATH"; exit 1; }
python3 -c "import bpy, numpy, PIL, cv2, fontTools" || { echo "missing python package (bpy numpy pillow opencv-python-headless fonttools)"; exit 1; }

# 1. Thai fonts where v3/paper/paper.py looks for them (fonts/th/). The skill ships both Kanit files there (SIL Open Font
#    License, fonts/th/OFL-Kanit.txt); the lines below only fill in a missing file, with Kanit Black standing in.
mkdir -p fonts/th
[ -f fonts/th/Kanit_900Black.ttf ] || cp fonts/Kanit_900Black.ttf fonts/th/
[ -f fonts/th/Kanit_800ExtraBold.ttf ] || { cp fonts/Kanit_900Black.ttf fonts/th/Kanit_800ExtraBold.ttf; echo "NOTE fonts/th/Kanit_800ExtraBold.ttf was missing: a copy of Kanit Black stands in"; }
[ -f /usr/share/fonts/opentype/tlwg/Loma-Bold.otf ] || echo "WARNING Loma-Bold.otf missing (apt-get install fonts-tlwg-loma-otf): typed Thai on paper props falls back"

t() { s=$(date +%s); "$@"; echo "   done in $(( $(date +%s) - s )) s: $*" >&2; }
t python3 v3/set3d/textures.py > /dev/null                      # office artwork -> v3/set3d/tex (needed by every office, kitchen and mech shot)
t python3 v3/paper/paper.py build                               # paper and text artwork -> v3/paper/tex (spinner disc, label, calendar, newspaper)
t python3 v3/set3d_ext/light/gen_tex.py > /dev/null             # office_grey / office_storm skies and rain loops (reads set3d/tex/sky.png: after step 1)
t python3 v3/set3d_ext/props/make_hi_map.py 2000                # 6000 px wall map (mech shots and any lens under ~1 D from the map)
t python3 v3/set3d_beach/beach_tex.py > /dev/null               # beach artwork
t python3 v3/set3d_kitchen/kitchen_tex.py > /dev/null           # kitchen artwork and its sequences (the kitchen set also reads paper/tex)
echo "kit ready in $PROJ. Next: cd examples && python3 smoke.py"
