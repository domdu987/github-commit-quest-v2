#!/usr/bin/env python3
"""qa_report.py -- collect the measured numbers into markdown tables (printed; QA.md is assembled from them).

    python3 qa_report.py <raw_dir with meta/> <tmp_dir with motion.json, light/, parallax_*.json, score/>
"""
import glob, json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def rng(v, fmt="%.0f"):
    v = list(v)
    return (fmt + " to " + fmt) % (min(v), max(v)) if v else "-"


def main(argv):
    raw, tmp = argv[0], argv[1]
    import film as F
    meta = {}
    for p in sorted(glob.glob(os.path.join(raw, "meta", "g_*.json"))):
        m = json.load(open(p)); meta[m["g"]] = m
    N = F.N
    out = []
    P = out.append
    # ---------------- timing
    T = F.T
    P("### Timing (from %s, provisional = %s)\n" % (os.path.relpath(T["path"], os.path.join(HERE, "..", "..")), T["provisional"]))
    P("| Item | Output frame g | Time s | Rule |\n|---|---|---|---|")
    P("| Clip length | %d frames | %.3f | max(5.0, speech_end %.3f + 0.4) |" % (N, N / 30.0, T["speech_end"]))
    b2 = [p for p in T["phrases"] if p["beat"] == 2][0]; b3 = [p for p in T["phrases"] if p["beat"] == 3][0]
    P("| Shot 2 (framing change centred on) | %d (pull-out g %d-%d) | %.3f | first beat-2 phrase \"%s\" at %.3f s, picture leads by %.1f frames |" % (F.G2, F.PULL[0], F.PULL[1], F.G2 / 30.0, b2["text"], b2["t0"], b2["t0"] * 30 - F.G2))
    P("| Shot 3 (cut inside the whip) | %d | %.3f | first beat-3 phrase \"%s\" at %.3f s, picture leads by %.1f frames |" % (F.G3, F.G3 / 30.0, b3["text"], b3["t0"], b3["t0"] * 30 - F.G3))
    ny = [p for p in T["phrases"] if "นิวยอร์ก" in p["text"]][0]
    P("| Jab lands on New York | %d | %.3f | phrase \"%s\" %.3f-%.3f s |" % (F.G_JAB, F.G_JAB / 30.0, ny["text"], ny["t0"], ny["t1"]))
    P("| Eraser touches the map | %d | %.3f | phrase \"%s\" starts %.3f s |" % (F.G_TOUCH, F.G_TOUCH / 30.0, [p for p in T["phrases"] if "ลบ" in p["text"]][0]["text"], [p for p in T["phrases"] if "ลบ" in p["text"]][0]["t0"]))
    last = T["phrases"][-1]
    P("| Rubbing, erase 0 -> 0.60 -> 1.0 | %d -> %d -> %d | %.3f -> %.3f -> %.3f | last phrase \"%s\" %.3f-%.3f s: erase %.2f to 1.0 under it |" % (
        F.G_TOUCH, F.G_LAST, F.G_DONE, F.G_TOUCH / 30.0, F.G_LAST / 30.0, F.G_DONE / 30.0, last["text"], last["t0"], last["t1"], F.erase_at(F.G_LAST)))
    P("| Hero wide-eyed (closed frame of the blink) | %d | %.3f | start of the last phrase |\n" % (F.SHOCK, F.SHOCK / 30.0))
    # ---------------- registration
    P("### Registration of the pinned prop (tip drawn on the card against the world target, through the camera of each frame; 720x1280 px)\n")
    P("| Shot | Prop | Frames g | max px | mean px | solver residual max (D) | arm stretch |\n|---|---|---|---|---|---|---|")
    groups = [("1 insert", "pencil on the growing end of the track", range(F.G_LAND, F.G2)), ("2 low angle", "pencil on the growing end, jab at New York", range(F.G2, F.G_JAB + 2)),
              ("3 two-shot", "eraser face on the upper end of what is left of the track", range(F.G_TOUCH, F.G_DONE + 1))]
    for name, prop, gs in groups:
        rs = [meta[g]["reg"] for g in gs if g in meta and "reg" in meta[g]]
        if rs:
            P("| %s | %s | %d-%d (%d) | %.2f | %.2f | %.4f | |" % (name, prop, min(gs), max(gs), len(rs), max(r["px"] for r in rs), np.mean([r["px"] for r in rs]), max(r["solve_err_D"] for r in rs)))
    P("")
    # ---------------- heads
    P("### Heads (projected from the cards; width = head diameter on screen; y from the top; frame 720x1280)\n")
    P("| Shot | Frames g | Actor | Head width px | Centre x px | Centre y px | Centre y / H | Lowest head edge y (must be < 880) |\n|---|---|---|---|---|---|---|---|")
    shots = [("2 low angle (before the snap)", range(F.PULL[1], F.SNAP2[0])), ("2 low angle (after the snap)", range(F.SNAP2[1], F.WHIP_OFF[0])),
             ("3 two-shot (settled)", range(F.WHIP_ON[1] + 1, F.SNAP3[0])), ("3 after the snap push", range(F.SNAP3[1], N))]
    ratio_rows = []
    for name, gs in shots:
        for who in ("heroA", "heroB", "bossB"):
            hs = [meta[g]["heads"][who] for g in gs if g in meta and who in meta[g]["heads"]]
            if not hs:
                continue
            P("| %s | %d-%d | %s | %s | %s | %s | %s | %.0f |" % (name, min(gs), max(gs), who[:-1], rng(h["w"] for h in hs), rng(h["x"] for h in hs), rng(h["y"] for h in hs),
                                                              rng((h["y"] / 1280.0 for h in hs), "%.2f"), max(h["y"] + h["h"] / 2.0 for h in hs)))
        rr = [meta[g]["heads"]["heroB"]["w"] / meta[g]["heads"]["bossB"]["w"] for g in gs if g in meta and "bossB" in meta[g]["heads"]]
        if rr:
            ratio_rows.append((name, min(rr), max(rr)))
    P("")
    for name, a, b in ratio_rows:
        P("- near head / far head, %s: %.2f to %.2f (reference two-shots 1.36 to 1.46)" % (name, a, b))
    P("")
    # ---------------- camera
    mo = json.load(open(os.path.join(tmp, "motion.json")))
    P("### Camera per shot (true camera path)\n")
    P("| Shot | Frames g | Height above the floor (D) | Pitch (deg, + = up) | Yaw (deg, + = looking toward +x) | Corner speed px/frame min / median / max |\n|---|---|---|---|---|---|")
    for n, d in mo["per_shot"].items():
        P("| %s | %d-%d | %.2f to %.2f | %+.1f to %+.1f | %+.1f to %+.1f | %.2f / %.2f / %.1f |" % (n, d["frames"][0], d["frames"][1], d["height"][0], d["height"][1], d["pitch"][0], d["pitch"][1], d["yaw"][0], d["yaw"][1], *d["speed_px"]))
    P("")
    P("### Framing changes (camera corner speed above %d px per frame)\n" % 12)
    P("| Move | Frames g | Start s | Peak s | End s | Peak px/frame | Peak / mean speed |\n|---|---|---|---|---|---|---|")
    names = {0: "opening drift (already moving on frame 0)"}
    for m in mo["moves"]:
        P("| %s | %d-%d | %.3f | %.3f | %.3f | %.0f | %.2f |" % ("contains the cut at g %d" % mo["cut"] if m["contains_cut"] else "", m["start"], m["end"], m["start_s"], m["peak_s"], m["end_s"], m["peak_px"], m["peak_px"] / m["mean_px"]))
    P("")
    P("- longest static run (camera slower than 0.25 px per frame): %d frames; slowest frame %.2f px per frame" % (mo["longest_static"], mo["slowest_px"]))
    P("- longest constant-speed (linear) run while moving: %d frames %s" % (mo["longest_linear"], mo["linear_runs"]))
    P("")
    # ---------------- render time
    for take in ("A", "B"):
        for th in sorted(set(m["threads"] for m in meta.values() if m["take"] == take)):
            ms = [m for m in meta.values() if m["take"] == take and m["threads"] == th]
            P("- delivered frames of take %s rendered with %d threads (%s): %d frames, %d samples: wall %.2f s mean (%.2f to %.2f), CPU %.2f s mean (%.2f to %.2f) per frame%s" % (
                take, th, "one process, machine to itself" if th == 4 else "two processes side by side", len(ms), ms[0]["samples"],
                np.mean([m["wall"] for m in ms]), min(m["wall"] for m in ms), max(m["wall"] for m in ms),
                np.mean([m["cpu"] for m in ms]), min(m["cpu"] for m in ms), max(m["cpu"] for m in ms),
                "; frames re-rendered by the black-card check: %s" % [m["g"] for m in ms if m.get("retried")]))
    P("")
    # ---------------- light
    ls = sorted(glob.glob(os.path.join(tmp, "light", "light_g*.json")))
    if ls:
        P("### Light on our frames (measurement passes of the film frames, 720x1280)\n")
        P("| Frame g | Sunny / lit / in cast shadow (share of frame) | Same surface shade / lit, linear p10 / median / p90 | The same as display luma, median | Lit -> shade colour (hue) | Cast-shadow edge 10-90 %, p10 / median / p90 / max px (n) | Actor-cast shadow px (share) | Actor shadow edge median px | Track samples under an actor's shadow |\n|---|---|---|---|---|---|---|---|---|")
        for p in ls:
            r = json.load(open(p))
            e = r.get("edge_width_px", {}); ae = r.get("actor_shadow_edge_px", {})
            P("| %d | %.2f / %.2f / %.2f | %s | %.2f | %s -> %s (%.0f -> %.0f) | %s | %d (%.3f) | %s | %s |" % (
                r["g"], r["sunny_share"], r["lit_share"], r["cast_shadow_share"], " / ".join("%.2f" % x for x in r.get("shadow_over_lit_linear", [0, 0, 0])),
                r.get("shadow_over_lit_display", [0, 0, 0])[1], r.get("lit_colour"), r.get("shade_colour"), r.get("hue_lit", 0), r.get("hue_shade", 0),
                ("%.1f / %.1f / %.1f / %.1f (%d)" % (e["p10"], e["median"], e["p90"], e["max"], e["n"])) if e else "-", r["actor_shadow_px"], r["actor_shadow_share"],
                ("%.1f" % ae["median"]) if ae else "-", r.get("track_under_actor_shadow", "-")))
        P("")
    # ---------------- parallax
    pr = os.path.join(tmp, "parallax_ref.json")
    if os.path.exists(pr):
        r = json.load(open(pr))
        P("### Share of frame pairs 0.5 s apart that a flat 2D zoom or pan explains\n")
        P("| Input | Pairs | Flat-2D pairs | Share | Median inlier ratio F / H / similarity (matched pairs) |\n|---|---|---|---|---|")
        for clip, pub in (("a", "12 percent (16 of 129)"), ("b", "43 percent (55 of 129)")):
            rows = r["pairs"][clip]; mt = [x for x in rows if x.get("n", 0) >= 30]
            nf = sum(1 for x in rows if x.get("n", 0) >= 30 and x["F"] > 0 and x["S"] >= r["ratio"] * x["F"])
            P("| reference clip %s, stills 0.5 s apart (published: %s) | %d | %d | %.1f %% | %.2f / %.2f / %.2f |" % (clip.upper(), pub, len(rows), nf, 100.0 * nf / len(rows),
              np.median([x["F"] for x in mt]), np.median([x["H"] for x in mt]), np.median([x["S"] for x in mt])))
        for tag, label in (("v2", "v2 (flat), v2/out/frames, every pair g, g + 15"), ("v3", "v3 (3D), v3/out/frames, every pair g, g + 15")):
            p = os.path.join(tmp, "parallax_%s.json" % tag)
            if os.path.exists(p):
                o = json.load(open(p))
                P("| %s | %d | %d | %.1f %% | %.2f / %.2f / %.2f |" % (label, o["pairs"], o["flat"], 100 * o["share"], o["F_median"] or 0, o["H_median"] or 0, o["S_median"] or 0))
        P("\nRATIO = %.2f (a pair is flat when the similarity keeps at least RATIO of the fundamental-matrix inliers), calibrated on the reference stills.\n" % r["ratio"])
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1:])
