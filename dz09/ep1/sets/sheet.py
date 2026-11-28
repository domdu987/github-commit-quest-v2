"""sheet.py -- sets_sheet.png (every set from its planned camera positions, draft stills) and cost_table.md."""
import os, json, glob
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
ORDER = ["X1", "X1S", "X2", "CAB", "GEAR", "STAIR", "UND"]
TITLE = {"X1": "(1) X1  scene 02 dressing of the rescue zone", "X1S": "(2) X1s  overturned sedan", "X2": "(3) X2  zone 2: lorry, taxi, gate",
         "CAB": "(4) CAB  rescue-truck cab from inside", "GEAR": "(5) equipment wall", "STAIR": "(6) service stair", "UND": "(7) UND  street under the expressway"}
HOOK = dict(draft=10.3, B=36.6, A=68.2)          # measured on the hook: CPU s / frame (draft 360x640 2 spp; final 75 %; final 100 %)


def make():
    from PIL import Image, ImageDraw, ImageFont
    import bpy
    import camdefs
    f = ImageFont.truetype(os.path.join(HERE, "..", "..", "fonts", "WorkSans-Black.ttf"), 22)
    f2 = ImageFont.truetype(os.path.join(HERE, "..", "..", "fonts", "WorkSans-Black.ttf"), 15)
    tw, th, pad, head = 360, 640, 10, 44
    ncol = 4
    rows = []
    for key in ORDER:
        tiles = []
        for cd in camdefs.CAMS[key]:
            p = os.path.join(OUT, "stills", "%s_%s_draft.png" % (key, cd["name"]))
            if os.path.exists(p): tiles.append((cd, p))
        rows.append((key, tiles))
    H = sum(head + th + 30 + pad for _ in rows) + pad
    W = pad + ncol * (tw + pad)
    sh = Image.new("RGB", (W, H), (16, 17, 22)); d = ImageDraw.Draw(sh)
    y = pad
    for key, tiles in rows:
        d.text((pad, y + 8), TITLE[key], font=f, fill=(240, 240, 235))
        y += head
        for i, (cd, p) in enumerate(tiles[:ncol]):
            im = Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS)
            x = pad + i * (tw + pad)
            sh.paste(im, (x, y))
            doc = (cd["fn"].__doc__ or "").strip().split(":")[0]
            tail = "  class %s%s" % (cd.get("cls", "B"), "  [cost cam]" if cd.get("cost") else "")
            while doc and d.textlength(doc + tail, font=f2) > tw - 6: doc = doc[:-1]
            d.text((x + 2, y + th + 5), doc + tail, font=f2, fill=(200, 205, 215))
        y += th + 30 + pad
    sh.save(os.path.join(HERE, "sets_sheet.png"))
    # the final-tier stills side by side at full size
    fin = [os.path.join(OUT, "final", n) for n in sorted(os.listdir(os.path.join(OUT, "final"))) if n.endswith("_final.png")] if os.path.isdir(os.path.join(OUT, "final")) else []
    fin = sorted(fin, key=lambda p: ORDER.index(os.path.basename(p).split("_")[0]))
    if fin:
        ims = [Image.open(p).convert("RGB") for p in fin]
        S = Image.new("RGB", (sum(i.width for i in ims) + 8 * (len(ims) - 1), 1280), (16, 17, 22))
        x = 0
        for im in ims: S.paste(im, (x, 0)); x += im.width + 8
        S.save(os.path.join(HERE, "sets_final_sheet.png"))
    print("sheet", sh.size, len(fin), "finals")


def table():
    L = ["# EP.1 sets: measured cost", "",
         "Machine: 4 cores shared with the hook final and other builders (load 8-11 while these ran), 1 thread per Blender process, niced. CPU seconds are process CPU (render + post + staging), so they are little affected by the sharing; wall times are not given because they are.",
         "",
         "- **Draft test**: 24 consecutive frames, 360x640, 2 spp, the set's cost camera (marked on the sheet), two v8 puppets (kong_wet, crew_wet) in frame. The mean leaves out the first frame, which pays the first scene sync and the puppet rasters.",
         "- **Extrapolated final**: draft mean x the hook's own ratio of final to draft (draft 10.3; final 36.6 at 75 %, 68.2 at 100 %: x 3.55 and x 6.62).",
         "- **Measured final**: ONE 720x1280 frame at the final tier (5 spp) at each render scale, first frame of a fresh process (so it includes that process's first sync; a running shot is cheaper by about the difference between the draft first frame and the draft mean).",
         "- Plan's assumption: 36.6 (class B, 75 %) and 68.2 (class A, 100 %) CPU s per frame.",
         "",
         "- **Steady final** (checker's re-run): the mean of 3 further consecutive final-tier frames at the shot's class scale in the same process, i.e. what a running shot pays per frame. This is the number to put in the plan; it is 3 frames, not the plan's 24.",
         "",
         "| Set | Cost camera (class) | Stage build CPU s (deck + set) | Draft: first frame | Draft: mean of 23 | Extrapolated final 75 % / 100 % | Measured final still 75 % / 100 % | Steady final at class scale (3 frames) | Steady against the plan (its class) |",
         "|---|---|---|---|---|---|---|---|---|"]
    tot = []
    for key in ORDER:
        cp = os.path.join(OUT, "cost_%s.json" % key); fp = os.path.join(OUT, "final_%s.json" % key)
        if not os.path.exists(cp): L.append("| %s | not run | | | | | | |" % key); continue
        c = json.load(open(cp)); fz = json.load(open(fp)) if os.path.exists(fp) else None
        m = c["cpu_mean_after_first"]
        eb, ea = m * HOOK["B"] / HOOK["draft"], m * HOOK["A"] / HOOK["draft"]
        if fz:
            p75 = fz["cpu"] if fz["pct"] == 75 else fz["alt"]["cpu"]; p100 = fz["cpu"] if fz["pct"] == 100 else fz["alt"]["cpu"]
            meas = "%.1f / %.1f" % (p75, p100)
        else:
            p75 = p100 = None; meas = "not run"
        cls = c["cls"]
        est = ea if cls == "A" else eb; plan = HOOK[cls]
        sd = (fz or {}).get("steady")
        L.append("| %s | %s (%s) | %.0f | %.1f | **%.1f** | %.1f / %.1f | %s | %s | %s |" % (key, c["cam"], cls, c["build_cpu"], c["cpu_first"], m, eb, ea, meas,
                 ("**%.1f** at %d %%" % (sd["cpu_mean"], sd["pct"])) if sd else "not run", ("%+.0f %%" % ((sd["cpu_mean"] / plan - 1) * 100)) if sd else "extrapolated %+.0f %%" % ((est / plan - 1) * 100)))
        tot.append((key, m))
    L += ["", "Per-frame detail is in `out/cost_<SET>.json` (24 records each) and `out/final_<SET>.json`; the frames themselves are in `out/cost/<SET>/` and `out/final/`."]
    open(os.path.join(HERE, "cost_table.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))


# ------------------------------------------------------------------------------------------------- v2 (brighten pass)
V2_PAIRS = [   # (set, camera, what changed)
    ("STAIR", "S111", "lit cages on landings 2-10, beacon spill from the deck, street lamp at the foot; camera 6.2 D from Kong (was 15)"),
    ("STAIR", "LOW", "lower cages lit, foot cage, soffit takes the pier lamps' up-wash; camera 7.3 D (was 15)"),
    ("UND", "S112", "now looks out from under the deck at the stair foot: cages, street lamp, sign, beacon spill (frame 10 = blue); 5.5 D (was 46)"),
    ("UND", "S122", "Kong turned away from the pier, phone throws him onto it; far-side lamp behind; 6.2 D (was 12.4)"),
    ("UND", "S133", "pier lamps + up-wash on the slab, wet street mirrors it; 7.5 D behind the last figure (was 24)"),
    ("X1S", "S62", "sedan on its LEFT side: wheels + underside to the lanes, both headlamps, tail lamps, sodium rim; camera on the shoulder"),
    ("X1S", "S63", "the nose end-on: stacked headlamps, vertical plate, steered front tyre, underside; Praew in the opening strip"),
    ("X1S", "S65", "into the opening from the shoulder north of the nose; steam moved off the opening"),
    ("CAB", "S81", "dash 40->95 W, cluster 2.2->3.4, radio face + channel line, red/blue sweep through the glass (beacon rocker on)"),
    ("CAB", "S84", "framed 0.08 lower: tape labels mid-frame, lit radio display fills the bottom; console spill 22->30 W"),
    ("CAB", "S78", "side effect of the cab's brighter dash/radio (no camera change)"),
    ("CAB", "S88", "side effect of the cab's brighter dash/radio and the beacon sweep (beacon rocker on)"),
    ("GEAR", "S100", "side effect only: the cab's brighter dash / console / radio (no camera change)"),
    ("GEAR", "S101", "side effect only (no camera change)"),
    ("GEAR", "S102", "side effect only (no camera change)"),
    ("GEAR", "WALL", "side effect only (not a planned shot)"),
]


def _cpu_before(key, cam):
    import re
    for fn in ("log2_still_%s.txt" % key, "log_still_%s.txt" % key):
        p = os.path.join(OUT, fn)
        if not os.path.exists(p): continue
        for line in open(p):
            m = re.match(r"STILL %s %s cpu ([0-9.]+)" % (key, cam), line)
            if m: return float(m.group(1))
    return None


def _figtxt(f):
    if not f: return "no figure"
    return ", ".join("%s %.0f%%" % (k, v["h"] * 100) + ("" if v.get("in_frame", True) else " (off frame)") for k, v in sorted(f.items()))


def make_v2():
    from PIL import Image, ImageDraw, ImageFont
    fb = os.path.join(HERE, "..", "..", "fonts", "WorkSans-Black.ttf")
    f = ImageFont.truetype(fb, 22); f2 = ImageFont.truetype(fb, 15); f3 = ImageFont.truetype(fb, 26)
    tw, th, gap, pad, cap = 300, 533, 6, 14, 112
    bw = 2 * tw + gap
    ncol = 3
    blocks = []
    for key, cam, note in V2_PAIRS:
        pb = os.path.join(OUT, "stills", "%s_%s_draft.png" % (key, cam)); pa = os.path.join(OUT, "stills_v2", "%s_%s_draft.png" % (key, cam))
        if not (os.path.exists(pb) and os.path.exists(pa)): continue
        ja = os.path.join(OUT, "stills_v2", "%s_%s_draft.json" % (key, cam))
        ra = json.load(open(ja)) if os.path.exists(ja) else {}
        mb = os.path.join(OUT, "measure_%s_v1.json" % key)
        fbef = (json.load(open(mb)).get(cam) if os.path.exists(mb) else None)
        blocks.append((key, cam, note, pb, pa, ra, fbef, _cpu_before(key, cam)))
    nrow = (len(blocks) + ncol - 1) // ncol
    W = pad + ncol * (bw + pad + 20)
    H = 70 + nrow * (30 + th + cap + pad) + pad
    sh = Image.new("RGB", (W, H), (16, 17, 22)); d = ImageDraw.Draw(sh)
    d.text((pad, 18), "EP.1 sets v2: before / after for every changed camera (draft 360x640, 2 spp; figure height = standing puppet as % of frame height)", font=f3, fill=(240, 240, 235))
    for i, (key, cam, note, pb, pa, ra, fbef, cb) in enumerate(blocks):
        r, c = divmod(i, ncol)
        x = pad + c * (bw + pad + 20); y = 70 + r * (30 + th + cap + pad)
        d.text((x, y + 2), "%s  %s" % (key, cam), font=f, fill=(255, 196, 64))
        y += 30
        for j, (p, tag) in enumerate(((pb, "BEFORE"), (pa, "AFTER"))):
            im = Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS)
            sh.paste(im, (x + j * (tw + gap), y))
            d.rectangle((x + j * (tw + gap), y, x + j * (tw + gap) + 92, y + 24), fill=(0, 0, 0))
            d.text((x + j * (tw + gap) + 6, y + 3), tag, font=f2, fill=(255, 90, 80) if j == 0 else (120, 230, 140))
        yy = y + th + 6
        lines = [note]
        ca = ra.get("cpu")
        if key in ("CAB", "GEAR"): lines.append("figures: seated or close-up, the 35 % floor does not apply")
        else: lines.append("figures: %s  ->  %s" % (_figtxt(fbef) if fbef is not None else "not measured (v1 anchors differ)", _figtxt(ra.get("figs"))))
        lm = os.path.join(OUT, "lum_v2.json")
        if os.path.exists(lm):
            L_ = json.load(open(lm)).get("%s_%s" % (key, cam))
            if L_: lines.append("mean luminance %.3f -> %.3f, near-black pixels %d%% -> %d%%" % (L_["mean_before"], L_["mean_after"], round(L_["black_before"] * 100), round(L_["black_after"] * 100)))
        lines.append("draft CPU s / frame: %s -> %s" % ("%.1f" % cb if cb else "n/a", "%.1f" % ca if ca else "n/a"))
        for ln in lines:
            words = ln.split(" "); cur = ""
            for w_ in words:
                if d.textlength((cur + " " + w_).strip(), font=f2) > bw - 4:
                    d.text((x, yy), cur, font=f2, fill=(205, 210, 220)); yy += 18; cur = w_
                else: cur = (cur + " " + w_).strip()
            if cur: d.text((x, yy), cur, font=f2, fill=(205, 210, 220)); yy += 18
    sh.save(os.path.join(HERE, "sets_sheet_v2.png"))
    print("sheet v2", sh.size, len(blocks), "pairs")


def make_169():
    """the 16:9 check: every planned camera of every set from its planned position at 640x360 (36 mm on the long side)."""
    from PIL import Image, ImageDraw, ImageFont
    import bpy, camdefs
    fb = os.path.join(HERE, "..", "..", "fonts", "WorkSans-Black.ttf")
    f = ImageFont.truetype(fb, 22); f2 = ImageFont.truetype(fb, 15)
    tw, th, pad, head = 480, 270, 10, 40
    ncol = 4
    rows = []
    for key in ORDER:
        tiles = [(cd, os.path.join(OUT, "stills_w169", "%s_%s_draft.png" % (key, cd["name"]))) for cd in camdefs.CAMS[key]]
        rows.append((key, [t for t in tiles if os.path.exists(t[1])]))
    H = sum(head + th + 26 + pad for _ in rows) + pad
    W = pad + ncol * (tw + pad)
    sh = Image.new("RGB", (W, H), (16, 17, 22)); d = ImageDraw.Draw(sh)
    y = pad
    for key, tiles in rows:
        d.text((pad, y + 8), TITLE[key] + "  (16:9 check, same camera position, 36 mm on the long side)", font=f, fill=(240, 240, 235))
        y += head
        for i, (cd, p) in enumerate(tiles[:ncol]):
            im = Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS)
            x = pad + i * (tw + pad); sh.paste(im, (x, y))
            d.text((x + 2, y + th + 4), cd["name"], font=f2, fill=(200, 205, 215))
        y += th + 26 + pad
    sh.save(os.path.join(HERE, "sets_169_check.png"))
    print("sheet 16:9", sh.size)
