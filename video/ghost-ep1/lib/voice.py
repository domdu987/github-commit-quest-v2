"""Generate narration/dialogue for an episode with Gemini TTS on fal.ai and derive beat timing from it.

Usage: python3 voice.py lines.json out_dir
lines.json: [{"id": "b01", "text": "...", "voice": "Puck", "style": "...", "tempo": 1.0}, ...]
Writes out_dir/<id>.wav (trimmed, 44.1 kHz stereo) and out_dir/durations.json.
Existing wavs are reused so re-runs only synthesize changed or missing lines.
"""
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.request

ENDPOINT = "https://fal.run/fal-ai/gemini-3.1-flash-tts"
DEFAULT_STYLE = ("เล่าเรื่องแบบยูทูบเบอร์สายเล่าเรื่องที่คนชอบฟัง น้ำเสียงสดใส เป็นกันเอง ชวนลุ้น "
                 "พูดกระชับ จังหวะเร็วพอดี ไม่ลากเสียง")


def synth(text, voice, style, mp3_path):
    body = json.dumps({"prompt": text, "style_instructions": style, "voice": voice,
                       "language_code": "Thai (Thailand)", "temperature": 0.8}).encode()
    for attempt in range(5):
        req = urllib.request.Request(ENDPOINT, data=body, headers={"Content-Type": "application/json"})
        try:
            res = json.load(urllib.request.urlopen(req, timeout=180))
            urllib.request.urlretrieve(res["audio"]["url"], mp3_path)
            return
        except Exception as e:  # 429 rate limits and the flaky content checker both clear on retry
            print(f"  retry {attempt + 1}: {e}", file=sys.stderr)
            time.sleep(6 * (attempt + 1))
    raise RuntimeError(f"TTS failed for: {text}")


def trim(mp3_path, wav_path, tempo):
    af = ("silenceremove=start_periods=1:start_threshold=-40dB:stop_periods=-1:stop_duration=0.3:"
          "stop_threshold=-40dB:stop_silence=0.22,areverse,silenceremove=start_periods=1:start_threshold=-40dB,areverse")
    if abs(tempo - 1.0) > 1e-3:
        af += f",atempo={tempo}"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3_path, "-af", af + ",apad=pad_dur=0.04",
                    "-ar", "44100", "-ac", "2", wav_path], check=True)


def duration(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", path]).decode().strip())


def main():
    lines = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    durs = {}
    for ln in lines:
        voice = ln.get("voice", "Puck")
        style = ln.get("style", DEFAULT_STYLE)
        key = hashlib.sha1(f"{voice}|{style}|{ln['text']}".encode()).hexdigest()[:10]
        mp3 = os.path.join(out, f"{ln['id']}.{key}.mp3")
        wav = os.path.join(out, f"{ln['id']}.wav")
        if not os.path.exists(mp3):
            print(f"tts {ln['id']} [{voice}] {ln['text']}")
            synth(ln["text"], voice, style, mp3)
            time.sleep(1.5)
        trim(mp3, wav, ln.get("tempo", 1.0))
        durs[ln["id"]] = round(duration(wav), 3)
    json.dump(durs, open(os.path.join(out, "durations.json"), "w"), indent=1)
    print(json.dumps(durs, indent=1))
    print("total", round(sum(durs.values()), 2))


if __name__ == "__main__":
    main()
