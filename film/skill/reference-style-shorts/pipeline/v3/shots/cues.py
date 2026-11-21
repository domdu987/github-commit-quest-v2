#!/usr/bin/env python3
"""cues.py -- sound cue sheet for the 5 s: every event that should make a sound, in OUTPUT-clip seconds.

    python3 cues.py <out.json>

All times are functions of the Thai timing file (through film.py), 30 fps, t = g / 30 (start of frame g).
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def main(argv):
    import film, qa_motion
    mo = qa_motion.main([])
    sp = dict((r["g"], r["speed"]) for r in mo["rows"])
    t = lambda g: round(g / 30.0, 3)
    ev = []

    def add(g0, g1, label, kind, **kw):
        e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label)
        e.update(kw)
        ev.append(e)

    def peak(a, b):
        return max(range(a, b + 1), key=lambda g: sp[g])

    F = film
    # ---- shot 1: insert
    add(0, F.G_LAND, "arm with the red pencil swings in from the lower left (whoosh, light)", "prop_move")
    add(F.G_LAND, F.G_LAND, "pencil point touches the map on the storm symbol off Florida (soft tick)", "pencil_touch", impact_frame=F.G_LAND)
    a, b = F.G_LAND, F.PULL[0] + 3
    add(a, b, "pencil draws the red track north, one continuous stroke (line 0 to 0.75); scratch of pencil on paper", "pencil_draw", line=[0.0, 0.75])
    p = peak(F.SNAP1[0], F.SNAP1[1])
    add(F.SNAP1[0], F.SNAP1[1], "snap push onto the pencil point (camera whoosh in)", "camera_snap", peak_time=t(p), peak_frame=p, peak_px_per_frame=round(sp[p], 1))
    # ---- framing change into shot 2
    p = peak(F.PULL[0], F.PULL[1])
    add(F.PULL[0], F.PULL[1], "snap pull-out and swing round the hero: insert becomes the low-angle medium (big whoosh out)", "camera_snap",
        peak_time=t(p), peak_frame=p, peak_px_per_frame=round(sp[p], 1))
    add(b, F.GATHER[0], "pencil keeps drawing, slowing (line 0.75 to 0.92)", "pencil_draw", line=[0.75, 0.92])
    add(F.GATHER[0], F.GATHER[1], "he draws back before the jab (pencil lifts a hair, tiny cloth rustle)", "anticipation")
    add(F.GATHER[1], F.G_JAB, "decisive jab stroke to New York (line 0.92 to 1.0), fast scratch", "pencil_draw", line=[0.92, 1.0])
    add(F.G_JAB, F.G_JAB, "JAB lands on New York: pencil point hits the map, arrow head complete (hard tap / thock)", "jab_impact", impact_frame=F.G_JAB)
    p = peak(F.SNAP2[0], F.SNAP2[1])
    add(F.SNAP2[0], F.SNAP2[1], "snap reframing on the jab (short whoosh in)", "camera_snap", peak_time=t(p), peak_frame=p, peak_px_per_frame=round(sp[p], 1))
    add(F.TURN[0], F.TURN[1], "hero turns his head to the viewer, pencil comes away from the map", "prop_move")
    # ---- whip into shot 3
    p = peak(F.WHIP_OFF[0], F.WHIP_ON[1])
    add(F.WHIP_OFF[0], F.WHIP_ON[1] + 1, "WHIP PAN to the right, cut inside it at %.3f s, the two-shot arrives braking" % t(F.G3), "whip_pan",
        peak_time=t(p), peak_frame=p, peak_px_per_frame=round(sp[p], 1), cut_time=t(F.G3), cut_frame=F.G3)
    add(F.G3, F.G_TOUCH - 4, "the chief steps up to the map with the eraser raised (two soft footfalls on wood)", "prop_move")
    add(F.G_TOUCH, F.G_TOUCH, "eraser touches the map at the New York end of the track (felt pad thump)", "eraser_touch", impact_frame=F.G_TOUCH)
    k, g = 0, F.G_TOUCH
    while g < F.G_DONE:
        g1 = min(F.G_DONE, g + F.STROKE)
        add(g, g1, "eraser rubbing stroke %d (one back-and-forth scrub; erased %.0f to %.0f percent)" % (k + 1, 100 * F.erase_at(g), 100 * F.erase_at(g1)),
            "eraser_rub", erase=[round(F.erase_at(g), 3), round(F.erase_at(g1), 3)])
        g = g1; k += 1
    add(F.SHOCK - 1, F.SHOCK + 1, "hero blinks (3 frames)", "blink")
    add(F.SHOCK, F.SHOCK + 6, "hero goes WIDE-EYED: face swaps to shock on the closed frame, sweat drop pops, small flinch (gasp / sting)", "hero_shock", impact_frame=F.SHOCK)
    p = peak(F.SNAP3[0], F.SNAP3[1])
    add(F.SNAP3[0], F.SNAP3[1], "snap push onto the hero's face (whoosh in)", "camera_snap", peak_time=t(p), peak_frame=p, peak_px_per_frame=round(sp[p], 1))
    add(F.G_DONE, F.G_DONE + 9, "last stroke done: the chief takes the eraser away, straightens and looks over, smug", "prop_move")
    ev.sort(key=lambda e: (e["time"], e["kind"]))
    T = F.T
    out = dict(fps=30, frames=F.N, duration=round(F.N / 30.0, 3), time_base="seconds from the first frame of proto_v3.mp4; frame g starts at g / 30",
               timing_file=T["path"], timing_provisional=T["provisional"],
               narration=dict(file=T["audio"], starts_at=T["audio_offset"], speech_end=T["speech_end"]),
               shots=[dict(shot=1, start=0.0, end=t(F.G2), frames=[0, F.G2 - 1], what="insert: red pencil draws the track on the wall map (raking low angle, camera 1.4 to 1.8 D)",
                           transition_out="continuous snap pull-out g %d-%d, centred on g %d (no cut)" % (F.PULL[0], F.PULL[1], F.G2)),
                      dict(shot=2, start=t(F.G2), end=t(F.G3), frames=[F.G2, F.G3 - 1], what="low-angle medium: hero finishes the track with a jab at New York, turns to the viewer",
                           transition_out="whip pan right, hard cut at frame %d" % F.G3),
                      dict(shot=3, start=t(F.G3), end=round(F.N / 30.0, 3), frames=[F.G3, F.N - 1], what="high-angle two-shot in depth: the chief rubs the track out, the hero goes wide-eyed")],
               captions=[dict(time=p["t0"], end=p["t1"], text=p["text"], beat=p["beat"]) for p in T["phrases"]],
               events=ev)
    if argv:
        json.dump(out, open(argv[0], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for e in ev:
        print("%6.3f s  +%.3f  %-13s %s" % (e["time"], e["duration"], e["kind"], e["label"]))
    return out


if __name__ == "__main__":
    main(sys.argv[1:])
