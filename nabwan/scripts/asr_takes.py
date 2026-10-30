# asr_takes.py DIR KEY... : Whisper large-v3 (plain, no prompt) on DIR/KEY16.wav; merges into DIR/words_all.json,
# DIR/bounds_all.json (speech start/end from the 44.1k take's energy) and prints one line per take.
import sys, json, os, numpy as np, soundfile as sf
from faster_whisper import WhisperModel
d, keys = sys.argv[1], sys.argv[2:]
m = WhisperModel('large-v3', device='cpu', compute_type='int8', cpu_threads=4)
wp, bp = os.path.join(d, 'words_all.json'), os.path.join(d, 'bounds_all.json')
W = json.load(open(wp)) if os.path.exists(wp) else {}
B = json.load(open(bp)) if os.path.exists(bp) else {}
for k in keys:
    a, sr = sf.read(os.path.join(d, k + '16.wav'), dtype='float32')
    segs, _ = m.transcribe(a, language='th', beam_size=5, word_timestamps=True, vad_filter=False, condition_on_previous_text=False)
    toks, txt = [], ''
    for s in segs:
        txt += s.text
        for w in s.words or []: toks.append([w.word, round(w.start, 2), round(w.end, 2)])
    W[k] = toks
    b, sr2 = sf.read(os.path.join(d, k + '44.wav')); f = int(sr2 * 0.01); n = len(b) // f
    r = np.sqrt((b[:n * f].reshape(n, f) ** 2).mean(1)); db = 20 * np.log10(r / r.max() + 1e-9)
    on = np.where(db > -38)[0]
    B[k] = [round(on[0] * 0.01, 2), round((on[-1] + 1) * 0.01, 2)]
    print(f'{k:15s} {len(b) / sr2:5.2f}s {txt.strip()}', flush=True)
json.dump(W, open(wp, 'w'), ensure_ascii=False); json.dump(B, open(bp, 'w'))
