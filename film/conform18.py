"""Film 18 conform: PASSED takes -> frames (conform_full logic) -> captions -> mix -> mp4.
usage:
  python3 conform18.py fetch            # extract every PASSED take (exact blob hash) into $TAKES/sNN/{take.mkv,meta.json}
  python3 conform18.py frames           # conform_full.py on $TAKES -> $OUT_frames (N=2112)
  python3 conform18.py final <out>      # captions + mix + mp4  (out basename, e.g. release18/oxclerk_v1)
env: TAKES (default scratchpad/takes18_passed), OUT (frames basename)
"""
import sys, os, json, glob, subprocess, re
P = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(P)
SCR = "/tmp/claude-0/-home-user-github-commit-quest-v2/64d228e2-e8b3-5935-8909-70298ec15c3e/scratchpad"
TAKES = os.environ.get("TAKES", SCR + "/takes18_passed"); OUTF = os.environ.get("OUT", SCR + "/conf18/film")
N = 2112; FPS = 30; OFF = 0.10; T = N / FPS
F18 = P + "/film18"

def sh(*a, **k): return subprocess.run(a, check=True, **k)

def _find_commit(shot, h):
    """the commit (on any render18/teamK branch) whose tree holds blob h at film/v3/film18/<shot>/take.mkv"""
    for k in range(1, 6):
        br = f"origin/render18/team{k}"
        subprocess.run(["git", "-C", REPO, "fetch", "-q", "origin", f"render18/team{k}:refs/remotes/{br}"], check=False)
        revs = subprocess.run(["git", "-C", REPO, "rev-list", br, "--", f"film/v3/film18/{shot}/take.mkv"], capture_output=True, text=True).stdout.split()
        for c in revs:
            t = subprocess.run(["git", "-C", REPO, "rev-parse", f"{c}:film/v3/film18/{shot}/take.mkv"], capture_output=True, text=True).stdout.strip()
            if t == h: return c
    raise SystemExit(f"blob {h} for {shot} not found on any render18 branch")

def fetch():
    for pf in sorted(glob.glob(F18 + "/qa/s*/PASSED")):
        shot = pf.split("/")[-2]; h = re.search(r"take hash ([0-9a-f]{40})", open(pf).read()).group(1)
        d = f"{TAKES}/{shot}"
        if os.path.exists(d + "/.hash") and open(d + "/.hash").read().strip() == h: print("have", shot); continue
        c = _find_commit(shot, h); os.makedirs(d, exist_ok=True)
        for f in ("take.mkv", "meta.json"):
            data = subprocess.run(["git", "-C", REPO, "show", f"{c}:film/v3/film18/{shot}/{f}"], capture_output=True, check=True).stdout
            open(f"{d}/{f}", "wb").write(data)
        for fr in glob.glob(d + "/frames/*.png"): os.remove(fr)
        open(d + "/.hash", "w").write(h); print("fetched", shot, h[:10], "from", c[:8])

WHIPS = json.load(open(F18 + "/qa/whips.json")) if os.path.exists(F18 + "/qa/whips.json") else []

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
    for w in WHIPS: whip(w["g"], w.get("dir", 1))

def grade_filter():
    """QA_TEAM §G colour: per-shot eq grade so every shot reaches saturation >= 0.48 and luma 87-108 (film 2: 0.49 / 94).
    Measured on the conformed frames per shot range; returns an ffmpeg filter chain with timeline enable."""
    import numpy as np
    sp = json.load(open(F18 + "/qa/shot_ranges.json"))  # [[shot, g0, g1], ...]
    chain = []
    for shot, a, b in sp:
        fr = [f"{OUTF}_frames/f_{i:04d}.png" for i in range(a, b, 6)]
        from PIL import Image
        x = np.stack([np.asarray(Image.open(f).convert("RGB").resize((90, 160), Image.BOX), np.float32) for f in fr])
        mx = x.max(-1); mn = x.min(-1); sat = ((mx - mn) / (mx + 1e-3)).mean(); L = x.mean()
        k = min(1.5, max(1.0, 0.54 / max(sat, 1e-3)))  # §I: film saturation >= 0.50, vivid >= 45 %
        T = 90.0 if L < 87 else (105.0 if L > 108 else L)
        gm = float(np.log(L / 255) / np.log(T / 255)) if T != L else 1.0
        gm = 1 / gm  # ffmpeg eq gamma > 1 brightens
        if k > 1.0 or abs(gm - 1) > 0.01:
            chain.append(f"eq=saturation={k:.3f}:gamma={gm:.3f}:enable='between(n,{a},{b-1})'")
        print(f"grade {shot}: sat {sat:.3f} luma {L:.1f} -> k {k:.2f} gamma {gm:.3f}")
    return ",".join(chain)

def music_bed(out):
    """music m1 with the audio-QA automation: -3.5 dB 40.0-43.6 s (0.5 s ramps), +1.5 dB 43.6-60, fade out to 70.4."""
    src = F18 + "/audio/music_pick.mp3"
    vol = ("volume='if(between(t,39.5,40.0),1-0.33*(t-39.5)/0.5,if(between(t,40.0,43.6),0.668,if(between(t,43.6,44.1),0.668+0.52*(t-43.6)/0.5,"
           "if(between(t,44.1,60),1.189,if(between(t,60,60.5),1.189-0.189*(t-60)/0.5,1)))))':eval=frame")
    sh("ffmpeg", "-y", "-v", "error", "-i", src, "-af", f"highpass=f=150,equalizer=f=2500:t=q:w=1:g=-2,{vol},afade=t=out:st={T-2.6:.2f}:d=2.6", "-t", f"{T:.3f}", "-ar", "48000", out)

def final(out):
    caps = json.load(open(F18 + "/script/captions.json"))
    ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 720", "PlayResY: 1280", "WrapStyle: 2", "", "[V4+ Styles]",
           "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
           "Style: Pop,Kanit Black,88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,5,0,5,30,30,0,1", "", "[Events]",
           "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    ts = lambda t: f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
    for c in caps:
        a = max(0, c["t"] + OFF); b = min(c["end"] + OFF, T)
        if a < T: ass.append(f"Dialogue: 0,{ts(a)},{ts(b)},Pop,,0,0,0,,{{\\pos(360,900)}}{c['text']}")
    os.makedirs(os.path.dirname(out), exist_ok=True); open(out + ".ass", "w").write("\n".join(ass))
    sh("ffmpeg", "-y", "-v", "error", "-framerate", "30", "-i", OUTF + "_frames/f_%04d.png", "-vf", ",".join(filter(None, [grade_filter() if os.environ.get("GRADE", "1") == "1" else "", f"ass={out}.ass:fontsdir={P}/fonts"])),
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", "-movflags", "+faststart", out + "_silent.mp4")
    mb = SCR + "/conf18/music_bed.wav"; music_bed(mb)
    B = F18 + "/audio/sfx/"; sfx = []
    def add(f, t, db, ln, fo=0.08):
        if t < T: sfx.append({"file": B + f + ".mp3", "at": t + OFF, "peak_db": db, "len": min(ln, T - t - OFF), "align": "onset", "fade_out": fo})
    # cues from the shot plan (narration seconds)
    for f, t, db, ln in [("night", 0.0, -32, 5.0), ("fire", 0.2, -30, 5.0), ("moo", 2.8, -22, 1.5), ("drum", 5.2, -22, 1.4),
                         ("camp", 5.5, -34, 4.5), ("moo", 17.2, -22, 1.4), ("herd", 18.3, -26, 1.8), ("camp", 19.9, -34, 5.5),
                         ("laugh", 21.2, -20, 2.4), ("crowd_laugh", 28.9, -20, 2.5), ("cheer", 33.5, -22, 3.0), ("clink", 36.2, -20, 1.0),
                         ("night", 40.15, -32, 3.4), ("dig", 40.9, -22, 2.6), ("crumble", 42.6, -20, 1.4), ("fire", 44.0, -30, 3.0),
                         ("ignite", 47.13, -16, 1.2), ("herd", 47.6, -18, 6.0), ("whoosh", 50.1, -24, 0.6), ("herd", 50.5, -20, 6.0),
                         ("panic", 53.3, -22, 3.5), ("pots", 58.0, -18, 2.4), ("panic", 60.3, -20, 3.0), ("tent", 61.0, -18, 1.2),
                         ("birds", 62.8, -30, 3.8), ("moo", 66.5, -20, 1.4), ("herd", 68.0, -24, 2.3)]:
        add(f, t, db, ln)
    v = F18 + "/audio/narration.wav"
    import numpy as np
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", v, "-ac", "1", "-ar", "8000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    env = np.sqrt(np.convolve(x**2, np.ones(800)/800, "same"))[::80]
    def talk(a, ln):
        s = env[max(0, int((a - OFF) * 100)):max(0, int((a - OFF + ln) * 100))]
        return s.size > 0 and (s > 0.02).mean() > 0.3
    for e in sfx:
        if talk(e["at"], e["len"]): e["peak_db"] -= 6 if e["len"] < 3 else 3
        if talk(e["at"], e["len"]) and any(k in e["file"] for k in ("laugh", "cheer", "panic", "pots", "herd")): e["peak_db"] -= 4
    spec = {"duration": T, "out_wav": out + ".wav", "video_in": out + "_silent.mp4", "video_out": out + ".mp4",
            "voice": {"file": v, "at": OFF, "gain": 10 ** ((float(os.environ.get("VOICE_DB", "-14.4")) - float(os.environ.get("NARR_DB", "-17.2"))) / 20)},
            "music": {"file": mb, "at": 0, "rms_db": float(os.environ.get("MUSIC_DB", "-31")), "fade_in": 0.3, "fade_out": 0.1}, "sfx": sfx}
    json.dump(spec, open(out + "_mix.json", "w"), indent=1)
    sh(sys.executable, P + "/audio/mixer.py", out + "_mix.json")

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "fetch": fetch()
    elif cmd == "frames": frames()
    elif cmd == "final": final(sys.argv[2])
