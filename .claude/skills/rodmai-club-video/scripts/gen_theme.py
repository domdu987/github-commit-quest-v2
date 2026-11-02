#!/usr/bin/env python3
"""Generate a story theme that can be heard on a phone speaker, then check where its energy sits.

    python3 -I gen_theme.py <out.mp3> <seconds> "<story part of the prompt>"
    python3 -I gen_theme.py --check <theme.mp3>           # only measure an existing file

Why (owner 2 Nov 2569 ~19:15: "เพลงหาย ไม่ได้ยินเลย"):
- The old shared prompt said "keep the midrange sparse".
- Every theme came back with 78-97 % of its energy below 300 Hz, where a phone speaker plays almost nothing.
- So on a phone the music was 22-24 dB under the voice, which sounds the same as no music.

What works (ต้นตะเคียน v3, 2 Nov):
- Name instruments the model knows well in the mid register: plucked lute "like a Thai phin or a mandolin", marimba, bamboo flute.
- Ask for a continuous lead melody "from the very first second to the end".
- Say "very little bass: no sub-bass, no drones".
- Result: 69 % of the energy in 300-4000 Hz, steady across the piece.
- Thai names alone (phin, ranat, khlui, khaen) gave a low drone plus cymbals: 0.4 % midrange in most windows.

Pass rule:
- >= 45 % of the energy in 300-4000 Hz overall.
- Every 10 s window except the last >= 25 %.
- If it fails, generate again with plainer instrument names. It costs about $0.60 per minute via fal ElevenLabs Music.

After mixing:
- Duck the music under the voice so "voice over music" stays >= 8 LU.
- A midrange theme masks the voice more than a bass drone did: ต้นตะเคียน needed duck depth 0.62 (about 8.4 dB) instead of 0.5.
- Then run musiccheck.py, which now checks the phone band too.
"""
import json
import os
import subprocess
import sys
import urllib.request

import numpy as np

COMMON = ("Instrumental cinematic theme for a dark animated survival short, mixed for phone speakers and played under spoken Thai narration. "
          "A continuous, clearly audible lead melody from the very first second to the end, in the middle register (about 300 Hz to 2 kHz), "
          "a repeating motif with small rests between phrases so the voice can sit in them. "
          "Very little bass: no sub-bass, no drones, no booming drums except a few hits on the biggest moments. "
          "No vocals, no choir, no lyrics, no sound effects, no rain, no wind, no noise or hiss beds. ")


def bands(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "48000", "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    sr, n = 48000, 4096
    win, fr = np.hanning(n), np.fft.rfftfreq(n, 1 / 48000)

    def share(seg):
        q = np.zeros(n // 2 + 1)
        for i in range(0, len(seg) - n, n // 2):
            q += np.abs(np.fft.rfft(seg[i:i + n] * win)) ** 2
        t = q.sum() + 1e-20
        return 100 * q[fr < 300].sum() / t, 100 * q[(fr >= 300) & (fr < 4000)].sum() / t

    lo, mid = share(x)
    wins = [share(x[s * sr:(s + 10) * sr])[1] for s in range(0, max(1, int(len(x) / sr) - 10), 10)]
    ok = mid >= 45 and (min(wins) if wins else 0) >= 25
    print(f"{os.path.basename(path)}: {len(x) / sr:.1f} s · below 300 Hz {lo:.1f}% · 300-4000 Hz {mid:.1f}% · "
          f"weakest 10 s window {min(wins) if wins else 0:.1f}% midrange → {'PASS' if ok else 'FAIL (phone speakers will lose it)'}")
    return ok


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--check":
        sys.exit(0 if bands(sys.argv[2]) else 1)
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    out, secs, story = sys.argv[1], float(sys.argv[2]), sys.argv[3]
    body = json.dumps({"prompt": COMMON + story, "music_length_ms": int(secs * 1000), "force_instrumental": True}).encode()
    req = urllib.request.Request("https://fal.run/fal-ai/elevenlabs/music", data=body, headers={"Content-Type": "application/json"})
    res = json.load(urllib.request.urlopen(req, timeout=500))
    urllib.request.urlretrieve(res["audio"]["url"], out)
    sys.exit(0 if bands(out) else 1)


if __name__ == "__main__":
    main()
