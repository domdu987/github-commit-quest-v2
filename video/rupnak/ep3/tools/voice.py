"""Generate narration/dialogue for an episode with Gemini TTS on fal.ai and derive beat timing from it.

Usage: python3 voice.py lines.json out_dir
lines.json: [{"id": "b01", "text": "...", "voice": "Puck", "style": "...", "tempo": 1.0, "take": 0}, ...]
Writes out_dir/<id>.wav (trimmed, 44.1 kHz stereo) and out_dir/durations.json.
Existing wavs are reused so re-runs only synthesize changed or missing lines.
"""
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

ENDPOINT = "https://fal.run/fal-ai/gemini-3.1-flash-tts"
DEFAULT_STYLE = ("เล่าเรื่องแบบยูทูบเบอร์สายเล่าเรื่องที่คนชอบฟัง น้ำเสียงสดใส เป็นกันเอง ชวนลุ้น "
                 "พูดกระชับ จังหวะเร็วพอดี ไม่ลากเสียง")


def synth(text, voice, style, mp3_path):
    # Gemini's checker sometimes rejects a line outright (HTTP 422), often over an ellipsis; then the same words
    # are tried with the ellipses as commas, then as plain spaces (the caption keeps its "…" either way)
    variants = [text] + [v for v in (text.replace("…", ","), text.replace("…", " ")) if v != text]
    for vi, prompt in enumerate(variants):
        body = json.dumps({"prompt": prompt, "style_instructions": style, "voice": voice,
                           "language_code": "Thai (Thailand)", "temperature": 0.8}).encode()
        for attempt in range(5 if vi == 0 else 3):
            req = urllib.request.Request(ENDPOINT, data=body, headers={"Content-Type": "application/json"})
            try:
                res = json.load(urllib.request.urlopen(req, timeout=180))
                urllib.request.urlretrieve(res["audio"]["url"], mp3_path)
                if vi:
                    print(f"  recorded as: {prompt}", file=sys.stderr)
                return
            except urllib.error.HTTPError as e:
                print(f"  retry {attempt + 1}: {e}", file=sys.stderr)
                if e.code == 422 and attempt >= 1:
                    break  # a rejected wording stays rejected: move on to the next variant
                time.sleep(6 * (attempt + 1))
            except Exception as e:  # 429 rate limits and dropped connections clear on retry
                print(f"  retry {attempt + 1}: {e}", file=sys.stderr)
                time.sleep(6 * (attempt + 1))
    raise RuntimeError(f"TTS failed for: {text}")


def trim(mp3_path, wav_path, tempo, extra=None, db=-40):
    # db: the silence threshold; a line ending on a soft consonant (เมตร) needs a lower one or its tail is cut
    af = (f"silenceremove=start_periods=1:start_threshold={db}dB:stop_periods=-1:stop_duration=0.3:"
          f"stop_threshold={db}dB:stop_silence=0.22,areverse,silenceremove=start_periods=1:start_threshold={db}dB,areverse")
    if abs(tempo - 1.0) > 1e-3:
        af += f",atempo={tempo}"
    if extra:  # per-line colour, e.g. an echo for a voice calling from the forest
        af += ",apad=pad_dur=0.45," + extra
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3_path, "-af", af + ",apad=pad_dur=0.04",
                    "-ar", "44100", "-ac", "2", wav_path], check=True)


def stretch(wav_path, cut, factor):
    # slow only the first `cut` seconds (after tempo) by `factor` (<1 = longer): a clipped first syllable
    # ("อย่า" read as "อยาก" before "กลับ") is heard right once its vowel is long
    tmp = wav_path + ".tmp.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav_path, "-filter_complex",
                    f"[0]atrim=0:{cut},asetpts=N/SR/TB,atempo={factor}[a];[0]atrim={cut},asetpts=N/SR/TB[b];"
                    "[a][b]concat=n=2:v=0:a=1", tmp], check=True)
    os.replace(tmp, wav_path)


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
        take = f"|{ln['take']}" if ln.get("take") else ""  # bumping "take" asks for a fresh recording of the same line
        key = hashlib.sha1(f"{voice}|{style}|{ln['text']}{take}".encode()).hexdigest()[:10]
        mp3 = os.path.join(out, f"{ln['id']}.{key}.mp3")
        wav = os.path.join(out, f"{ln['id']}.wav")
        if not os.path.exists(mp3):
            print(f"tts {ln['id']} [{voice}] {ln['text']}")
            synth(ln["text"], voice, style, mp3)
            time.sleep(1.5)
        trim(mp3, wav, ln.get("tempo", 1.0), ln.get("af"), ln.get("trim_db", -40))
        if ln.get("stretch"):
            stretch(wav, *ln["stretch"])
        durs[ln["id"]] = round(duration(wav), 3)
    json.dump(durs, open(os.path.join(out, "durations.json"), "w"), indent=1)
    print(json.dumps(durs, indent=1))
    print("total", round(sum(durs.values()), 2))


if __name__ == "__main__":
    main()
