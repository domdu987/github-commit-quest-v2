"""Thai narration through fal.ai (ElevenLabs v3) with character timestamps, plus caption alignment.
usage:
  python3 tts_fal.py synth <text_file> <out_basename> [voice_id] [speed]     -> <out>.mp3, <out>.wav, <out>.json (raw), <out>.chars.json
  python3 tts_fal.py align <out_basename> <captions_json> <timing_out.json>   captions_json: [{"text": "...", ...extra keys kept}]
The fal key is injected by the session proxy for host fal.run; no key is read here.
"""
import sys, json, subprocess, re, difflib, wave

EP = "fal-ai/elevenlabs/tts/eleven-v3"
OHM = "tKtPl8obOBs5uPMei6yN"

def synth(text, out, voice=OHM, speed=1.1):
    body = {"text": text, "voice": voice, "language_code": "th", "timestamps": True, "speed": float(speed)}
    r = subprocess.run(["curl", "-sS", "-m", "300", "-X", "POST", f"https://fal.run/{EP}", "-H", "Content-Type: application/json",
                        "-d", json.dumps(body, ensure_ascii=False), "-w", "\n%{http_code}"], capture_output=True, text=True)
    txt, code = r.stdout.rsplit("\n", 1)
    open(out + ".json", "w", encoding="utf8").write(txt)
    if code != "200":
        raise SystemExit(f"fal HTTP {code}: {txt[:500]}")
    d = json.loads(txt)
    subprocess.run(["curl", "-sS", "-m", "120", "-o", out + ".mp3", d["audio"]["url"]], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", out + ".mp3", "-ar", "48000", "-ac", "1", out + ".wav"], check=True)
    chars, t0, t1 = [], [], []
    for seg in d["timestamps"]:
        chars += seg["characters"]; t0 += seg["character_start_times_seconds"]; t1 += seg["character_end_times_seconds"]
    w = wave.open(out + ".wav"); dur = w.getnframes() / w.getframerate()
    json.dump({"text": "".join(chars), "chars": chars, "t0": t0, "t1": t1, "duration": dur, "voice": voice, "speed": speed},
              open(out + ".chars.json", "w", encoding="utf8"), ensure_ascii=False)
    print(f"wrote {out}.mp3 {dur:.2f}s, {len(chars)} chars")
    return dur

_skip = re.compile(r"[\s\.,!?\"“”‘’:;…\-–—()]")
def _norm_index(s):
    """normalized string and, for each normalized char, its index in s"""
    out, idx = [], []
    for i, ch in enumerate(s):
        if not _skip.match(ch):
            out.append(ch); idx.append(i)
    return "".join(out), idx

def align(base, caps, hold_tail=0.35):
    c = json.load(open(base + ".chars.json", encoding="utf8"))
    spoken, sidx = _norm_index(c["text"])
    joined = "".join(p["text"] for p in caps)
    cap_norm, _ = _norm_index(joined)
    # boundary positions of each caption in the normalized caption string
    bounds, pos = [], 0
    for p in caps:
        n = len(_norm_index(p["text"])[0]); bounds.append((pos, pos + n)); pos += n
    # map caption-normalized index -> spoken-normalized index through matching blocks
    sm = difflib.SequenceMatcher(None, cap_norm, spoken, autojunk=False)
    amap = {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1): amap[i1 + k] = j1 + k
        else:  # replaced / inserted / deleted span (digits written as words and so on): spread linearly
            for k in range(i2 - i1):
                amap[i1 + k] = j1 + int((j2 - j1) * k / max(1, i2 - i1))
    def t_start(ci):
        j = min(max(amap.get(ci, 0), 0), len(sidx) - 1); return c["t0"][sidx[j]]
    out = []
    for p, (a, b) in zip(caps, bounds):
        q = dict(p); q["t0"] = round(t_start(a), 3); out.append(q)
    for i, q in enumerate(out):
        q["t1"] = out[i + 1]["t0"] if i + 1 < len(out) else round(min(c["duration"], c["t1"][-1] + hold_tail), 3)
    ratio = sm.ratio()
    return out, ratio, c

if __name__ == "__main__":
    if sys.argv[1] == "synth":
        text = open(sys.argv[2], encoding="utf8").read().strip()
        synth(text, sys.argv[3], *(sys.argv[4:5] or [OHM]), *(sys.argv[5:6] or [1.1]))
    elif sys.argv[1] == "align":
        caps = json.load(open(sys.argv[3], encoding="utf8"))
        out, ratio, c = align(sys.argv[2], caps)
        json.dump(out, open(sys.argv[4], "w", encoding="utf8"), ensure_ascii=False, indent=1)
        print("match ratio", round(ratio, 3)); [print(f'{q["t0"]:6.2f} {q["t1"]:6.2f}  {q["text"]}') for q in out]
