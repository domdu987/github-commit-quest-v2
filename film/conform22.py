"""Film 22 conform: PASSED takes -> frames (conform_full logic) -> captions -> mix -> mp4.
usage:
  python3 conform22.py fetch            # extract every PASSED take (exact blob hash) into $TAKES/sNN/{take.mkv,meta.json}
  python3 conform22.py frames           # conform_full.py on $TAKES -> $OUT_frames (N=1890)
  python3 conform22.py final <out>      # captions + mix + mp4  (out basename, e.g. release22/circuit_v1)
env: TAKES (default scratchpad/takes22_passed), OUT (frames basename)
"""
import sys, os, json, glob, subprocess, re
P = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(P)
SCR = os.environ.get("SCR", "/tmp/claude-0/-home-user-github-commit-quest-v2/60761534-f10c-5695-ab47-6eb0ea3132ae/scratchpad")
TAKES = os.environ.get("TAKES", SCR + "/takes22_passed"); OUTF = os.environ.get("OUT", SCR + "/conf22/film")
N = 1890; FPS = 30; OFF = 0.10; T = N / FPS
F22 = P + "/film22"

def sh(*a, **k): return subprocess.run(a, check=True, **k)

def _find_commit(shot, h):
    """the commit (on any render22/teamK branch) whose tree holds blob h at film/v3/film22/<shot>/take.mkv"""
    for k in range(1, 6):
        br = f"origin/render22/team{k}"
        subprocess.run(["git", "-C", REPO, "fetch", "-q", "origin", f"render22/team{k}:refs/remotes/{br}"], check=False)
        revs = subprocess.run(["git", "-C", REPO, "rev-list", br, "--", f"film/v3/film22/{shot}/take.mkv"], capture_output=True, text=True).stdout.split()
        for c in revs:
            t = subprocess.run(["git", "-C", REPO, "rev-parse", f"{c}:film/v3/film22/{shot}/take.mkv"], capture_output=True, text=True).stdout.strip()
            if t == h: return c
    raise SystemExit(f"blob {h} for {shot} not found on any render22 branch")

def fetch():
    for pf in sorted(glob.glob(F22 + "/qa/s*/PASSED")):
        shot = pf.split("/")[-2]; h = re.search(r"take hash ([0-9a-f]{40})", open(pf).read()).group(1)
        d = f"{TAKES}/{shot}"
        if os.path.exists(d + "/.hash") and open(d + "/.hash").read().strip() == h: print("have", shot); continue
        c = _find_commit(shot, h); os.makedirs(d, exist_ok=True)
        for f in ("take.mkv", "meta.json"):
            data = subprocess.run(["git", "-C", REPO, "show", f"{c}:film/v3/film22/{shot}/{f}"], capture_output=True, check=True).stdout
            open(f"{d}/{f}", "wb").write(data)
        m = json.load(open(f"{d}/meta.json")); ti = m.get("transition_in") or {}
        if isinstance(ti, str): ti = {"type": ti}
        t = ti.get("type", "cut")
        if t in ("match", "match_dissolve"): ti = {"type": "dissolve", "frames": ti.get("frames", 9)}
        elif t in ("travel", "whip", "none", "—"): ti = {"type": "cut"}
        m["transition_in"] = ti; json.dump(m, open(f"{d}/meta.json", "w"), indent=1)
        for fr in glob.glob(d + "/frames/*.png"): os.remove(fr)
        open(d + "/.hash", "w").write(h); print("fetched", shot, h[:10], "from", c[:8])

WHIPS = json.load(open(F22 + "/qa/whips.json")) if os.path.exists(F22 + "/qa/whips.json") else []

def whip(g0, direction=1, k=3):
    """§I: replace a hard cut at g0 with an in-camera whip: horizontal streak blur ramping up over the last k frames of the
    outgoing shot and down over the first k frames of the incoming one (no handles needed), plus a small slide in the whip direction."""
    import numpy as np
    from PIL import Image
    for j in range(-k, k):
        g = g0 + j; f = f"{OUTF}_frames/f_{g:04d}.png"
        if not os.path.lexists(f): continue
        a = np.asarray(Image.open(f).convert("RGB"), np.float32)
        w = int(90 * (1 - abs(j + 0.5) / k)) | 1          # blur width peaks at the cut
        sh_ = int(direction * 60 * (j + 0.5) / k)           # slide: outgoing moves out, incoming moves in
        a = np.roll(a, sh_, axis=1)
        c = np.cumsum(np.pad(a, ((0, 0), (w // 2 + 1, w // 2), (0, 0)), mode="edge"), axis=1)
        b = (c[:, w:, :] - c[:, :-w, :]) / w
        os.remove(f); Image.fromarray(np.clip(b[:, :a.shape[1]] + 0.5, 0, 255).astype(np.uint8)).save(f)
    print("whip at", g0)

def frames():
    os.makedirs(os.path.dirname(OUTF), exist_ok=True)
    sh(sys.executable, P + "/conform_full.py", TAKES, OUTF, env=dict(os.environ, N=str(N)))
    # teams wrote g1 as their last frame: fill any frame no take covers from the outgoing take's handle
    for g in range(N):
        dst = f"{OUTF}_frames/f_{g:04d}.png"
        if not os.path.lexists(dst):
            c = sorted(glob.glob(f"{TAKES}/s*/frames/g_{g:04d}.png"))
            if c: os.symlink(c[0], dst); print("filled", g, "from", c[0].split("/")[-3])
    for w in WHIPS: whip(w["g"], w.get("dir", 1))
    # COLOUR_SPEC.md: the conform grade only (spec pre-grade where needed + v1.1 grade), graded in place
    sh(sys.executable, P + "/grade22.py", OUTF + "_frames", "4")

def grade_filter():
    """QA_TEAM §G colour: per-shot eq grade so every shot reaches saturation >= 0.48 and luma 87-108 (film 2: 0.49 / 94).
    Measured on the conformed frames per shot range; returns an ffmpeg filter chain with timeline enable."""
    import numpy as np
    sp = json.load(open(F22 + "/qa/shot_ranges.json"))  # [[shot, g0, g1], ...]
    chain = []
    for shot, a, b in sp:
        fr = [f"{OUTF}_frames/f_{i:04d}.png" for i in range(a, b, 6)]
        from PIL import Image
        x = np.stack([np.asarray(Image.open(f).convert("RGB").resize((90, 160), Image.BOX), np.float32) for f in fr])
        mx = x.max(-1); mn = x.min(-1); sat = ((mx - mn) / (mx + 1e-3)).mean(); L = x.mean()
        k = min(1.5, max(1.0, 0.54 / max(sat, 1e-3)))  # §I: film saturation >= 0.50, vivid >= 45 %
        T = 90.0 if L < 87 else (105.0 if L > 108 else L)
        gm = float(np.log(L / 255) / np.log(T / 255)) if T != L else 1.0
        # ffmpeg eq: out = in^(1/gamma); gamma = log(L)/log(T) maps mean L -> T
        if k > 1.0 or abs(gm - 1) > 0.01:
            chain.append(f"eq=saturation={k:.3f}:gamma={gm:.3f}:enable='between(n,{a},{b-1})'")
        print(f"grade {shot}: sat {sat:.3f} luma {L:.1f} -> k {k:.2f} gamma {gm:.3f}")
    return ",".join(chain)

def music_bed(out):
    """music = the client's own Suno track "The Curious Commuter" (87.2 s; film22/audio/music_suno.mp3, from claude/new-session-73ou27 d4927bc).
    MUSIC=m2 uses the fal backup take instead. Light HPF and -2 dB at 2.5 kHz under the voice, trimmed and faded at the film end."""
    src = F22 + ("/audio/music_pick.mp3" if os.environ.get("MUSIC") == "m2" else "/audio/music_suno.mp3")
    sh("ffmpeg", "-y", "-v", "error", "-i", src, "-af", f"highpass=f=70,equalizer=f=2500:t=q:w=1:g=-2,afade=t=out:st={T-2.5:.2f}:d=2.5", "-t", f"{T:.3f}", "-ar", "48000", out)

def final(out):
    caps = json.load(open(F22 + "/script/captions.json"))
    ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 720", "PlayResY: 1280", "WrapStyle: 2", "", "[V4+ Styles]",
           "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
           "Style: Pop,Kanit Black,88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,5,0,5,30,30,0,1", "", "[Events]",
           "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    ts = lambda t: f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
    for c in caps:
        a = max(0, c["t"] + OFF); b = min((c["end"] if c.get("end") is not None else T - OFF) + OFF, T)
        if a < T: ass.append(f"Dialogue: 0,{ts(a)},{ts(b)},Pop,,0,0,0,,{{\\pos(360,900)}}{c['text']}")
    os.makedirs(os.path.dirname(out), exist_ok=True); open(out + ".ass", "w").write("\n".join(ass))
    sh("ffmpeg", "-y", "-v", "error", "-framerate", "30", "-i", OUTF + "_frames/f_%04d.png", "-vf", ",".join(filter(None, [grade_filter() if os.environ.get("GRADE", "0") == "1" else "", f"ass={out}.ass:fontsdir={P}/fonts"])),
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", "-movflags", "+faststart", out + "_silent.mp4")
    mb = SCR + "/conf22/music_bed.wav"; music_bed(mb)
    B = F22 + "/audio/sfx/"; sfx = []
    def add(f, t, db, ln, fo=0.08):
        if t < T: sfx.append({"file": B + f + ".mp3", "at": t + OFF, "peak_db": db, "len": min(ln, T - t - OFF), "align": "onset", "fade_out": fo})
    # cues from the shot plan (narration seconds)
    for f, t, db, ln in [("night", 0.0, -34, 3.6), ("quill_scratch", 0.1, -22, 1.6), ("thud", 0.7, -24, 0.4), ("quill_scratch", 1.9, -24, 1.2),
                         ("street", 3.6, -32, 3.0), ("whoosh_fast", 5.9, -24, 0.8), ("train", 6.5, -26, 2.5), ("crowd_murmur", 7.4, -32, 3.4),
                         ("thud", 9.4, -24, 0.4), ("paper", 11.6, -24, 0.8), ("letter_open", 13.0, -24, 0.9), ("quill_scratch", 16.0, -22, 0.9),
                         ("ding", 16.9, -26, 0.6), ("telegraph_click", 19.3, -32, 3.0), ("thud", 20.45, -16, 0.5), ("belly_laugh", 21.85, -20, 1.6),
                         ("drawer_slide", 28.1, -18, 1.0), ("crowd_laugh", 29.2, -20, 2.4), ("footstep", 31.3, -26, 2.0), ("door", 32.4, -22, 0.8),
                         ("crowd_murmur", 33.5, -32, 6.4), ("paper", 34.5, -26, 0.8), ("newspaper_rustle", 36.2, -26, 1.0),
                         ("train", 39.96, -22, 3.4), ("paper_flutter", 41.3, -22, 1.0), ("gasp", 42.4, -22, 0.8), ("train_chug", 43.4, -30, 6.0),
                         ("ding", 47.3, -26, 0.5), ("ding", 48.0, -25, 0.5), ("ding", 48.8, -24, 0.5), ("whoosh_fast", 49.4, -24, 0.7),
                         ("train", 49.6, -26, 2.3), ("crowd_murmur", 52.0, -28, 3.5), ("paper_flutter", 53.7, -22, 1.2), ("trunk", 54.8, -22, 1.0),
                         ("electric_crackle", 55.6, -30, 2.6), ("sting", 57.7, -26, 1.0), ("night", 58.4, -32, 4.5), ("street", 58.4, -34, 2.5),
                         ("gulp", 61.3, -18, 0.8), ("thud", 61.8, -20, 0.5)]:
        add(f, t, db, ln)
    v = F22 + "/audio/narration.wav"
    import numpy as np
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", v, "-ac", "1", "-ar", "8000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    env = np.sqrt(np.convolve(x**2, np.ones(800)/800, "same"))[::80]
    def talk(a, ln):
        s = env[max(0, int((a - OFF) * 100)):max(0, int((a - OFF + ln) * 100))]
        return s.size > 0 and (s > 0.02).mean() > 0.3
    for e in sfx:
        if talk(e["at"], e["len"]): e["peak_db"] -= 6 if e["len"] < 3 else 3
        if talk(e["at"], e["len"]) and any(k in e["file"] for k in ("laugh", "cheer", "murmur", "train")): e["peak_db"] -= 4
    spec = {"duration": T, "out_wav": out + ".wav", "video_in": out + "_silent.mp4", "video_out": out + ".mp4",
            "voice": {"file": v, "at": OFF, "gain": 10 ** ((float(os.environ.get("VOICE_DB", "-14.4")) - float(os.environ.get("NARR_DB", "-17.2"))) / 20)},
            "music": {"file": mb, "at": 0, "rms_db": float(os.environ.get("MUSIC_DB", "-31")), "fade_in": 0.3, "fade_out": 0.1}, "sfx": sfx}
    json.dump(spec, open(out + "_mix.json", "w"), indent=1)
    sh(sys.executable, P + "/audio/mixer.py", out + "_mix.json")
    # true-peak safety: linear loudnorm to -12 LUFS / -1.5 dBTP, then remux (FINAL gate: TP <= -1)
    sh("ffmpeg", "-v", "error", "-y", "-i", out + ".wav", "-af", "loudnorm=I=-12:TP=-1.5:LRA=11:linear=true,aresample=48000", "-ar", "48000", out + "_tp.wav")
    sh("ffmpeg", "-v", "error", "-y", "-i", out + "_silent.mp4", "-i", out + "_tp.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out + ".mp4")

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "fetch": fetch()
    elif cmd == "frames": frames()
    elif cmd == "final": final(sys.argv[2])
