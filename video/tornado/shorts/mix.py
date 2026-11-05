"""เสียงรถไฟ Shorts soundtrack: python3 combine.py, then MIXOUT=<work dir> python3 mix.py s1|s2  → mix.wav, vo_stem.wav,
music_stem.wav there. Times follow sN/schedule.json; the cues are the full story's (../full/mix.py), so a short sounds like the long.
  s1 (EP.1): the full story's EP.1 cues verbatim (read from ../full/mix.py), plus the shorts-only sounds of ../ep1/mix.py: the steel
      clank of the follow tag (0:10) and the end card. suno1 from 0 (ทะเลลด recipe), silent through the black after the choice,
      then back soft under the end card.
  s2 (EP.2): the ride and the choice as in the full story (suno1 where it stood at the truck), then the ending's first half: the roar
      under the overpass, into the ditch, peaking as it passes over; a hard cut to black and silence on that peak (the cliffhanger),
      then the same end card with only its own sounds."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "lib"))
from mixcore import Mix, SR

name = sys.argv[1] if len(sys.argv) > 1 else "s1"
assert name in ("s1", "s2"), "python3 mix.py s1|s2"
m = Mix(os.path.join(HERE, name), os.environ.get("MIXOUT"), vo_dirs=[os.path.join(HERE, "..", "ep1", "vo"), os.path.join(HERE, "..", "ep2", "vo")])
m.voices()
F, T = m.fx, m.T


def end_card():   # as ../ep1/mix.py: a far rumble on the cut in, the plate's clank on n19's "กดติดตาม"
    F("end", 0.1, "rumble", 0.6); F("end", 0.45 + 1.32 - 0.12 + 0.145, "signclank", 0.9)


if name == "s1":
    src = open(os.path.join(HERE, "..", "full", "mix.py")).read()
    exec(src[src.index("# ================= EP.1"): src.index("# ================= the ending")], {"m": m, "F": F, "T": T})
    F("stall", 0.38, "signclank", 0.8)   # the follow tag drops in at 0:10 (shorts only)
    end_card()
    # the black after the choice stays silent (a hole); the theme then comes back soft under the end card from where it stopped
    m.dip(T("end", 0.0), m.TOTAL, 0.7)
    # the ditch set-up moved suno1 6.9 s against the picture: its quiet bars now fall on the roof and the bathroom, so lift them.
    # After every dip: Mix.dip clamps the whole gain to <= 1, so a boost made before any dip is lost (as in the long's EP.1 part)
    m.boost(T("run", 0.0), T("house", 1.0), 1.4)
    cut, card = T("choice", -0.12), T("end", 0.1)
    m.finish(holes=[(T("hit") - 0.4, T("hit")), (cut, card)], segments=[(0.0, cut, 0.0), (card, m.TOTAL, cut)], fade=(m.TOTAL - 2.0, m.TOTAL))
else:
    OFF = m.SC["from_full"]["truck"]   # where suno1 stood at the truck in the full story
    # the ride and the choice (the full story's EP.1 part)
    m.roar(T("truck", 0.0), T("choice", -0.1), 1.0, fade=0.3)
    F("truck", 0.05, "pickup", 0.6); F("truck", 1.6, "debris", 0.5); F("truck", 3.6, "debris", 0.4)
    m.roar_level(T("choice", 0.0), T("choice", -0.1), 0.6, 0.3)
    F("choice", 0.25, "zincflap", 0.7); F("choice", 4.8 - 1.6, "signclank", 0.8)
    # under the overpass and into the ditch (the full story's ending)
    m.roar(T("xunder", 0.0), T("end", 0.1), 1.0, fade=0.1)   # in at once; full level up to the cut
    F("xunder", 0.2, "doorslam", 0.6); F("xunder", 1.6, "debris", 0.45)
    m.roar_level(T("xwind", 0.0), T("xwind", -0.1), 1.3, 0.2)
    F("xwind", 0.6, "debris", 0.5)
    F("xrule3", 0.25, "zincflap", 0.8)
    F("xpull", 0.2, "thump", 0.85); F("xpull", 0.5, "debris", 0.5); F("xpull", 2.8, "thump", 0.6)
    m.roar_level(T("xknow3", 0.0), T("xknow3", -0.1), 0.45, 0.3)
    F("xknow3", 0.45, "signclank", 0.6)
    F("xflat", 0.4, "debris", 0.6); F("xflat", 2.2, "debris", 0.5)
    m.roar_level(T("xpass", 0.0), T("end", 0.0), 1.45, 0.2)
    F("xpass", 0.15, "boom", 0.9); F("xpass", 0.4, "roofrip", 0.8); F("xpass", 0.9, "debris", 0.8); F("xpass", 1.9, "debris", 0.6)
    m.dip(T("xpass", 0.0), T("end", 0.0), 0.75)   # the roar is the climax here; the theme sits under it (musiccheck: between lines)
    c = int(T("end", 0.0) * SR); m.sfx[c:] = 0; m.amb[c:] = 0   # the cliffhanger: no debris tail or roar leaks into the card
    end_card()
    m.finish(cut=T("end", 0.0), card=T("end", 0.1),
             segments=[(0.0, T("choice", -0.12), OFF), (T("xunder", 0.0), T("end", 0.0), 0.0)])
