#!/usr/bin/env python3
"""timing.py -- every shot boundary and acting beat of the hook as a function of the Thai timing file.

    import timing; T = timing.load()            # reads audio/th/hook_timing.json
    T["N"]            number of output frames (30 fps): max(5.0 s, speech_end + 0.4 s) rounded to whole frames
    T["g2"]           the framing change insert -> low-angle medium is centred here: first beat-2 phrase minus LEAD frames
    T["g3"]           first frame of shot 3 (the cut inside the whip pan): first beat-3 phrase minus LEAD frames
    T["g_jab"]        the jab at New York lands on this frame: first frame inside the phrase that names New York
    T["g_touch"]      the eraser touches the map: start of the phrase that says "erased" (the beat-3 phrase before the last
                      one; the last phrase itself when beat 3 has fewer than three phrases)
    T["g_last"]       first frame of the last phrase (the hero's shock and the bulk of the rubbing happen under it)
    T["g_done"]       last rubbing stroke ends: the frame after the end of speech
All frame numbers are 0-based OUTPUT frames g (time = g / 30); the Blender frame of g is g + 1.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
TIMING_JSON = os.path.join(PROJ, "audio", "th", "hook_timing.json")
FPS = 30
LEAD = 3                      # frames by which the picture leads the word at a shot change (reference: 2 to 4)
NY_WORDS = ("นิวยอร์ก", "New York")
ERASE_WORDS = ("ลบ", "erase")


def load(path=TIMING_JSON):
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    ph = d["phrases"]
    beat = lambda b: [p for p in ph if p["beat"] == b]
    b1, b2, b3 = beat(1), beat(2), beat(3)
    fr = lambda t: int(round(t * FPS))
    N = int(round(max(5.0, float(d["speech_end"]) + 0.4) * FPS))
    g2 = fr(b2[0]["t0"]) - LEAD
    g3 = fr(b3[0]["t0"]) - LEAD
    ny = [p for p in b2 if any(w in p["text"] for w in NY_WORDS)] or [b2[-1]]
    g_jab = int(math.ceil(ny[0]["t0"] * FPS - 1e-6))
    er = [p for p in b3 if any(w in p["text"] for w in ERASE_WORDS)]
    touch_p = er[0] if er else (b3[-2] if len(b3) >= 3 else b3[-1])
    g_touch = fr(touch_p["t0"])
    g_last = fr(ph[-1]["t0"])
    g_done = min(N - 16, fr(d["speech_end"]) + 1)
    T = dict(N=N, fps=FPS, lead=LEAD, g2=g2, g3=g3, g_jab=g_jab, g_touch=g_touch, g_last=g_last, g_done=g_done,
             provisional=bool(d.get("provisional", False)), audio=d.get("audio"), audio_offset=float(d.get("audio_offset") or 0.0),
             speech_end=float(d["speech_end"]), caption_style_prefix=d.get("caption_style_prefix", ""), phrases=ph,
             path=path, mtime=os.path.getmtime(path))
    # sanity: the beats must come in order and leave room for the acting
    assert 20 <= g2 < g_jab - 12 < g3 - 16, ("timing leaves no room for shot 2", T)
    assert g3 + 12 <= g_touch < g_done - 12 and g_done <= N - 10, ("timing leaves no room for shot 3", T)
    return T


if __name__ == "__main__":
    T = load()
    for k in ("N", "g2", "g3", "g_jab", "g_touch", "g_last", "g_done", "provisional", "audio", "audio_offset", "speech_end"):
        print("%-12s %s" % (k, T[k]))
    for p in T["phrases"]:
        print("  beat %d  %.3f-%.3f  g %5.1f-%5.1f  %s" % (p["beat"], p["t0"], p["t1"], p["t0"] * FPS, p["t1"] * FPS, p["text"]))
