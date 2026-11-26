"""build_narr.py -- lay the recorded EP.1 narration (s17-s101) on the episode timeline.

    python3 build_narr.py        -> narr_ep1.wav (48 kHz mono, film time 0 = sample 0, silence under the hook),
                                    narr_ep1_timing.json, scNN/captions_timing.json (the hook's shape, for ep1/pipe/cut.py)

Method (after audio/narr_ohm/join_fit.py, the hook):
  * each chosen take is trimmed with the hook's trim (5 ms envelope > 0.01, 20 ms lead, 40 ms tail);
  * internal silences longer than PAUSE_CAP are shortened to PAUSE_CAP (the hook cut everything over 0.14 s to 0.10 s);
  * free running: sentence start = previous voice end + TAIL + the plan's pause_before, snapped to a film frame; tempo 1.0;
  * the countdown is in real time (bite 43.795): s23 '30 วินาที' is pinned at 73.80, s31 '10 วินาที' at 93.80, s33 at 100.90.
    A stretch between two pins that does not fit is fitted in this order: the picture-beat gap before the pin gives up to
    15 %; pause cap 0.25, 0.15; one atempo for the stretch, at most 1.10; then all its gaps scaled down (not under GAP_FLOOR);
  * level: every sentence is brought to the hook narration's median per-sentence active RMS, keeping +-KEEP_DB of its own
    character, then a look-ahead limiter at CEIL (no hard clipping);
  * captions: character timestamps (tts_fal.align) -> trim -> pause map -> tempo -> film time; a caption that the
    timestamps start inside a silence is moved to 40 ms before the voice comes back.
No network, no TTS / STT: only local files, numpy, ffmpeg atempo.
"""
import json, sys, os, subprocess, numpy as np
from numpy.lib.stride_tricks import sliding_window_view
def minimum_filter1d(g, n):
    return sliding_window_view(np.pad(g, n // 2, mode='edge'), n).min(axis=1)
def uniform_filter1d(g, n):
    return np.convolve(np.pad(g, n // 2, mode='edge'), np.ones(n) / n, 'valid')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); import measure as M
tts_fal = M.tts_fal; PROJ = M.PROJ; SR = M.SR; FPS = 24
snap = lambda t: round(t * FPS) / float(FPS)
HOOK_END = 53.32; LEAD = 0.30                # the title ends at 53.32; first word 0.30 later (the plan, and the hook's NARR0)
TAIL = 0.30                                  # silence after a sentence before the plan's written pause_before starts
PAUSE_CAP = 0.40; PAUSE_CAP_BY = {"s71": 0.60}   # 'ข้างล่างมืด ... และเงียบ': the take holds 1.30 s; kept as a beat, but shorter
PINS = {"s23": 73.80, "s31": 93.80, "s33": snap(100.90)}       # s33 opens a word-cut shot (S48): on a frame, so the watch insert before it stays silent
TEMPO_MAX, TEMPO_MIN = 1.10, 0.92; GAP_FLOOR = 0.20
KEEP_DB = 1.5; CEIL = 0.94; BEAT_GAP = 1.5; BEAT_FLEX = 0.15   # a gap of BEAT_GAP or more before a pin holds a picture beat: it may give up BEAT_FLEX of itself first
EMPH_MIN, EMPH_PUSH = 0.42, 0.20
CAP_HOLD = 0.30                              # the last caption of a sentence stays this long after the voice (or to the next sentence)

def act_rms_db(y):
    env = np.convolve(np.abs(y), np.ones(480) / 480, 'same'); a = y[env > 0.006]
    return 20 * np.log10(np.sqrt((a ** 2).mean()) + 1e-12) if len(a) else -99.0

def hook_levels():
    caps = json.load(open(os.path.join(PROJ, "audio", "narr_ohm", "captions_timing.json"), encoding="utf8"))
    x = M.load(os.path.join(PROJ, "audio", "narr_ohm", "narr_final.wav")); span = {}
    for c in caps:
        a, b = span.get(c["id"], (c["t0"], c["t1"])); span[c["id"]] = (min(a, c["t0"]), max(b, c["t1"]))
    return {k: round(act_rms_db(x[int(a * SR):int(b * SR)]), 2) for k, (a, b) in span.items()}, round(20 * np.log10(np.sqrt((x ** 2).mean())), 2)

def tighten(y, cap):
    """-> (pieces [(a, b, newlen)], removed list [(at_s, was_s)])"""
    runs = [(i, j) for i, j in M.quiet_runs(y) if i > 0 and j < len(y) and j - i > cap * SR]
    segs, pos, cut = [], 0, []
    for i, j in runs:
        segs.append((pos, i, i - pos)); segs.append((i, j, int(cap * SR))); cut.append((round(i / SR, 3), round((j - i) / SR, 3))); pos = j
    segs.append((pos, len(y), len(y) - pos))
    return segs, cut

def atempo(y, tp):
    if abs(tp - 1.0) < 1e-4: return y
    r = subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f64le', '-ar', str(SR), '-ac', '1', '-i', '-', '-af', 'atempo=%.5f' % tp, '-f', 'f64le', '-'], input=y.astype(np.float64).tobytes(), capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.float64)

def limiter(y, ceil=CEIL, blk=48, half=15):
    """look-ahead limiter without pitch-rate gain wobble: 1 ms peak blocks, the lowest needed gain within +-15 ms, smoothed twice over +-7 ms
    (the smoothing stays inside the minimum's window, so the ceiling is never passed)."""
    n = len(y); m = -(-n // blk); pk = np.abs(np.pad(y, (0, m * blk - n))).reshape(m, blk).max(axis=1)
    g = minimum_filter1d(np.minimum(1.0, ceil / np.maximum(pk, 1e-9)), 2 * half + 1); g = np.repeat(g, blk)[:n]
    for _ in range(2): g = uniform_filter1d(g, 2 * 7 * blk + 1)
    g = np.minimum(g[:n], 1.0); return y * g, float(20 * np.log10(g.min()))

class Sent:
    def __init__(s, plan):
        s.p = plan; s.id = plan["id"]
        rep = json.load(open(os.path.join(M.TAKES, "takes", s.id + ".report.json"), encoding="utf8"))
        s.take = rep["take"]; s.rep = rep; s.base = os.path.join(M.TAKES, rep["take"])
        s.x = M.load(s.base + ".wav"); s.a, s.b = M.trim_idx(s.x); s.y = s.x[s.a:s.b]
        s.al, s.ratio, s.c = tts_fal.align(s.base, [dict(text=q["text"]) for q in plan["captions"]])
        s.raw_db = act_rms_db(s.y); s.raw_runs = [(i, j) for i, j in M.quiet_runs(s.y) if i > 0 and j < len(s.y) and j - i > 0.12 * SR]
    def shape(s, cap):
        cap = max(cap, 0.0) if s.id not in PAUSE_CAP_BY else min(PAUSE_CAP_BY[s.id], max(cap, 0.0) if cap > PAUSE_CAP else PAUSE_CAP_BY[s.id] * cap / PAUSE_CAP)
        s.cap = cap; s.segs, s.cut = tighten(s.y, cap); s.len0 = sum(L for _, _, L in s.segs) / float(SR); return s.len0
    def render(s, tp):
        out = []
        for a, b, L in s.segs:
            out.append(s.y[a:b] if L == b - a else np.concatenate([s.y[a:a + L // 2], s.y[b - (L - L // 2):b]]))
        z = atempo(np.concatenate(out), tp); f = int(0.005 * SR); z = z.copy(); z[:f] *= np.linspace(0, 1, f); z[-f:] *= np.linspace(1, 0, f)
        s.tempo = tp; s.z = z; s.dur = len(z) / float(SR); return z
    def map_t(s, traw):
        """raw take time -> seconds from the sentence's start in the laid track"""
        q = traw * SR - s.a
        for i, j in s.raw_runs:                       # a caption the timestamps start inside a silence: 40 ms before the voice returns
            if i - 0.03 * SR <= q <= j: q = max(i, j - 0.04 * SR); break
        pos = 0
        for a, b, L in s.segs:
            if q <= b: return max(0.0, (pos + (min(max(q, a), b) - a) * L / float(max(b - a, 1))) / SR / s.tempo)
            pos += L
        return pos / SR / s.tempo

def main():
    N = json.load(open(os.path.join(PROJ, "ep1", "plan", "narration_ep1.json"), encoding="utf8"))
    S = [Sent(p) for p in N["sentences"]]; ids = [s.id for s in S]
    hook_db, hook_whole = hook_levels(); target = float(np.median(list(hook_db.values()))); ep_med = float(np.median([s.raw_db for s in S]))
    for s in S: s.shape(PAUSE_CAP); s.tp = 1.0; s.fit = ""
    gap = {s.id: TAIL + s.p["pause_before"] for s in S}            # desired silence before each sentence
    start = {}
    # ---- the pinned stretches (countdown)
    first = S[0].id; start[first] = HOOK_END + LEAD
    pin_ids = [first] + list(PINS); pin_t = dict(PINS); pin_t[first] = start[first]; fits = []
    for k in range(len(pin_ids) - 1):
        i0, i1 = ids.index(pin_ids[k]), ids.index(pin_ids[k + 1]); seg = S[i0:i1]; avail = pin_t[pin_ids[k + 1]] - pin_t[pin_ids[k]]
        gaps = [gap[s.id] for s in S[i0 + 1:i1 + 1]]; G = sum(gaps); tp, kk, capu = 1.0, 1.0, PAUSE_CAP
        flex = BEAT_FLEX * gaps[-1] if gaps[-1] >= BEAT_GAP else 0.0; avail_real = avail; avail = avail + flex
        for capu in (PAUSE_CAP, 0.25, 0.15):
            V = sum(s.shape(capu) for s in seg)
            if V + G <= avail: break
        if V + G > avail:
            tp = min(TEMPO_MAX, V / (avail - G))
            if V / tp + G > avail + 1e-6:
                kk = (avail - V / tp) / G
                if min(gaps) * kk < GAP_FLOOR: raise SystemExit("stretch %s-%s does not fit: gaps would be %.2f s" % (pin_ids[k], pin_ids[k + 1], min(gaps) * kk))
        t = pin_t[pin_ids[k]]
        for n, s in enumerate(seg):
            s.tp = tp; s.fit = "countdown stretch %s..%s" % (pin_ids[k], pin_ids[k + 1]); s.render(tp); start[s.id] = t if n == 0 else snap(t)
            t = start[s.id] + s.dur + (gaps[n] * kk if n < len(seg) - 1 else 0)
        fits.append(dict(stretch=[pin_ids[k], pin_ids[k + 1]], from_t=pin_t[pin_ids[k]], to_t=pin_t[pin_ids[k + 1]], pause_cap=capu, tempo=round(tp, 4), gap_scale=round(kk, 3),
                         voice_s=round(sum(s.dur for s in seg), 3), last_gap_s=round(pin_t[pin_ids[k + 1]] - (start[seg[-1].id] + seg[-1].dur), 3), planned_last_gap_s=round(gaps[-1], 3)))
    # ---- free running from the last pin on
    i0 = ids.index(pin_ids[-1]); t = pin_t[pin_ids[-1]]
    for n, s in enumerate(S[i0:]):
        s.render(1.0); start[s.id] = t if n == 0 else snap(t + gap[s.id]); t = start[s.id] + s.dur
    # ---- level, limiter, lay
    total = snap(t + 6.0);     # retime_shots.py cuts the wav to the episode's exact length
    track = np.zeros(int(total * SR) + SR); rows = []; caps_all = []
    for n, s in enumerate(S):
        want = target + float(np.clip(s.raw_db - ep_med, -KEEP_DB, KEEP_DB)); z = s.z
        g = 10 ** ((want - act_rms_db(z)) / 20.0)
        for _ in range(8):                                      # the limiter takes a little back: iterate the gain
            z2, gr = limiter(z * g); d = want - act_rms_db(z2)
            if abs(d) < 0.05: break
            g *= 10 ** (d / 20.0)
        s.out = z2; s.gr = gr; s.out_db = act_rms_db(z2); p0 = int(round(start[s.id] * SR)); track[p0:p0 + len(z2)] += z2
        nxt = start[S[n + 1].id] if n + 1 < len(S) else None; v_end = start[s.id] + s.dur
        end = min(v_end + CAP_HOLD, nxt) if nxt is not None else v_end + CAP_HOLD
        cs = []
        for q, pc in zip(s.al, s.p["captions"]):
            cs.append(dict(id=s.id, text=pc["text"], t0=round(start[s.id] + s.map_t(q["t0"]), 3)))
        cs[0]["t0"] = round(start[s.id], 3)
        for i in range(len(cs) - 1):                            # a caption with a coloured key word is on screen at least EMPH_MIN: the next one waits (at most EMPH_PUSH)
            if s.p["captions"][i].get("emph") and cs[i + 1]["t0"] - cs[i]["t0"] < EMPH_MIN:
                cs[i + 1]["held_s"] = round(min(cs[i]["t0"] + EMPH_MIN, cs[i + 1]["t0"] + EMPH_PUSH) - cs[i + 1]["t0"], 3); cs[i + 1]["t0"] = round(cs[i + 1]["t0"] + cs[i + 1]["held_s"], 3)
        for i, c in enumerate(cs):
            c["t1"] = cs[i + 1]["t0"] if i + 1 < len(cs) else round(end, 3)
            c["voice_end"] = cs[i + 1]["t0"] if i + 1 < len(cs) else round(v_end, 3)
            pc = s.p["captions"][i]; c["emph"] = pc.get("emph", ""); c["colour"] = pc.get("colour", "") if pc.get("emph") else ""
            c["plan_t0"] = pc["t0"]; c["plan_t1"] = pc["t1"]
        caps_all += cs
        rows.append(dict(id=s.id, scene=s.p["scene"], speaker=s.p["speaker"], text=s.p["text"], take=s.take, start=round(start[s.id], 3), voice_end=round(v_end, 3), end=round(end, 3),
                         dur=round(s.dur, 3), tempo=round(s.tempo, 4), fit=s.fit, pause_cap=round(s.cap, 3), pauses_shortened=s.cut, gap_before=round(start[s.id] - (rows[-1]["voice_end"] if rows else HOOK_END), 3),
                         plan_pause_before=s.p["pause_before"], plan_start=s.p["start"], plan_voiced=s.p["voiced"], trim_lead_s=round(s.a / SR, 3), trim_tail_s=round((len(s.x) - s.b) / SR, 3),
                         raw_voiced=round(len(s.y) / SR, 3), raw_rms_db=round(s.raw_db, 2), gain_db=round(s.out_db - s.raw_db, 2), limiter_max_reduction_db=round(gr, 2), rms_db=round(s.out_db, 2),
                         peak=round(float(np.abs(z2).max()), 3), align_ratio=round(s.ratio, 3), stt_accuracy=s.rep.get("accuracy"), captions=cs))
    track = track[:int(round(total * SR))]
    assert np.abs(track).max() <= CEIL + 1e-6
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f64le', '-ar', str(SR), '-ac', '1', '-i', '-', '-c:a', 'pcm_s16le', os.path.join(HERE, 'narr_ep1.wav')], input=track.astype(np.float64).tobytes(), check=True)
    doc = dict(note="film time (s) = time in narr_ep1.wav; the wav starts at film time 0 and is silent under the hook (0-53.32). Hook narration: audio/narr_ohm/narr_final.wav at +0.30.",
               wav="ep1/audio/narr_ep1.wav", sr=SR, fps=FPS, offset=0.0, hook_end=HOOK_END, first_word=start[first], last_voice_end=rows[-1]["voice_end"], wav_seconds=round(len(track) / SR, 3),
               rules=dict(tail_s=TAIL, pause_cap_s=PAUSE_CAP, pause_cap_by=PAUSE_CAP_BY, pins=PINS, tempo_range=[TEMPO_MIN, TEMPO_MAX], gap_floor_s=GAP_FLOOR, caption_hold_s=CAP_HOLD),
               level=dict(method="RMS of the samples whose 10 ms envelope is over 0.006 (-44 dBFS)", hook_sentence_rms_db=hook_db, hook_median_db=round(target, 2), hook_whole_file_rms_db=hook_whole,
                          ep_raw_median_db=round(ep_med, 2), keep_db=KEEP_DB, ceiling=CEIL),
               countdown_fits=fits, sentences=rows, captions=caps_all)
    json.dump(doc, open(os.path.join(HERE, "narr_ep1_timing.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
    for sc in sorted(set(r["scene"] for r in rows)):               # the hook's shape, per scene, for ep1/pipe/cut.py: seconds from the scene's first word
        cc = [c for c in caps_all if next(r for r in rows if r["id"] == c["id"])["scene"] == sc]; t0 = cc[0]["t0"]
        os.makedirs(os.path.join(HERE, "sc" + sc), exist_ok=True)
        json.dump([dict(id=c["id"], text=c["text"], t0=round(c["t0"] - t0, 3), t1=round(c["t1"] - t0, 3)) for c in cc], open(os.path.join(HERE, "sc" + sc, "captions_timing.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
    for f in fits: print(f)
    for r in rows: print("%-5s %7.3f-%7.3f gap %.2f (plan pb %.2f) tempo %.3f cap %.2f gain %+5.1f lim %5.1f rms %.1f pk %.2f %s" % (r["id"], r["start"], r["voice_end"], r["gap_before"], r["plan_pause_before"], r["tempo"], r["pause_cap"], r["gain_db"], r["limiter_max_reduction_db"], r["rms_db"], r["peak"], r["pauses_shortened"] or ""))
    print("hook median", target, "last voice end", rows[-1]["voice_end"], "plan", N["sentences"][-1]["start"] + N["sentences"][-1]["voiced"])
if __name__ == "__main__":
    main()
