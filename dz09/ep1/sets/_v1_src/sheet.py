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
