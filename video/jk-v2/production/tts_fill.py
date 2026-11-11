"""Pre-record lines that Gemini's checker rejects (HTTP 422): try the text, then '...'→',', then '...'→' ', then a softened
wording for the spoken take only (the caption keeps the original). Saves the mp3 under the exact name voice.py expects, so
`voice.py lines.json vo` then only trims. Usage: python3 tts_fill.py lines.json vo"""
import hashlib, json, os, sys, time, urllib.request, urllib.error
ENDPOINT = "https://fal.run/fal-ai/gemini-3.1-flash-tts"
SOFT = [("ฟันคอขาด", "ฟันคอ"), ("ตุ้บ!", "ตุ้บ"), ("!", "")]
lines = json.load(open(sys.argv[1], encoding="utf-8")); out = sys.argv[2]
def call(prompt, style, voice):
    body = json.dumps({"prompt": prompt, "style_instructions": style, "voice": voice, "language_code": "Thai (Thailand)", "temperature": 0.8}).encode()
    for attempt in range(3):
        try:
            res = json.load(urllib.request.urlopen(urllib.request.Request(ENDPOINT, data=body, headers={"Content-Type": "application/json"}), timeout=180))
            return res["audio"]["url"]
        except urllib.error.HTTPError as e:
            print(f"   {e.code} on attempt {attempt + 1}", file=sys.stderr)
            if e.code == 422: return None
            time.sleep(5 * (attempt + 1))
        except Exception as e:
            print(f"   {e}", file=sys.stderr); time.sleep(5 * (attempt + 1))
    return None
for ln in lines:
    voice, style, text = ln.get("voice", "Puck"), ln.get("style"), ln["text"]
    take = ln.get("take", 0) or ""
    key = hashlib.sha1(f"{voice}|{style}|{text}{take}".encode()).hexdigest()[:10]
    mp3 = os.path.join(out, f"{ln['id']}.{key}.mp3")
    if os.path.exists(mp3): print("have", ln["id"]); continue
    variants = [text, text.replace("...", ","), text.replace("...", " ")]
    soft = text
    for a, b in SOFT: soft = soft.replace(a, b)
    variants += [soft.replace("...", ","), soft.replace("...", " ")]
    seen, ok = set(), False
    for v in variants:
        if v in seen: continue
        seen.add(v); print("tts", ln["id"], v)
        url = call(v, style, voice)
        if url:
            urllib.request.urlretrieve(url, mp3); ok = True
            if v != text: print("   recorded as:", v)
            break
    if not ok: print("FAILED", ln["id"]); sys.exit(1)
print("all recorded")
