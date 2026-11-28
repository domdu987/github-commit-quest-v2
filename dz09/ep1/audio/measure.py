"""measure.py -- trim every chosen EP.1 take, measure voiced length, internal pauses, level; no audio is written."""
import json, sys, os, wave, numpy as np
PROJ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(PROJ, "audio", "th")); import tts_fal
TAKES = os.path.join(PROJ, "audio", "narr_ep1"); SR = 48000
def load(p):
    w = wave.open(p); assert w.getframerate() == SR and w.getnchannels() == 1 and w.getsampwidth() == 2, p
    return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
def trim_idx(x, thr=0.01):          # the hook's trim (join_fit.py): 5 ms envelope, 20 ms lead, 40 ms tail
    env = np.convolve(np.abs(x), np.ones(240) / 240, 'same'); idx = np.where(env > thr)[0]
    return max(0, idx[0] - int(0.02 * SR)), min(len(x), idx[-1] + int(0.04 * SR))
def quiet_runs(x, thr=0.006, win=480):
    env = np.convolve(np.abs(x), np.ones(win) / win, 'same'); q = env < thr; runs = []; i = 0; n = len(x)
    while i < n:
        if q[i]:
            j = i
            while j < n and q[j]: j += 1
            runs.append((i, j)); i = j
        else: i += 1
    return runs
def measure():
    N = json.load(open(os.path.join(PROJ, "ep1", "plan", "narration_ep1.json"), encoding="utf8")); rows = []
    for s in N["sentences"]:
        rep = json.load(open(os.path.join(TAKES, "takes", s["id"] + ".report.json"), encoding="utf8"))
        base = os.path.join(TAKES, rep["take"]); x = load(base + ".wav"); a, b = trim_idx(x)
        al, ratio, c = tts_fal.align(base, [dict(text=q["text"]) for q in s["captions"]])
        y = x[a:b]; runs = [(i, j) for i, j in quiet_runs(y) if i > 0 and j < len(y)]
        act = np.ones(len(y), bool)
        for i, j in runs:
            if j - i > 0.05 * SR: act[i:j] = False
        rms = 20 * np.log10(np.sqrt((y[act] ** 2).mean()) + 1e-12)
        rows.append(dict(id=s["id"], scene=s["scene"], take=rep["take"], accuracy=rep.get("accuracy"), heard=rep.get("heard"), tts=s["tts"], file_s=round(len(x) / SR, 3),
                         lead_s=round(a / SR, 3), tail_s=round((len(x) - b) / SR, 3), voiced=round((b - a) / SR, 3), plan_voiced=s["voiced"],
                         start_peak=round(float(np.abs(x[:96]).max()), 4), end_peak=round(float(np.abs(x[-96:]).max()), 4), peak=round(float(np.abs(x).max()), 3),
                         rms_active_db=round(rms, 2), pauses=[(round(i / SR, 3), round((j - i) / SR, 3)) for i, j in runs if j - i > 0.14 * SR],
                         align_ratio=round(ratio, 3), chars_dur=c["duration"], chars_last=c["t1"][-1], caps_raw=[(q["text"], q["t0"]) for q in al]))
    return rows
if __name__ == "__main__":
    R = measure(); json.dump(R, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "measure.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
    for r in R:
        print("%-5s %s v=%.2f plan=%.2f (%+.0f%%) lead=%.2f tail=%.2f sp=%.3f pk=%.2f rms=%.1f ratio=%.2f acc=%s pauses=%s" % (r["id"], r["scene"], r["voiced"], r["plan_voiced"], 100 * (r["voiced"] / r["plan_voiced"] - 1),
              r["lead_s"], r["tail_s"], r["start_peak"], r["peak"], r["rms_active_db"], r["align_ratio"], r["accuracy"], r["pauses"]))
    print("sum voiced", sum(r["voiced"] for r in R), "plan", sum(r["plan_voiced"] for r in R))
