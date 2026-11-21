#!/usr/bin/env python3
"""ghost_sheet.py : drafts, the contact sheet, the finals, the colour numbers and the ground check of the film-23 set.

    python3 ghost.py frames S01 [t,t,...] [outdir] [scale] [samples]   one build, several t of the move (0..1.25)
    python3 ghost.py sheet            every shot: first / middle / last frame at 360x640, 6 samples (one bpy process per shot) -> set_sheet.jpg
    python3 ghost.py finals           S01 S07 S09 S12 S14 S17 first frame, 720x1280 final quality -> set_work/final/ + numbers.json
    python3 ghost.py ground [LOC..]   ground_check (film/v3/tools) on every location over its shots' marks and moving states -> GROUND_SET.md
Every heavy step runs in its own `python3` process (one render at a time, 4 threads)."""
import os, sys, json, time, subprocess, re
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.join(HERE, 'set_work')
SHEET_T = (0.0, 0.625, 1.25)

def frames_main(a):
    """frames S01 [ts] [outdir] [scale] [samples]: build once, render each t."""
    import bpy, ghost as GH
    name = a[1]; ts = [float(x) for x in a[2].split(',')] if len(a) > 2 and a[2] else list(SHEET_T)
    out = a[3] if len(a) > 3 else os.path.join(WORK, 'drafts'); scale = float(a[4]) if len(a) > 4 else 0.5; spp = int(a[5]) if len(a) > 5 else 6
    os.makedirs(out, exist_ok=True); t0 = time.time(); A = GH.build(name); tb = time.time() - t0; sc = bpy.context.scene
    GH.quality(sc, 'final', scale=scale, samples=spp)
    from ghost_shots import frames as NF
    n = NF(name); rows = []
    for t in ts:
        f = 1 + int(round(t / 1.25 * n)); sc.frame_set(f)
        GH.shot_camera(name, t); _states_at(name, t)
        p = os.path.join(out, '%s_t%03d.png' % (name, int(round(t * 100)))); w, c = GH.T.render(p); rows.append(dict(t=t, frame=f, png=p, wall=round(w, 1), cpu=round(c, 1)))
        print('RENDER %s t=%.3f %.1f wall s' % (name, t, w), flush=True)
    rep = dict(shot=name, build_s=round(tb, 1), rows=rows, heads=head_rows(name, ts))
    json.dump(rep, open(os.path.join(out, '%s.json' % name), 'w'), indent=1); print('BUILD %.1f s' % tb)

def _states_at(name, t):
    """The per-shot setter keys a render worker would make (so the drafts show the action): ghost_shot_table.ACTION[name](GH, t)."""
    import ghost_shot_table as TB, ghost as GH
    fn = getattr(TB, 'ACTION', {}).get(name)
    if fn: fn(GH, t)

def head_rows(name, ts):
    """Screen rows (720x1280 px) of every placeholder card's head top / feet at each t: heads must stay out of the caption band 880-950."""
    import bpy, ghost as GH
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Vector
    sc = bpy.context.scene; out = []
    for t in ts:
        GH.shot_camera(name, t); _states_at(name, t); bpy.context.view_layer.update(); cam = sc.camera
        for ob in GH.STATE['cards']:
            mw = ob.matrix_world; h = ob.dimensions.z; top = mw @ Vector((0, 0, h * 0.92)); ft = mw @ Vector((0, 0, 0)); hd = mw @ Vector((0, 0, h * 0.62))
            a = world_to_camera_view(sc, cam, top); b = world_to_camera_view(sc, cam, ft); c = world_to_camera_view(sc, cam, hd)
            if a.z <= 0 or not (0 <= a.x <= 1): continue
            out.append(dict(t=t, card=ob.name, head_top=round((1 - a.y) * 1280), chin=round((1 - c.y) * 1280), feet=round((1 - b.y) * 1280)))
    return out

# ----------------------------------------------------------------------------- sheet
def _font(sz):
    from PIL import ImageFont
    try: return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', sz)
    except Exception: return ImageFont.load_default()

def run_frames(name, ts, out, scale=0.5, spp=6):
    t0 = time.time(); r = subprocess.run([sys.executable, os.path.join(HERE, 'ghost.py'), 'frames', name, ','.join('%g' % t for t in ts), out, str(scale), str(spp)], capture_output=True, text=True)
    if r.returncode: print(r.stdout[-1500:], r.stderr[-3000:]); raise SystemExit('frames failed ' + name)
    return time.time() - t0

def sheet_main(a):
    import ghost_shots as SH
    out = os.path.join(WORK, 'sheet'); os.makedirs(out, exist_ok=True); only = a[1:] or list(SH.SHOTS)
    for n in only:
        dt = run_frames(n, SHEET_T, out); print('%s %.0f s' % (n, dt), flush=True)
    make_sheet()

def make_sheet():
    from PIL import Image, ImageDraw
    import ghost_shots as SH
    out = os.path.join(WORK, 'sheet'); W, H = 360, 640; gap, lab = 10, 40; cols = 3; per_row = 3          # 3 shots per row, 3 frames each
    names = list(SH.SHOTS); rows = (len(names) + per_row - 1) // per_row; cw = cols * W + (cols - 1) * 4
    S = Image.new('RGB', (per_row * cw + (per_row + 1) * gap * 2, rows * (H + lab + gap) + gap), (16, 16, 24)); d = ImageDraw.Draw(S); f = _font(22); fs = _font(16)
    for i, n in enumerate(names):
        r, c = divmod(i, per_row); x0 = gap * 2 + c * (cw + gap * 2); y0 = gap + r * (H + lab + gap); sh = SH.SHOTS[n]
        for j, t in enumerate(SHEET_T):
            p = os.path.join(out, '%s_t%03d.png' % (n, int(round(t * 100))))
            if not os.path.exists(p): continue
            im = Image.open(p).convert('RGB').resize((W, H)); x = x0 + j * (W + 4); S.paste(im, (x, y0))
            d.line([(x, y0 + 440), (x + W - 1, y0 + 440)], fill=(0, 230, 255), width=1)                 # y 880 of 1280
            d.text((x + 6, y0 + 6), ('first', 'mid', 'last')[j], fill=(255, 255, 255), font=fs, stroke_width=2, stroke_fill=(0, 0, 0))
        d.text((x0, y0 + H + 8), '%s  %s  %s  %.2f s x1.25' % (n, sh['loc'], sh['light'], sh['dur']), fill=(235, 235, 245), font=f)
    p = os.path.join(HERE, 'set_sheet.jpg'); S.save(p, quality=88); print('sheet ->', p, S.size)

# ----------------------------------------------------------------------------- finals + numbers
FINALS = ('S01', 'S07', 'S09', 'S12', 'S14', 'S17')
def finals_main(a):
    out = os.path.join(WORK, 'final'); os.makedirs(out, exist_ok=True); only = a[1:] or list(FINALS); rows = []
    for n in only:
        dt = run_frames(n, (0.0,), out, 1.0, 12); rep = json.load(open(os.path.join(out, '%s.json' % n))); r = rep['rows'][0]
        rows.append(dict(shot=n, png=os.path.basename(r['png']), render_wall_s=r['wall'], render_cpu_s=r['cpu'], build_s=rep['build_s'], process_s=round(dt, 1)))
        print(rows[-1], flush=True)
    numbers(rows)

def numbers(rows=None):
    import ghost_hue
    out = os.path.join(WORK, 'final'); jp = os.path.join(WORK, 'numbers.json')
    if rows is None: rows = json.load(open(jp))
    rep = ghost_hue.report([os.path.join(out, r['png']) for r in rows])
    for r, h in zip(rows, rep): r.update({k: h[k] for k in ('sat_qa', 'luma_qa', 'luma_709', 'magenta_pct', 'shade_hue', 'vivid_pct', 'dark_v025')})
    json.dump(rows, open(jp, 'w'), indent=1)
    for r in rows: print(r)
    # the finals strip (6 x 720x1280 side by side, labels, cyan y 880)
    from PIL import Image, ImageDraw
    W, H, gap = 720, 1280, 16; S = Image.new('RGB', (len(rows) * (W + gap) + gap, H + 70 + 2 * gap), (16, 16, 24)); d = ImageDraw.Draw(S)
    for i, r in enumerate(rows):
        im = Image.open(os.path.join(out, r['png'])).convert('RGB'); x = gap + i * (W + gap); S.paste(im, (x, gap)); d.line([(x, gap + 880), (x + W - 1, gap + 880)], fill=(0, 230, 255), width=2)
        d.text((x + 10, gap + H + 14), '%s first frame  sat %.2f  luma %.0f  hue %.0f' % (r['shot'], r['sat_qa'], r['luma_qa'], r['shade_hue']), fill=(235, 235, 245), font=_font(30))
    S.save(os.path.join(HERE, 'set_finals.jpg'), quality=90)

def main(a):
    if a[0] == 'frames': frames_main(a)
    elif a[0] == 'sheet': sheet_main(a)
    elif a[0] == 'finals': finals_main(a)
    elif a[0] == 'ground':
        import ghost_ground; ghost_ground.main(a)
