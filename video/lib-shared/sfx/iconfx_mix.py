"""Place IconFX "file:<name>" cues (sounds in this folder) into a mono buffer, frame-exact.
usage in mix.py:
    sys.path.insert(0, "<repo>/video/lib-shared/sfx"); import iconfx_mix
    synth_cues, samp = iconfx_mix.split(json.load(open("iconfx_cues.json")), N, SR)   # samp: np.float32 buffer, ~-24 dB RMS per hit × gain
    CUES += [(None, c["t"], c["type"], c["gain"]) for c in synth_cues];  …later:  sfx = sfx + samp
"""
import os, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))


def _load(path, sr):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(sr), "-"])
    return np.frombuffer(raw, dtype=np.float32).copy()


def split(cues, n, sr, level_db=-24.0):
    out, buf, cache = [], np.zeros(n, np.float32), {}
    for c in cues:
        if not str(c["type"]).startswith("file:"):
            out.append(c); continue
        name = c["type"][5:]
        if name not in cache:
            x = _load(os.path.join(HERE, f"{name}.mp3"), sr)
            nz = x[np.abs(x) > 1e-4]
            rms = 20 * np.log10(np.sqrt(np.mean(nz ** 2)) + 1e-9) if len(nz) else -60
            cache[name] = x * 10 ** ((level_db - rms) / 20)
        x = cache[name] * c["gain"] / 0.5
        i = int(c["t"] * sr); j = min(n, i + len(x))
        if 0 <= i < n: buf[i:j] += x[: j - i]
    return out, buf
