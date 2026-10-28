import sys, json
from faster_whisper import WhisperModel
audio_path, model_name, out = sys.argv[1], sys.argv[2], sys.argv[3]
import wave, numpy as np
with wave.open(audio_path) as wf:
    audio = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
model = WhisperModel(model_name, device="cpu", compute_type="int8", cpu_threads=4)
segments, info = model.transcribe(audio, language="th", beam_size=5, word_timestamps=True, vad_filter=False, condition_on_previous_text=False)
res = {"language": info.language, "prob": info.language_probability, "segments": []}
for s in segments:
    seg = {"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text,
           "words": [{"s": round(w.start, 2), "e": round(w.end, 2), "w": w.word} for w in (s.words or [])]}
    res["segments"].append(seg)
    print(f"[{s.start:6.2f} - {s.end:6.2f}] {s.text}", flush=True)
json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)
