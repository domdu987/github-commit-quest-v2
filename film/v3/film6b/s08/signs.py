"""signs.py -- Thai text props for film 6b s08 (SVG in D units, Kanit Black embedded as a data-URI @font-face, rasterised with
headless Chromium after document.fonts.ready).  Ink outline like the set (plum ink #2a1630)."""
import os, json, base64, hashlib, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
FONT = os.path.join(PROJ, "fonts", "Kanit_900Black.ttf")
NODE_PATH = os.environ.get("NODE_PATH", "/opt/node22/lib/node_modules")
INK = "#2a1630"
_F = None


def _font():
    global _F
    if _F is None:
        _F = base64.b64encode(open(FONT, "rb").read()).decode()
    return _F


def board_svg(text, w, h, fs, wood=("#c98a4e", "#8a5226", "#e8b27a"), txt="#fff4d8", rope=True):
    """hanging shop board: wooden plank w x h D (centre at 0, 0), two ropes up, bold text with a thick ink outline."""
    x0, y0 = -w / 2, -h / 2
    o = ['<defs><style>@font-face{font-family:K;src:url(data:font/ttf;base64,%s) format("truetype");}</style></defs>' % _font()]
    if rope:
        for sx in (-0.38, 0.38):
            o.append('<line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f" stroke="%s" stroke-width="0.05"/>' % (sx * w, y0 - 0.6, sx * w, y0 + 0.05, INK))
            o.append('<line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f" stroke="#c8a870" stroke-width="0.022"/>' % (sx * w, y0 - 0.6, sx * w, y0 + 0.05))
    o.append('<rect x="%.3f" y="%.3f" width="%.3f" height="%.3f" rx="0.08" fill="%s" stroke="%s" stroke-width="0.06"/>' % (x0, y0, w, h, wood[0], INK))
    o.append('<rect x="%.3f" y="%.3f" width="%.3f" height="%.3f" rx="0.05" fill="none" stroke="%s" stroke-width="0.035"/>' % (x0 + 0.08, y0 + 0.08, w - 0.16, h - 0.16, wood[1]))
    for k in range(3):
        yy = y0 + h * (0.28 + 0.24 * k)
        o.append('<path d="M%.3f %.3f q %.3f -0.03 %.3f 0" stroke="%s" stroke-width="0.012" fill="none" opacity="0.5"/>' % (x0 + 0.15, yy, w * 0.3, w * 0.6, wood[1]))
    o.append('<rect x="%.3f" y="%.3f" width="%.3f" height="0.06" rx="0.03" fill="%s" opacity="0.6"/>' % (x0 + 0.1, y0 + 0.1, w - 0.2, wood[2]))
    st = 'font-family:K;font-size:%.3fpx;font-weight:900;text-anchor:middle;dominant-baseline:central' % fs
    o.append('<text x="0" y="%.3f" style="%s" fill="none" stroke="%s" stroke-width="%.3f" stroke-linejoin="round">%s</text>' % (0.02, st, INK, fs * 0.22, text))
    o.append('<text x="0" y="%.3f" style="%s" fill="%s">%s</text>' % (0.02, st, txt, text))
    return "".join(o), (x0 - 0.05, y0 - (0.65 if rope else 0.05), -x0 + 0.05, -y0 + 0.05)


def tag_svg(text, w, h, fs):
    """paper price tag (parchment, punched hole + string to the left), red ink text."""
    x0, y0 = -w / 2, -h / 2
    o = ['<defs><style>@font-face{font-family:K;src:url(data:font/ttf;base64,%s) format("truetype");}</style></defs>' % _font()]
    p = "M%.3f %.3f L%.3f %.3f L%.3f %.3f L%.3f %.3f L%.3f %.3f Z" % (x0 + 0.12, y0, -x0, y0, -x0, -y0, x0 + 0.12, -y0, x0, 0)
    o.append('<path d="%s" fill="#fbefcf" stroke="%s" stroke-width="0.035" stroke-linejoin="round"/>' % (p, INK))
    o.append('<circle cx="%.3f" cy="0" r="0.03" fill="%s"/>' % (x0 + 0.1, INK))
    st = 'font-family:K;font-size:%.3fpx;font-weight:900;text-anchor:middle;dominant-baseline:central' % fs
    o.append('<text x="%.3f" y="0.01" style="%s" fill="none" stroke="#fff8e6" stroke-width="%.3f" stroke-linejoin="round">%s</text>' % (0.05, st, fs * 0.12, text))
    o.append('<text x="%.3f" y="0.01" style="%s" fill="#c8202c">%s</text>' % (0.05, st, text))
    return "".join(o), (x0 - 0.04, y0 - 0.04, -x0 + 0.04, -y0 + 0.04)


def rasterise(items, out_dir):
    """items: [(fragment, box, ppd)] -> png paths (cached by content hash)."""
    os.makedirs(out_dir, exist_ok=True)
    paths, todo = [], []
    for frag, box, ppd in items:
        x0, y0, x1, y1 = box
        w, h = int(round((x1 - x0) * ppd)), int(round((y1 - y0) * ppd))
        doc = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="%.5f %.5f %.5f %.5f" style="display:block">%s</svg>'
               % (w, h, x0, y0, x1 - x0, y1 - y0, frag))
        png = os.path.join(out_dir, "sign_%s.png" % hashlib.sha1(doc.encode()).hexdigest()[:16])
        paths.append(png)
        if not os.path.exists(png):
            src = png[:-4] + ".svg"; open(src, "w").write(doc)
            todo.append(dict(src=src, out=png, w=w, h=h))
    if todo:
        jp = os.path.join(out_dir, "jobs_%d.json" % os.getpid()); json.dump(todo, open(jp, "w"))
        r = subprocess.run(["node", os.path.join(HERE, "raster_fonts.js"), jp], env=dict(os.environ, NODE_PATH=NODE_PATH),
                           capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(r.stderr[-2000:])
    return paths


if __name__ == "__main__":
    a = board_svg("ร้านลุงเฮนรี่", 2.2, 0.62, 0.40)
    b = tag_svg("500 ก.", 0.62, 0.28, 0.19)
    print(rasterise([(a[0], a[1], 300), (b[0], b[1], 600)], os.path.join(HERE, "work", "props")))
