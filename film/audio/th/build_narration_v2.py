"""Full Thai narration for script v2 (formula-matched) through fal.ai (ElevenLabs v3, voice Ohm), in paragraph chunks.
The hook chunk is reused from the first build so the opening audio and its timing stay identical.
usage: python3 build_narration_v2.py
"""
import sys, json, os, wave, subprocess, re, difflib, shutil
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tts_fal
P = "/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj"
OUT = P + "/audio/th/full_v2"; OLD = P + "/audio/th/full"; os.makedirs(OUT, exist_ok=True)
SPEED = 1.2; SR = 48000
TEMPO = json.load(open(OLD + "/narration.chars.json", encoding="utf8"))["tempo"]   # same stretch as the hook already delivered
sc = json.load(open(P + "/script_th_v2/script_th.json", encoding="utf8")); sents = sc["sentences"]
GROUPS = [[0], [1, 2, 3], [4, 5], [6, 7], [8, 9, 10], [11, 12, 13], [14, 15, 16], [17, 18], [19, 20]]
assert sorted(sum(GROUPS, [])) == list(range(len(sents)))
NUM = {"1938": "หนึ่งเก้าสามแปด", "120": "ร้อยยี่สิบ", "100": "ร้อย"}
norm = lambda s: re.sub(r"[\s\.,!?\"“”ๆ]", "", s)

def read_wav(path):
    w = wave.open(path); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768; return x, w.getframerate()

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
    return x[km], [rm(t) for t in t0], [rm(t) for t in t1], sum(b - a for a, b in cuts) / sr

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

chunks = []
for gi, g in enumerate(GROUPS):
    base = f"{OUT}/chunk{gi:02d}"
    text = "\n".join(sents[i]["tts"] for i in g)
    if gi == 0 and not os.path.exists(base + ".chars.json"):
        for ext in (".json", ".mp3", ".wav", ".chars.json"): shutil.copy(OLD + "/chunk00_s1.2" + ext, base + ext)
    if not os.path.exists(base + ".chars.json") or json.load(open(base + ".chars.json", encoding="utf8")).get("src_text") not in (None, text):
        best = None
        for take in range(1, 4):
            tb = f"{base}_take{take}"
            tts_fal.synth(text, tb, tts_fal.OHM, SPEED)
            ratio, heard = asr_ratio(tb, text)
            print(f"  chunk {gi} take {take}: ASR match {ratio}")
            if best is None or (ratio or 0) > best[0]: best = (ratio or 0, tb)
            if ratio is not None and ratio >= 0.985: break
        for ext in (".json", ".mp3", ".wav", ".chars.json"): shutil.copy(best[1] + ext, base + ext)
        c = json.load(open(base + ".chars.json", encoding="utf8")); c["src_text"] = text; c["asr_match"] = best[0]
        json.dump(c, open(base + ".chars.json", "w", encoding="utf8"), ensure_ascii=False)
    c = json.load(open(base + ".chars.json", encoding="utf8"))
    x, sr = read_wav(base + ".wav"); assert sr == SR
    y, t0, t1, cut = tighten(x, sr, c["t0"], c["t1"]) if gi > 0 else (lambda r: r)(__import__("build_narration_tighten_v1").tighten(x, sr, c["t0"], c["t1"]))
    act = y[np.abs(y) > 0.02]; rms = float(np.sqrt((act ** 2).mean()))
    chunks.append({"g": g, "chars": c["chars"], "t0": t0, "t1": t1, "y": y, "rms": rms})
    print(f"chunk {gi} sentences {g}: {len(x)/sr:.2f}s -> {len(y)/sr:.2f}s, asr {c.get('asr_match')}")

TARGET = 65.4
target = float(np.median([c["rms"] for c in chunks]))
def write(path, x):
    w = wave.open(path, "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
# part A = the hook exactly as already delivered (same tighten, same tempo, same 0.20 s gap after it)
h = chunks[0]; yA = np.concatenate([h["y"] * (target / h["rms"]), np.zeros(int(0.20 * SR))])
# part B = everything else, tighter pauses, its own tempo so the film lands on TARGET seconds
GAPB = 0.16; partsB, charsB, T0B, T1B, offs = [], [], [], [], 0.0
for ci, c in enumerate(chunks[1:]):
    y = c["y"] * (target / c["rms"])
    if ci > 0:
        partsB.append(np.zeros(int(GAPB * SR))); charsB.append("\n"); T0B.append(offs); T1B.append(offs + GAPB); offs += GAPB
    partsB.append(y); charsB += c["chars"]; T0B += [t + offs for t in c["t0"]]; T1B += [t + offs for t in c["t1"]]; offs += len(y) / SR
yB = np.concatenate(partsB)
lenA = len(yA) / SR / TEMPO
TEMPO_B = max(TEMPO, min(1.22, (len(yB) / SR) / (TARGET - lenA)))
peak = max(np.abs(yA).max(), np.abs(yB).max()); g = min(1.0, 0.89 / peak)
write(OUT + "/partA_raw.wav", yA * g); write(OUT + "/partB_raw.wav", yB * g)
for part, tp in (("A", TEMPO), ("B", TEMPO_B)):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{OUT}/part{part}_raw.wav", "-af", f"atempo={tp:.5f}", "-ar", str(SR), f"{OUT}/part{part}.wav"], check=True)
xa, _ = read_wav(OUT + "/partA.wav"); xb, _ = read_wav(OUT + "/partB.wav")
offB = len(xa) / SR
x = np.concatenate([xa, xb]); write(OUT + "/narration_pre.wav", x)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", OUT + "/narration_pre.wav", "-af", "alimiter=limit=0.9", "-ar", str(SR), OUT + "/narration.wav"], check=True)
total = len(x) / SR
chars = h["chars"] + ["\n"] + charsB
T0 = [t / TEMPO for t in h["t0"]] + [len(h["y"]) / SR / TEMPO] + [offB + t / TEMPO_B for t in T0B]
T1 = [t / TEMPO for t in h["t1"]] + [offB] + [offB + t / TEMPO_B for t in T1B]
print(f"hook tempo {TEMPO:.4f}, rest tempo {TEMPO_B:.4f}; part A {offB:.2f}s, part B {len(xb)/SR:.2f}s")
json.dump({"text": "".join(chars), "chars": chars, "t0": T0, "t1": T1, "duration": total, "voice": "Ohm", "speed": SPEED, "tempo_hook": TEMPO, "tempo_rest": TEMPO_B}, open(OUT + "/narration.chars.json", "w", encoding="utf8"), ensure_ascii=False)
caps = [{"text": t, "sentence": si, "beat": s["beat"], "k": k} for si, s in enumerate(sents) for k, t in enumerate(s["captions"])]
timed, ratio, _ = tts_fal.align(OUT + "/narration", caps)
json.dump({"duration": total, "audio": OUT + "/narration.wav", "match_ratio": ratio, "phrases": timed}, open(OUT + "/narration_timing.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
d = [q["t1"] - q["t0"] for q in timed]
print(f"TOTAL {total:.2f}s; captions {len(timed)} match {ratio:.3f}; phrase min {min(d):.2f} median {np.median(d):.2f} max {max(d):.2f}")
for q in timed[:8]: print(f'  {q["t0"]:6.2f}-{q["t1"]:6.2f} {q["text"]}')
