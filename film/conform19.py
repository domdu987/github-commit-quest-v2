"""Film 19 (ไอ้ช่างไม้) conform + mix: takes -> frames, dissolves, burned captions, SFX from cues, music bed, mix, reports.
usage: python3 conform19.py [--preview]
  full    -> release19/harrison_v1.mp4 (+ sheets, MIX_REPORT_v1.md/json)
  preview -> release19/harrison_preview.mp4 (360x640, fast encode; same cut, captions and mix)
Takes: v3/film19/sNN (meta.json, cues.json, take.mkv or take.mkv.part* -- parts are the CURRENT render and win over a stale take.mkv).
Frames are decoded in memory and streamed to ffmpeg (no frame PNGs); intermediates (.ass, concatenated parts, silent video, mix audio) go to WORK.
Env: WORK (scratch dir), VOICE_DB (-14.4), MUSIC_DB (-31).  Re-run any time takes change."""
import os, sys, re, json, glob, subprocess, argparse, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont

P = os.path.dirname(os.path.abspath(__file__))
WORK = os.environ.get("WORK", "/tmp/claude-0/-home-user-github-commit-quest-v2/a108c86f-deb9-528c-85fa-39b541349af8/scratchpad/conform19")
ap = argparse.ArgumentParser(); ap.add_argument("--preview", action="store_true"); ARGS = ap.parse_args()
PREV = ARGS.preview
FPS, N, W, H, OFF = 30, 2160, 720, 1280, 0.10
T = N / FPS
VOICE_DB = float(os.environ.get("VOICE_DB", "-14.4")); MUSIC_DB = float(os.environ.get("MUSIC_DB", "-31"))
SR = 48000
REL = P + "/release19"; os.makedirs(REL, exist_ok=True); os.makedirs(WORK, exist_ok=True)
OUT = REL + ("/harrison_preview.mp4" if PREV else "/harrison_v1.mp4")
TAG = "preview" if PREV else "v1"
FA = P + "/film19/audio"
log = lambda *a: print(*a, flush=True)

# ------------------------------------------------------------------ takes
def concat_parts(d, name):
    parts = sorted(glob.glob(d + "/take.mkv.part*"))
    if not parts: return d + "/take.mkv", False
    key = hashlib.md5("|".join(f"{p}:{os.path.getsize(p)}:{int(os.path.getmtime(p))}" for p in parts).encode()).hexdigest()[:10]
    dst = f"{WORK}/takes/{name}_{key}.mkv"
    if not os.path.exists(dst):
        os.makedirs(WORK + "/takes", exist_ok=True)
        for old in glob.glob(f"{WORK}/takes/{name}_*.mkv"): os.remove(old)
        with open(dst + ".tmp", "wb") as o:
            for p in parts:
                with open(p, "rb") as f:
                    while (b := f.read(1 << 24)): o.write(b)
        os.rename(dst + ".tmp", dst)
    return dst, True

class Take:
    def __init__(s, d):
        s.name = os.path.basename(d); s.m = json.load(open(d + "/meta.json")); m = s.m
        s.g0, s.g1, s.first, s.n = m["g0"], m["g1"], m["first_g"], m["n_frames"]
        s.ti = m.get("transition_in", {"type": "cut", "frames": 0})
        s.path, s.from_parts = concat_parts(d, s.name)
        s.cues = json.load(open(d + "/cues.json"))["cues"]
        s.arr = None; s.diffs = None; s.got = 0
    def load(s):
        if s.arr is not None: return
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", s.path, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        k = len(raw) // (W * H * 3)
        s.arr = np.frombuffer(raw, np.uint8, k * W * H * 3).reshape(k, H, W, 3); s.got = k
        if k != s.n: log(f"  WARN {s.name}: decoded {k} frames, meta says {s.n}")
        if s.diffs is None:                                   # deliver.py method: 90x160 grey, in-shot pairs only (g0+1..g1-1, no handles)
            prev, s.diffs = None, []
            for g in range(s.g0, s.g1):
                i = g - s.first
                if not (0 <= i < k): prev = None; continue
                a = np.asarray(Image.fromarray(s.arr[i]).resize((90, 160), Image.BILINEAR), dtype=np.float32).mean(-1)
                if prev is not None: s.diffs.append(float(np.abs(a - prev).mean()))
                prev = a
    def free(s): s.arr = None
    def frame(s, g):
        s.load(); i = g - s.first
        return s.arr[i] if 0 <= i < s.got else None

takes = sorted((Take(d) for d in sorted(glob.glob(P + "/v3/film19/s*"))), key=lambda t: t.g0)
log("takes:", ", ".join(f"{t.name}{'(parts)' if t.from_parts else ''}" for t in takes))
assert takes[0].g0 == 0 and takes[-1].g1 == N and all(takes[i].g1 == takes[i + 1].g0 for i in range(len(takes) - 1)), "take ranges do not tile 0..N"
CUTS = [t.g0 for t in takes if t.g0 > 0 and t.ti.get("type") != "dissolve"]

def pair_for(g):
    """(take, pair) where pair = (A, B, p) when g lies in a dissolve, else None.  Same geometry as conform_full.py."""
    i = next(i for i, t in enumerate(takes) if t.g0 <= g < t.g1); cur = takes[i]; pair = None
    if i + 1 < len(takes):
        nx = takes[i + 1]
        if nx.ti.get("type") == "dissolve":
            n = nx.ti["frames"]; a = nx.g0 - n // 2
            if a <= g < nx.g0: pair = (cur, nx, (g - a + 1) / (n + 1))
    if cur.ti.get("type") == "dissolve" and i > 0:
        n = cur.ti["frames"]; a = cur.g0 - n // 2
        if cur.g0 <= g < a + n: pair = (takes[i - 1], cur, (g - a + 1) / (n + 1))
    return cur, pair

# ------------------------------------------------------------------ captions (.ass, Kanit Black 88, centred y 900)
caps = json.load(open(P + "/film19/script/captions.json"))
font = ImageFont.truetype(P + "/fonts/Kanit_900Black.ttf", 88)
def cs(t): c = int(round(t * 100)); return f"{c//360000}:{c//6000%60:02d}:{c//100%60:02d}.{c%100:02d}"
ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 720", "PlayResY: 1280", "WrapStyle: 2", "", "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: Pop,Kanit Black,88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,5,0,5,30,30,0,1", "", "[Events]",
       "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
shrunk = []; ncap = 0
for k, c in enumerate(caps):
    a = max(0.0, c["t"] + OFF); e = c["end"] if c.get("end") is not None else (caps[k + 1]["t"] if k + 1 < len(caps) else T - OFF)
    if k + 1 < len(caps): e = min(e, caps[k + 1]["t"])
    b = min(e + OFF, T)
    if a >= T or b <= a: continue
    wpx = font.getlength(c["text"]); fs = 88
    if wpx > 640: fs = max(56, int(88 * 640 / wpx)); shrunk.append((c["text"], fs))
    ass.append(f"Dialogue: 0,{cs(a)},{cs(b)},Pop,,0,0,0,,{{\\pos(360,900)}}{'{\\fs%d}' % fs if fs != 88 else ''}{c['text']}"); ncap += 1
ASS = f"{WORK}/captions19.ass"; open(ASS, "w").write("\n".join(ass))
log(f"captions: {ncap} phrases, {len(shrunk)} shrunk to fit 640 px: {shrunk}")

# ------------------------------------------------------------------ video: take frames -> dissolves -> ffmpeg (ass burn)
SIL = f"{WORK}/silent_{TAG}.mp4"
vf = ("scale=360:640," if PREV else "") + f"ass={ASS}:fontsdir={P}/fonts"
enc = ["-preset", "veryfast", "-crf", "28"] if PREV else ["-preset", "medium", "-crf", "17"]
ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-framerate", "30", "-i", "-",
                       "-vf", vf, "-c:v", "libx264", *enc, "-pix_fmt", "yuv420p", "-movflags", "+faststart", SIL], stdin=subprocess.PIPE)
missing, blends, last = [], 0, None
for g in range(N):
    for t in takes:                                           # keep memory bounded: only takes near g stay decoded
        if t.arr is not None and (t.first + t.n + 20 < g or t.first - 40 > g): t.free()
    cur, pair = pair_for(g); fr = None
    if pair:
        A, B, p = pair; fa, fb = A.frame(g), B.frame(g)
        if fa is not None and fb is not None:
            p = p * p * (3 - 2 * p); fr = np.clip(fa.astype(np.float32) * (1 - p) + fb.astype(np.float32) * p + 0.5, 0, 255).astype(np.uint8); blends += 1
    if fr is None: fr = cur.frame(g)
    if fr is None: missing.append(g); fr = last if last is not None else np.zeros((H, W, 3), np.uint8)
    ff.stdin.write(np.ascontiguousarray(fr).tobytes()); last = fr
    if g % 300 == 0: log(f"  frame {g}/{N}")
ff.stdin.close(); assert ff.wait() == 0, "ffmpeg video encode failed"
log(f"video: {N} frames, {blends} blended, missing {len(missing)} {missing[:10]}")
for t in takes:
    if t.diffs is None: t.load()
dall = [d for t in takes for d in t.diffs or []]
fd = {"median": round(float(np.median(dall)), 2), "p90": round(float(np.percentile(dall, 90)), 2), "pairs": len(dall),
      "per_take": {t.name: [round(float(np.median(t.diffs)), 2), round(float(np.percentile(t.diffs, 90)), 2)] for t in takes if t.diffs}}
for t in takes: t.free()

# ------------------------------------------------------------------ audio helpers
def load_audio(path, sr=SR):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(sr), "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
db = lambda x: 20 * np.log10(max(x, 1e-12))
rms_db = lambda x: db(float(np.sqrt((x ** 2).mean())))
def fades(x, fi, fo):
    n = len(x)
    if fi: k = min(n, int(fi * SR)); x[:k] *= np.linspace(0, 1, k)[:, None]
    if fo: k = min(n, int(fo * SR)); x[-k:] *= np.linspace(1, 0, k)[:, None]
    return x
mix_n = int(T * SR)
def place(buf, x, at):
    i = int(round(at * SR))
    if i < 0: x = x[-i:]; i = 0
    j = min(len(buf), i + len(x))
    if j > i: buf[i:j] += x[: j - i]
_cache = {}
def lib(name):
    if name not in _cache: _cache[name] = load_audio(f"{FA}/sfx/{name}.mp3")
    return _cache[name]

# ---- voice: narration at +0.10 s, gain so the voice stem is VOICE_DB RMS
nar = load_audio(FA + "/narration.wav"); nar_db = rms_db(nar)
voice = nar * 10 ** ((VOICE_DB - nar_db) / 20)
vbuf = np.zeros((mix_n, 2)); place(vbuf, voice, OFF)
# voice activity (100 Hz envelope of the raw narration) for ducking
mono = nar.mean(1); e100 = np.sqrt(np.convolve(mono ** 2, np.ones(480) / 480, "same"))[::480]
THR = 10 ** (-34 / 20)
def talking(a, ln):
    i0 = int((a - OFF) * 100); i1 = int((a - OFF + ln) * 100); seg = e100[max(0, i0):max(0, i1)]
    return seg.size > 0 and (seg > THR).mean() > 0.3

# ------------------------------------------------------------------ SFX from cues
BED = [(r"storm", "storm_sea", -28), (r"candlelight|evening", "hall_evening", -30),
       (r"hall|board|observatory", "hall_tone", -30), (r"workshop.*night|night.*workshop", "workshop_night", -30),
       (r"workshop", "workshop_day", -30), (r"tropical|barbados|beach", "tropical_shore", -30), (r"sea|sail", "sea_open", -30)]
PROP = [(r"watch|h3 ticking|h4", "watch_tick", -33), (r"h1|clock|regulator", "clock_tick", -33)]
# (regex on label, library file, peak dB, length s, priority, onset offset s); priority 3 > 2 > 1 when two point effects are < GAP s apart
POINT = [(r"mocker's belly laugh", "belly_laugh", -17, 1.8, 3, 0.0), (r"board's belly laughs", "hall_laugh", -18, 3.0, 3, 0.0),
         (r"money bag drops|thud of a heavy bag", "coins_bag", -17, 0.9, 3, 0.0), (r"cloth money bag scraping", "coins_half", -19, 0.9, 3, 0.0),
         (r"lid shut", "box_lock", -18, 0.9, 2, 0.0), (r"wax seals", "wax_seal", -17, 1.5, 3, 0.0),
         (r"double door creaks", "door_creak", -18, 1.5, 3, 0.0), (r"sailors' cheers", "crowd_cheer", -20, 2.0, 3, 0.1),
         (r"gulp|deflating", "sweat_pop", -20, 0.5, 2, 0.0), (r"watch-click", "pocketwatch_click", -20, 0.73, 2, 0.15),
         (r"chime", "glint_shimmer", -21, 1.0, 2, 0.1), (r"quadrant", "quadrant_clank", -23, 0.84, 2, 0.15),
         (r"file on brass", "file_rasp", -22, 1.5, 2, 0.0), (r"buckets scooped", "water_bail", -22, 1.5, 2, 0.2),
         (r"timber crash", "wave_crash", -16, 1.5, 3, 0.0), (r"telescope creak", "timber_creak", -27, 1.2, 1, 0.0)]
WHOOSH = (r"snap|whoosh|whip", "whoosh_fast", -25, 0.6, 1, 0.0)
GAP = 2.0
beds, cands, props = [], [], []
for t in takes:
    a0, b0 = max(0.0, t.g0 / FPS - 0.15), min(T, t.g1 / FPS + 0.15)
    for c in t.cues:
        lab = c["label"].lower(); kind = c["kind"]; ct = c["time"]
        if kind == "ambience":
            for rx, f, pk in BED:
                if re.search(rx, lab): beds.append([f, a0, b0, pk, t.name]); break
        elif kind == "prop" or (kind == "foley" and "watch ticks" in lab):
            for rx, f, pk in PROP:
                if re.search(rx, lab): props.append([f, max(a0, ct), b0, pk, t.name]); break
        elif kind in ("accent", "foley", "voice"):
            for rx, f, pk, ln, pr, off in POINT:
                if re.search(rx, lab): cands.append(dict(file=f, at=ct + off, peak=pk, len=ln, prio=pr, take=t.name, label=c["label"][:60])); break
            else:
                if kind == "accent" and re.search(WHOOSH[0], lab):
                    cands.append(dict(file=WHOOSH[1], at=ct, peak=WHOOSH[2], len=WHOOSH[3], prio=1, take=t.name, label=c["label"][:60]))
# merge consecutive takes that use the same bed (one continuous loop, no restart at the cut)
merged = []
for b in beds:
    if merged and merged[-1][0] == b[0] and b[1] <= merged[-1][2] + 0.31: merged[-1][2] = b[2]; merged[-1][4] += "+" + b[4]
    else: merged.append(list(b))
accepted, dropped = [], []
for c in sorted(cands, key=lambda c: (-c["prio"], c["at"])):
    if c["at"] >= T - 0.05: dropped.append(c); continue
    if any(abs(c["at"] - a["at"]) < GAP for a in accepted): dropped.append(c)
    else: accepted.append(c)
accepted.sort(key=lambda c: c["at"])
sbuf = np.zeros((mix_n, 2))
def loop_layer(name, a, b, pk, fin=0.4, fout=0.4, ov=0.5):
    x = lib(name); x = x * 10 ** (pk / 20) / max(np.abs(x.mean(1)).max(), 1e-9); dur = len(x) / SR; t = a
    while t < b - 0.05:
        ln = min(dur, b - t); seg = x[: int(ln * SR)].copy(); fades(seg, fin, fout); place(sbuf, seg, t)
        if ln < dur: break
        t += dur - ov
for f, a, b, pk, nm in merged: loop_layer(f, a, b, pk)
for f, a, b, pk, nm in props: loop_layer(f, a, b, pk, 0.2, 0.2, 0.2)
placed = []
for c in accepted:
    x = lib(c["file"]); m = x.mean(1); pk = np.abs(m).max(); on = int(np.argmax(np.abs(m) > 0.25 * pk)); x = x[max(0, on - int(0.005 * SR)):]
    x = x[: int(min(c["len"], T - c["at"]) * SR)].copy(); x *= 10 ** (c["peak"] / 20) / max(np.abs(x.mean(1)).max(), 1e-9)
    duck = 0.0
    if talking(c["at"], c["len"]):
        duck = 6 if c["len"] < 3 else 3
        if any(k in c["file"] for k in ("laugh", "gasp", "cheer")): duck += 4
    x *= 10 ** (-duck / 20); fades(x, 0.005, 0.08); place(sbuf, x, c["at"]); placed.append({**c, "duck_db": duck, "final_peak_db": round(c["peak"] - duck, 1)})
# ---- music: music_B.mp3 trimmed to the film, 1.5 s fade-out, ducked 3 dB under speech, stem normalised to MUSIC_DB RMS
mus = load_audio(FA + "/music/music_B.mp3")[: mix_n].copy()
if len(mus) < mix_n: mus = np.vstack([mus, np.zeros((mix_n - len(mus), 2))])
env = np.zeros(mix_n)
for i, v in enumerate(e100):
    a = int((i / 100 + OFF) * SR); b = int(((i + 1) / 100 + OFF) * SR)
    if v > THR and a < mix_n: env[a:min(b, mix_n)] = 1.0
k = int(0.35 * SR); env = np.convolve(env, np.ones(k) / k, "same"); mus *= (10 ** (-3 / 20) * env + (1 - env))[:, None]
mus = fades(mus, 0.3, 1.5); mus *= 10 ** ((MUSIC_DB - rms_db(mus)) / 20)
# ---- sum, limit, encode, measure true peak; tighten the limiter until TP <= -1 dBTP
mixf = vbuf + sbuf + mus
AUD = f"{WORK}/mix_{TAG}.m4a"
def measure(path):
    r = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    s = r[r.rfind("Summary:"):]
    g = lambda rx: float(re.search(rx, s).group(1))
    return dict(lufs=g(r"I:\s+(-?[\d.]+) LUFS"), lra=g(r"LRA:\s+([\d.]+) LU"), tp=g(r"Peak:\s+(-?[\d.]+) dBFS"))
lim = 0.85
for it in range(6):
    p = subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-af",
                        f"alimiter=limit={lim:.3f}:attack=3:release=60:level=disabled", "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), AUD],
                       input=mixf.astype(np.float32).tobytes(), capture_output=True)
    assert p.returncode == 0, p.stderr.decode()
    ms = measure(AUD); log(f"  limiter {lim:.3f}: {ms}")
    if ms["tp"] <= -1.0: break
    lim *= 0.92
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", SIL, "-i", AUD, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy", "-shortest", "-movflags", "+faststart", OUT], check=True)
fin = measure(OUT)
voice_stem = rms_db(voice); music_stem = rms_db(mus); sfx_stem = rms_db(sbuf)
rep = dict(output=os.path.relpath(OUT, P), integrated_lufs=fin["lufs"], lra=fin["lra"], true_peak_dbtp=fin["tp"], limiter=round(lim, 3),
           voice_rms_db=round(voice_stem, 2), music_rms_db=round(music_stem, 2), sfx_rms_db=round(sfx_stem, 2), narration_raw_rms_db=round(nar_db, 2),
           target=dict(lufs="-14..-11", tp="<= -1", voice=VOICE_DB, music=MUSIC_DB),
           pass_lufs=-14 <= fin["lufs"] <= -11, pass_tp=fin["tp"] <= -1.0,
           beds=[dict(file=f, a=round(a, 2), b=round(b, 2), peak=pk, takes=nm) for f, a, b, pk, nm in merged],
           props=[dict(file=f, a=round(a, 2), b=round(b, 2), peak=pk, take=nm) for f, a, b, pk, nm in props],
           point_effects=[dict(file=c["file"], at=round(c["at"], 2), peak_db=c["final_peak_db"], duck=c["duck_db"], take=c["take"]) for c in placed],
           dropped_for_spacing=[dict(file=c["file"], at=round(c["at"], 2), take=c["take"]) for c in dropped],
           frame_diff_in_shot=fd, planned_cuts=CUTS, missing_frames=missing, captions=ncap, captions_shrunk=shrunk,
           takes={t.name: dict(g0=t.g0, g1=t.g1, frames_decoded=t.got, parts=t.from_parts) for t in takes})
json.dump(rep, open(REL + f"/mix_report_{TAG}.json", "w"), indent=1, ensure_ascii=False)
gaps = [round(b["at"] - a["at"], 2) for a, b in zip(placed, placed[1:])]
md = [f"# Mix report {os.path.basename(OUT)}", "",
      f"- Integrated loudness: **{fin['lufs']:.1f} LUFS** (target -14..-11): {'PASS' if rep['pass_lufs'] else 'FAIL'}; LRA {fin['lra']:.1f} LU",
      f"- True peak: **{fin['tp']:.2f} dBTP** (limit -1.0): {'PASS' if rep['pass_tp'] else 'FAIL'} (limiter {lim:.3f})",
      f"- Voice RMS {voice_stem:.1f} dB (target {VOICE_DB}), music RMS {music_stem:.1f} dB (target {MUSIC_DB}; music_B trimmed to {T:.0f} s, 1.5 s fade-out, -3 dB duck under speech), SFX stem RMS {sfx_stem:.1f} dB",
      f"- Point effects: {len(placed)} placed, {len(dropped)} dropped for spacing (>= {GAP} s apart); min gap {min(gaps) if gaps else '-'} s",
      f"- Beds: {len(merged)}, prop loops: {len(props)}; SFX under speech ducked 6 dB (3 dB if >= 3 s; laugh/gasp/cheer a further 4 dB)",
      f"- In-shot frame-diff (90x160 grey, deliver.py method): median {fd['median']}, p90 {fd['p90']} over {fd['pairs']} pairs (target 4 / 12)",
      f"- Frames: {N}, dissolve blends {blends}, missing {len(missing)}; planned cuts g {CUTS}", "", "## Point effects", "| t | file | peak dB | take |", "|---|---|---|---|"]
md += [f"| {c['at']:.2f} | {c['file']} | {c['final_peak_db']} | {c['take']} |" for c in placed]
open(REL + f"/MIX_REPORT_{TAG}.md", "w").write("\n".join(md) + "\n")
log("\n".join(md[:9]))

# ------------------------------------------------------------------ sheets from the final video
def decode_small(w, h, vfx):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", OUT, "-vf", vfx + f",scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
def sheet(frames, times, cols, path, w, h):
    rows = (len(frames) + cols - 1) // cols; S = Image.new("RGB", (cols * w, rows * (h + 14)), (20, 20, 20)); d = ImageDraw.Draw(S)
    for k, (f, tt) in enumerate(zip(frames, times)):
        x, y = (k % cols) * w, (k // cols) * (h + 14); S.paste(Image.fromarray(f), (x, y)); d.text((x + 3, y + h), f"{tt:.0f}s", fill=(235, 235, 235))
    S.save(path, quality=86)
f1 = decode_small(160, 284, "fps=1"); sheet(f1, range(len(f1)), 9, REL + f"/sheet_1fps_{TAG}.jpg", 160, 284)
fp = decode_small(360, 640, "fps=1/3"); sheet(fp, [3 * i for i in range(len(fp))], 6, REL + f"/sheet_phone_360x640_{TAG}.jpg", 360, 640)
log("sheets written;", OUT)
