"""ต้นตะเคียนกลางนา ฉบับเต็ม (16:9) soundtrack: the ทะเลลด recipe of video/release/audio/takhian-tide-mix (suno1 from 0 s, unfiltered,
-30 dB RMS, duck 0.65) over the whole story. Times follow full/schedule.json (combine.py). Needs, next to full/: ../lib/mixcore.py,
../sfxlib/, ../music/takhian-theme.mp3 = video/music/suno1.mp3 (mixcore reads that name), and vo/ with EP.1 ids, EP.2 ids as e2_<id>, x01–x03.
EP.1 cues as takhian-tide-mix/ep1/mix.py without the shorts card (next); EP.2 cues as ep2/mix.py without its hook and recap; the bridge new.
Every dip is laid before every boost: mixcore's dip takes a minimum and would cancel a boost laid before it (coordinator 5 Nov)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "lib"))
from mixcore import Mix
m = Mix(HERE)
m.voices({"t03": -1, "y01": 1, "e2_t05": 1})
F, T = m.fx, m.T
# ================= EP.1 =================
F("hook", 0.0, "splash", 0.4*0.8); F("hook", 0.45, "rumble", 0.7); F("hook", 1.0, "bark", 0.6); F("hook", 1.6, "splash", 0.4*0.6)
F("cmd", 0.08, "crack", 1.0); F("cmd", 0.2, "flinch", 0.6)
F("stop", 0.0, "splash", 0.4*0.5)
F("why", 0.12, "crack2", 0.7); F("why", 0.3, "zap", 0.6)
F("nosafe", 1.1, "rumble", 0.6)
F("timer", 1.0, "stopwatch", 0.8)
F("buff", 0.6, "buffalo", 0.7)
F("leg1", 0.0, "cloth", 0.7)
F("sci1", 0.75, "rumble", 0.6); F("sci1", 2.35, "rumble", 0.5)
F("sci2", 0.18, "crack2", 0.75); F("sci2", 0.4, "zap", 0.6)
F("rule1", 0.15, "plankdrop", 0.9); F("rule1", m.vo_end("rule1") - 0.25, "bambootick", 0.8)
F("hut", 0.1, "splash", 0.4*0.6)
F("nohut", 0.12, "rumble", 0.8)
F("go", 0.3, "splash", 0.4*0.7); F("spread", 0.2, "splash", 0.4*0.6); F("spread", 1.6, "splash", 0.4*0.5)
F("flat", 0.05, "bodyflop", 0.9)
F("wflat", 0.18, "crack2", 0.7); F("wflat", 0.35, "zap", 0.7)
F("crouch", 0.28, "crack2", 0.65)
F("up", 0.0, "splash", 0.4*0.6)
F("truck", 0.1, "doorslam", 0.8); F("truck", 0.6, "bark", 0.5); F("truck", 2.2, "rumble", 0.5); F("truck", 3.25, "rumble", 0.45)
F("rope", 0.1, "splash", 0.4*0.6); F("rope", 0.6, "rumble", 0.45); F("rope", 0.9, "buffalo", 0.6)
F("strike", 0.15, "zap", 0.3)                       # long cut: the build (hair lifting) before the bolt
F("strike", 0.97, "crack", 1.1); F("strike", 1.29, "crack2", 0.45); F("strike", 1.5, "fall", 0.9); F("strike", 1.75, "buffalo", 0.5)   # + the re-stroke
F("strike", 1.8, "zap", 0.3); F("strike", 2.8, "splash", 0.4*0.4)   # the crown sizzling (close) · ลุง in the mud (close)   # the bolt moved 0.75 s later (long cut)
F("taken", 0.3, "rumble", 0.5)
# ================= the bridge =================
F("xwait", 0.3, "splash", 0.4*0.5); F("xwait", 1.6, "rumble", 0.45)
F("xnow", 0.2, "rumble", 0.55)                      # the soft far flicker at 0.2 s
F("xchap", 0.3, "plankdrop", 0.62)                   # the title sign staked in the paddy
# ================= EP.2 (fear → end) =================
F("rap", 0.3, "splash", 0.4*0.6); F("rap", 0.6, "plankdrop", 0.8)
F("phone", 0.3, "phonedial", 0.8)
F("speak", 1.2, "thump", 0.5); F("hands", 0.2, "thump", 0.5); F("hands", 3.0, "thump", 0.5); F("rate", 0.1, "thump", 0.55); F("rate", 2.9, "thump", 0.55)
F("count", 0.0, "thump", 0.45); F("only", 0.1, "thump", 0.5); F("only", 3.0, "thump", 0.5); F("swap", 0.3, "thump", 0.5)
F("drag", 0.4, "rumble", 0.6)
F("gasp", 0.4, "gasp", 1.0)
F("clear", 0.0, "siren", 0.6)
F("e2_buff", 0.1, "splash", 0.4*0.5); F("e2_buff", 0.8, "buffalo", 0.5)
F("far", 0.6, "rumble", 0.35)
F("watch", 0.3, "stopwatch", 0.9)
F("rule3", 0.3, "plankdrop", 0.9); F("rule3", m.vo_end("rule3") - 0.25, "bambootick", 0.8)
F("again", 0.22, "crack", 1.1); F("again", 0.45, "fall", 0.7)
F("grand", 4.22, "crack2", 0.6)                     # long cut: the flashback's bolt (sepia, 30 years ago)
F("end", 0.3, "plankdrop", 0.7); F("end", 2.0, "bambootick", 0.7); F("end", 2.3, "bambootick", 0.7)
# ================= music: all dips first, then the boosts =================
m.dip(T("cmd") - 0.1, T("cmd", 0.15), 0.15)
m.dip(T("leg1"), T("leg2", -0.01), 0.7)
m.dip(T("strike") - 0.3, T("strike", 0.9), 0.25)     # the held breath runs through the build
m.dip(T("none"), T("xnow", -0.01), 0.55)            # EP.1's held breath carries through the bridge until "ลุงรอไม่ได้แล้ว" is over
m.dip(T("still"), T("still", -0.01), 0.4)
m.dip(T("gasp"), T("gasp", 0.8), 0.2)
m.dip(T("clear"), T("far", -0.01), 0.55)
m.dip(T("again") - 0.3, T("again", 0.15), 0.25)
m.dip(T("photo"), T("truth", -0.01), 0.5)
m.boost(T("hook"), T("cmd", 0.1), 1.6)
m.boost(T("strike", 1.05), T("taken", -0.01), 1.2)   # 1.6 in the shorts; the full story has only three long voice-free stretches, so the swell after each strike sat ~5 LU over ทะเลลด
m.boost(T("xchap"), T("xchap", -0.01), 1.4)        # the chapter card
m.boost(T("hands"), T("count", -0.01), 1.3)
m.boost(T("again", 0.3), T("alive", -0.01), 1.2)
m.mus_db = -30; m.duck_depth = 0.65; m.mus_lp = False; m.mus_af = None
# suno1 (133.6 s) is shorter than the story: it plays from 0 s for EP.1 and the bridge, fades over 0.6 s into the chapter card,
# and starts again from 0 s on the card for EP.2 (as video/tornado/full/mix.py restarts the theme for its ending)
import numpy as np
_load = m.load
def _music(path):
    x = _load(path)
    if not path.endswith("takhian-theme.mp3"): return x
    sr = 48000; c = int(T("xchap") * sr); f = int(0.6 * sr)
    a = x[:c].copy(); a[-f:] *= np.linspace(1, 0, f, dtype=np.float32)
    b = x.copy(); b[: int(0.05 * sr)] *= np.linspace(0, 1, int(0.05 * sr), dtype=np.float32)
    out = np.concatenate([a, b]); assert len(out) >= m.N + int(7.5 * sr), (len(out) / sr, m.N / sr)
    return out
m.load = _music
m.finish(music_offset=0.0, fade_from=T("end", -2.5))   # the theme fades under the last 2.5 s of the end card (the story ends, no follow card)
