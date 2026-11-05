"""Turn a built vertical ทะเลลด project into its 16:9 (1920x1080) long-form version, in place.

    python3 land.py <project dir> [badge text]

Edits (video/longform/README.md + the 16:9 paint fix):
  - viewport, html/body and #root sizes, #root data-width/height -> 1920x1080
  - window.LANDSCAPE = {} and assets/landscape.js after engine.js (landscape.js copied from video/longform/)
  - CSS: 50 px captions, the lfit backdrop, badge at the bottom, and
    .clip[style*="visibility: hidden"] { display: none !important; } so Chrome does not run out of raster memory
    (black tiles) with every widened clip laid out at once
  - the corner badge: one name for the whole film (default "ทะเลลด") instead of "ทะเลลด · EP.N"
"""
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
proj = sys.argv[1]
badge = sys.argv[2] if len(sys.argv) > 2 else "ทะเลลด"
p = os.path.join(proj, "index.html")
s = open(p).read()
assert "<script>window.LANDSCAPE = {};</script>" not in s, "already landscape"


def sub(a, b, count=1):
    global s
    n = s.count(a)
    assert n == count, f"expected {count} x {a!r}, found {n}"
    s = s.replace(a, b)


sub('content="width=1080, height=1920"', 'content="width=1920, height=1080"')
sub("html, body { width: 1080px; height: 1920px;", "html, body { width: 1920px; height: 1080px;")
sub("#root { position: relative; width: 1080px; height: 1920px;", "#root { position: relative; width: 1920px; height: 1080px;")
sub('data-width="1080" data-height="1920"', 'data-width="1920" data-height="1080"')
sub('<script src="assets/engine.js"></script>',
    '<script src="assets/engine.js"></script>\n    <script>window.LANDSCAPE = {};</script>\n    <script src="assets/landscape.js"></script>')
css = ("\n      .clip > .capwrap .capbox { font-size: 50px; }"
       "\n      .clip.lfit { background: radial-gradient(ellipse 60% 80% at 50% 50%, #1a2226, #05080a); }"
       "\n      .badge { bottom: 40px; }"
       '\n      .clip[style*="visibility: hidden"] { display: none !important; }'
       "\n    </style>")
i = s.index("</style>")
s = s[:i] + css + s[i + len("</style>"):]
s, n = re.subn(r'<div class="badge" id="badge">ทะเลลด · EP\.\d</div>', f'<div class="badge" id="badge">{badge}</div>', s)
assert n == 1, "badge not found"
open(p, "w").write(s)
shutil.copy(os.path.join(HERE, "landscape.js"), os.path.join(proj, "assets", "landscape.js"))
print("landscape:", proj, "badge:", badge)
