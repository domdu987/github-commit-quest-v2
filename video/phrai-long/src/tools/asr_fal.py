"""ASR QA through fal whisper: python3 asr_fal.py lines.json vo id [id...] -> prints CER per line, updates vo/asr.json"""
import base64, json, os, re, subprocess, sys, urllib.request
lines = {l["id"]: l for l in json.load(open(sys.argv[1]))}
vo = sys.argv[2]
asrp = os.path.join(vo, "asr.json")
asr = json.load(open(asrp)) if os.path.exists(asrp) else {}
def norm(s): return re.sub(r"[\s…!?.,ๆ\"'“”]", "", s)
def cer(a, b):
    a, b = norm(a), norm(b)
    d = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        p, d[0] = d[0], i
        for j, cb in enumerate(b, 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (ca != cb))
    return d[len(b)] / max(1, len(a))
for vid in sys.argv[3:]:
    wav = os.path.join(vo, f"{vid}.wav")
    mp3 = subprocess.check_output(["ffmpeg", "-v", "error", "-i", wav, "-ac", "1", "-ar", "16000", "-f", "mp3", "-b:a", "64k", "-"])
    uri = "data:audio/mpeg;base64," + base64.b64encode(mp3).decode()
    body = json.dumps({"audio_url": uri, "task": "transcribe", "language": "th", "chunk_level": "segment"}).encode()
    req = urllib.request.Request("https://fal.run/fal-ai/whisper", data=body, headers={"Content-Type": "application/json"})
    res = json.load(urllib.request.urlopen(req, timeout=240))
    txt = res.get("text", "").strip()
    asr[vid] = txt
    c = cer(lines[vid]["text"], txt)
    print(f"{vid} CER {c:.3f} {'OK' if c <= 0.25 else 'BAD'} | {lines[vid]['text']} | {txt}", flush=True)
json.dump(asr, open(asrp, "w"), ensure_ascii=False, indent=1)
