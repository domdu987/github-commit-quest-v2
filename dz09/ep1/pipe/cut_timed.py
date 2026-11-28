"""cut_timed.py -- a scene's production shot table from the RECORDED timing of the whole episode.

    python3 cut_timed.py --scene 02            -> cut/sc02.json  (the plan-estimate table it replaces is kept as cut/sc02_plan.json)

Sources (written by the narration pass, ep1/audio):
    plan/shots_ep1_timed.json      every shot's real frame range on the EPISODE clock (word cuts on their caption's first frame,
                                   the picture beats by the rules in its `retime` block)
    audio/narr_ep1_timing.json     every caption's real start / end on the episode clock (narr_ep1.wav sample 0 = film time 0)
    plan/narration_ep1.json        speaker per sentence
    cut/scNN.cfg.json (optional)   hard_cuts, fx, cues, mix, ... as for cut.py

Why not cut.py: cut.py places picture-beat shots by the plan's proportion between word cuts, while the shot authors staged
against shots_ep1_timed.json (lead-in / carry rules, see that file's `retime` block); the two differ by a few frames on
S35, S36, S44-S47 and S58.  This tool keeps the timed frames exactly, so the cut, the authors' stills and the narration agree.
The table has cut.py's shape plus `film_f0` (episode frame of the scene's first frame).  narr0 = -film_f0 / 24, because
narr_ep1.wav starts at film time 0; mouth.py then reads the same wav at the right place.
"""
import os, sys, json, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import epcommon as E

FPS = E.FPS


def build(sc, cfg):
    timed = json.load(open(os.path.join(E.EP1, "plan", "shots_ep1_timed.json"), encoding="utf-8"))
    tim = json.load(open(os.path.join(E.EP1, "audio", "narr_ep1_timing.json"), encoding="utf-8"))
    narr = json.load(open(os.path.join(E.EP1, "plan", "narration_ep1.json"), encoding="utf-8"))
    spk = {s["id"]: s.get("speaker", "narr") for s in narr["sentences"]}
    sh = [s for s in timed["shots"] if s["scene"] == sc]
    if not sh:
        raise SystemExit("scene %s has no shots in shots_ep1_timed.json" % sc)
    F0 = sh[0]["f0"]; T0 = F0 / float(FPS)
    for a, b in zip(sh, sh[1:]):
        if a["f1"] != b["f0"]:
            raise SystemExit("shots_ep1_timed.json: %s ends at %d but %s starts at %d" % (a["id"], a["f1"], b["id"], b["f0"]))
    shots = [dict(id=E.norm_id(s["id"]), plan_id=s["id"], f0=s["f0"] - F0, f1=s["f1"] - F0, frames=s["frames"], plan_frames=s.get("plan_frames", s["frames"]),
                  cls=s["cls"], set=s["set"], size=s.get("size", ""), cut_on=s.get("cut_on", ""), how=s.get("how", ""), narration=s.get("narration", []),
                  action=s.get("action", "")) for s in sh]
    want = [(n["id"], c) for s in sh for n in s.get("narration", []) for c in n["captions"]]
    pool = [c for c in tim["captions"]]
    caps, miss = [], []
    for sid, text in want:
        hit = next((c for c in pool if c["id"] == sid and c["text"] == text), None)
        if hit is None:
            miss.append((sid, text)); continue
        if any(x["id"] == sid and x["text"] == text for x in caps):
            continue                                       # a caption carried by two shots (a carry / lead shot) is one caption
        row = dict(id=sid, text=text, t0=round(hit["t0"] - T0, 4), t1=round(hit["t1"] - T0, 4), speaker=spk.get(sid, "narr"))
        if hit.get("emph"): row.update(emph=hit["emph"], colour=hit.get("colour") or "amber")
        caps.append(row)
    if miss:
        raise SystemExit("captions named by the shots but not in narr_ep1_timing.json: %s" % miss)
    caps.sort(key=lambda c: c["t0"])
    by = {}
    for r in shots: by[r["cls"]] = by.get(r["cls"], 0) + r["frames"]
    cost = timed.get("totals", {}).get("cpu_s_per_frame", {"A": 68.2, "B": 36.6, "C2": 32.0, "C1": 2.0})
    nframes = shots[-1]["f1"]
    return dict(scene=E.scene_name(sc), source="shots_ep1_timed.json + narr_ep1_timing.json (cut_timed.py)", timing_file=os.path.join("ep1", "audio", "narr_ep1_timing.json"),
                narr0=round(-T0, 6), film_f0=F0, fps=FPS, g_base=int(cfg.get("g_base", int(sc) * E.G_PER_SCENE)), frames=nframes, seconds=round(nframes / float(FPS), 3),
                plan_frames=sum(r["plan_frames"] for r in shots), frames_by_class=by,
                final_cpu_h_estimate=round(sum(by[c] * cost.get(c, 60.0) for c in by) / 3600.0, 2),
                hard_cuts=[E.norm_id(x) for x in cfg.get("hard_cuts", [])], fx=cfg.get("fx", []),
                cues={k: (float(v) if not isinstance(v, dict) else round(next(c["t0"] for c in caps if c["text"] == v["word"] and (not v.get("sid") or c["id"] == v["sid"])) + float(v.get("dt", 0.0)), 4))
                      for k, v in cfg.get("cues", {}).items()},
                mix=cfg.get("mix", ""), narration_wav=cfg.get("narration_wav", "ep1/audio/narr_ep1.wav"), warnings=[], shots=shots, captions=caps)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", required=True); ap.add_argument("--out", default="")
    a = ap.parse_args()
    sc = "%02d" % int(str(a.scene).lower().lstrip("sc"))
    name = E.scene_name(sc)
    out = a.out or os.path.join(HERE, "cut", name + ".json")
    cfg_p = out[:-5] + ".cfg.json"
    cfg = json.load(open(cfg_p, encoding="utf-8")) if os.path.exists(cfg_p) else {}
    cut = build(sc, cfg)
    if os.path.exists(out):
        old = json.load(open(out, encoding="utf-8"))
        if old.get("source") == "plan" and not os.path.exists(out[:-5] + "_plan.json"):
            os.replace(out, out[:-5] + "_plan.json"); print("kept the plan-estimate table as", out[:-5] + "_plan.json")
    json.dump(cut, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("%s: %d shots, %d frames = %.2f s (film frames %d..%d), %d captions, narr0 %.4f, est. final %.1f CPU h %s" % (
        name, len(cut["shots"]), cut["frames"], cut["seconds"], cut["film_f0"], cut["film_f0"] + cut["frames"], len(cut["captions"]), cut["narr0"],
        cut["final_cpu_h_estimate"], cut["frames_by_class"]))
    print("wrote", out)


if __name__ == "__main__":
    main()
