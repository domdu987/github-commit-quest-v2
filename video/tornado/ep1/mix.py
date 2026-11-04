"""เสียงรถไฟ EP.1 soundtrack. Times follow schedule.json and the shot code in video/tornado/stylekit/e1/body.part.
Run: MIXOUT=<episode work dir> python3 mix.py  (writes mix.wav, vo_stem.wav, music_stem.wav there; default: this folder).
- the roar (the title's freight train) is heard in the hook, then from "ก็มา" until the black after the choice;
  "ฟ้าร้องจะดังแล้วเงียบ" plays a thunder that dies while the roar is held low, "แต่เสียงนี้ ไม่หยุด" brings the roar back up
- a held breath (0.4 s of silence) before the first roof goes; inside the bathroom the roar is muffled and a heart beats
- material SFX: zinc for the rule sign and the choice boards, a steel clank for the follow tag (0:10) and the end-card plate
- music: suno1 by the ทะเลลด recipe (A5); it stops with the black after the choice, the end card has only its own sounds."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "lib"))
from mixcore import Mix
m = Mix(HERE, os.environ.get("MIXOUT"))
m.voices()
F, T = m.fx, m.T
# ---- the hook: the roar under the title, the red box, the plain with no railway
m.roar(0.0, T("clock", 0.2), 0.8, fade=0.5)
F("open", 0.8, "debris", 0.35)
F("hook", m.vo_t("hook") - 0.02, "thump", 0.9)
# ---- one hour earlier: the clock, the follow tag, the bright stall
F("clock", 0.1, "stopwatch", 0.7)
F("stall", 0.38, "signclank", 0.8)
F("pu", 3.0, "shutter", 0.45)
F("cloud", 1.5, "rumble", 0.6)
F("tale", 2.3, "rumble", 0.4)
F("dark", 0.05, "stopwatch", 0.6)
F("dark", m.frag("dark", 0, 1) + 0.1, "rumble", 0.6)
# ---- the roar comes and does not stop
m.roar(T("roar", m.frag("roar", 0, 1) - 0.35), T("count", 0.3), 1.0, fade=1.0)   # outside: from "ก็มา" until the bathroom door shuts
m.roar(T("truck", 0.0), T("choice", -0.1), 1.0, fade=0.3)                     # outside again with ตาเทียน and ปู in the pickup
F("know1", m.frag("know1") + 0.05, "rumble", 0.9)                                   # "ฟ้าร้องจะดังแล้วเงียบ": thunder that dies…
m.roar_level(T("know1", 0.1), T("know1", m.frag("know1", 0, 1) - 0.2), 0.3, 0.3)     # …while the roar is held low
F("touch", 1.0, "boom", 1.0); F("touch", 1.3, "debris", 0.45)
m.roar_level(T("touch", 1.0), T("lure", -0.5), 1.25, 0.4)
F("rule", 0.75, "zincflap", 0.9)
m.roar_level(T("know2", 0.2), T("know2", -0.3), 0.6, 0.4)
F("know2", m.vo_t("know2", 1) + 0.1, "rumble", 0.5)
F("pickup", 1.2, "doorslam", 0.8); F("pickup", 1.55, "pickup", 0.65)
F("run", 1.2, "debris", 0.6); F("run", 2.6, "debris", 0.5)
# ---- the first roof: a held breath, then the rip
F("hit", 0.05, "boom", 0.8); F("hit", 0.15, "roofrip", 1.0); F("hit", 0.9, "debris", 0.6)
F("hit", 1.0, "zap", 0.5); F("hit", 2.0, "zap", 0.45); F("hit", 2.2, "crack", 0.9)   # the power flashes and the sky flash in the picture
m.roar_level(T("hit", 0.0), T("house", 0.2), 1.3, 0.15)
F("house", 0.3, "windowrattle", 0.7); F("house", 1.4, "crack2", 0.8); F("house", 2.2, "windowrattle", 0.55)
F("house", -0.35, "bathdoor", 0.9)
# ---- inside the bathroom: the roar muffled, the count, the heart
m.roar(T("count", 0.0), T("truck", 0.1), 0.75, lp=320, fade=0.3)   # inside the bathroom: the roar muffled by the walls
beat = 0.75
for i in range(int((T("truck", 0.0) - T("count", m.vo_t("count", 1))) / beat)):
    m.fx(None, T("count", m.vo_t("count", 1)) + i * beat, "heart", 0.8)
F("where", 0.05, "gasp", 0.45)
# ---- the pickup racing for the overpass, the choice, the black
F("truck", 0.05, "pickup", 0.6); F("truck", 1.6, "debris", 0.5); F("truck", 3.6, "debris", 0.4)
m.roar_level(T("choice", 0.0), T("choice", -0.1), 0.6, 0.3)
F("choice", 0.25, "zincflap", 0.7); F("choice", 4.8 - 1.6, "signclank", 0.8)
# ---- the end card: only its own sounds
F("end", 0.1, "rumble", 0.6); F("end", 0.45 + 1.32 - 0.12 + 0.145, "signclank", 0.9)
# ---- music: dread before the roar, a lift at the touchdown and the roof, held low in the bathroom
m.dip(T("dark", 0.0), T("roar", m.frag("roar", 0, 1)), 0.5)
m.boost(T("touch", 0.9), T("lure", 0.5), 1.35)
m.boost(T("hit", 0.0), T("house", 0.3), 1.3)
m.dip(T("count", 0.0), T("gone", -0.01), 0.55)
m.finish(cut=T("choice", -0.12), card=T("end", 0.1), holes=[(T("hit") - 0.4, T("hit"))])
