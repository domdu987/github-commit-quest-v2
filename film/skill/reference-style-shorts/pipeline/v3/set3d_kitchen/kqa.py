#!/usr/bin/env python3
"""kqa.py <take dir> : meta.json, cues.json, contact.jpg and the numbers of QA.md (work/qa.json) for a kitchen take.
Run after `shot.py post`. Camera numbers come from the take's own cam(g) (the true 3D camera), text positions are the
projected page points of the weather box (kitchen3d.wb_point), frame numbers from the final frames."""
import os, sys, json, math, subprocess, importlib.util
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(PROJ, 'v3', 'shots'))
import kshot as KS, kitchen_geom as KG, post

def load(d):
    sys.path.insert(0, d); spec = importlib.util.spec_from_file_location('take_' + os.path.basename(d), os.path.join(d, 'shot.py'))
    m = importlib.util.module_from_spec(spec); sys.argv = ['x']; spec.loader.exec_module(m); return m

def proj(cam, p):
    xy, z = post.project(cam[0], cam[1], np.array([p], float)); return float(xy[0, 0]), float(xy[0, 1]), float(z[0])

def main(d):
    T = load(d); import kitchen3d as K
    gs = list(range(T.R0, T.R1))
    # ---- text on the weather box (page y: header 1.051-1.135, ฝนตก 1.288-1.47, ลมกระโชก 1.536-1.65; x 0.62-1.38)
    P = dict(hdr_top=K.wb_point(1.0, 1.051), w1_top=K.wb_point(1.0, 1.288), w1_bot=K.wb_point(1.0, 1.47), w2_bot=K.wb_point(1.0, 1.65),
             wb_l=K.wb_point(0.56, 1.42), wb_r=K.wb_point(1.44, 1.42), w2_l=K.wb_point(0.62, 1.6), w2_r=K.wb_point(1.38, 1.6))
    text = {}
    for g in gs:
        c = T.cam(g); q = {k: proj(c, v) for k, v in P.items()}
        text[g] = dict(header_top_y=round(q['hdr_top'][1]), word1_cap_px=round(q['w1_bot'][1] - q['w1_top'][1], 1), thai_bottom_y=round(q['w2_bot'][1]),
                       wb_centre_x=round(0.5 * (q['wb_l'][0] + q['wb_r'][0])), word2_x=(round(q['w2_l'][0]), round(q['w2_r'][0])))
    # ---- camera motion from the true camera
    spd = []
    for g in gs:
        M1, s = KS.camera_speed(T, KG, g); spd.append(round(s, 2))
    moves, cur = [], None
    for g, s in zip(gs, spd):
        if s > 8 and cur is None: cur = [g, g, s]
        elif s > 8: cur[1] = g; cur[2] = max(cur[2], s)
        elif cur is not None: moves.append(dict(start=cur[0], end=cur[1], peak_px_per_frame=round(cur[2], 1))); cur = None
    if cur: moves.append(dict(start=cur[0], end=cur[1], peak_px_per_frame=round(cur[2], 1)))
    static, run = [], 0
    for g, s in zip(gs, spd):
        run = run + 1 if s < 0.3 else 0
        if run == 7: static.append(g - 6)
    lin, run = [], 0
    for i in range(1, len(spd)):
        run = run + 1 if spd[i] > 0.5 and abs(spd[i] - spd[i - 1]) < 0.01 * spd[i] else 0
        if run == 8: lin.append(gs[i] - 8)
    # ---- frames: popcheck, darks, hue report
    fr = os.path.join(d, 'frames'); prev = None; diffs = []
    for g in gs:
        a = np.asarray(Image.open(os.path.join(fr, 'g_%04d.png' % g)).convert('RGB').resize((180, 320), Image.BILINEAR), np.float32)
        if prev is not None: diffs.append(float(np.abs(a - prev).mean()))
        prev = a
    pops = [gs[i + 1] for i in range(1, len(diffs) - 1) if diffs[i] > 1.8 * diffs[i - 1] and diffs[i] > 1.8 * diffs[i + 1] and diffs[i] > 2.0]
    hue = subprocess.run([sys.executable, os.path.join(PROJ, 'v3', 'tools', 'hue_report.py'), fr], capture_output=True, text=True).stdout
    secs = [json.load(open(os.path.join(d, 'raw', 'meta', 'g_%04d.json' % g)))['seconds'] for g in gs if os.path.exists(os.path.join(d, 'raw', 'meta', 'g_%04d.json' % g))]
    plog = json.load(open(os.path.join(d, 'work', 'post_log.json'))) if os.path.exists(os.path.join(d, 'work', 'post_log.json')) else []
    out = dict(take=T.TAKE, frames=[gs[0], gs[-1]], text=text, cam_speed_px=dict(zip(gs, spd)), moves=moves, static_runs_over_6=static, linear_runs_over_8=lin,
               frame_diff=dict(zip(gs[1:], [round(x, 2) for x in diffs])), pops=pops, hue_report=hue,
               seconds_per_frame=dict(n=len(secs), median=float(np.median(secs)) if secs else None, max=max(secs) if secs else None),
               streaked=[(r['g'], r['streaked']) for r in plog if r['streaked']])
    if hasattr(T, 'arm'):
        reg = []
        for g in gs:
            a = T.arm(g)
            if a:
                c = T.cam(g); f = np.array(c[1]) - np.array(c[0]); f /= np.linalg.norm(f)
                h = proj(c, a['hand']); h2 = proj(c, tuple(np.array(a['hand']) - f * 0.06)); reg.append((g, round(math.hypot(h[0] - h2[0], h[1] - h2[1]), 2), round(h[0]), round(h[1])))
        out['hand_registration'] = reg
    json.dump(out, open(os.path.join(d, 'work', 'qa.json'), 'w'), indent=1, ensure_ascii=False)
    # ---- meta.json, cues.json, contact.jpg
    meta = dict(take=T.TAKE, shots=T.SHOTS, g0=T.G0, g1=T.G1, handle_in=T.H_IN, handle_out=T.H_OUT, transition_in=T.TRANSITION_IN, set='kitchen', light=T.LIGHT,
                samples=KS.SAMPLES, frames_dir='frames', first_rendered=T.R0, last_rendered=T.R1 - 1, resolution=[720, 1280], fps=30,
                note='samples 8 instead of 12: measured identical (mean difference 0.25 of 255) at 5.8 s instead of 8.5 s per frame; see QA.md')
    json.dump(meta, open(os.path.join(d, 'meta.json'), 'w'), indent=1, ensure_ascii=False)
    ev = []
    for (x, dur, kind, label) in T.CUES:
        t = round(x + 0.1, 3); ev.append(dict(time=t, duration=dur, frame=int(round(t * 30)), end_frame=int(round((t + dur) * 30)), kind=kind, label=label, clock=x))
    json.dump(dict(fps=30, time_base='film seconds (narration clock + 0.100); frame g starts at g / 30', take=T.TAKE, events=ev), open(os.path.join(d, 'cues.json'), 'w'), indent=1, ensure_ascii=False)
    KS.contact(T, 16)
    print(json.dumps(dict(moves=moves, static=static, linear=lin, pops=pops, secs=out['seconds_per_frame'], streaked=out['streaked']), indent=0)); print(hue)
    return out

if __name__ == '__main__':
    main(os.path.abspath(sys.argv[1]))
