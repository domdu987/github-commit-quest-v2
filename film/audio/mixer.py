"""Film sound mixer: narration + music bed + sound effects -> stereo WAV, then mux into an MP4.
usage: python3 mixer.py <spec.json>
spec: {"duration": s, "out_wav": path, "video_in": mp4 (optional), "video_out": mp4 (optional),
       "voice": {"file": wav, "at": s, "gain": linear},
       "music": {"file": wav, "at": s, "start": s into the file, "rms_db": target RMS of the bed, "fade_in": s, "fade_out": s},
       "sfx": [{"file": wav, "at": s, "peak_db": target peak | "rms_db": target RMS, "start": s into file, "len": s, "fade_in": s, "fade_out": s, "pan": -1..1, "align": "start"|"onset"}]}
Levels follow the reference clips: voice about -17.4 dBFS RMS, bed about -38 dBFS RMS, effects peaking -20 to -9 dBFS.
"""
import sys, json, wave, subprocess, os
import numpy as np
SR = 48000
db2 = lambda d: 10 ** (d / 20)
def load(path):
    tmp = None
    if not path.endswith(".wav"):
        tmp = path + ".tmp.wav"; subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", path, "-ar", str(SR), "-ac", "2", tmp], check=True); path = tmp
    w = wave.open(path); ch = w.getnchannels(); sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
    x = x.reshape(-1, ch) if ch > 1 else np.repeat(x[:, None], 2, axis=1)
    if tmp: os.remove(tmp)
    if sr != SR:
        n = int(len(x) * SR / sr); idx = np.linspace(0, len(x) - 1, n); x = np.stack([np.interp(idx, np.arange(len(x)), x[:, c]) for c in range(2)], axis=1)
    return x
def fades(x, fi, fo):
    n = len(x)
    if fi and fi > 0: k = min(n, int(fi * SR)); x[:k] *= np.linspace(0, 1, k)[:, None]
    if fo and fo > 0: k = min(n, int(fo * SR)); x[-k:] *= np.linspace(1, 0, k)[:, None]
    return x
def place(mix, x, at):
    i = int(round(at * SR))
    if i < 0: x = x[-i:]; i = 0
    j = min(len(mix), i + len(x))
    if j > i: mix[i:j] += x[: j - i]
def main(spec):
    n = int(spec["duration"] * SR); mix = np.zeros((n, 2)); log = []
    v = spec.get("voice")
    if v:
        x = load(v["file"]) * v.get("gain", 1.0); place(mix, x, v.get("at", 0.0)); log.append(("voice", 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-12)))
    m = spec.get("music")
    if m:
        x = load(m["file"]); x = x[int(m.get("start", 0) * SR):][: n - int(m.get("at", 0) * SR)].copy()
        full = load(m["file"]); rms = np.sqrt((full.mean(1) ** 2).mean()); x *= db2(m.get("rms_db", -38)) / rms
        x = fades(x, m.get("fade_in", 0), m.get("fade_out", 0)); place(mix, x, m.get("at", 0.0)); log.append(("music", m.get("rms_db", -38)))
    for e in spec.get("sfx", []):
        x = load(e["file"]); mono = x.mean(1)
        if e.get("align") == "onset":
            pk = np.abs(mono).max(); on = int(np.argmax(np.abs(mono) > 0.25 * pk)); x = x[max(0, on - int(0.005 * SR)):]
        x = x[int(e.get("start", 0) * SR):]
        if e.get("len"): x = x[: int(e["len"] * SR)]
        x = x.copy(); mono = x.mean(1)
        if "peak_db" in e: x *= db2(e["peak_db"]) / max(np.abs(mono).max(), 1e-9)
        else: x *= db2(e.get("rms_db", -26)) / max(np.sqrt((mono ** 2).mean()), 1e-9)
        x = fades(x, e.get("fade_in", 0.005), e.get("fade_out", 0.03))
        p = e.get("pan", 0.0); x[:, 0] *= min(1.0, 1 - p); x[:, 1] *= min(1.0, 1 + p)
        place(mix, x, e["at"])
    pk = np.abs(mix).max(); scale = min(1.0, 0.5 / pk) if pk > 0.5 else 1.0
    pre = spec["out_wav"].replace(".wav", "_pre.wav")
    w = wave.open(pre, "w"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * scale * 32767).astype(np.int16).tobytes()); w.close()
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", pre, "-af", f"volume={1/scale:.5f},alimiter=limit=0.89:attack=2:release=40:level=disabled", "-ar", str(SR), spec["out_wav"]], check=True)
    os.remove(pre)
    y = load(spec["out_wav"]); print(f'mix: peak before limiter {pk:.2f}, final RMS {20*np.log10(np.sqrt((y.mean(1)**2).mean())+1e-12):.1f} dBFS, final peak {np.abs(y).max():.2f}, sfx {len(spec.get("sfx", []))}')
    if spec.get("video_in") and spec.get("video_out"):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", spec["video_in"], "-i", spec["out_wav"], "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", spec["video_out"]], check=True)
        print("wrote", spec["video_out"])
if __name__ == "__main__":
    main(json.load(open(sys.argv[1], encoding="utf8")))
