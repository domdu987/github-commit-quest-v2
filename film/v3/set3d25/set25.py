#!/usr/bin/env python3
"""set25.py : entry point for every film-25 location.   python3 set25.py render <preset> out.png [--draft 0.4] [--samples 64] [--set k=v ...]   |   python3 set25.py list
    import set25 as W; A = W.build('fac_wide'); W.render_still(path)"""
import os, sys, json, importlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import front as F
MODS = ['front', 'factory', 'trial', 'street', 'dock', 'sky']
def registry():
    reg = {}
    for m in MODS:
        try: mod = importlib.import_module(m)
        except ImportError: continue
        for k in getattr(mod, 'PRESETS', {}): reg[k] = mod
    return reg
def build(preset, samples=None, quality=None):
    reg = registry(); return reg[preset].build(preset, samples, quality)
render_still = F.render_still
if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument('cmd'); ap.add_argument('preset', nargs='?'); ap.add_argument('out', nargs='?'); ap.add_argument('--draft', type=float, default=0.0); ap.add_argument('--samples', type=int, default=0)
    ap.add_argument('--set', nargs='*', default=[]); a = ap.parse_args()
    if a.cmd == 'list': print(' '.join(registry())); sys.exit()
    for kv in a.set: k, v = kv.split('='); F.OVR[k] = float(v) if v.replace('.', '', 1).replace('-', '', 1).isdigit() else v
    A = build(a.preset, a.samples or None); print('build %.1f s' % F.S['build_s'], flush=True)
    if a.draft: w, c = F.render_still(a.out, 'draft', a.samples or 16, a.draft)
    else: w, c = F.render_still(a.out, 'final', a.samples or None)
    print('render %.1f s wall, %.1f s cpu' % (w, c), flush=True)
    json.dump(dict(preset=a.preset, wall_s=round(w, 1), cpu_s=round(c, 1), build_s=round(F.S['build_s'], 1), settings=F.render_settings(), cards=F.card_report(), anchors=F.proj_report()), open(a.out[:-4] + '_log.json', 'w'), indent=1, default=str)
