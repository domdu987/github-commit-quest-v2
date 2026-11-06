"""Copy a built vertical project to <dst> and re-lay it at 1920x1080 with landscape.js.  usage: toland.py <src proj> <dst proj> [landfix.json]"""
import json, os, shutil, sys
src, dst = sys.argv[1], sys.argv[2]
fix = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else {}
if os.path.isdir(dst) and os.path.basename(dst).startswith("L"): shutil.rmtree(dst)
shutil.copytree(src, dst)
shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)), "landscape.js"), os.path.join(dst, "assets"))
p = os.path.join(dst, "index.html"); s = open(p).read()
for a, b in [('content="width=1080, height=1920"', 'content="width=1920, height=1080"'), ('width: 1080px; height: 1920px;', 'width: 1920px; height: 1080px;'), ('data-width="1080" data-height="1920"', 'data-width="1920" data-height="1080"'), ('<script src="assets/engine.js"></script>', '<script src="assets/engine.js"></script>\n    <script>window.LANDSCAPE = {};</script>\n    <script src="assets/landbg.js"></script>\n    <script src="assets/landscape.js"></script>')]:
    assert a in s, a; s = s.replace(a, b)
a = "Engine.build(root, tl, shots);"; assert s.count(a) == 1, s.count(a)
s = s.replace(a, f"const LANDFIX = {json.dumps(fix)};\n      shots.forEach((sh) => {{ if (LANDFIX[sh.key] != null) sh.land = typeof LANDFIX[sh.key] === 'object' ? LANDFIX[sh.key] : {{ y0: LANDFIX[sh.key] }}; }});\n      " + a)
s = s.replace('</style>', '\n      .clip > .capwrap .capbox { font-size: 50px; }\n      .clip > .capwrap { top: 905px !important; }\n      .clip.lfit { background: radial-gradient(ellipse 60% 80% at 50% 50%, #1a2226, #05080a); }\n      .clip[style*="visibility: hidden"] { display: none !important; }\n      .badge { bottom: 40px; }\n    </style>', 1)
open(p, "w").write(s)
c = os.path.join(dst, "assets", "cine.js"); t = open(c).read()
for a, b in [('x="0" y="0" width="${W}" height="${H}" color-interpolation-filters', 'x="-2400" y="-600" width="5880" height="3120" color-interpolation-filters'),
             ('<rect id="${id}-cineflash" width="${W}" height="${H}"', '<rect id="${id}-cineflash" x="-660" width="2400" height="${H}"'),
             ('<rect id="${gid}" width="${W}" height="${H}"', '<rect id="${gid}" x="-660" width="2400" height="${H}"')]:
    assert t.count(a) == 1, a; t = t.replace(a, b)
open(c, "w").write(t)
print("landscape", dst)
