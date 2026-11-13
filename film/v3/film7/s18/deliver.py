#!/usr/bin/env python3
"""deliver.py -- (identical copy in s16 / s18 / s19; the take is the folder name) from raw/s<id>/g_%04d.png build frames/g_%04d.png,
meta.json, cues.json, contact.jpg (16 frames, cyan line = y 880), compare.jpg (final frames beside the closest ref a frames), qa.txt
numbers (heads, caption band, pops, black / magenta, hue rows, s per frame) and take.mkv (libx264rgb crf 6, every frame).
    python3 deliver.py"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
TAKE = os.path.basename(HERE)
sys.path.insert(0, os.path.join(PROJ, "v3", "tools"))

NARR = "film7/audio/narration_bankky.wav at +0.10 s; captions film7/script/captions.json"
DOF = "none (client rule: cam.data.dof.use_dof False + L.setup_dof(scene, None, None, cam=cam) at build and before every render)"

CFG = {
 "s16": dict(
    shots=[16, 17], g0=1536, g1=1764, shot_ranges={"16": [1536, 1663], "17": [1664, 1763]},
    setups={"1": dict(g=[1530, 1576], set="louvre wall_eye area, GALLERY_DAY ramping to sunset (sun colour / elevation / skylight fills / grade slope keyed per frame, torches 1.0 -> 1.9), shaft sheets hidden", what="wide on the empty wall, time-lapse passers-by, guard at ease"),
            "2": dict(g=[1577, 1617], set="same, light ramp continues", what="medium: the guard turns to the empty spot"),
            "3": dict(g=[1618, 1663], set="same, sunset gold", what="punch-in: the guard shrugs at us"),
            "4": dict(g=[1664, 1712], set="louvre wall_eye area, GALLERY_DAY (next morning), runtime easel card", what="the painter walks in to his easel"),
            "5": dict(g=[1713, 1769], set="same", what="closer: he dabs, looks up, points at the empty hooks")},
    transitions=[{"at": 1530, "type": "in", "handle": [1530, 1535]}, {"at": 1536, "type": "cut", "note": "plan: hard cut from shot 15 (exit door)"},
                 {"at": 1577, "type": "cut", "note": "inside the take on 'ยามเห็นผนัง' (52.48)"}, {"at": 1618, "type": "cut", "note": "punch-in on 'ก็นึกว่า' (53.48)"},
                 {"at": 1664, "type": "cut", "note": "shot 17, next morning (55.46, 'วันรุ่งขึ้น')"}, {"at": 1713, "type": "cut", "note": "on 'วาดรูป' (57.17)"},
                 {"at": 1764, "type": "out", "handle": [1764, 1769]}],
    transition_in="cut", transition_out="cut",
    events={"passers_by_time_lapse": [1530, 1576], "light_midday_to_sunset": [1530, 1663], "guard_looks_at_empty_spot": [1595, 1605],
            "guard_shrug": [1625, 1663], "next_morning_painter_walks_in": [1664, 1696], "painter_paints": [1696, 1754],
            "painter_looks_up": [1754, 1760], "painter_points_at_hooks": [1745, 1769]},
    light="GALLERY_DAY -> keyed sunset (shot 16) | GALLERY_DAY (shot 17)",
    cast="v3/cast7: guard (guard_at_ease -> guard_shrug), lady x2 + gentleman (walk cycles, time-lapse speed), painter (walk, painter_paint, painter_point, palette); mouths static",
    set="v3/set3d7/louvre.py gallery (wall_eye area), set_mona(False) keyed every frame (the four hooks + unfaded patch), set_flames keyed every frame; runtime: easel PropCard (cast7.easel_svg, a faint sketch of her) in shot 17; custom cameras 21-26 mm",
    compare=[(1610, 13, "guard by the wall | ref a t0013"), (1650, 63, "sunset | ref a t0063"), (1760, 49, "character, red interior | ref a t0049")],
    hue=[("s16 shot 16 (g 1536-1663)", 1536, 1663), ("s16 shot 17 (g 1664-1763)", 1664, 1763)],
    refs=[("ref a t0013 t0049 (red interiors)", [13, 49]), ("ref a t0063 (sunset)", [63])]),
 "s18": dict(
    shots=[18], g0=1764, g1=1879, shot_ranges={"18": [1764, 1878]},
    setups={"1": dict(g=[1758, 1801], set="paris notre_dame_view area, STREET_DUSK, papers 24", what="the quai at dusk, Notre-Dame's two towers, strollers, slow push"),
            "2": dict(g=[1802, 1835], set="same", what="low angle 48 mm tilt up the west front to the towers"),
            "3": dict(g=[1836, 1884], set="louvre wall_eye area, GALLERY_DAY, set_mona(False)", what="hard cut: the director at the empty wall whips round, shocked; low angle, punch-in")},
    transitions=[{"at": 1758, "type": "in", "handle": [1758, 1763]}, {"at": 1764, "type": "cut", "note": "plan: from shot 17 (louvre) to paris; a dissolve can use the in-handle"},
                 {"at": 1802, "type": "cut", "note": "inside the shot: tilt-up set-up"}, {"at": 1836, "type": "cut", "note": "HARD CUT on 'แต่โมนาลิซ่า' (61.11)"},
                 {"at": 1879, "type": "out", "handle": [1879, 1884]}],
    transition_in="cut", transition_out="cut",
    events={"notre_dame_dusk": [1758, 1801], "tilt_up_towers": [1802, 1835], "hard_cut_director": 1836, "director_whips_round_shocked": [1847, 1851]},
    light="STREET_DUSK | GALLERY_DAY",
    cast="v3/cast7: lady + gentleman strolling (walk cycles); director (director_proud stunned at the wall -> director_shocked, trembling); mouths static",
    set="v3/set3d7/louvre.py: (1-2) paris street area at dusk (notre_dame_view), set_papers(24) + set_flames keyed every frame; (3) louvre gallery, set_mona(False) keyed every frame; custom cameras 22-48 mm",
    compare=[(1790, 57, "facade at the end of the view | ref a t0057"), (1860, 13, "shock, low angle | ref a t0013")],
    hue=[("s18 notre-dame (g 1764-1835)", 1764, 1835), ("s18 director (g 1836-1878)", 1836, 1878)],
    refs=[("ref a t0063 t0065 (dusk exteriors)", [63, 65]), ("ref a t0013 (red interior)", [13])]),
 "s19": dict(
    shots=[19, 20], g0=1879, g1=2044, shot_ranges={"19": [1879, 1964], "20": [1965, 2043]},
    setups={"1": dict(g=[1873, 1918], set="louvre gallery_wide area, GALLERY_DAY, set_mona(False)", what="wide: police run across the salon, one searches with a lantern, the guard waves"),
            "2": dict(g=[1919, 1964], set="louvre wall_eye area", what="at the empty wall: inspector with lantern at the hooks, guard shrugs, a policeman runs through"),
            "3": dict(g=[1965, 2004], set="louvre gallery (service-door corner) + runtime table, lantern, papers", what="the inspector questions the generic young painter (striped shirt)"),
            "4": dict(g=[2005, 2049], set="same", what="punch-in: the painter indignant; vincenzo strolls by unnoticed in the background, a smug glance")},
    transitions=[{"at": 1873, "type": "in", "handle": [1873, 1878]}, {"at": 1879, "type": "cut", "note": "plan: hard cut from shot 18 (director) to the police chaos"},
                 {"at": 1919, "type": "cut", "note": "on 'ตำรวจค้นทั้งตึก' (63.85)"}, {"at": 1965, "type": "cut", "note": "shot 20 (65.50)"},
                 {"at": 2005, "type": "cut", "note": "punch-in on 'แต่ไม่มีใคร' (66.38)"}, {"at": 2044, "type": "out", "handle": [2044, 2049]}],
    transition_in="cut", transition_out="cut",
    events={"police_chaos": [1873, 1964], "questioning": [1965, 2049], "painter_indignant": [1986, 2049], "vincenzo_walks_by": [1990, 2049], "vincenzo_smug_glance": [2025, 2049]},
    light="GALLERY_DAY",
    cast="v3/cast7: police x5 (run cycles, police_search with lantern, police_question), guard (wave / shrug), young_painter (generic, striped shirt: questioned -> indignant, anger_fill fx dropped: it renders magenta), vincenzo (normal clothes, walk, hands in pockets, smug); mouths static",
    set="v3/set3d7/louvre.py gallery, set_mona(False) + set_flames keyed every frame; runtime office dressing in shot 20 (table, papers, ink pot, lit lantern); custom cameras 22-24 mm",
    compare=[(1900, 45, "busy wide interior | ref a t0045"), (2030, 51, "medium, red interior | ref a t0051")],
    hue=[("s19 shot 19 (g 1879-1964)", 1879, 1964), ("s19 shot 20 (g 1965-2043)", 1965, 2043)],
    refs=[("ref a t0045 t0047 (busy interior)", [45, 47]), ("ref a t0013 t0051 (red interior)", [13, 51])]),
}[TAKE]

H = 6
FIRST, LAST = CFG["g0"] - H, CFG["g1"] + H - 1
N = LAST - FIRST + 1
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
SID = {}
for sid, s in CFG["setups"].items():
    for g in range(s["g"][0], s["g"][1] + 1):
        SID[g] = sid
rows = []
for g in range(FIRST, LAST + 1):
    raw = os.path.join(HERE, "raw", "s%s" % SID[g])
    shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]
by = {sid: dict(wall=round(float(np.mean([m["wall"] for m in rows if str(m["shot"]) == sid])), 2),
                cpu=round(float(np.mean([m["cpu"] for m in rows if str(m["shot"]) == sid])), 2)) for sid in CFG["setups"]}

meta = {"take": TAKE, "film": 7, "shots": CFG["shots"], "first_g": FIRST, "n_frames": N, "g0": CFG["g0"], "g1": CFG["g1"],
        "handle_in": H, "handle_out": H, "transition_in": CFG["transition_in"],
        "transition_out": CFG["transition_out"], "transitions": CFG["transitions"], "shot_ranges": CFG["shot_ranges"],
        "setups": CFG["setups"], "events": CFG["events"], "set": CFG["set"], "dof": DOF,
        "denoiser": "OpenImageDenoise, albedo+normal, prefilter FAST", "narration": NARR, "light": CFG["light"], "cast": CFG["cast"],
        "mouths": "static expression mouths only (no quoted line in these shots)",
        "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "s_per_frame_by_setup": by, "frame_source": {str(g): SID[g] for g in range(FIRST, LAST + 1)}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

# ----------------------------------------------------------------------------- cues
t = lambda g: round(g / 30.0, 3)
ev = []


def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)


if TAKE == "s16":
    add(1530, 1663, "Salon Carre all day: a soft hubbub of footsteps and murmurs on parquet, sped up (time-lapse), thinning toward evening", "ambience")
    add(1530, 1576, "quick time-lapse footsteps and skirts swishing past, nobody stops", "foley", peak_frame=1550)
    add(1530, 1663, "a ticking clock speeding up, the light warming: a gentle rising string pad", "music")
    add(1577, 1577, "cut", "cut")
    add(1595, 1605, "the guard's head turn to the empty spot: a small 'hm?' pizzicato", "accent", peak_frame=1600)
    add(1618, 1618, "punch-in", "cut")
    add(1625, 1640, "the shrug: a bored double bassoon 'bwomp-bwomp'", "accent", peak_frame=1628)
    add(1640, 1663, "gas torcheres hiss as they come up at dusk", "ambience")
    add(1664, 1664, "cut: next morning, birdsong through the skylight", "cut")
    add(1664, 1712, "quiet morning gallery: distant pigeons on the skylight, a single pair of footsteps (the painter) on parquet", "ambience")
    add(1700, 1704, "easel legs set down, a brush tapping the palette", "foley", peak_frame=1702)
    add(1713, 1713, "cut", "cut")
    add(1720, 1745, "brush dabs on canvas", "foley", peak_frame=1730)
    add(1745, 1769, "the point at the empty hooks: a sharp 'dun!' sting", "accent", peak_frame=1747)
elif TAKE == "s18":
    add(1758, 1835, "the Seine quai at dusk: water lapping, a distant church bell, a horse cab far off, gas lamps hissing", "ambience")
    add(1764, 1835, "a proud, warm brass motif of the towers (callback to the director's boast), held", "music")
    add(1802, 1802, "cut: low angle on the towers", "cut")
    add(1836, 1836, "HARD CUT: the music stops dead, a high violin stab", "cut", peak_frame=1836)
    add(1847, 1852, "the director whips round: whoosh + a comic gasp (no words)", "accent", peak_frame=1848)
    add(1852, 1884, "trembling: a shaky timpani roll", "music")
else:
    add(1873, 1964, "chaos in the salon: running boots on parquet, whistles, doors slamming, echoes under the skylight", "ambience")
    add(1873, 1964, "busy comic chase music (pizzicato strings + snare)", "music")
    add(1880, 1900, "police whistle blasts", "accent", peak_frame=1885)
    add(1919, 1919, "cut", "cut")
    add(1925, 1964, "lantern creak, a magnifier tap on the wall by the hooks", "foley", peak_frame=1940)
    add(1965, 1965, "cut: the make-shift office", "cut")
    add(1965, 2049, "quieter room tone, the lantern hissing, papers shuffled", "ambience")
    add(1970, 1985, "the inspector's finger stab: a low staccato 'dun-dun'", "accent", peak_frame=1972)
    add(1986, 1992, "the painter flares up: an indignant comic 'pfff!' brass blat (no words)", "accent", peak_frame=1988)
    add(2005, 2005, "punch-in", "cut")
    add(1995, 2049, "vincenzo's casual footsteps far behind, a carefree whistled tune (diegetic, tiny)", "foley", peak_frame=2010)
    add(2025, 2049, "his smug glance: a sly clarinet trill", "accent", peak_frame=2026)
json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration PROJ/" + NARR, cues=ev), open(os.path.join(HERE, "cues.json"), "w"), indent=1)

# ----------------------------------------------------------------------------- contact + compare
gs = [FIRST + int(round(i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
    sh = [k for k, (a, b) in CFG["shot_ranges"].items() if a <= g <= b]
    dr.text((x + 4, y + 3), "g %d  %.2f s  %s  set-up %s" % (g, g / 30.0, ("shot " + sh[0]) if sh else "handle", SID[g]), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

w, h, lab = 360, 640, 20
P = CFG["compare"]
Cm = Image.new("RGB", (len(P) * 2 * w + (len(P) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(Cm)
x = 0
for g, tref, note in P:
    Cm.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
    dr.text((x + 4, 4), "%s g %d (%.2f s)" % (TAKE, g, g / 30.0), fill=(255, 255, 255))
    Cm.paste(Image.open(os.path.join(PROJ, "ref", "a", "t%04d.jpg" % tref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
    dr.text((x + w + 4, 4), note, fill=(255, 220, 160))
    x += 2 * w + 12
Cm.save(os.path.join(HERE, "compare.jpg"), quality=88)

# ----------------------------------------------------------------------------- QA numbers -> work/qa.txt
os.makedirs(os.path.join(HERE, "work"), exist_ok=True)
qa = []
for sid in CFG["setups"]:
    rs = [r for r in rows if str(r["shot"]) == sid]
    for n in sorted({n for r in rs for n in r["heads"]}):
        hs = [(r["g"], r["heads"][n]) for r in rs if n in r["heads"]]
        vis = [(g, hh) for g, hh in hs if -hh["w"] / 2 < hh["x"] < 720 + hh["w"] / 2]
        if not vis:
            continue
        ww = [hh["w"] for g, hh in vis]; yy = [hh["y"] for g, hh in vis]; xx = [hh["x"] for g, hh in vis]
        low = [g for g, hh in vis if hh["y"] + hh["w"] / 2 > 880]
        qa.append("set-up %s %-7s head w %4.0f..%4.0f px, x %5.0f..%5.0f, centre y %4.0f..%4.0f (%.2f..%.2f H); bottom below 880: %s"
                  % (sid, n, min(ww), max(ww), min(xx), max(xx), min(yy), max(yy), min(yy) / 1280, max(yy) / 1280, (low[0], low[-1], len(low)) if low else "none"))
qa.append("render: wall %.2f s, cpu %.2f s per frame (mean); by set-up %s; retried: %s" % (np.mean(walls), np.mean(cpus), by, [r["g"] for r in rows if r.get("retried")]))
fs = [os.path.join(OUT, "g_%04d.png" % g) for g in range(FIRST, LAST + 1)]
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
        pops.append((FIRST + i, FIRST + i + 1, round(v, 1)))
qa.append("popcheck (g -> g+1, change): %s   planned cuts: %s" % (pops, [tr["at"] for tr in CFG["transitions"] if tr["type"] == "cut"]))
qa.append("near-still transitions (< 0.35 levels): %s" % [FIRST + i for i, v in enumerate(d) if v < 0.35])
qa.append("frame change median %.2f, max %.2f levels" % (float(np.median(d)), max(d)))
bad = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((90, 160)), dtype=np.int16)
    mag = ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean()
    if mag > 0.002 or (a.max(axis=2) < 6).mean() > 0.2:
        bad.append(os.path.basename(f))
qa.append("magenta / black frames: %s" % bad)
open(os.path.join(HERE, "work", "qa.txt"), "w").write("\n".join(qa) + "\n")
print("\n".join(qa))
try:
    import hue_report as HR
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in HR.NAMES) + "   sat  val dark")
        for name, a, b in CFG["hue"]:
            HR.row(name, [os.path.join(OUT, "g_%04d.png" % g) for g in range(a, b + 1, 2)])
        for name, ts in CFG["refs"]:
            HR.row(name, [os.path.join(PROJ, "ref", "a", "t%04d.jpg" % tt) for tt in ts])
    open(os.path.join(HERE, "work", "hue.txt"), "w").write(buf.getvalue()); print(buf.getvalue())
except Exception as ex:
    print("hue report failed:", ex)

mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
print("delivered %s: %d frames g %d..%d + take.mkv; mean wall %.2f s, cpu %.2f s" % (TAKE, N, FIRST, LAST, np.mean(walls), np.mean(cpus)))
