#!/usr/bin/env python3
"""deliver.py <take>  (s33 | s34 | s35) -- render team 7, film 6.  From <take>/raw/s<N>/g_*.png build <take>/frames/g_%04d.png,
meta.json, cues.json, contact.jpg, compare.jpg (final frames beside ref a / ref b frames), take.mkv (libx264rgb crf 6), and
work/qa.txt (heads vs the caption band, pops, black / magenta frames, hue rows, s per frame).  Same copy in s33 / s34 / s35."""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw

FILM6 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJ = os.path.normpath(os.path.join(FILM6, "..", ".."))
sys.path.insert(0, os.path.join(FILM6, "..", "tools"))

TAKES = {
    "s33": dict(shot=33, g0=2836, g1=2965, first=2830, last=2970, loc="market AFTERNOON",
                transition_in="dissolve", transition_out="dissolve",
                note_in="plan: dissolve in from shot 32 (bakery small_scale_insert); in-handle g 2830..2835 rendered in 3D",
                note_out="plan: dissolve to shot 34 (bakery DAWN counter); out-handle g 2965..2970 rendered in 3D (tilt + steam continue)",
                framings={"A": [2830, 2878], "B": [2879, 2922], "C": [2923, 2970]},
                events={"A_row_of_three_bakers_steaming_baskets": [2830, 2878], "B_punch_in_middle_baker_tears_steam": [2879, 2922],
                        "C_steam_rises_past_faces_tilt_up": [2923, 2970], "bakers_look_up_after_the_steam": [2929, 2951]},
                refs=[("a", 61), ("b", 121)], pairs=[2850, 2900, 2950],
                set="v3/set3d6/bakery.py: market AFTERNOON; the set pillory's 3D board + post cut out of the 'pillory' mesh at runtime "
                    "(platform, rails, lanterns, splats kept); three cast6 'pillory' pose cards (baker2 + runtime recolours baker3 / baker4); "
                    "three cast6.basket_svg PropCards on the platform with local camera-only steam cards (the set's steam material, set_steam 1.5)",
                cues=[(2830, 2971, "market square in the late afternoon: distant crowd murmur, a crow, a soft breeze, the bunting flapping", "ambience", None),
                      (2830, 2971, "sad, slow musical bed: a lone low woodwind (the bakers' innocence)", "music", None),
                      (2850, 2905, "three slow sighs from the pilloried bakers, a creak of the boards", "vocal-nonverbal", 2858),
                      (2879, 2879, "framing change (cut): punch-in on the middle baker over his steaming basket", "cut", None),
                      (2879, 2922, "a soft airy 'whoosh' rising with the steam, a tiny sniff from the crying baker", "accent", 2895),
                      (2923, 2923, "framing change (cut): low from the right, tilt up after the steam", "cut", None),
                      (2929, 2965, "airy rising shimmer as the steam floats away into the sky ('ลอยหายไปในอากาศ')", "accent", 2945)]),
    "s34": dict(shot=34, g0=2965, g1=3075, first=2959, last=3080, loc="bakery MORNING (the plan's DAWN)",
                transition_in="dissolve", transition_out="dissolve",
                note_in="plan: dissolve in from shot 33 (market); in-handle g 2959..2964 rendered in 3D",
                note_out="plan: shot 35 (market MORNING) follows; out-handle g 3075..3080 rendered in 3D (push + kit's grin continue)",
                framings={"A": [2959, 3002], "B": [3003, 3045], "C": [3046, 3080]},
                events={"henry_counts_12_finger_taps": [2961, 3000], "pale_loaf_up_from_under_counter": [3014, 3024],
                        "henry_looks_at_pale_loaf": [3024, 3032], "loaf_carried_to_basket": [3032, 3041], "loaf_13_lands": 3042,
                        "henry_turns_to_kit": [3043, 3051], "henry_nods": [3052, 3072], "kit_beams_and_hops": [3056, 3071]},
                refs=[("a", 46), ("a", 1)], pairs=[2990, 3030, 3065],
                set="v3/set3d6/bakery.py: bakery MORNING, steam 0.35, oven 1.0 flicker keyed per frame; the hand balance (small_*) hidden at runtime "
                    "(it stood in front of Henry); custom street-side cameras of the s01 family; basket = cast6.basket_svg 12 / 13 (13th drawn pale) on a PropCard; "
                    "Henry's held loaf drawn with a pale crust (cast6.BREAD patched only while his sprites render)",
                cues=[(2959, 3081, "bakery at dawn: oven fire crackling low, a rooster far off through the counter opening, birds", "ambience", None),
                      (2959, 3081, "warm, gentle resolving music (strings), building slightly to the nod", "music", None),
                      (2961, 3000, "soft wooden taps / ticks as Henry's finger counts along the loaves (12)", "prop", 2999),
                      (3003, 3003, "framing change (cut): punch-in on Henry and the basket", "cut", None),
                      (3014, 3024, "a loaf is lifted from under the counter: soft crusty rustle", "prop", 3020),
                      (3032, 3042, "the 13th loaf set on top of the pile: soft thump + wicker creak", "prop", 3042),
                      (3046, 3046, "framing change (cut): two-shot, push toward kit", "cut", None),
                      (3052, 3072, "Henry's slow nod (warm low 'mm' hum, no words)", "vocal-nonverbal", 3060),
                      (3056, 3071, "kit beams: bright happy sparkle sting + tiny hop", "accent", 3060)]),
    "s35": dict(shot=35, g0=3075, g1=3194, first=3069, last=3193, loc="market MORNING",
                transition_in="dissolve", transition_out="end",
                note_in="plan: dissolve in from shot 34 (bakery counter); in-handle g 3069..3074 rendered in 3D",
                note_out="end of film: last frame g 3193 (N = 3194); no out-handle",
                framings={"close_on_shop": [3069, 3109], "crane_pull_back": [3109, 3183], "wide_drift_to_end": [3183, 3193]},
                events={"kit_glances_up_at_henry": [3077, 3113], "henry_nods": [3083, 3101], "kit_hop": [3115, 3127],
                        "pull_back_starts": 3109, "pull_back_lands": 3183},
                refs=[("a", 61), ("b", 121)], pairs=[3085, 3150, 3193],
                set="v3/set3d6/bakery.py: market MORNING; Henry's bakery front (west row); basket of 13 (13th drawn pale) = cast6.basket_svg PropCard x1.7 "
                    "on the shutter board, three local camera-only steam cards (set's steam material, set_steam 1.5); the bread sign on its bracket",
                cues=[(3069, 3194, "market square waking up in the morning: birdsong, a distant church bell, a cart rolling, soft chatter", "ambience", None),
                      (3069, 3194, "closing theme: warm full statement of the music, swelling with the pull-back, resolving on the last frame", "music", None),
                      (3083, 3101, "Henry's contented nod, kit's happy giggle (no words)", "vocal-nonverbal", 3090),
                      (3109, 3183, "the camera rises: airy swell, bunting flutter", "accent", 3150),
                      (3193, 3193, "end of film", "end", None)]),
}


def main(take):
    T = TAKES[take]
    here = os.path.join(FILM6, take)
    raw = os.path.join(here, "raw", "s%d" % T["shot"])
    out = os.path.join(here, "frames"); os.makedirs(out, exist_ok=True)
    gs = list(range(T["first"], T["last"] + 1))
    missing = [g for g in gs if not os.path.exists(os.path.join(raw, "g_%04d.png" % g))]
    if missing:
        raise SystemExit("missing frames: %s" % missing[:20])
    for g in gs:
        shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(out, "g_%04d.png" % g))
    rows = [json.load(open(os.path.join(raw, "g_%04d.json" % g))) for g in gs]
    walls = [r["wall"] for r in rows]; cpus = [r["cpu"] for r in rows]
    meta = {"take": take, "film": 6, "shots": [T["shot"]], "first_g": T["first"], "n_frames": len(gs), "g0": T["g0"], "g1": T["g1"],
            "handle_in": T["g0"] - T["first"], "handle_out": T["last"] + 1 - T["g1"] if T["last"] + 1 > T["g1"] else 0,
            "transition_in": T["transition_in"],
            "transition_in_detail": {"type": T["transition_in"], "frames": 10, "note": T["note_in"]},
            "transition_out": {"type": T["transition_out"], "note": T["note_out"]},
            "shot_ranges": {str(T["shot"]): [T["g0"], min(T["g1"], T["last"] + 1) - 1]},
            "framings": T["framings"], "events": T["events"], "set": T["set"],
            "dof": "none (client rule: cam.data.dof.use_dof False + B.setup_dof(scene, None, None, cam=cam) at build and before every render)",
            "denoiser": "OpenImageDenoise, albedo+normal, prefilter FAST",
            "narration": "film6/audio/narration_bankky.wav at +0.10 s; captions film6/script/captions.json",
            "mouths": "no quoted line in this shot: static expression mouths only",
            "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
            "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
            "blender_frame": "g - 2700"}
    json.dump(meta, open(os.path.join(here, "meta.json"), "w"), indent=1)
    ev = []
    for (a, b, label, kind, peak) in T["cues"]:
        e = dict(time=round(a / 30.0, 3), duration=round(max(0, b - a) / 30.0, 3), frame=a, end_frame=b, kind=kind, label=label)
        if peak is not None:
            e["peak_frame"] = peak
        ev.append(e)
    json.dump(dict(take=take, fps=30, note="time = film seconds (g / 30); narration at +0.10 s", cues=ev),
              open(os.path.join(here, "cues.json"), "w"), indent=1)
    # contact sheet: 16 frames
    sel = [gs[int(round(i * (len(gs) - 1) / 15.0))] for i in range(16)]
    w, h, lab, cols = 270, 480, 18, 8
    S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
    for i, g in enumerate(sel):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(os.path.join(out, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        tag = " handle" if (g < T["g0"] or g >= T["g1"]) else ""
        dr.text((x + 4, y + 3), "g %d  %.2f s  shot %d%s" % (g, g / 30.0, T["shot"], tag), fill=(255, 255, 255))
        dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(255, 80, 80))
    S.save(os.path.join(here, "contact.jpg"), quality=88)
    # compare: three finals + two refs
    w, h, lab = 360, 640, 20
    items = [(os.path.join(out, "g_%04d.png" % g), "%s g %d (%.2f s)" % (take, g, g / 30.0)) for g in T["pairs"]]
    items += [(os.path.join(PROJ, "ref", d, "t%04d.jpg" % t), "ref %s t%04d" % (d, t)) for d, t in T["refs"]]
    Cm = Image.new("RGB", (len(items) * w + (len(items) - 1) * 8, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(Cm)
    for i, (p, t) in enumerate(items):
        Cm.paste(Image.open(p).convert("RGB").resize((w, h), Image.LANCZOS), (i * (w + 8), lab))
        dr.text((i * (w + 8) + 4, 4), t, fill=(255, 220, 160) if t.startswith("ref") else (255, 255, 255))
    Cm.save(os.path.join(here, "compare.jpg"), quality=88)
    mkv = os.path.join(here, "take.mkv")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(T["first"]), "-i", os.path.join(out, "g_%04d.png"),
                    "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
    qa(take, T, here, rows, gs)
    print("delivered %s: %d frames g %d..%d + take.mkv; wall %.2f s, cpu %.2f s" % (take, len(gs), gs[0], gs[-1], np.mean(walls), np.mean(cpus)))


def qa(take, T, here, rows, gs):
    import hue_report as H
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        print("%s shot %d, g %d..%d (%d frames)" % (take, T["shot"], gs[0], gs[-1], len(gs)))
        names = sorted({n for r in rows for n in r["heads"]})
        for n in names:
            hs = [(r["g"], r["heads"][n]) for r in rows if n in r["heads"]]
            vis = [(g, hh) for g, hh in hs if -hh["w"] / 2 < hh["x"] < 720 + hh["w"] / 2 and hh["y"] < 1280 + hh["w"]]
            if not vis:
                continue
            ww = [hh["w"] for g, hh in vis]; y = [hh["y"] for g, hh in vis]; x = [hh["x"] for g, hh in vis]
            low = [g for g, hh in vis if hh["y"] + hh["w"] / 2 > 880]
            print("  %-6s head w %4.0f..%4.0f px, centre x %4.0f..%4.0f, y %4.0f..%4.0f (%.2f..%.2f H); head bottom below 880: %s"
                  % (n, min(ww), max(ww), min(x), max(x), min(y), max(y), min(y) / 1280, max(y) / 1280, (low[0], low[-1], len(low)) if low else "none"))
        for fr, (a, b) in T["framings"].items():
            print("  framing %s: g %d..%d (%.2f s)" % (fr, a, b, (b - a + 1) / 30.0))
        print("  render: wall %.2f s, cpu %.2f s per frame (mean); retried: %s" % (np.mean([r["wall"] for r in rows]), np.mean([r["cpu"] for r in rows]),
                                                                                   [r["g"] for r in rows if r.get("retried")]))
        fs = [os.path.join(here, "frames", "g_%04d.png" % g) for g in gs]
        prev = None; d = []
        for f in fs:
            a = np.asarray(Image.open(f).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
            if prev is not None:
                d.append(float(np.abs(a - prev).mean()))
            prev = a
        pops = []
        for i, v in enumerate(d):
            p = d[i - 1] if i else v; n = d[i + 1] if i + 1 < len(d) else v
            if v > 1.8 * p and v > 1.8 * n and v > 1.0:
                pops.append((gs[i], gs[i + 1], round(v, 1)))
        print("  popcheck (g -> g+1, change):", pops, " (framing cuts expected at", [a for fr, (a, b) in T["framings"].items()][1:], ")")
        print("  near-still transitions (< 0.35 levels):", [gs[i] for i, v in enumerate(d) if v < 0.35])
        print("  frame change median %.2f, max %.2f levels" % (float(np.median(d)), max(d)))
        bad = []
        for f in fs:
            a = np.asarray(Image.open(f).convert("RGB").resize((90, 160)), dtype=np.int16)
            mag = ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean()
            blk = (a.max(axis=2) < 6).mean()
            if mag > 0.002 or blk > 0.2:
                bad.append(os.path.basename(f))
        print("  magenta / black frames:", bad)
        print()
        print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
        H.row("%s shot %d (g %d-%d)" % (take, T["shot"], T["g0"], min(T["g1"], gs[-1] + 1) - 1),
              [os.path.join(here, "frames", "g_%04d.png" % g) for g in range(T["g0"], min(T["g1"], gs[-1] + 1))])
        for d_, t in T["refs"]:
            H.row("ref %s t%04d" % (d_, t), [os.path.join(PROJ, "ref", d_, "t%04d.jpg" % t)])
    os.makedirs(os.path.join(here, "work"), exist_ok=True)
    open(os.path.join(here, "work", "qa.txt"), "w").write(buf.getvalue())
    print(buf.getvalue())


if __name__ == "__main__":
    main(sys.argv[1])
