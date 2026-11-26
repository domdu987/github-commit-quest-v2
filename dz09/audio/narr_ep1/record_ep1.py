import json, subprocess, sys, base64, difflib, re, os
sys.path.insert(0, '../th'); import tts_fal
VOICE = "tKtPl8obOBs5uPMei6yN"; SPEED = 1.15
W, N = int(sys.argv[1]), int(sys.argv[2])
norm = lambda s: re.sub(r"[\s\.\,\!\?…\"“”'ๆ\-—]", "", s)
def stt(path):
    b = base64.b64encode(open(path, 'rb').read()).decode()
    f = f'_stt{W}.json'
    open(f, 'w').write(json.dumps({"audio_url": "data:audio/mpeg;base64," + b, "language_code": "th"}))
    r = subprocess.run(["curl", "-s", "-m", "120", "-X", "POST", "https://fal.run/fal-ai/elevenlabs/speech-to-text", "-H", "Content-Type: application/json", "-d", "@" + f], capture_output=True, text=True)
    try: return json.loads(r.stdout).get("text", "")
    except Exception: return ""
S = json.load(open('../../ep1/plan/narration_ep1.json'))['sentences']
for i, s in enumerate(S):
    if i % N != W: continue
    rp = f"takes/{s['id']}.report.json"
    if os.path.exists(rp): continue
    best = None; calls = 0; chars = 0
    for attempt in range(1, 4):
        out = f"takes/{s['id']}_a{attempt}"
        try: tts_fal.synth(s['tts'], out, VOICE, SPEED)
        except SystemExit as e: print(s['id'], 'ERR', e, flush=True); continue
        calls += 1; chars += len(s['tts'])
        heard = stt(out + ".mp3")
        acc = difflib.SequenceMatcher(None, norm(s['tts']), norm(heard)).ratio()
        print(f"{s['id']} try {attempt}: {acc*100:.1f}%  heard: {heard}", flush=True)
        if best is None or acc > best[1]: best = (out, acc, heard, attempt)
        if acc >= 0.95: break
    if best:
        json.dump({"id": s['id'], "take": best[0], "accuracy": round(best[1]*100, 1), "heard": best[2], "tts": s['tts'], "tts_calls": calls, "chars_sent": chars}, open(rp, 'w'), ensure_ascii=False)
