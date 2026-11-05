"""Bridge lines for ต้นตะเคียนกลางนา ฉบับเต็ม: Gemini TTS on fal (same voices/styles as video/takhian/mklines.py).
At most 3 calls per line (1 + 2 retries, coordinator 5 Nov). Writes <out>/<id>.<hash>.mp3 and trimmed <id>.wav."""
import hashlib, json, os, subprocess, sys, time, urllib.request
EP = "https://fal.run/fal-ai/gemini-3.1-flash-tts"
NAR = "อ่านแบบผู้บรรยายสารคดี น้ำเสียงเรียบ เป็นกลาง จริงจัง ไม่ตื่นเต้น ไม่กระซิบ ชัดถ้อยชัดคำ จังหวะสม่ำเสมอ ไม่ลากเสียง พูดประโยคนี้แค่ครั้งเดียว ไม่พูดซ้ำ"
TON = "เด็กผู้ชายอายุเก้าขวบ เสียงแหลมเล็ก ซน มั่นใจเกินตัว พูดเร็วแบบเด็กไทย พูดประโยคนี้แค่ครั้งเดียว ไม่พูดซ้ำ"
LINES = [
 {"id": "x01", "text": "ฝนยังกระหน่ำ… ทุกคนยังยืนนิ่ง ไม่มีใครขยับ", "cap": "ฝนยังกระหน่ำ… / ทุกคนยัง[ยืนนิ่ง] / ไม่มีใครขยับ", "voice": "Puck", "tempo": 1.2, "style": NAR},
 {"id": "x02", "text": "ยาย… นางจะมาเอาพวกเราไปด้วยไหม", "cap": "ยาย… / นางจะมา[เอาพวกเราไป]ด้วยไหม", "voice": "Leda", "tempo": 1.22, "style": TON.replace(" พูดประโยคนี้", " เสียงสั่น กลัว แต่พูดชัดทุกคำ ออกเสียง ยาย และ นาง ชัดเจน พูดประโยคนี้")},
 {"id": "x03", "text": "แต่นาทีนี้… ลุงรอไม่ได้แล้ว", "cap": "แต่นาทีนี้… / ลุง[รอไม่ได้แล้ว]", "voice": "Puck", "tempo": 1.2, "style": NAR},
]
def synth(text, voice, style, mp3):
    body = json.dumps({"prompt": text, "style_instructions": style, "voice": voice, "language_code": "Thai (Thailand)", "temperature": 0.8}).encode()
    for a in range(3):
        try:
            res = json.load(urllib.request.urlopen(urllib.request.Request(EP, data=body, headers={"Content-Type": "application/json"}), timeout=180))
            urllib.request.urlretrieve(res["audio"]["url"], mp3); return a + 1
        except Exception as e:
            print(f"  attempt {a + 1} failed: {e}", file=sys.stderr); time.sleep(6 * (a + 1))
    raise SystemExit(f"TTS failed: {text}")
def trim(mp3, wav, tempo):
    af = ("silenceremove=start_periods=1:start_threshold=-40dB:stop_periods=-1:stop_duration=0.3:stop_threshold=-40dB:stop_silence=0.22,"
          "areverse,silenceremove=start_periods=1:start_threshold=-40dB,areverse" + (f",atempo={tempo}" if abs(tempo - 1) > 1e-3 else "") + ",apad=pad_dur=0.04")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-af", af, "-ar", "44100", "-ac", "2", wav], check=True)
out = sys.argv[1]; only = sys.argv[2:]
json.dump(LINES, open(os.path.join(out, "..", "lines.json"), "w"), ensure_ascii=False, indent=1)
for ln in LINES:
    if only and ln["id"] not in only: continue
    key = hashlib.sha1(f"{ln['voice']}|{ln['style']}|{ln['text']}|{ln.get('take', 0)}".encode()).hexdigest()[:10]
    mp3 = os.path.join(out, f"{ln['id']}.{key}.mp3"); wav = os.path.join(out, f"{ln['id']}.wav")
    if not os.path.exists(mp3): print(ln["id"], "calls", synth(ln["text"], ln["voice"], ln["style"], mp3))
    trim(mp3, wav, ln["tempo"])
    print(ln["id"], subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav]).decode().strip())
