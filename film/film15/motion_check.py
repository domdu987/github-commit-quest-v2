"""In-shot camera-motion check (production-lessons §10). usage: python3 motion_check.py video.mp4 [--cuts g1,g2,...] [--first_g G]
Frame-diff = mean |grey(t)-grey(t-1)| on 90x160 frames (0-255). Diffs at a planned cut (+-1 frame) are excluded; without --cuts,
frames whose diff is > 4x the local median AND > 25 are treated as cuts. Reports median and p90 of the in-shot diffs.
Targets (client, film 15 on): median >= 4, p90 >= 12. Film 2 measured 5.3 / 19.1."""
import sys, subprocess, numpy as np, argparse
ap = argparse.ArgumentParser(); ap.add_argument('video'); ap.add_argument('--cuts', default=''); ap.add_argument('--first_g', type=int, default=0)
ap.add_argument('--per_shot', default='', help='comma list of shot start g (same clock as --first_g) to print per-shot medians')
a = ap.parse_args()
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', a.video, '-vf', 'scale=90:160,format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
f = np.frombuffer(raw, np.uint8).reshape(-1, 160, 90).astype(np.float32)
d = np.abs(np.diff(f, axis=0)).mean(axis=(1, 2))            # d[i] = diff between frame i and i+1
g = np.arange(1, len(f)) + a.first_g                        # g of the later frame
mask = np.ones(len(d), bool)
if a.cuts:
    for c in [int(x) for x in a.cuts.split(',') if x]:
        mask &= np.abs(g - c) > 1
else:
    loc = np.array([np.median(d[max(0, i - 15):i + 15]) for i in range(len(d))])
    mask &= ~((d > 4 * loc) & (d > 25))
x = d[mask]
print(f"frames {len(f)}  in-shot diffs {len(x)}  median {np.median(x):.1f}  p90 {np.percentile(x, 90):.1f}  (target median>=4, p90>=12; film 2: 5.3/19.1)")
if a.per_shot:
    s = [int(v) for v in a.per_shot.split(',')] + [g[-1] + 1]
    for k in range(len(s) - 1):
        m = mask & (g >= s[k]) & (g < s[k + 1])
        if m.any(): print(f"  shot from g{s[k]}: median {np.median(d[m]):.1f} p90 {np.percentile(d[m], 90):.1f}" + ("  LOW" if np.median(d[m]) < 3 else ""))
