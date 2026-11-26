import json, subprocess, sys, base64, difflib, re
sys.path.insert(0, '../th'); import tts_fal
VOICE = "tKtPl8obOBs5uPMei6yN"; SPEED = 1.15
norm = lambda s: re.sub(r"[\s\.\,\!\?…\"“”'ๆ]", "", s).replace("หกสิบ","60").replace("สาม","3").replace("สี่","4")
def stt(path):
    b = base64.b64encode(open(path, 'rb').read()).decode()
    body = json.dumps({"audio_url": "data:audio/mpeg;base64," + b, "language_code": "th"})
    open('_stt.json', 'w').write(body)
    r = subprocess.run(["curl", "-s", "-m", "120", "-X", "POST", "https://fal.run/fal-ai/elevenlabs/speech-to-text", "-H", "Content-Type: application/json", "-d", "@_stt.json"], capture_output=True, text=True)
    return json.loads(r.stdout).get("text", "")
report = []
for s in json.load(open('script.json')):
    best = None
    for attempt in range(1, 4):
        out = f"takes/{s['id']}_a{attempt}"
        tts_fal.synth(s['tts'], out, VOICE, SPEED)
        heard = stt(out + ".mp3")
        acc = difflib.SequenceMatcher(None, norm(s['tts']), norm(heard)).ratio()
        print(f"{s['id']} try {attempt}: {acc*100:.1f}%  heard: {heard}", flush=True)
        if best is None or acc > best[1]: best = (out, acc, heard, attempt)
        if acc >= 0.97: break
    report.append({"id": s['id'], "take": best[0], "accuracy": round(best[1]*100, 1), "heard": best[2], "tries": attempt})
json.dump(report, open('verify_report.json', 'w'), ensure_ascii=False, indent=1)
