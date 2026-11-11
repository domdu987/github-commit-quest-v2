"""The music bed for สกิลจอมโกหก from the owner's Suno tracks (music/suno: quest = main theme, tension = the count-up and the
guards, musicbox = the warm ending). bed(N, SR, segments, load) → mono float32 of N samples: each (start, end, name) plays that
track from its top (looped if the segment is longer), fading in over 1 s and out over 1.5 s; neighbours overlap on the fades."""
import os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
TRACKS = {"quest": "quest.mp3", "tension": "tension.mp3", "musicbox": "musicbox.mp3", "cartoon": "Cartoon_Quest.mp3"}   # cartoon = the owner's "Cartoon Quest" (11 Nov) for everything after the hook
_cache = {}


def bed(N, SR, segments, load, fade_in=1.0, fade_out=1.5):
    out = np.zeros(N, np.float32)
    for k, (start, end, name) in enumerate(segments):
        if name not in _cache:
            _cache[name] = load(os.path.join(HERE, "..", "music", "suno", TRACKS[name]))
        src = _cache[name]
        s0, s1 = int(start * SR), int(min(end + (fade_out if k + 1 < len(segments) else 0), N / SR) * SR)
        n = s1 - s0
        x = np.tile(src, int(np.ceil(n / len(src))))[:n].copy()
        fi, fo = int((0.3 if start == 0 else fade_in) * SR), int(fade_out * SR)
        x[:fi] *= np.linspace(0, 1, fi, dtype=np.float32)
        x[-fo:] *= np.linspace(1, 0, fo, dtype=np.float32)
        out[s0:s1] += x
    return out
