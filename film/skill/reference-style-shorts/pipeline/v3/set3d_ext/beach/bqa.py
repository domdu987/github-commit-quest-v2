#!/usr/bin/env python3
"""bqa.py : meta.json, cues.json, contact.jpg and work/qa.json (numbers for QA.md) of a beach take.  Called by `shot.py qa`
after `shot.py post` (and `shot.py probe` for the head numbers, read from work/probe.json when present)."""
import os, sys, json, subprocess
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
import bshot as BS

def main(T):
    d = T.DIR; gs = list(range(T.R0, T.R1))
    spd = [round(BS.camera_speed(T, g)[1], 2) for g in gs]
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
    fr = os.path.join(d, 'frames'); prev = None; diffs = []; dark_cards = []
    for g in gs:
        im = Image.open(os.path.join(fr, 'g_%04d.png' % g)).convert('RGB')
        assert im.size == (720, 1280), (g, im.size)
        a = np.asarray(im.resize((180, 320), Image.BILINEAR), np.float32)
        mag = ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean()
        if mag > 0.001: dark_cards.append((g, 'magenta', float(mag)))
        if prev is not None: diffs.append(float(np.abs(a - prev).mean()))
        prev = a
    pops = [gs[i + 1] for i in range(1, len(diffs) - 1) if diffs[i] > 1.8 * diffs[i - 1] and diffs[i] > 1.8 * diffs[i + 1] and diffs[i] > 2.0]
    hue = subprocess.run([sys.executable, os.path.join(PROJ, 'v3', 'tools', 'hue_report.py'), fr], capture_output=True, text=True).stdout
    metas = [json.load(open(os.path.join(d, 'raw', 'meta', 'g_%04d.json' % g))) for g in gs if os.path.exists(os.path.join(d, 'raw', 'meta', 'g_%04d.json' % g))]
    secs = [m['seconds'] for m in metas]; cpus = [m.get('cpu', 0) for m in metas]
    retried = [(m['g'], m.get('retried'), m.get('still_wrong')) for m in metas if m.get('retried') or m.get('still_wrong')]
    plog = json.load(open(os.path.join(d, 'work', 'post_log.json'))) if os.path.exists(os.path.join(d, 'work', 'post_log.json')) else []
    probe = json.load(open(os.path.join(d, 'work', 'probe.json'))) if os.path.exists(os.path.join(d, 'work', 'probe.json')) else []
    out = dict(take=T.TAKE, frames=[gs[0], gs[-1]], cam_speed_px=dict(zip(gs, spd)), moves=moves, static_runs_over_6=static, linear_runs_over_8=lin,
               frame_diff=dict(zip(gs[1:], [round(x, 2) for x in diffs])), pops=pops, magenta=dark_cards, hue_report=hue,
               seconds_per_frame=dict(n=len(secs), median=float(np.median(secs)) if secs else None, max=max(secs) if secs else None,
                                      cpu_median=float(np.median(cpus)) if cpus else None),
               card_retries=retried, streaked=[(r['g'], r['streaked']) for r in plog if r['streaked']], probe=probe)
    json.dump(out, open(os.path.join(d, 'work', 'qa.json'), 'w'), indent=1, ensure_ascii=False)
    meta = dict(take=T.TAKE, shots=T.SHOTS, g0=T.G0, g1=T.G1, handle_in=T.H_IN, handle_out=T.H_OUT, transition_in=T.TRANSITION_IN, set='beach', light=T.LIGHT,
                samples=BS.SAMPLES, frames_dir='frames', first_rendered=T.R0, last_rendered=T.R1 - 1, resolution=[720, 1280], fps=30)
    json.dump(meta, open(os.path.join(d, 'meta.json'), 'w'), indent=1, ensure_ascii=False)
    ev = []
    for (x, dur, kind, label) in T.CUES:
        t = round(x + 0.1, 3); ev.append(dict(time=t, duration=dur, frame=int(round(t * 30)), end_frame=int(round((t + dur) * 30)), kind=kind, label=label, clock=x))
    json.dump(dict(fps=30, time_base='film seconds (narration clock + 0.100); frame g starts at g / 30', take=T.TAKE, events=ev), open(os.path.join(d, 'cues.json'), 'w'), indent=1, ensure_ascii=False)
    BS.contact(T, 'frames', 'contact.jpg', n=16)
    print(json.dumps(dict(moves=moves, static=static, linear=lin, pops=pops, magenta=dark_cards, secs=out['seconds_per_frame'], streaked=out['streaked'], retries=retried), indent=0)); print(hue)
    return out
