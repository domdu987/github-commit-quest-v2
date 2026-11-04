"""เสียงรถไฟ ฉบับเต็ม (YouTube 16:9) soundtrack. Times follow full/schedule.json (python3 combine.py) and stylekit/f1/body.part.
Run: MIXOUT=<work dir> python3 mix.py  → mix.wav, vo_stem.wav, music_stem.wav there (default: this folder).
EP.1's cues as in ../ep1/mix.py, without its shorts-only sounds (the 0:10 follow tag, the end card). suno1 plays from 0 for EP.1,
stops with the black after the choice, and starts again from 0 for the ending; it fades out under the final card.
The ending: the roar under the overpass and into the ditch (peaking as it passes over), muffled in the house, then gone at
"เสียงรถไฟก็หยุด"; the window bursting in; the downed line's crackle on every spark in the picture."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "lib"))
from mixcore import Mix
m = Mix(HERE, os.environ.get("MIXOUT"), vo_dirs=[os.path.join(HERE, "..", "ep1", "vo"), os.path.join(HERE, "..", "ep2", "vo")])
m.voices()
F, T = m.fx, m.T
# ================= EP.1 (as ../ep1/mix.py) =================
m.roar(0.0, T("clock", 0.2), 0.8, fade=0.5)
F("open", 0.8, "debris", 0.35)
F("hook", m.vo_t("hook") - 0.02, "thump", 0.9)
F("clock", 0.1, "stopwatch", 0.7)
F("pu", 3.0, "shutter", 0.45)
F("cloud", 1.5, "rumble", 0.6)
F("tale", 2.3, "rumble", 0.4)
F("dark", 0.05, "stopwatch", 0.6)
F("dark", m.frag("dark", 0, 1) + 0.1, "rumble", 0.6)
m.roar(T("roar", m.frag("roar", 0, 1) - 0.35), T("count", 0.3), 1.0, fade=1.0)
m.roar(T("truck", 0.0), T("choice", -0.1), 1.0, fade=0.3)
F("know1", m.frag("know1") + 0.05, "rumble", 0.9)
m.roar_level(T("know1", 0.1), T("know1", m.frag("know1", 0, 1) - 0.2), 0.3, 0.3)
F("touch", 1.0, "boom", 1.0); F("touch", 1.3, "debris", 0.45)
m.roar_level(T("touch", 1.0), T("lure", -0.5), 1.25, 0.4)
F("rule", 0.75, "zincflap", 0.9)
m.roar_level(T("know2", 0.2), T("know2", -0.3), 0.6, 0.4)
F("know2", m.vo_t("know2", 1) + 0.1, "rumble", 0.5)
F("pickup", 1.2, "doorslam", 0.8); F("pickup", 1.55, "pickup", 0.65)
F("run", 1.2, "debris", 0.6); F("run", 2.6, "debris", 0.5)
F("hit", 0.05, "boom", 0.8); F("hit", 0.15, "roofrip", 1.0); F("hit", 0.9, "debris", 0.6)
F("hit", 1.0, "zap", 0.5); F("hit", 2.0, "zap", 0.45); F("hit", 2.2, "crack", 0.9)
m.roar_level(T("hit", 0.0), T("house", 0.2), 1.3, 0.15)
F("house", 0.3, "windowrattle", 0.7); F("house", 1.4, "crack2", 0.8); F("house", 2.2, "windowrattle", 0.55)
F("house", -0.35, "bathdoor", 0.9)
m.roar(T("count", 0.0), T("truck", 0.1), 0.75, lp=320, fade=0.3)
beat = 0.75
for i in range(int((T("truck", 0.0) - T("count", m.vo_t("count", 1))) / beat)):
    m.fx(None, T("count", m.vo_t("count", 1)) + i * beat, "heart", 0.8)
F("where", 0.05, "gasp", 0.45)
F("truck", 0.05, "pickup", 0.6); F("truck", 1.6, "debris", 0.5); F("truck", 3.6, "debris", 0.4)
m.roar_level(T("choice", 0.0), T("choice", -0.1), 0.6, 0.3)
F("choice", 0.25, "zincflap", 0.7); F("choice", 4.8 - 1.6, "signclank", 0.8)
m.dip(T("dark", 0.0), T("roar", m.frag("roar", 0, 1)), 0.5)
m.boost(T("touch", 0.9), T("lure", 0.5), 1.35)
m.boost(T("hit", 0.0), T("house", 0.3), 1.3)
m.dip(T("count", 0.0), T("gone", -0.01), 0.55)
# ================= the ending =================
# under the overpass and into the ditch: the roar back at once, louder in the gap, peaking as it passes over
m.roar(T("xunder", 0.0), T("xwin", 0.1), 1.0, fade=0.25)
F("xunder", 0.2, "doorslam", 0.6); F("xunder", 1.6, "debris", 0.45)
m.roar_level(T("xwind", 0.0), T("xwind", -0.1), 1.3, 0.2)
F("xwind", 0.6, "debris", 0.5)
F("xrule3", 0.25, "zincflap", 0.8)
F("xpull", 0.2, "thump", 0.85); F("xpull", 0.5, "debris", 0.5); F("xpull", 2.8, "thump", 0.6)   # ปู's hand clamps ตาเทียน's wrist (the insert)
m.roar_level(T("xknow3", 0.0), T("xknow3", -0.1), 0.45, 0.3)       # the card: the roar held low under the explanation
F("xknow3", 0.45, "signclank", 0.6)                                   # the zinc board lands on its ropes
F("xflat", 0.4, "debris", 0.6); F("xflat", 2.2, "debris", 0.5)
m.roar_level(T("xpass", 0.0), T("xpass", -0.05), 1.45, 0.2)
F("xpass", 0.15, "boom", 0.9); F("xpass", 0.4, "roofrip", 0.8); F("xpass", 0.9, "debris", 0.8); F("xpass", 1.9, "debris", 0.6)
# the house: the roar muffled through the walls, the window bursts in, then the bathroom
m.roar(T("xwin", 0.0), T("xquiet", 0.25), 0.8, lp=420, fade=0.35)
F("xwin", 0.4, "windowrattle", 0.6); F("xwin", m.vo_t("xwin", 1), "glassburst", 1.0)
# the roar stops ("แล้ว… เสียงรถไฟก็หยุด"): nothing but the voice and the theme
# aftermath, the twist: the line crackles on every spark the picture shows
for k in ("xafter",):
    for i in range(int(2.6 / 0.9)): F(k, 0.3 + i * 0.9, "zap", 0.18)
for i in range(int((m.SH["xcam"]["dur"] - 0.2) / 0.8)): F("xcam", 0.2 + i * 0.8, "zap", 0.28)
for i in range(int(2.2 / 0.7)): F("xstop", i * 0.7, "zap", 0.3)
c = m.SH["xstop"]["vo"][1]["t"] - 0.15
for i in range(int(3.2 / 0.6)): F("xstop", c + i * 0.6, "zap", 0.45)
F("xknow4", 0.45, "signclank", 0.6); v = m.SH["xknow4"]["vo"]; F("xknow4", v[0]["t"] + 0.35, "thump", 0.7)
for i in range(int((m.SH["xknow4"]["dur"] - v[0]["t"] - 0.6) / 0.8)): F("xknow4", v[0]["t"] + 0.6 + i * 0.8, "zap", 0.2)
F("xrule4", 0.1, "zincflap", 0.7)
F("xend", 0.25, "zincflap", 0.6); F("xend", 0.45, "thump", 0.4)
# music: the chapter break, the storm overhead, the calm after, the bookend
m.boost(T("xpass", 0.0), T("xwin", 0.2), 1.35)
m.dip(T("xquiet", 0.0), T("xafter", 0.4), 0.6)
m.boost(T("xfin", 0.0), T("xend", 0.0), 1.2)
m.finish(holes=[(T("hit") - 0.4, T("hit"))], segments=[(0.0, T("choice", -0.12), 0.0), (T("xunder", 0.0), m.TOTAL, 0.0)],
         fade=(m.TOTAL - 3.0, m.TOTAL))   # the theme stays under the end screen and fades over its last 3 s
