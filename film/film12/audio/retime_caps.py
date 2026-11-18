# Re-time caption phrase starts from the ElevenLabs character timestamps (bk0/sNN.json),
# mapped through the same trim -> tighten -> atempo chain as build_bk0.py. Run from film/film12/.
import json, re, subprocess, sys, numpy as np
sys.path.insert(0, '../audio/fal'); import tl
SR = 48000
L = [l.rstrip('\n').split('|') for l in open('script/script_th.txt')]
tim = json.load(open('audio/timing.json')); start, tempo = tim['sent_start'], tim['tempo']
caps = json.load(open('script/captions.json'))
def load(f): return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar",str(SR),"-f","f64le","-"],capture_output=True).stdout,np.float64).copy()
key = lambda c: re.sub(r"[\s\.,!?\"“”ๆ]", "", c)
out = []
for k in range(len(L)):
    d = json.load(open(f'audio/bk0/s{k:02d}.json'))['timestamps']
    chars = [c for seg in d for c in seg['characters']]; t0 = [t for seg in d for t in seg['character_start_times_seconds']]
    # drop bracketed tags, keep spoken characters with their start times
    sp, inb = [], False
    for c, t in zip(chars, t0):
        if c == '[': inb = True; continue
        if c == ']': inb = False; continue
        if not inb and key(c): sp.append((c, t))
    text = ''.join(c for c, _ in sp)
    x = load(f'audio/bk0/s{k:02d}.wav')
    env = np.sqrt(np.convolve(x**2, np.ones(960)/960, 'same')); v = np.flatnonzero(env > 0.01); off = max(0, v[0]-480)/SR
    xs = x[int(off*SR): v[-1]+1441]
    ph = [c for c in caps if c['sent'] == k]
    pos = 0; times = []
    for c in ph:
        p = key(c['text']); i = text.find(p, pos)
        if i < 0: i = pos  # fallback: sequential
        times.append(max(0.0, sp[min(i, len(sp)-1)][1] - off)); pos = i + len(p)
    _, mapped, _, _ = tl.tighten(xs, SR, times, [], max_gap=0.10, keep=0.06)
    for c, m in zip(ph, mapped):
        new = round(start[k] + m/tempo - 0.03, 2)
        out.append((c['t'], new, c['text'])); c['t'] = max(0.0, new)
for i, c in enumerate(caps):
    if i+1 < len(caps): c['end'] = caps[i+1]['t']
    else: c['end'] = round(tim['sent_end'][-1], 2)
json.dump(caps, open('script/captions.json', 'w'), ensure_ascii=False, indent=0)
d = [abs(a-b) for a, b, _ in out]
print('phrases', len(out), 'mean|shift| %.3f max %.3f' % (np.mean(d), max(d)))
for a, b, t in sorted(out, key=lambda r: -abs(r[0]-r[1]))[:8]: print(f'{a:6.2f} -> {b:6.2f}  {t}')
