"""Film 23 conform: takes rendered on ESTIMATED timing -> retimed to the real narration -> captions -> mix -> mp4.
usage:
  python3 conform23.py fetch            # latest take of every shot from render23/teamK -> $TAKES/sNN/{take.mkv,meta.json,frames/}
  python3 conform23.py frames           # retime + dissolves -> $OUT_frames/f_%04d.png (N frames)
  python3 conform23.py final <out>      # captions + music + sfx + mix -> <out>.mp4
Retime rule: shot k occupies real frames [R_k, R_k+1) from film23/shot_times_REAL.json; output frame f shows take frame g0_k + (f - R_k)
(1:1 speed, the x1.25 tail is trimmed). Dissolves of D frames are centred on R_k and use the outgoing tail and the incoming handle.
"""
import sys, os, json, glob, subprocess
import numpy as np
P = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(P)
SCR = os.environ.get("SCR", "/tmp/claude-0/-home-user-github-commit-quest-v2/2a0c59b5-a3d7-55d7-882d-e9614c92cb8b/scratchpad")
TAKES = os.environ.get("TAKES", SCR + "/takes23"); OUTF = os.environ.get("OUT", SCR + "/conf23/film")
F23 = P + "/film23"; FPS = 30; OFF = 0.10
SHOTS = json.load(open(F23 + "/shot_times_REAL.json"))
TEAM = {**{s: 1 for s in "S02 S03 S04 S05 S06 S07 S08".split()}, **{s: 2 for s in "S09 S10 S11 S12 S13 S19".split()},
        **{s: 3 for s in "S01 S14 S15 S16 S17 S18".split()}}
N = int(round(SHOTS[-1]["real"][1] * FPS)) + 6          # last shot end + 0.2 s
T = N / FPS

def sh(*a, **k): return subprocess.run(a, check=True, **k)

def fetch():
    for k in (1, 2, 3):
        subprocess.run(["git", "-C", REPO, "fetch", "-q", "--depth", "1", "origin", f"render23/team{k}:refs/remotes/origin/render23/team{k}"], check=False)
    for s in SHOTS:
        shot = s["shot"]; n = shot.lower(); br = f"origin/render23/team{TEAM[shot]}"; src = f"film/v3/film23/{n}"
        ls = subprocess.run(["git", "-C", REPO, "ls-tree", "--name-only", f"{br}:{src}"], capture_output=True, text=True).stdout.split()
        parts = sorted(f for f in ls if f.startswith("take.mkv"))
        if not parts: print("MISSING", shot); continue
        h = subprocess.run(["git", "-C", REPO, "rev-parse", f"{br}:{src}"], capture_output=True, text=True).stdout.strip()
        d = f"{TAKES}/{n}"; os.makedirs(d, exist_ok=True)
        if os.path.exists(d + "/.tree") and open(d + "/.tree").read() == h: print("have", shot); continue
        data = b"".join(subprocess.run(["git", "-C", REPO, "show", f"{br}:{src}/{p}"], capture_output=True, check=True).stdout for p in parts)
        open(d + "/take.mkv", "wb").write(data)
        open(d + "/meta.json", "wb").write(subprocess.run(["git", "-C", REPO, "show", f"{br}:{src}/meta.json"], capture_output=True, check=True).stdout)
        m = json.load(open(d + "/meta.json"))
        for f in glob.glob(d + "/frames/*.png"): os.remove(f)
        os.makedirs(d + "/frames", exist_ok=True)
        sh("ffmpeg", "-v", "error", "-y", "-i", d + "/take.mkv", "-start_number", str(m["first_g"]), d + "/frames/g_%04d.png")
        open(d + "/.tree", "w").write(h); print("fetched", shot, len(glob.glob(d + "/frames/*.png")), "frames")

def _take(shot):
    n = shot.lower(); m = json.load(open(f"{TAKES}/{n}/meta.json"))
    fr = sorted(glob.glob(f"{TAKES}/{n}/frames/g_*.png")); lo = int(fr[0][-8:-4]); hi = int(fr[-1][-8:-4])
    return dict(dir=f"{TAKES}/{n}/frames", g0=m["g0"], lo=lo, hi=hi, tin=m.get("transition_in") or {})

def frames():
    from PIL import Image
    os.makedirs(OUTF + "_frames", exist_ok=True)
    for f in glob.glob(OUTF + "_frames/*.png"): os.remove(f)
    tk = [_take(s["shot"]) for s in SHOTS]; R = [int(round(s["real"][0] * FPS)) for s in SHOTS] + [N]
    def src(k, f):
        t = tk[k]; g = t["g0"] + (f - R[k]); c = min(max(g, t["lo"]), t["hi"])
        if c != g and abs(c - g) > 1: print(f"  clamp {SHOTS[k]['shot']} f{f} g{g}->{c}")
        return f"{t['dir']}/g_{c:04d}.png"
    blend = {}
    for k in range(1, len(SHOTS)):
        tin = tk[k]["tin"]; D = int(tin.get("frames", 0)) if tin.get("type") == "dissolve" else 0
        for j in range(D):
            f = R[k] - D // 2 + j; a = (j + 0.5) / D; blend[f] = (k, a * a * (3 - 2 * a))
    for k in range(len(SHOTS)):
        for f in range(R[k], R[k + 1]):
            dst = f"{OUTF}_frames/f_{f:04d}.png"
            if f in blend:
                kk, a = blend[f]
                A = np.asarray(Image.open(src(kk - 1, f)).convert("RGB"), np.float32); B = np.asarray(Image.open(src(kk, f)).convert("RGB"), np.float32)
                Image.fromarray(np.clip(A * (1 - a) + B * a + 0.5, 0, 255).astype(np.uint8)).save(dst)
            else:
                os.symlink(src(k, f), dst)
    print("frames", N, "->", OUTF + "_frames")

def music_bed(out):
    sh("ffmpeg", "-y", "-v", "error", "-i", F23 + "/audio/music_pick.mp3", "-af",
       f"highpass=f=150,equalizer=f=2500:t=q:w=1:g=-2,afade=t=out:st={T-2.0:.2f}:d=2.0", "-t", f"{T:.3f}", "-ar", "48000", out)

# SFX cues in narration seconds (real timing): (file, t, peak dB, length)
CUES = [("dawn", 0.0, -30, 4.2), ("squeak", 1.6, -24, 1.2), ("dawn", 4.0, -32, 4.6), ("squeak", 6.5, -24, 1.2), ("hiss", 10.6, -18, 2.4),
        ("pump", 12.4, -26, 3.2), ("pump", 16.2, -26, 3.0), ("squeak", 17.5, -24, 1.2), ("jeep", 19.2, -24, 2.4), ("laugh", 20.0, -20, 2.2),
        ("night", 28.2, -32, 8.8), ("rumble", 29.0, -22, 4.0), ("radio", 32.8, -24, 4.0), ("bell", 37.1, -22, 1.8), ("dawn", 37.0, -34, 6.0),
        ("gasp", 41.6, -20, 1.1), ("bump", 45.2, -20, 1.1), ("night", 47.1, -32, 11.4), ("river", 47.1, -30, 14.0), ("pump", 53.0, -28, 3.0),
        ("rumble", 55.6, -24, 3.0), ("radio", 57.0, -26, 1.8), ("paddle", 61.1, -24, 2.4), ("dawn", 63.6, -34, 4.9), ("balloon", 64.0, -24, 3.5),
        ("pop", 67.4, -20, 1.4)]

def final(out):
    caps = json.load(open(F23 + "/script/captions.json"))
    ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 720", "PlayResY: 1280", "WrapStyle: 2", "", "[V4+ Styles]",
           "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
           "Style: Pop,Kanit Black,88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,5,0,5,30,30,0,1", "", "[Events]",
           "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    ts = lambda t: f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
    for c in caps:
        a = max(0, c["t"] + OFF); b = min((c["end"] if c.get("end") is not None else T - OFF) + OFF, T)
        if a < T: ass.append(f"Dialogue: 0,{ts(a)},{ts(b)},Pop,,0,0,0,,{{\\pos(360,900)}}{c['text']}")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True); open(out + ".ass", "w").write("\n".join(ass))
    sh("ffmpeg", "-y", "-v", "error", "-framerate", "30", "-i", OUTF + "_frames/f_%04d.png", "-vf", f"ass={out}.ass:fontsdir={P}/fonts",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", "-movflags", "+faststart", out + "_silent.mp4")
    os.makedirs(SCR + "/conf23", exist_ok=True); mb = SCR + "/conf23/music_bed.wav"; music_bed(mb)
    v = F23 + "/audio/narration.wav"; B = F23 + "/audio/sfx/"
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", v, "-ac", "1", "-ar", "8000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    env = np.sqrt(np.convolve(x**2, np.ones(800)/800, "same"))[::80]
    def talk(a, ln):
        s = env[max(0, int((a - OFF) * 100)):max(0, int((a - OFF + ln) * 100))]
        return s.size > 0 and (s > 0.02).mean() > 0.3
    narr_db = 20 * np.log10(np.sqrt((x[np.repeat(env > 0.02, 80)[:len(x)]] ** 2).mean()) + 1e-9)
    sfx = []
    for f, t, db, ln in CUES:
        if t >= T: continue
        e = {"file": B + f + ".mp3", "at": t + OFF, "peak_db": db, "len": min(ln, T - t - OFF), "align": "onset", "fade_out": 0.08}
        if talk(e["at"], e["len"]): e["peak_db"] -= 6 if e["len"] < 3 else 3
        if talk(e["at"], e["len"]) and f in ("laugh", "gasp", "rumble"): e["peak_db"] -= 4
        sfx.append(e)
    spec = {"duration": T, "out_wav": out + ".wav", "video_in": out + "_silent.mp4", "video_out": out + ".mp4",
            "voice": {"file": v, "at": OFF, "gain": 10 ** ((-14.4 - narr_db) / 20)},
            "music": {"file": mb, "at": 0, "rms_db": float(os.environ.get("MUSIC_DB", "-31")), "fade_in": 0.3, "fade_out": 0.1}, "sfx": sfx}
    json.dump(spec, open(out + "_mix.json", "w"), indent=1)
    sh(sys.executable, P + "/audio/mixer.py", out + "_mix.json")
    sh("ffmpeg", "-v", "error", "-y", "-i", out + ".wav", "-af", "loudnorm=I=-12:TP=-1.5:LRA=11:linear=true,aresample=48000", "-ar", "48000", out + "_tp.wav")
    sh("ffmpeg", "-v", "error", "-y", "-i", out + "_silent.mp4", "-i", out + "_tp.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
       "-b:a", "256k", "-movflags", "+faststart", out + ".mp4")
    print("narration active RMS %.1f dB -> -14.4; wrote %s.mp4" % (narr_db, out))

if __name__ == "__main__":
    {"fetch": fetch, "frames": frames}.get(sys.argv[1], lambda: final(sys.argv[2]))()
