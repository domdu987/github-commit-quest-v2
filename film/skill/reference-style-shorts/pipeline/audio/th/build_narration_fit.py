"""Re-voice the narration and FIT it to the existing film clock, so the picture does not change.
Each sentence of the new voice is time-stretched into the slot the same sentence has in the reference narration
(start of its first caption phrase to the start of the next sentence), so every sentence starts where it did.
Caption phrase times are recomputed from the new voice (they move only inside their sentence).

usage: python3 build_narration_fit.py <voice_id> <voice_name> <out_dir> [speed=1.2]
Film 1's sentence groups (GROUPS) and number readings (NUM) are written into this file: edit both for a new script
before running it, or it records film 1's text.
The fal key is injected by the session proxy for host fal.run; no key is read here.
"""
import sys, json, os, wave, subprocess, re, difflib, shutil
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tts_fal
P = os.path.dirname(os.path.dirname(HERE))
REF = P + "/audio/th/full_v2_oldvoice" if os.path.isdir(P + "/audio/th/full_v2_oldvoice") else P + "/audio/th/full_v2"
VOICE, VNAME, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
SPEED = float(sys.argv[4]) if len(sys.argv) > 4 else 1.2
SR = 48000; os.makedirs(OUT, exist_ok=True)
sc = json.load(open(P + "/script_th_v2/script_th.json", encoding="utf8")); sents = sc["sentences"]
GROUPS = [[0], [1, 2, 3], [4, 5], [6, 7], [8, 9, 10], [11, 12, 13], [14, 15, 16], [17, 18], [19, 20]]
GAP = 0.16                                    # silence between chunks before stretching (as in the reference build)
NUM = {"1938": "หนึ่งเก้าสามแปด", "120": "ร้อยยี่สิบ", "100": "ร้อย"}
norm = lambda s: re.sub(r"[\s\.,!?\"“”ๆ]", "", s)

def read_wav(path):
    w = wave.open(path); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768; return x, w.getframerate()
def write_wav(path, x):
    w = wave.open(path, "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()

def tighten(x, sr, t0, t1, max_gap=0.14, keep=0.10, thr=0.012):
    win = int(0.02 * sr); env = np.sqrt(np.convolve(x ** 2, np.ones(win) / win, "same")); sil = env < thr
    cuts, i, n = [], 0, len(x)
    while i < n:
        if sil[i]:
            j = i
            while j < n and sil[j]: j += 1
            if i == 0: cuts.append((0, max(0, j - int(0.03 * sr))))
            elif j == n: cuts.append((min(n, i + int(0.08 * sr)), n))
            elif (j - i) / sr > max_gap: cuts.append((i + int(keep * sr / 2), j - int(keep * sr / 2)))
            i = j
        else: i += 1
    km = np.ones(n, bool)
    for a, b in cuts: km[a:b] = False
    rb = np.cumsum(~km)
    rm = lambda t: (min(n - 1, max(0, int(t * sr))) - rb[min(n - 1, max(0, int(t * sr)))]) / sr
    return x[km], [rm(t) for t in t0], [rm(t) for t in t1]

def asr_ratio(base, text):
    url = json.load(open(base + ".json", encoding="utf8"))["audio"]["url"]
    r = subprocess.run(["curl", "-sS", "-m", "180", "-X", "POST", "https://fal.run/fal-ai/elevenlabs/speech-to-text", "-H", "Content-Type: application/json",
                        "-d", json.dumps({"audio_url": url, "language_code": "tha", "tag_audio_events": False, "diarize": False}), "-w", "\n%{http_code}"], capture_output=True, text=True)
    txt, code = r.stdout.rsplit("\n", 1)
    if code != "200": return None, "ASR HTTP " + code
    t = json.loads(txt)["text"]; open(base + ".asr.txt", "w", encoding="utf8").write(t)
    t2 = t
    for k, v in NUM.items(): t2 = t2.replace(k, v)
    return difflib.SequenceMatcher(None, norm(text), norm(t2), autojunk=False).ratio(), t

def atempo(x, tempo, tag):
    a, b = f"{OUT}/_seg_{tag}_in.wav", f"{OUT}/_seg_{tag}_out.wav"; write_wav(a, x)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", a, "-af", f"atempo={tempo:.6f}", "-ar", str(SR), b], check=True)
    y, _ = read_wav(b); os.remove(a); os.remove(b); return y

# ---------------------------------------------------------------- the reference clock
ref = json.load(open(REF + "/narration_timing.json", encoding="utf8")); rph = ref["phrases"]
xref, _ = read_wav(REF + "/narration.wav"); NTOT = len(xref); DUR = NTOT / SR
S_old = [next(q["t0"] for q in rph if q["sentence"] == i) for i in range(len(sents))]; S_old[0] = 0.0
E_old = S_old[1:] + [DUR]
act = xref[np.abs(xref) > 0.02]; REF_RMS = float(np.sqrt((act ** 2).mean()))

# ---------------------------------------------------------------- synth per chunk (best of up to 3 takes by ASR match)
out = np.zeros(NTOT); phrases = []; fit = []; chars_all, T0_all, T1_all = [], [], []
for gi, g in enumerate(GROUPS):
    base = f"{OUT}/chunk{gi:02d}"
    text = "\n".join(sents[i]["tts"] for i in g)
    if not os.path.exists(base + ".chars.json") or json.load(open(base + ".chars.json", encoding="utf8")).get("src_text") != text:
        best = None
        for take in range(1, 4):
            tb = f"{base}_take{take}"
            tts_fal.synth(text, tb, VOICE, SPEED)
            ratio, heard = asr_ratio(tb, text)
            print(f"  chunk {gi} take {take}: ASR match {ratio}", flush=True)
            if best is None or (ratio or 0) > best[0]: best = (ratio or 0, tb)
            if ratio is not None and ratio >= 0.985: break
        for ext in (".json", ".mp3", ".wav", ".chars.json"): shutil.copy(best[1] + ext, base + ext)
        c = json.load(open(base + ".chars.json", encoding="utf8")); c["src_text"] = text; c["asr_match"] = best[0]
        json.dump(c, open(base + ".chars.json", "w", encoding="utf8"), ensure_ascii=False)
    c = json.load(open(base + ".chars.json", encoding="utf8"))
    x, sr = read_wav(base + ".wav"); assert sr == SR
    y, t0, t1 = tighten(x, sr, c["t0"], c["t1"])
    y = np.concatenate([y, np.zeros(int(GAP * SR))])                      # the pause after the chunk, stretched with it
    tb = base + "_t"; json.dump({"text": c["text"], "chars": c["chars"], "t0": t0, "t1": t1, "duration": len(y) / SR}, open(tb + ".chars.json", "w", encoding="utf8"), ensure_ascii=False)
    caps = [{"text": t, "sentence": si, "beat": sents[si]["beat"], "k": k} for si in g for k, t in enumerate(sents[si]["captions"])]
    timed, ratio, _ = tts_fal.align(tb, caps)
    # cut points between sentences: the quietest 20 ms in the 150 ms before the first phrase of the sentence
    win = int(0.02 * SR); env = np.sqrt(np.convolve(y ** 2, np.ones(win) / win, "same"))
    cuts = [0]
    for si in g[1:]:
        tp = next(q["t0"] for q in timed if q["sentence"] == si); a, b = max(0, int((tp - 0.15) * SR)), max(1, int((tp + 0.01) * SR))
        cuts.append(a + int(np.argmin(env[a:b])))
    cuts.append(len(y))
    for k, si in enumerate(g):
        seg = y[cuts[k]:cuts[k + 1]].copy(); n_old = int(round(E_old[si] * SR)) - int(round(S_old[si] * SR))
        tempo = len(seg) / n_old
        z = atempo(seg, tempo, f"{si:02d}")
        z = z[:n_old] if len(z) >= n_old else np.concatenate([z, np.zeros(n_old - len(z))])
        f = int(0.004 * SR); z[:f] *= np.linspace(0, 1, f); z[-f:] *= np.linspace(1, 0, f)
        a = int(round(S_old[si] * SR)); out[a:a + n_old] = z
        fit.append({"sentence": si, "tempo": round(tempo, 4), "new_len": round(len(seg) / SR, 3), "slot": round(n_old / SR, 3)})
        mp = lambda t, k=k, si=si, tempo=tempo: S_old[si] + (t - cuts[k] / SR) / tempo
        for q in timed:
            if q["sentence"] == si:
                r = dict(q); r["t0"] = round(max(S_old[si], mp(q["t0"])), 3); phrases.append(r)
        for ch, a0, a1 in zip(c["chars"], t0, t1):
            if cuts[k] / SR <= a0 < cuts[k + 1] / SR or (k == len(g) - 1 and a0 >= cuts[k] / SR):
                chars_all.append(ch); T0_all.append(mp(a0)); T1_all.append(mp(a1))
    print(f"chunk {gi} sentences {g}: asr {c.get('asr_match')}, caption match {ratio:.3f}", flush=True)

phrases.sort(key=lambda q: (q["sentence"], q["k"]))
phrases[0]["t0"] = 0.0
for i, q in enumerate(phrases): q["t1"] = phrases[i + 1]["t0"] if i + 1 < len(phrases) else round(DUR, 3)
a2 = out[np.abs(out) > 0.02]; rms = float(np.sqrt((a2 ** 2).mean())); out *= REF_RMS / rms
write_wav(OUT + "/narration_pre.wav", out * min(1.0, 0.98 / np.abs(out).max()) if np.abs(out).max() > 0.98 else out)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", OUT + "/narration_pre.wav", "-af", "alimiter=limit=0.9", "-ar", str(SR), OUT + "/narration_lim.wav"], check=True)
y, _ = read_wav(OUT + "/narration_lim.wav"); y = y[:NTOT] if len(y) >= NTOT else np.concatenate([y, np.zeros(NTOT - len(y))]); write_wav(OUT + "/narration.wav", y)
json.dump({"duration": DUR, "audio": P + "/audio/th/full_v2/narration.wav", "match_ratio": ref.get("match_ratio"), "voice": VNAME, "voice_id": VOICE, "speed": SPEED,
           "fitted_to": "the sentence starts of the first narration (the first voice)", "fit": fit, "phrases": phrases}, open(OUT + "/narration_timing.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
json.dump({"text": "".join(chars_all), "chars": chars_all, "t0": T0_all, "t1": T1_all, "duration": DUR, "voice": VNAME, "speed": SPEED}, open(OUT + "/narration.chars.json", "w", encoding="utf8"), ensure_ascii=False)
# ---------------------------------------------------------------- report
tp = [f["tempo"] for f in fit]; d = [abs(a["t0"] - b["t0"]) for a, b in zip(phrases, rph)]
print(f"TOTAL {DUR:.3f}s ({NTOT} samples, same as the reference). tempo per sentence: min {min(tp):.3f} median {np.median(tp):.3f} max {max(tp):.3f}")
print("tempo:", " ".join(f"{f['sentence']}:{f['tempo']:.2f}" for f in fit))
print(f"caption phrases {len(phrases)} (reference {len(rph)}); phrase start drift vs reference: median {np.median(d):.3f}s, p90 {np.percentile(d, 90):.3f}s, max {max(d):.3f}s")
worst = sorted(zip(d, phrases, rph), key=lambda t: -t[0])[:6]
for dd, a, b in worst: print(f"  drift {dd:.2f}s  s{a['sentence']} '{a['text']}'  new {a['t0']:.2f}  old {b['t0']:.2f}")
print(f"active RMS {20*np.log10(np.sqrt((y[np.abs(y)>0.02]**2).mean())):.1f} dBFS (reference {20*np.log10(REF_RMS):.1f}), peak {20*np.log10(np.abs(y).max()):.1f} dBFS")
