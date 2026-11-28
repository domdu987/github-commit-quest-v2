"""check.py -- checks on narr_ep1.wav, narr_ep1_timing.json, captions_ep1.ass and plan/shots_ep1_timed.json -> check_report.json"""
import json, os, sys, re, subprocess, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import measure as M, build_narr as B
SR = M.SR; FPS = 24; BITE = 43.795
def lufs(path, ss=None):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats"] + (["-ss", str(ss)] if ss else []) + ["-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1]), float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)[-1])
def main():
    T = json.load(open(os.path.join(HERE, "narr_ep1_timing.json"), encoding="utf8")); N = json.load(open(os.path.join(M.PROJ, "ep1", "plan", "narration_ep1.json"), encoding="utf8"))
    D = json.load(open(os.path.join(M.PROJ, "ep1", "plan", "shots_ep1_timed.json"), encoding="utf8")); P = json.load(open(os.path.join(M.PROJ, "ep1", "plan", "shots_ep1.json"), encoding="utf8"))
    x = M.load(os.path.join(HERE, "narr_ep1.wav")); S = T["sentences"]; C = T["captions"]; R = {}; bad = []
    # 1 sentences
    R["sentences"] = len(S); R["order_as_plan"] = [s["id"] for s in S] == [s["id"] for s in N["sentences"]]
    ov = [(a["id"], b["id"]) for a, b in zip(S, S[1:]) if a["end"] > b["start"] + 1e-6 or a["voice_end"] > b["start"] - 0.15]; R["sentence_overlaps"] = ov
    R["min_silence_between_voices_s"] = round(min(b["start"] - a["voice_end"] for a, b in zip(S, S[1:])), 3)
    # 2 captions
    byid = {s["id"]: s for s in S}; out = [(c["id"], c["text"]) for c in C if not (byid[c["id"]]["start"] - 1e-6 <= c["t0"] < c["t1"] <= byid[c["id"]]["end"] + 1e-6)]
    R["captions"] = len(C); R["captions_outside_their_sentence"] = out; R["captions_out_of_order"] = [(a["text"], b["text"]) for a, b in zip(C, C[1:]) if b["t0"] < a["t1"] - 1e-6]
    R["caption_text_equals_plan"] = [(c["id"], c["text"]) for c in C] == [(s["id"], q["text"]) for s in N["sentences"] for q in s["captions"]]
    R["emph_equals_plan"] = [(c["emph"], c["colour"]) for c in C] == [(q.get("emph", ""), q.get("colour", "") if q.get("emph") else "") for s in N["sentences"] for q in s["captions"]]
    R["shortest_captions"] = sorted((round(c["t1"] - c["t0"], 2), c["id"], c["text"]) for c in C)[:6]
    ass = [l for l in open(os.path.join(HERE, "captions_ep1.ass"), encoding="utf8").read().split("\n") if l.startswith("Dialogue:")]
    R["ass_lines"] = dict(total=len(ass), cap=sum(",Cap," in l for l in ass), title=sum(",Title," in l for l in ass), coloured_new=sum("\\c&H" in l for l in ass[-len(C):]))
    # 3 level
    hook = T["level"]["hook_sentence_rms_db"]; hm = T["level"]["hook_median_db"]; lev = {}
    for s in S: lev[s["id"]] = round(B.act_rms_db(x[int(s["start"] * SR):int(s["voice_end"] * SR)]), 2)
    R["level"] = dict(hook_median_db=hm, hook_min_db=min(hook.values()), hook_max_db=max(hook.values()), ep_median_db=round(float(np.median(list(lev.values()))), 2), ep_min_db=min(lev.values()), ep_max_db=max(lev.values()),
                      over_2db_from_hook_median=[(k, v) for k, v in lev.items() if abs(v - hm) > 2.0], peak=round(float(np.abs(x).max()), 3), per_sentence_db=lev)
    hl = lufs(os.path.join(M.PROJ, "audio", "narr_ohm", "narr_final.wav")); el = lufs(os.path.join(HERE, "narr_ep1.wav"), 53.32)
    R["level"].update(hook_narration_lufs=hl[0], hook_narration_peak_dbfs=hl[1], ep_narration_lufs_from_53_32=el[0], ep_narration_peak_dbfs=el[1])
    R["silent_under_hook"] = bool(np.abs(x[:int(53.6 * SR)]).max() == 0.0); R["wav_seconds"] = len(x) / SR
    R["limiter"] = dict(sentences_reduced_over_3db=[(s["id"], s["limiter_max_reduction_db"]) for s in S if s["limiter_max_reduction_db"] < -3.0])
    # 4 shots
    sh = D["shots"]; R["shots"] = len(sh); R["shots_contiguous"] = all(a["f1"] == b["f0"] for a, b in zip(sh, sh[1:])) and sh[0]["f0"] == 1280
    R["shortest_shots"] = sorted((q["frames"], q["id"]) for q in sh)[:6]; R["shots_under_12"] = [q["id"] for q in sh if q["frames"] < 12]
    cap = {(c["id"], c["text"]): c for c in C}; off = []
    for q in sh:
        w = [(n["id"], c) for n in q["narration"] for c in n["captions"] if c == q["cut_on"]]
        if w and q["f0"] != int(round(cap[w[0]]["t0"] * FPS)): off.append((q["id"], q["f0"], round(cap[w[0]]["t0"] * FPS, 2)))
    R["word_cuts_off_their_caption"] = off; pp = {q["id"]: q for q in P["shots"]}
    R["picture_only_beats"] = [(q["id"], q["frames"], pp[q["id"]]["frames"]) for q in sh if not q["narration"]]
    env = np.convolve(np.abs(x), np.ones(480) / 480, 'same')
    R["voice_inside_picture_only_beats"] = [q["id"] for q in sh if not q["narration"] and env[int(q["t0"] * SR):int(q["t1"] * SR)].max() > 0.006]
    R["voice_after_black"] = bool(env[int(sh[-2]["t0"] * SR):].max() > 0.006)
    R["episode"] = dict(frames=sh[-1]["f1"], seconds=round(sh[-1]["f1"] / FPS, 3), running_time=D["episode"]["running_time"], plan_frames=P["episode"]["new_frames"][1])
    R["scenes"] = [dict(scene=s["scene"], f0=s["f0"], f1=s["f1"], frames=s["frames"], plan_frames=s["plan_frames"], seconds=s["seconds"]) for s in D["scenes"]]
    # 5 the countdown, seconds after the bite
    R["countdown_after_bite_s"] = {k: round(cap[k]["t0"] - BITE, 2) for k in [("s17", "50 วินาที"), ("s23", "30 วินาที"), ("s31", "10 วินาที"), ("s33", "ก็ลืมตา")]}
    R["countdown_after_bite_s"] = {"%s %s" % k: v for k, v in R["countdown_after_bite_s"].items()}
    R["watch_shots_after_bite_s"] = {q["id"]: [round(q["t0"] - BITE, 2), round(q["t1"] - BITE, 2)] for q in sh if q["id"] in ("S26", "S36", "S44", "S47")}
    # 6 the takes
    R["tempo_changed"] = [(s["id"], s["tempo"]) for s in S if abs(s["tempo"] - 1) > 1e-3]
    R["pauses_shortened"] = [(s["id"], s["pause_cap"], s["pauses_shortened"]) for s in S if s["pauses_shortened"]]
    Mx = {r["id"]: r for r in json.load(open(os.path.join(HERE, "measure.json"), encoding="utf8"))}
    ons = {}
    for s in S:
        raw = M.load(os.path.join(M.TAKES, s["take"] + ".wav")); e = np.convolve(np.abs(raw), np.ones(240) / 240, 'same'); i = np.where(e > 0.01)[0]
        ons[s["id"]] = (round(i[0] / SR * 1000, 1), round((len(raw) - i[-1]) / SR * 1000, 1), round(float(np.abs(raw[:48]).max()), 4), round(float(np.abs(raw[-48:]).max()), 4))
    R["takes_voice_within_10ms_of_file_start"] = [(k, v[0], v[2]) for k, v in ons.items() if v[0] < 10]
    R["takes_voice_within_10ms_of_file_end"] = [(k, v[1], v[3]) for k, v in ons.items() if v[1] < 10]
    R["takes_internal_pause_over_0_45s"] = [(k, [p for p in Mx[k]["pauses"] if p[1] >= 0.45]) for k in Mx if any(p[1] >= 0.45 for p in Mx[k]["pauses"])]
    R["takes_stt_accuracy_under_100"] = [(s["id"], s["stt_accuracy"]) for s in S if s["stt_accuracy"] is None or s["stt_accuracy"] < 100]
    R["takes_align_ratio_under_1"] = [(s["id"], s["align_ratio"]) for s in S if s["align_ratio"] < 0.999]
    R["takes_not_a1"] = [(s["id"], s["take"]) for s in S if not s["take"].endswith("_a1")]
    R["real_vs_plan_voiced"] = dict(raw_s=round(sum(s["raw_voiced"] for s in S), 2), laid_s=round(sum(s["dur"] for s in S), 2), plan_s=round(sum(s["plan_voiced"] for s in S), 2))
    json.dump(R, open(os.path.join(HERE, "check_report.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
    for k, v in R.items():
        if k == "level": v = {a: b for a, b in v.items() if a != "per_sentence_db"}
        print(k, ":", json.dumps(v, ensure_ascii=False))
if __name__ == "__main__":
    main()
