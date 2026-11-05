"""Find lines where the TTS read its style prompt aloud before the line (the recording runs far longer than the text) and keep only the final phrase.
usage: python3 autotrim.py <ep dir>   — prints what it trimmed; originals kept as vo/<id>.full.wav; vo/durations.json updated."""
import json, os, re, subprocess, sys
import numpy as np
ep = sys.argv[1]
L = json.load(open(os.path.join(ep, "lines.json"))); D = json.load(open(os.path.join(ep, "vo", "durations.json")))
def gaps(path):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"])
    x = np.frombuffer(raw, np.float32); n = len(x) // 160
    db = 20 * np.log10(np.sqrt((x[:n * 160].reshape(n, 160) ** 2).mean(1) + 1e-12) + 1e-9); quiet = db < db.max() - 34
    out, i = [], 0
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]: j += 1
            if j - i >= 20 and i > 5 and j < n - 20: out.append((i / 100, (j - i) / 100))
            i = j
        else: i += 1
    return out, len(x) / 16000
for ln in L:
    vid = ln["id"]; chars = len(re.sub(r"[\s…!?.,\"“”]", "", ln["text"])); expect = chars * 0.085 + 0.6
    if D.get(vid, 0) < max(3.0, expect * 1.7): continue
    g, dur = gaps(os.path.join(ep, "vo", f"{vid}.wav"))
    cut = None
    for s, l in reversed(g):
        rest = dur - (s + l)
        if expect * 0.6 <= rest <= expect * 1.35: cut = s + l - 0.12; break
    if cut is None: print(vid, "LONG but no clean cut", round(dur, 2), "expected", round(expect, 2), g[-4:]); continue
    subprocess.check_call(["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "trimvo.py"), ep, vid, f"{cut:.2f}"])
