"""Build the landscape (1920×1080) twin of an episode folder: jk/<ep>L → hf/<proj>L.
usage: python3 mkland.py <ep folder> <hf project name>   e.g.  python3 mkland.py ep1 jk1
The parts are the portrait ones; only head.part is rewritten: stage size, camera conversion (fr), overlay mapping, caption placement."""
import os, re, shutil, sys
src, proj = sys.argv[1], sys.argv[2]
dst = src + "L"; os.makedirs(dst, exist_ok=True)
for f in os.listdir(src):
    if f.endswith(".part") and f != "head.part" or f in ("schedule.json", "lines.json", "timing.py", "mix.wav"):
        shutil.copy(os.path.join(src, f), os.path.join(dst, f))
h = open(os.path.join(src, "head.part")).read()
def rep(old, new, cnt=1):
    global h; assert h.count(old) == cnt, (old[:60], h.count(old)); h = h.replace(old, new)
rep('data-resolution="portrait"', 'data-resolution="landscape"')
rep('<meta name="viewport" content="width=1080, height=1920" />', '''<meta name="viewport" content="width=1920, height=1080" />
    <script>
      window.STAGE_W = 1920; window.STAGE_H = 1080; window.LAND = 1; window.LAND_K = 0.75;          // landscape twin of the portrait episode
      window.LIGHT_MAP = "scale(1.7777778,0.5625)";                                                  // overlay layer: 1080×1920 design space stretched over the frame
      window.OVFIX = "scale(0.421875,1.3333333)";                                                     // per-overlay counter-stretch → uniform 0.75
      window.PX_MAP = (x, y) => [x * 1.7777778, y * 0.5625, 0.75];                                    // HTML words and bubbles
      window.LAND_ADJ = window.LAND_ADJ || {};
    </script>''')
rep('html, body { width: 1080px; height: 1920px;', 'html, body { width: 1920px; height: 1080px;')
rep('#root { position: relative; width: 1080px; height: 1920px;', '#root { position: relative; width: 1920px; height: 1080px;')
rep('data-width="1080" data-height="1920"', 'data-width="1920" data-height="1080"')
rep('<svg id="grain" width="1200" height="2040">', '<svg id="grain" width="2040" height="1200">')
rep('<rect width="1200" height="2040" filter="url(#nz)" />', '<rect width="2040" height="1200" filter="url(#nz)" />')
rep('const fr = (wx, wy, s, sx = 540, sy = 760, extra = {}) => ({ x: wx - 540 - (sx - 540) / s, y: wy - 960 - (sy - 960) / s, s, ...extra });',
    '''// landscape: the portrait framing (world point at a portrait screen point, scale s) becomes the same relative placement in the wide frame, a little wider (×LAND_K)
      const fr = (wx, wy, s, sx = 540, sy = 760, extra = {}) => { const S = s * window.LAND_K, SX = sx * (1920 / 1080), SY = sy * (1080 / 1920);
        return { x: wx - 960 - (SX - 960) / S, y: wy - 540 - (SY - 540) / S, s: S, ...extra }; };''')
rep('const add = (k, spec) => { if (SH[k]) shots.push({ start: SH[k].start, dur: SH[k].dur, key: k, ...spec }); };',
    '''const add = (k, spec) => { if (!SH[k]) return; const sh = { start: SH[k].start, dur: SH[k].dur, key: k, ...spec }, adj = window.LAND_ADJ[k];
        if (adj && sh.cam) { const fix = (c) => { if (!c) return; if (adj.k) c.s *= adj.k; c.x += adj.dx || 0; c.y += adj.dy || 0; }; (sh.cam.keys || []).forEach(fix); fix(sh.cam.from); fix(sh.cam.to); }
        shots.push(sh); };''')
# captions low in the wide frame, a touch smaller; HUD a little higher
rep('.capwrap { top: 1185px !important; }', '.capwrap { top: 880px !important; } .capbox { font-size: 46px !important; } .sghud { top: 44px !important; }')
open(os.path.join(dst, "head.part"), "w").write(h)
mk = open(os.path.join(src, "make.py")).read().replace('"hf", "%s")' % proj, '"hf", "%sL")' % proj)
assert '"%sL")' % proj in mk
open(os.path.join(dst, "make.py"), "w").write(mk)
print("landscape parts →", dst)
