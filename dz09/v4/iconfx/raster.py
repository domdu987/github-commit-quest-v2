"""raster.py -- SVG text -> RGBA PNG through one persistent headless Chromium page (Playwright, raster_page.js).

    from raster import render, close
    render([{"svg": svg_text, "w": 256, "h": 256, "out": "/abs/a.png"}, ...])    # -> list of ms per job
    close()                                                                        # optional; atexit does it

Text in an SVG may use font-family "WS" (Work Sans Black) or "Kanit" (Kanit Black, Thai): page.html loads both
from PROJ/fonts.  A job with "bg": "#rrggbb" is rendered opaque on that colour.
"""
import atexit, json, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))


class _Page(object):
    def __init__(self):
        self.proc = None
        self.n = 0

    def start(self):
        if self.proc is None or self.proc.poll() is not None:
            env = dict(os.environ)
            env.setdefault("NODE_PATH", "/usr/local/lib/node_modules_global")
            self.proc = subprocess.Popen(["node", os.path.join(HERE, "raster_page.js")], stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE, cwd=HERE, text=True, bufsize=1, env=env)

    def request(self, job):
        self.start()
        self.n += 1
        job = dict(job, id=self.n)
        self.proc.stdin.write(json.dumps(job) + "\n")
        self.proc.stdin.flush()
        line = self.proc.stdout.readline()
        if not line:
            raise RuntimeError("raster_page.js exited")
        rep = json.loads(line)
        if not rep.get("ok"):
            raise RuntimeError("raster failed: %s" % rep.get("error"))
        return rep["ms"]

    def stop(self):
        if self.proc is not None and self.proc.poll() is None:
            try:
                self.proc.stdin.write(json.dumps({"cmd": "quit"}) + "\n")
                self.proc.stdin.flush()
                self.proc.wait(timeout=10)
            except Exception:
                self.proc.kill()
        self.proc = None


_PAGE = _Page()
atexit.register(_PAGE.stop)


def render(jobs):
    out = []
    for j in jobs:
        d = os.path.dirname(os.path.abspath(j["out"]))
        os.makedirs(d, exist_ok=True)
        out.append(_PAGE.request({"svg": j["svg"], "w": int(j["w"]), "h": int(j["h"]),
                                  "out": os.path.abspath(j["out"]), "bg": j.get("bg")}))
    return out


def close():
    _PAGE.stop()
