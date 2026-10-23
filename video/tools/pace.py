"""Speech pace of a clip: Thai characters per second while talking, share of time spent talking, pause lengths."""
import re
import subprocess
import sys

import numpy as np
from faster_whisper import WhisperModel

m = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", download_root=sys.argv[1])
for name, path in zip(sys.argv[2::2], sys.argv[3::2]):
    a = np.frombuffer(subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"]), np.float32)
    segs, _ = m.transcribe(a, language="th", beam_size=5, temperature=0, word_timestamps=True, vad_filter=True)
    words = [w for s in segs for w in s.words]
    chars = sum(len(re.sub(r"[\s\W\d]", "", w.word)) for w in words)
    # talking time = word spans merged where the gap < 0.25 s
    spans, cur = [], None
    for w in words:
        if cur and w.start - cur[1] < 0.25:
            cur[1] = w.end
        else:
            if cur: spans.append(cur)
            cur = [w.start, w.end]
    if cur: spans.append(cur)
    talk = sum(b - a for a, b in spans)
    gaps = [spans[i + 1][0] - spans[i][1] for i in range(len(spans) - 1)]
    dur = len(a) / 16000
    print(f"{name:14s} dur {dur:6.1f}s  talk {talk:6.1f}s ({100 * talk / dur:4.1f}%)  chars {chars:5d}  chars/s talking {chars / talk:5.2f}  chars/s overall {chars / dur:5.2f}  "
          f"median pause {np.median(gaps):.2f}s  phrases {len(spans)}  avg phrase {talk / max(1, len(spans)):.2f}s", flush=True)
