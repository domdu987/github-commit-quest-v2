"""ต้นตะเคียนกลางนา EP.2 soundtrack (times follow schedule.json and ep2/body.part)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "lib"))
from mixcore import Mix
m = Mix(HERE)
m.voices({"t05": 1})
F = m.fx
PER = 60 / 110
F("hook", 0.2, "rumble", 0.6)
F("cmd", 0.0, "flinch", 0.4)
F("rap", 0.3, "splash", 0.4*0.6); F("rap", 0.6, "plankdrop", 0.8)
F("phone", 0.3, "phonedial", 0.8)
F("speak", 1.2, "thump", 0.5); F("hands", 0.2, "thump", 0.5); F("hands", 3.0, "thump", 0.5); F("rate", 0.1, "thump", 0.55); F("rate", 2.9, "thump", 0.55)
F("count", 0.0, "thump", 0.45); F("only", 0.1, "thump", 0.5); F("only", 3.0, "thump", 0.5); F("swap", 0.3, "thump", 0.5)
F("drag", 0.4, "rumble", 0.6)
F("gasp", 0.4, "gasp", 1.0)
F("clear", 0.0, "siren", 0.6)
F("buff", 0.1, "splash", 0.4*0.5); F("buff", 0.8, "buffalo", 0.5)
F("far", 0.6, "rumble", 0.35)
F("watch", 0.3, "stopwatch", 0.9)
F("rule3", 0.3, "plankdrop", 0.9); F("rule3", m.vo_end("rule3") - 0.25, "bambootick", 0.8)
F("again", 0.22, "crack", 1.1); F("again", 0.45, "fall", 0.7)
F("scars", 0.2, "cloth", 0.0)
F("end", 0.3, "plankdrop", 0.7); F("end", 2.0, "bambootick", 0.7); F("end", 2.3, "bambootick", 0.7)
m.dip(m.T("still"), m.T("still", -0.01), 0.4)
m.boost(m.T("hands"), m.T("count", -0.01), 1.3)
m.dip(m.T("gasp"), m.T("gasp", 0.8), 0.2)
m.dip(m.T("clear"), m.T("far", -0.01), 0.55)
m.dip(m.T("again") - 0.3, m.T("again", 0.15), 0.25)
m.boost(m.T("again", 0.3), m.T("alive", -0.01), 1.6)
m.dip(m.T("photo"), m.T("truth", -0.01), 0.5)
# music = ทะเลลด recipe (owner 2 พ.ย. ~21:00: "เอาซาวเพลงแบบทะเลลด ใช้ทุกคลิปเลย"): suno1 from 0 s, unfiltered, -30 dB RMS, duck 0.65
m.mus_db = -30; m.duck_depth = 0.65; m.mus_lp = False; m.mus_af = None
m.finish(music_offset=0.0, fade_from=m.T("end", -0.5))
