"""Check every recorded line against its script with Whisper and re-record the ones that came out wrong.

Usage: python3 voice_qa.py lines.json vo_dir [--fix N]
For each line: transcribe vo_dir/<id>.wav (faster-whisper large-v3-turbo, Thai), compare with the script
after dropping spaces, punctuation and caption marks (character error rate), and flag lines whose CER is
above 0.25 or that run much longer than the text (Gemini sometimes says a line twice).
With --fix N, flagged lines get "take" bumped in lines.json and voice.py re-records them, up to N rounds;
the best take seen is kept. Whisper leans toward the words it expects, so a pass here does not prove a
subtle mispronunciation is gone (see brand/splice_signature.py for "ถูกทาง"); it catches wrong, missing
and repeated words. Writes vo_dir/qa.json.
"""
import json
import os
import re
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.environ.get("WHISPER_DIR", os.path.join(HERE, "..", "..", "whisper"))
DIGITS = "ศูนย์ หนึ่ง สอง สาม สี่ ห้า หก เจ็ด แปด เก้า".split()


def thai_number(n):
    if n < 10:
        return DIGITS[n]
    if n < 100:
        t, u = divmod(n, 10)
        tens = "สิบ" if t == 1 else ("ยี่สิบ" if t == 2 else DIGITS[t] + "สิบ")
        return tens + ("" if u == 0 else ("เอ็ด" if u == 1 else DIGITS[u]))
    h, r = divmod(n, 100)
    return DIGITS[h] + "ร้อย" + (thai_number(r) if r else "")


def norm(s):
    s = re.sub(r"\d+", lambda m: thai_number(int(m.group())) if int(m.group()) < 1000 else m.group(), s)
    return re.sub(r"[\s\[\]{}…!?.,\"“”'ๆ-]", "", s)


def cer(ref, hyp):
    a, b = norm(ref), norm(hyp)
    d = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        prev, d[0] = d[0], i
        for j, cb in enumerate(b, 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (ca != cb))
    return d[len(b)] / max(1, len(a))


def transcribe(model, path):
    x = np.frombuffer(subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"]), np.float32)
    segs, _ = model.transcribe(x, language="th", beam_size=5, temperature=0, vad_filter=False)
    return " ".join(s.text.strip() for s in segs), len(x) / 16000


def check(model, lines, vo):
    rep = {}
    for ln in lines:
        wav = os.path.join(vo, f"{ln['id']}.wav")
        hyp, dur = transcribe(model, wav)
        c = cer(ln["text"], hyp)
        long = dur > 0.6 + 0.17 * len(norm(ln["text"])) / max(0.5, ln.get("tempo", 1.0))  # ~6 Thai chars/s is already slow
        rep[ln["id"]] = {"text": ln["text"], "heard": hyp, "cer": round(c, 3), "dur": round(dur, 2), "bad": c > 0.25 or long, "long": long}
        print(f"{ln['id']:4s} cer {c:4.2f} {'LONG ' if long else ''}{'BAD ' if rep[ln['id']]['bad'] else 'ok  '} {ln['text']}  →  {hyp}", flush=True)
    return rep


def main():
    from faster_whisper import WhisperModel
    lines_path, vo = sys.argv[1], sys.argv[2]
    rounds = int(sys.argv[sys.argv.index("--fix") + 1]) if "--fix" in sys.argv else 0
    model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", download_root=MODEL_DIR)
    lines = json.load(open(lines_path))
    rep = check(model, lines, vo)
    best = {k: v["cer"] for k, v in rep.items()}
    for r in range(rounds):
        bad = [ln for ln in lines if rep[ln["id"]]["bad"] and ln["id"] != "s01"]
        if not bad:
            break
        print(f"round {r + 1}: re-recording", [ln["id"] for ln in bad])
        for ln in bad:
            ln["take"] = ln.get("take", 0) + 1
        json.dump(lines, open(lines_path, "w"), ensure_ascii=False, indent=1)
        subprocess.run(["python3", os.path.join(HERE, "voice.py"), lines_path, vo], check=True, stdout=subprocess.DEVNULL)
        new = check(model, bad, vo)
        for ln in bad:
            if new[ln["id"]]["cer"] <= best[ln["id"]] or rep[ln["id"]]["long"]:
                rep[ln["id"]], best[ln["id"]] = new[ln["id"]], new[ln["id"]]["cer"]
            else:  # the earlier take was better: go back to it
                ln["take"] -= 1
        json.dump(lines, open(lines_path, "w"), ensure_ascii=False, indent=1)
        subprocess.run(["python3", os.path.join(HERE, "voice.py"), lines_path, vo], check=True, stdout=subprocess.DEVNULL)
    json.dump(rep, open(os.path.join(vo, "qa.json"), "w"), ensure_ascii=False, indent=1)
    print("still flagged:", [k for k, v in rep.items() if v["bad"]] or "none")


if __name__ == "__main__":
    main()
