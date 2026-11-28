"""cut.py -- build a scene's shot table (cut-on-word) from the plan's shot list and a caption-timing file.

    python3 cut.py --scene 02                                  plan times (the fallback until the recording exists)
    python3 cut.py --scene 02 --timing PROJ/audio/ep1/sc02/captions_timing.json [--narr0 0.30]
    python3 cut.py --all                                       every scene of the plan, plan times
    options: --shots shots_ep1.json  --narration narration_ep1.json  --cfg cut/sc02.cfg.json  --out cut/sc02.json

The timing file has the hook's shape: [{"id": "s17", "text": "เหลืออีก", "t0": 0.0, "t1": 0.63}, ...], seconds from the
start of the scene's narration wav.  narr0 is the lead-in before that wav starts in the scene.

Rules
  1. the scene's first shot starts at 0;
  2. a shot whose `cut_on` is one of its own captions starts on that caption's t0 (+ narr0);
  3. a picture-beat shot (no word) keeps its place BETWEEN the two word cuts round it, in the plan's proportion;
  4. the scene ends at the last caption's end + the plan's tail (plan scene end - plan last caption end);
  5. the cfg file may pin any cut:  {"pin": {"S36": {"word": "30 วินาที", "sid": "s23", "dt": -0.30}}}  or  {"S47": {"t": 46.0}};
     it also carries narr0, cues ({"name": {"word": .., "dt": ..} | seconds}), hard_cuts and fx for finish_ep.
Every caption of the plan must be in the timing file (same sentence id, same text, same order) or the tool stops.
"""
import os, sys, json, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import epcommon as E

PLAN = os.path.join(E.EP1, "plan")
FPS = E.FPS
MIN_FRAMES = 8


def plan_timing(sents, t_scene0):
    """the fallback: the plan's estimated caption times as a timing file (narr0 = the first caption's offset)."""
    caps = [dict(id=s["id"], text=c["text"], t0=c["t0"], t1=c["t1"]) for s in sents for c in s["captions"]]
    narr0 = round(caps[0]["t0"] - t_scene0, 4) if caps else 0.0
    return [dict(c, t0=round(c["t0"] - t_scene0 - narr0, 4), t1=round(c["t1"] - t_scene0 - narr0, 4)) for c in caps], narr0


def build(scene_no, shots_doc, narr_doc, timing=None, narr0=None, cfg=None, timing_path=None):
    cfg = cfg or {}
    sc = "%02d" % int(scene_no) if str(scene_no).isdigit() else str(scene_no)
    shots = [s for s in shots_doc["shots"] if s["scene"] == sc]
    sents = [s for s in narr_doc["sentences"] if s["scene"] == sc]
    if not shots:
        raise SystemExit("scene %s has no shots in the plan" % sc)
    meta = [m for m in shots_doc.get("scenes", []) if m["scene"] == sc]
    T0 = meta[0]["t0"] if meta else shots[0]["t0"]
    T1 = meta[0]["t1"] if meta else shots[-1]["t1"]
    # the two plan files must agree before anything is timed: a caption a shot names that the narration does not have
    # (a word changed in one file only) would otherwise surface as a lost cut, or after a paid recording
    have = {(s["id"], c["text"]) for s in sents for c in s["captions"]}
    bad = ["%s names caption %r of %s, which narration has as %s" % (s["id"], c, n["id"], [x["text"] for q in sents if q["id"] == n["id"] for x in q["captions"]] or "no such sentence")
           for s in shots for n in s.get("narration", []) for c in n["captions"] if (n["id"], c) not in have]
    used = {(n["id"], c) for s in shots for n in s.get("narration", []) for c in n["captions"]}
    bad += ["caption %r of %s is in the narration but no shot of scene %s carries it" % (c, i, sc) for i, c in sorted(have - used)]
    if bad:
        raise SystemExit("cut.py scene %s: shots and narration plan files disagree (fix the plan, nothing written):\n  " % sc + "\n  ".join(bad))
    plan_caps, plan_narr0 = plan_timing(sents, T0)
    source = "recording"
    if timing is None:
        timing, source = plan_caps, "plan"
        if narr0 is None: narr0 = plan_narr0
    if narr0 is None:
        narr0 = cfg.get("narr0", plan_narr0)
    # ---- captions: plan order, real times; the plan's emph / colour / speaker ride along
    pool = list(timing)
    caps, problems = [], []
    for s in sents:
        for c in s["captions"]:
            hit = next((i for i, x in enumerate(pool) if x.get("id") == s["id"] and x["text"] == c["text"]), None)
            if hit is None:
                problems.append("caption %s %r is not in the timing file" % (s["id"], c["text"]))
                continue
            x = pool.pop(hit)
            row = dict(id=s["id"], text=c["text"], t0=round(x["t0"] + narr0, 4), t1=round(x["t1"] + narr0, 4), speaker=s.get("speaker", "narr"))
            if c.get("emph"): row.update(emph=c["emph"], colour=c.get("colour", "amber"))
            caps.append(row)
    if pool:
        problems.append("timing file has %d captions the plan does not: %s" % (len(pool), [(x.get("id"), x["text"]) for x in pool[:5]]))
    if problems:
        raise SystemExit("cut.py scene %s:\n  " % sc + "\n  ".join(problems))
    for a, b in zip(caps, caps[1:]):
        if b["t0"] < a["t0"] - 1e-6:
            raise SystemExit("captions out of order: %r after %r" % (b["text"], a["text"]))

    def cap_t(text, sid=None):
        for c in caps:
            if c["text"] == text and (sid is None or c["id"] == sid):
                return c["t0"]
        raise SystemExit("cut.py: caption %r (%s) not found" % (text, sid))

    plan_end_tail = T1 - max([c["t1"] for s in sents for c in s["captions"]] or [T1])
    end = (max(c["t1"] for c in caps) if caps else 0.0) + max(plan_end_tail, 0.0)
    if "end" in cfg: end = float(cfg["end"])
    # ---- anchors
    pin = cfg.get("pin", {})
    start = [None] * len(shots); how = [""] * len(shots)
    for i, s in enumerate(shots):
        p = pin.get(s["id"]) or pin.get(E.norm_id(s["id"]))
        if p is not None:
            start[i] = float(p["t"]) if "t" in p else cap_t(p["word"], p.get("sid")) + float(p.get("dt", 0.0)); how[i] = "pin"
        elif i == 0:
            start[i] = 0.0; how[i] = "scene start"
        else:
            own = [(n["id"], c) for n in s.get("narration", []) for c in n["captions"]]
            m = [sid for sid, c in own if c == s.get("cut_on")]
            if m:
                start[i] = cap_t(s["cut_on"], m[0]); how[i] = "word"
    # ---- picture beats: the plan's proportion between the anchors round them
    anchors = [i for i in range(len(shots)) if start[i] is not None]
    for i in range(len(shots)):
        if start[i] is not None: continue
        a = max(j for j in anchors if j < i)
        nb = [j for j in anchors if j > i]
        pa = shots[a]["t0"]; pb = shots[nb[0]]["t0"] if nb else T1
        ra = start[a]; rb = start[nb[0]] if nb else end
        u = (shots[i]["t0"] - pa) / max(pb - pa, 1e-6)
        start[i] = ra + u * (rb - ra); how[i] = "beat (%.0f %% between %s and %s)" % (100 * u, shots[a]["id"], shots[nb[0]]["id"] if nb else "end")
    f = [int(round(t * FPS)) for t in start] + [int(round(end * FPS))]
    if source == "plan" and not pin and "end" not in cfg and all("f0" in s for s in shots):
        # the plan rounded on the episode clock: keep its frame numbers exactly (scene-local rounding moves 1 frame here and there)
        f = [s["f0"] - shots[0]["f0"] for s in shots] + [shots[-1]["f1"] - shots[0]["f0"]]
    rows, warn = [], []
    for i, s in enumerate(shots):
        f0, f1 = f[i], f[i + 1]
        if f1 - f0 < MIN_FRAMES:
            warn.append("%s is %d frames (plan %d)" % (s["id"], f1 - f0, s["frames"]))
        if f1 <= f0:
            raise SystemExit("cut.py: %s has no frames (%d..%d); pin it in the cfg" % (s["id"], f0, f1))
        rows.append(dict(id=E.norm_id(s["id"]), plan_id=s["id"], f0=f0, f1=f1, frames=f1 - f0, plan_frames=s["frames"], cls=s["cls"], set=s["set"],
                         size=s.get("size", ""), cut_on=s.get("cut_on", ""), how=how[i], narration=s.get("narration", []), action=s.get("action", "")))
    # ---- cues
    cues = {}
    for k, v in cfg.get("cues", {}).items():
        cues[k] = float(v) if not isinstance(v, dict) else round(cap_t(v["word"], v.get("sid")) + float(v.get("dt", 0.0)), 4)
    name = E.scene_name(sc)
    cost = shots_doc.get("totals", {}).get("cpu_s_per_frame", {"A": 68.2, "B": 36.6, "C2": 32.0, "C1": 2.0})
    by = {}
    for r in rows: by[r["cls"]] = by.get(r["cls"], 0) + r["frames"]
    out = dict(scene=name, source=source, timing_file=timing_path or "(plan estimate: %s)" % os.path.basename(PLAN), narr0=round(narr0, 4), fps=FPS,
               g_base=int(cfg.get("g_base", int(sc) * E.G_PER_SCENE if sc.isdigit() else 0)), frames=f[-1], seconds=round(f[-1] / float(FPS), 3),
               plan_frames=sum(s["frames"] for s in shots), frames_by_class=by,
               final_cpu_h_estimate=round(sum(by[c] * cost.get(c, 60.0) for c in by) / 3600.0, 2),
               hard_cuts=[E.norm_id(x) for x in cfg.get("hard_cuts", [])], fx=cfg.get("fx", []), cues=cues, mix=cfg.get("mix", ""), narration_wav=cfg.get("narration_wav", ""),
               warnings=warn, shots=rows, captions=caps)
    return out


def report(cut):
    print("%s  source=%s  narr0=%.2f  %d frames = %.2f s (plan %d)  est. final %.1f CPU h  %s" % (
        cut["scene"], cut["source"], cut["narr0"], cut["frames"], cut["seconds"], cut["plan_frames"], cut["final_cpu_h_estimate"], cut["frames_by_class"]))
    for r in cut["shots"]:
        d = r["frames"] - r["plan_frames"]
        print("  %s %-2s %-4s %5d..%-5d %4d f (%+d)  %s%s" % (r["id"], r["cls"], r["set"], r["f0"], r["f1"], r["frames"], d, r["how"],
                                                             ("  on %r" % r["cut_on"]) if r["how"] == "word" else ""))
    for w in cut["warnings"]:
        print("  WARNING short shot:", w)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", default=""); ap.add_argument("--all", action="store_true")
    ap.add_argument("--shots", default=os.path.join(PLAN, "shots_ep1.json")); ap.add_argument("--narration", default=os.path.join(PLAN, "narration_ep1.json"))
    ap.add_argument("--timing", default=""); ap.add_argument("--narr0", type=float, default=None)
    ap.add_argument("--cfg", default=""); ap.add_argument("--out", default=""); ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    sd = json.load(open(a.shots, encoding="utf-8")); nd = json.load(open(a.narration, encoding="utf-8"))
    scenes = sorted(set(s["scene"] for s in sd["shots"])) if a.all else [a.scene]
    for sc in scenes:
        name = E.scene_name(sc)
        out = a.out or os.path.join(HERE, "cut", name + ".json")
        cfg_p = a.cfg or out[:-5] + ".cfg.json"
        cfg = json.load(open(cfg_p, encoding="utf-8")) if os.path.exists(cfg_p) else {}
        timing = json.load(open(a.timing, encoding="utf-8")) if a.timing else None
        cut = build(sc, sd, nd, timing, a.narr0, cfg, os.path.abspath(a.timing) if a.timing else None)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        json.dump(cut, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        if not a.quiet: report(cut)
        print("wrote", out)


if __name__ == "__main__":
    main()
