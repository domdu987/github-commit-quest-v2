#!/usr/bin/env python3
"""deliver.py <take dir> : in-shot frame-diff, take.mkv, contact.jpg, meta.json, cues.json, qa_auto, QA.md skeleton numbers.  Reads SHOT/G0/G1/H_IN/H_OUT from shot.py."""
import sys, os, re, json, subprocess, numpy as np, cv2
d = os.path.abspath(sys.argv[1]); sp = open(os.path.join(d, 'shot.py')).read()
def get(n): return int(re.search(r'%s\s*=\s*(\d+)' % n, sp.replace(';', '\n')).group(1))
shot = re.search(r"SHOT = '(s\d+)'", sp).group(1); G0, G1 = map(int, re.search(r'G0, G1 = (\d+), (\d+)', sp).groups()); HI, HO = map(int, re.search(r'H_IN, H_OUT = (\d+), (\d+)', sp).groups())
fr = os.path.join(d, 'frames'); first = G0 - HI; last = G1 + HO
miss = [g for g in range(first, last + 1) if not os.path.exists(os.path.join(fr, 'g_%04d.png' % g))]
assert not miss, 'missing frames %s' % miss[:10]
gr = {g: cv2.resize(cv2.cvtColor(cv2.imread(os.path.join(fr, 'g_%04d.png' % g)), cv2.COLOR_BGR2GRAY), (90, 160), interpolation=cv2.INTER_AREA).astype(np.float32) for g in range(G0, G1 + 1)}
df = np.array([np.abs(gr[g + 1] - gr[g]).mean() for g in range(G0, G1)])
st = dict(median=round(float(np.median(df)), 2), p90=round(float(np.percentile(df, 90)), 2), min=round(float(df.min()), 2), max=round(float(df.max()), 2), n=len(df))
print(shot, st)
mkv = os.path.join(d, 'take.mkv')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-framerate', '30', '-start_number', str(first), '-i', os.path.join(fr, 'g_%04d.png'), '-frames:v', str(last - first + 1), '-c:v', 'libx264rgb', '-crf', '20', '-preset', 'slow', mkv], check=True)
meta = dict(take=shot, film=18, shots=[int(shot[1:])], first_g=first, n_frames=last - first + 1, g0=G0, g1=G1, handle_in=HI, handle_out=HO,
            transition_in=json.loads(sys.argv[2]) if len(sys.argv) > 2 else dict(type='cut', frames=0), frame_diff=st)
json.dump(meta, open(os.path.join(d, 'meta.json'), 'w'), indent=1)
# contact sheet: 8 frames across the shot
ids = [int(round(G0 + (G1 - G0) * i / 7.0)) for i in range(8)]
tiles = [cv2.resize(cv2.imread(os.path.join(fr, 'g_%04d.png' % g)), (270, 480), interpolation=cv2.INTER_AREA) for g in ids]
for t, g in zip(tiles, ids): cv2.putText(t, 'g%d' % g, (6, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2); cv2.line(t, (0, int(880 / 1280 * 480)), (270, int(880 / 1280 * 480)), (255, 255, 0), 1)
cv2.imwrite(os.path.join(d, 'contact.jpg'), np.hstack(tiles[:4])); cv2.imwrite(os.path.join(d, 'contact2.jpg'), np.hstack(tiles[4:]))
r = subprocess.run(['python3', os.path.join(os.path.dirname(d), '..', '..', 'qa_auto.py'), mkv, '--first_g', str(first), '--out', d], capture_output=True, text=True)
print(r.stdout[-1500:], r.stderr[-500:], 'qa_auto exit', r.returncode)
