"""retime_shots.py -- plan/shots_ep1.json + narr_ep1_timing.json -> plan/shots_ep1_timed.json (same schema, real times).

Rules (the plan's cut-on-word list, as ep1/pipe/cut.py reads it, with the picture beats held at their planned lengths):
  word      a shot whose cut_on is one of its own captions starts on that caption's first frame;
  first     the first new shot starts where the hook ends (53.32 s, frame 1280);
  lead      a picture-beat shot in which a caption begins starts the plan's lead before that caption (S36 0.30 s before '30 วินาที');
  carry     a picture-beat shot that only carries the end of a caption begun in the shot before starts at the same proportion
            through that caption's voiced length as in the plan (S160: black as 'ใคร' ends);
  beat      a picture-only shot (no caption) keeps its planned frame count and ends on the next shot's start;
  end       the two closing shots (black, end card) keep their planned frame counts.
A shot that would come out under MIN_FRAMES takes frames from its longer neighbour and is flagged in "how".
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); PLAN = os.path.join(HERE, "..", "plan"); FPS = 24; MIN_FRAMES = 12; TAILM = 0.38
def main():
    D = json.load(open(os.path.join(PLAN, "shots_ep1.json"), encoding="utf8")); N = json.load(open(os.path.join(PLAN, "narration_ep1.json"), encoding="utf8"))
    T = json.load(open(os.path.join(HERE, "narr_ep1_timing.json"), encoding="utf8"))
    real = {(c["id"], c["text"]): c for c in T["captions"]}; plan = {}
    for s in N["sentences"]:
        for i, c in enumerate(s["captions"]):
            plan[(s["id"], c["text"])] = dict(t0=c["t0"], v1=c["t1"] - (TAILM if i == len(s["captions"]) - 1 else 0.0))
    FIX = {"แต่เขาจะฟาด": "แต่เขาจะหวด"}                       # s101 was re-recorded with the user's wording; shots_ep1.json still has the old word
    shots = json.loads(json.dumps(D["shots"])); fixed = []
    for s in shots:
        if s["cut_on"] in FIX: s["cut_on"] = FIX[s["cut_on"]]; fixed.append(s["id"] + ".cut_on")
        for n in s["narration"]:
            if any(c in FIX for c in n["captions"]): n["captions"] = [FIX.get(c, c) for c in n["captions"]]; fixed.append(s["id"] + ".narration")
    miss = [(s["id"], n["id"], c) for s in shots for n in s["narration"] for c in n["captions"] if (n["id"], c) not in real]
    if miss: raise SystemExit("captions the timing file does not have: %s" % miss)
    n = len(shots); start = [None] * n; how = [""] * n
    for i, s in enumerate(shots):
        own = [(m["id"], c) for m in s["narration"] for c in m["captions"]]
        w = [k for k in own if k[1] == s["cut_on"]]
        if i == 0: start[i] = T["hook_end"]; how[i] = "first: the hook's end"
        elif w: start[i] = real[w[0]]["t0"]; how[i] = "word"
        elif own:
            begun = [k for k in own if plan[k]["t0"] >= s["t0"] - 1e-3]
            if begun:
                lead = plan[begun[0]]["t0"] - s["t0"]; start[i] = real[begun[0]]["t0"] - lead; how[i] = "lead: %.2f s before %r" % (lead, begun[0][1])
            else:
                k = own[-1]; u = (s["t0"] - plan[k]["t0"]) / max(plan[k]["v1"] - plan[k]["t0"], 1e-6); r = real[k]
                start[i] = r["t0"] + u * (r["voice_end"] - r["t0"]); how[i] = "carry: %.0f %% through %r" % (100 * u, k[1])
    f = [None if t is None else int(round(t * FPS)) for t in start] + [None]
    # closing shots and pure beats
    for i in range(n - 1, -1, -1):
        if f[i] is None:                                             # pure picture beat: planned length, ending on the next start
            if i == n - 1: continue
            f[i] = f[i + 1] - shots[i]["frames"] if f[i + 1] is not None else None; how[i] = "beat: planned %d frames, ends on the next cut" % shots[i]["frames"]
    if f[n - 1] is None:                                             # the end card after the black
        f[n - 1] = f[n - 2] + shots[n - 2]["frames"]; how[n - 1] = "end: planned length after %s" % shots[n - 2]["id"]; how[n - 2] += "; planned %d frames" % shots[n - 2]["frames"]
    f[n] = f[n - 1] + shots[n - 1]["frames"]
    assert all(x is not None for x in f)
    for i in range(n):                                               # short shots: take from the longer neighbour
        L = f[i + 1] - f[i]
        if L < MIN_FRAMES:
            need = MIN_FRAMES - L; prevL = f[i] - f[i - 1] if i else 0; nextL = f[i + 2] - f[i + 1] if i + 1 < n else 0
            if nextL - need >= prevL - need and nextL - need >= MIN_FRAMES: f[i + 1] += need; how[i] += "; +%d frames from %s (was %d)" % (need, shots[i + 1]["id"], L); how[i + 1] += "; starts %d frames late for %s" % (need, shots[i]["id"])
            elif prevL - need >= MIN_FRAMES: f[i] -= need; how[i] += "; starts %d frames early, taken from %s (was %d)" % (need, shots[i - 1]["id"], L)
            else: raise SystemExit("cannot make %s %d frames" % (shots[i]["id"], MIN_FRAMES))
    out = []
    for i, s in enumerate(shots):
        q = dict(s); L = f[i + 1] - f[i]; assert L >= MIN_FRAMES, (s["id"], L)
        q.update(t0=round(f[i] / FPS, 3), t1=round(f[i + 1] / FPS, 3), f0=f[i], f1=f[i + 1], frames=L, plan_frames=s["frames"], plan_f0=s["f0"], how=how[i]); out.append(q)
    cost = D["totals"]["cpu_s_per_frame"]; doc = json.loads(json.dumps(D)); doc["shots"] = out
    doc["note"] = "RETIMED to the recorded narration (ep1/audio/narr_ep1_timing.json) by ep1/audio/retime_shots.py; the plan's estimate is shots_ep1.json. Each shot has plan_frames, plan_f0 and how (the rule that placed its first frame). " + D.get("note", "")
    tot = f[n]; doc["episode"].update(new_frames=[f[0], tot], running_time="%d:%05.2f" % (tot / FPS // 60, tot / FPS % 60), frames_total=tot, seconds=round(tot / FPS, 3))
    table = []
    for sc in doc["scenes"]:
        ss = [q for q in out if q["scene"] == sc["scene"]]; by = {}
        for q in ss: by[q["cls"]] = by.get(q["cls"], 0) + q["frames"]
        old = dict(frames=sc["frames"], seconds=sc["seconds"], t0=sc["t0"], t1=sc["t1"])
        cpu = sum(by[c] * cost[c] for c in by) / 3600.0
        sc.update(t0=ss[0]["t0"], t1=ss[-1]["t1"], seconds=round(ss[-1]["t1"] - ss[0]["t0"], 2), frames=ss[-1]["f1"] - ss[0]["f0"], f0=ss[0]["f0"], f1=ss[-1]["f1"],
                  A=by.get("A", 0), B=by.get("B", 0), C2=by.get("C2", 0), C1=by.get("C1", 0), cpu_h=round(cpu, 1), wall_h=round(cpu * 1.08 / 4, 1), cpu_h_allow=round(cpu * 1.35, 1), wall_h_allow=round(cpu * 1.35 * 1.08 / 4, 1),
                  draft_cpu_h=round(sc["draft_cpu_h"] * (ss[-1]["f1"] - ss[0]["f0"]) / old["frames"], 1), draft_wall_h=round(sc["draft_wall_h"] * (ss[-1]["f1"] - ss[0]["f0"]) / old["frames"], 1), plan_frames=old["frames"], plan_seconds=old["seconds"])
        table.append(dict(scene=sc["scene"], shots=len(ss), plan_frames=old["frames"], frames=sc["frames"], delta_frames=sc["frames"] - old["frames"], plan_s=old["seconds"], s=sc["seconds"], pct=round(100.0 * (sc["frames"] / old["frames"] - 1), 1),
                          t0=sc["t0"], t1=sc["t1"], f0=sc["f0"], f1=sc["f1"], cpu_h=sc["cpu_h"], plan_cpu_h=round(sum(q["plan_frames"] * cost[q["cls"]] for q in ss) / 3600.0, 1)))
    by = {}; bs = {}
    for q in out: by[q["cls"]] = by.get(q["cls"], 0) + q["frames"]; bs[q["set"]] = bs.get(q["set"], 0) + q["frames"]
    cpu = sum(by[c] * cost[c] for c in by) / 3600.0; newf = tot - f[0]
    doc["totals"].update(frames_by_class=by, frames_by_set=bs, frames_by_scene={t["scene"]: t["frames"] for t in table}, mean_shot_s=round(newf / FPS / n, 2), cpu_hours=round(cpu, 1), wall_hours_4_cores=round(cpu * 1.08 / 4, 1),
                         cpu_hours_with_35pct_allowance=round(cpu * 1.35, 1), wall_hours_with_35pct_allowance=round(cpu * 1.35 * 1.08 / 4, 1))
    table.append(dict(scene="new picture", shots=n, plan_frames=D["episode"]["new_frames"][1] - D["episode"]["new_frames"][0], frames=newf, delta_frames=newf - (D["episode"]["new_frames"][1] - D["episode"]["new_frames"][0]),
                      plan_s=round((D["episode"]["new_frames"][1] - D["episode"]["new_frames"][0]) / FPS, 2), s=round(newf / FPS, 2), pct=round(100.0 * (newf / (D["episode"]["new_frames"][1] - D["episode"]["new_frames"][0]) - 1), 1), cpu_h=round(cpu, 1), plan_cpu_h=D["totals"]["cpu_hours"]))
    table.append(dict(scene="episode with hook", plan_frames=D["episode"]["new_frames"][1], frames=tot, delta_frames=tot - D["episode"]["new_frames"][1], plan_s=round(D["episode"]["new_frames"][1] / FPS, 2), s=round(tot / FPS, 2), running_time=doc["episode"]["running_time"], plan_running_time=D["episode"]["running_time"]))
    doc["retime"] = dict(source="ep1/audio/narr_ep1_timing.json", rules=__doc__, plan_text_fixes=fixed, table=table,
                         adjusted=[dict(id=q["id"], how=q["how"]) for q in out if "frames from" in q["how"] or "frames late" in q["how"] or "frames early" in q["how"]])
    # the narration wav and its timing file get the episode's exact length
    import wave
    wp = os.path.join(HERE, "narr_ep1.wav"); w = wave.open(wp); sr = w.getframerate(); x = w.readframes(w.getnframes()); w.close()
    want = int(round(tot / float(FPS) * sr)) * 2; x = (x + b"\0" * max(0, want - len(x)))[:want]
    w = wave.open(wp, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(x); w.close()
    T.update(episode_frames=tot, episode_seconds=round(tot / float(FPS), 4), wav_seconds=round(want / 2 / sr, 4), shots="ep1/plan/shots_ep1_timed.json")
    json.dump(T, open(os.path.join(HERE, "narr_ep1_timing.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
    json.dump(doc, open(os.path.join(PLAN, "shots_ep1_timed.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
    for q in out: print("%-5s %s %-2s %5d..%-5d %4d f (plan %3d, %+4d)  %s" % (q["id"], q["scene"], q["cls"], q["f0"], q["f1"], q["frames"], q["plan_frames"], q["frames"] - q["plan_frames"], q["how"]))
    for t in table: print(t)
    print("fixed", fixed)
if __name__ == "__main__":
    main()
