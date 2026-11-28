"""finish_ep.py -- conform of EP.1: per scene, then the master (hook mezzanine + scenes).  No status icons anywhere.

    python3 finish_ep.py scene  --scene sc02 --tier draft --size 720x1280 --base-size 360x640 --out sc02_draft.mp4
        = comp (shot joins, picture fx of the cut cfg) + ass (captions) + mix (scene audio at one static gain) + video
    python3 finish_ep.py comp   --scene sc02 --tier final --size 720x1280 [--worker i/n] [--frames a:b]
    python3 finish_ep.py ass    --scene sc02            -> <comp dir>/../captions_sc02.ass
    python3 finish_ep.py video  --scene sc02 --tier final --size 720x1280 --out PROJ/deliver/ep1_sc02_v1.mp4
    python3 finish_ep.py missing --scene sc02 --tier final --size 720x1280
    python3 finish_ep.py sheet  --scene sc02 --video sc02_draft.mp4 --sheet sc02_sheet.png
    python3 finish_ep.py master --hook PROJ/deliver/ep1_sc01_hook_final.mp4 --scenes sc02,sc03 --tier final --size 720x1280 --out ep1_master_v1.mp4
        options: --hook-tail S (use only the last S seconds of the hook: tests)   --scene-mp4 sc02=path (use a scene mezzanine
        when its frames are gone)

Captions: Kanit Black 88 at (360, 900) of 720x1280, white with a 5 px black outline (the hook's Cap style); a caption
with an `emph` word (narration_ep1.json, carried into the cut table) colours that word amber (fact) or red (threat)
and pops 12 % for 3 frames, exactly as the hook's finish.emph().
Audio: the scene mix named in the cut cfg ("mix"), else the narration wav alone placed at narr0, else silence; one
static gain to -14 LUFS with true peak <= -1 dBTP of the encoded track.  The master joins the hook's audio and the
scene mixes (each at its scene gain) and applies ONE more static gain to the whole.
Encode: libx264 CRF 15, tune animation, preset slow, yuv420p, AAC 320 kb/s, +faststart.
"""
import os, sys, json, math, argparse, subprocess, glob
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import epcommon as E

FPS = E.FPS
AMBER_ASS, RED_ASS = "&H03B7FF&", "&H4F45F5&"               # the hook's finish.py values
COL = {"amber": AMBER_ASS, "red": RED_ASS}
JOIN = [0.0, 0.0, 0.0]                                     # user 11-28: NO zoom push at cuts ("not like a film"); straight cuts only. Was [0.04, 0.09, 0.15].
ASS_HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Kanit Black,88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,5,0,5,20,20,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ENC = ["-c:v", "libx264", "-preset", "slow", "-crf", "15", "-tune", "animation", "-pix_fmt", "yuv420p"]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("ffmpeg failed:\n%s\n%s" % (" ".join(cmd), r.stderr[-3000:]))
    return r


# ------------------------------------------------------------------------------------------------ picture
def zoom_blur(a, amount, n=18):
    if amount <= 0.002: return a
    h, w = a.shape[:2]
    acc = np.zeros_like(a, np.float32)
    for i in range(n):
        s = 1.0 + amount * i / (n - 1)
        M = np.float32([[s, 0, (1 - s) * w / 2], [0, s, (1 - s) * h / 2]])
        acc += cv2.warpAffine(a, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return acc / n


def join_amount(S, k):
    """blurred push across a cut inside the scene; none into / out of a shot listed in hard_cuts, none at the scene's ends."""
    row = S.shot_at(k); i = S.ids.index(row["id"]); amt = 0.0
    if i + 1 < len(S.ids) and S.ids[i + 1] not in S.hard_cuts and row["f1"] - k <= 3:
        amt = JOIN[3 - (row["f1"] - k)]
    if i > 0 and row["id"] not in S.hard_cuts and k - row["f0"] < 3:
        amt = max(amt, JOIN[2 - (k - row["f0"])])
    return amt


def fx_time(S, f):
    if "word" in f:
        c = [c for c in S.caps if c["text"] == f["word"] and (not f.get("sid") or c["id"] == f["sid"])][0]
        return (c["t1"] if f.get("end") else c["t0"]) + float(f.get("dt", 0.0))
    if "cue" in f: return float(S.cues[f["cue"]]) + float(f.get("dt", 0.0))
    return float(f.get("t", 0.0))


def apply_fx(S, a, k):
    """picture fx of the cut cfg (BGR float 0..1): flash {frames, colour [r,g,b], mix}, fade_out / fade_in {frames},
    dim {mix, colour, ramp} from a word / cue / t on."""
    for f in S.d.get("fx", []):
        k0 = int(round(fx_time(S, f) * FPS)); ty = f.get("type")
        col = np.float32(list(f.get("colour", [0, 0, 0]))[::-1])[None, None] / 255.0
        if ty == "flash" and k0 <= k < k0 + int(f.get("frames", 2)):
            m = float(f.get("mix", 0.58)); a = a * (1 - m) + col * m
        elif ty == "fade_out" and k >= k0:
            m = min(1.0, (k - k0 + 1) / float(max(int(f.get("frames", 12)), 1))); a = a * (1 - m) + col * m
        elif ty == "fade_in" and k < k0 + int(f.get("frames", 12)):
            m = 1.0 - min(1.0, max(0.0, (k - k0) / float(max(int(f.get("frames", 12)), 1)))); a = a * (1 - m) + col * m
        elif ty == "dim" and k >= k0:
            m = float(f.get("mix", 0.45)) * min(1.0, (k - k0) / float(max(int(f.get("ramp", 12)), 1))); a = a * (1 - m) + col * m
    return a


_C1 = {}


def redraw_c1(S, row, k, W, H, tier, base):
    """a class C1 frame drawn again at the conform size (BGR float), or None when the shot has no draw()."""
    try:
        if row["id"] not in _C1:
            if E._ACTIVE is None or E._ACTIVE.name != S.name: E.activate(S.name, S.path)
            _C1[row["id"]] = E.load_shot(S.name, row["id"])
        mod = _C1[row["id"]]
        if mod is None or not hasattr(mod, "draw"): return None
        import ep2d
        im = mod.draw(ep2d.Ctx(E.scene(), row, k, W, H, tier, base))
        if not hasattr(im, "save"): im = Image.fromarray(im)
        return cv2.cvtColor(np.asarray(im.convert("RGB").resize((W, H))), cv2.COLOR_RGB2BGR).astype(np.float32) / 255.0
    except Exception as e:
        print("C1 redraw of %s failed (%s): the rendered frame is scaled instead" % (row["id"], e))
        return None


def src(base, S, k):
    row = S.shot_at(k)
    return os.path.join(base, row["id"], E.frame_name(k - row["f0"]) + ".png")


def dirs(S, tier, W, H, base_size=None, name="comp"):
    base = E.out_dir(tier, *(base_size or (W, H)), S.name)
    odir = base if not base_size else E.out_dir(tier + "_from%dx%d" % tuple(base_size), W, H, S.name)
    return base, os.path.join(odir, name)


def comp_name(k):
    return "f_%05d.png" % (k + 1)


def comp(S, tier, W, H, frames=None, base_size=None, name="comp", worker=(0, 1)):
    base, out = dirs(S, tier, W, H, base_size, name)
    os.makedirs(out, exist_ok=True)
    miss = []
    for k in (frames or range(S.frames)):
        if k % worker[1] != worker[0]: continue
        p = src(base, S, k)
        if not os.path.exists(p):
            miss.append(k); continue
        row = S.shot_at(k)
        a = None
        if base_size and tuple(base_size) != (W, H) and row["cls"] == "C1":
            a = redraw_c1(S, row, k - row["f0"], W, H, tier, base)     # drawn frames are drawn at the output size, not scaled up
        if a is None:
            a = cv2.imread(p, cv2.IMREAD_COLOR).astype(np.float32) / 255.0
        if a.shape[1] != W or a.shape[0] != H:
            a = cv2.resize(a, (W, H), interpolation=cv2.INTER_AREA if a.shape[1] > W else cv2.INTER_LANCZOS4)
        a = zoom_blur(a, join_amount(S, k))
        a = apply_fx(S, a, k)
        tmp = os.path.join(out, ".tmp%d_%s" % (os.getpid(), comp_name(k)))
        cv2.imwrite(tmp, (np.clip(a, 0, 1) * 255).astype(np.uint8), [cv2.IMWRITE_PNG_COMPRESSION, 1])
        os.replace(tmp, os.path.join(out, comp_name(k)))
    if not frames and worker[1] == 1:
        for p in glob.glob(os.path.join(out, "f_*.png")):  # a cut that got shorter leaves frames past its end: they would block `video`
            if int(os.path.basename(p)[2:7]) > S.frames: os.remove(p)
    print("comp %s -> %s; missing %d frames %s" % (S.name, out, len(miss), miss[:20]))
    return miss


def missing(S, tier, W, H):
    base = E.out_dir(tier, W, H, S.name)
    m = [k for k in range(S.frames) if not os.path.exists(src(base, S, k))]
    print("%s: %d of %d frames missing %s" % (S.name, len(m), S.frames, m[:40]))
    return m


# ------------------------------------------------------------------------------------------------ captions
def emph(c):
    part = c.get("emph")
    if part and part in c["text"]:
        a, b = c["text"].split(part, 1)
        return "{\\fscx112\\fscy112\\t(0,125,\\fscx100\\fscy100)}%s{\\c%s}%s{\\c&HFFFFFF&}%s" % (a, COL.get(c.get("colour", "amber"), AMBER_ASS), part, b)
    return c["text"]


def ts(t):
    t = max(0.0, t)
    cs = int(round(t * 100))
    return "%d:%02d:%02d.%02d" % (cs // 360000, (cs // 6000) % 60, (cs // 100) % 60, cs % 100)


def ass_lines(S, offset=0.0):
    return ["Dialogue: 0,%s,%s,Cap,,0,0,0,,{\\pos(360,900)}%s" % (ts(c["t0"] + offset), ts(min(c["t1"], S.frames / float(FPS)) + offset), emph(c)) for c in S.caps]


def ass_path(S, out_dir_):
    os.makedirs(out_dir_, exist_ok=True)
    p = os.path.join(out_dir_, "captions_%s.ass" % S.name)
    open(p, "w", encoding="utf-8").write(ASS_HEAD + "\n".join(ass_lines(S)) + "\n")
    return p


# ------------------------------------------------------------------------------------------------ audio
def loudness(path, stream="0:a"):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-map", stream, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    tail = r[r.rindex("Summary:"):]
    I = float(tail.split("I:")[1].split("LUFS")[0]); tp = tail.split("Peak:")[1].split("dBFS")[0].strip()
    return I, (float(tp) if tp not in ("-inf", "inf") else -120.0)


def scene_wav(S, out_dir_):
    """the scene's audio as a 48 kHz stereo wav of exactly the scene's length (un-gained), and what it was made from."""
    os.makedirs(out_dir_, exist_ok=True)
    dur = S.frames / float(FPS)
    out = os.path.join(out_dir_, "audio_%s.wav" % S.name)
    mix = S.d.get("mix") or ""; narr = S.d.get("narration_wav") or ""
    fix = lambda p: p if os.path.isabs(p) else os.path.join(E.PROJ, p)
    post = "aresample=48000,aformat=channel_layouts=stereo,apad,atrim=0:%.4f" % dur
    if mix and os.path.exists(fix(mix)):
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", fix(mix), "-af", post, out]); what = "mix " + mix
    elif narr and os.path.exists(fix(narr)):
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", fix(narr), "-af", "adelay=%d:all=1,%s" % (int(round(S.narr0 * 1000)), post), out]); what = "narration only " + narr
    else:
        run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", "%.4f" % dur, out]); what = "SILENCE (no mix, no narration wav)"
    return out, what


def static_gain(path, target=-14.0, ceil=-1.0):
    """one gain for a whole track: toward -14 LUFS, never past a true peak of -1 dBTP (before encoding)."""
    I, tp = loudness(path)
    if I < -60.0: return 0.0, I, tp                        # silence: nothing to normalise
    return min(target - I, ceil - tp), I, tp


def encode_audio(wav, out_m4a, gain, ceil=-1.0):
    """AAC 320k at a static gain; the encoder overshoots, so the gain steps down until the ENCODED peak is <= ceil."""
    for _ in range(8):
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-af", "volume=%.2fdB" % gain, "-c:a", "aac", "-b:a", "320k", out_m4a])
        I2, tp2 = loudness(out_m4a)
        if tp2 <= ceil or I2 < -60: break
        gain -= max(0.1, tp2 - ceil)
    return gain, I2, tp2


def scene_audio(S, out_dir_):
    wav, what = scene_wav(S, out_dir_)
    g, I, tp = static_gain(wav)
    m4a = wav[:-4] + ".m4a"
    g, I2, tp2 = encode_audio(wav, m4a, g)
    info = dict(scene=S.name, source=what, gain_db=round(g, 2), source_lufs=I, source_tp=tp, lufs=I2, true_peak=tp2, codec="aac 320k")
    json.dump(info, open(wav[:-4] + ".json", "w"), indent=1)
    print("audio %s: %s; gain %.2f dB -> %.1f LUFS, true peak %.1f dBTP (encoded)" % (S.name, what, g, I2, tp2))
    return m4a, info


# ------------------------------------------------------------------------------------------------ video
def video(S, tier, W, H, out, base_size=None, name="comp"):
    base, cdir = dirs(S, tier, W, H, base_size, name)
    have = len(glob.glob(os.path.join(cdir, "f_*.png")))
    if have != S.frames:
        raise SystemExit("video %s: %d finished frames in %s, the cut has %d (run comp; `missing` lists the unrendered ones)" % (S.name, have, cdir, S.frames))
    adir = os.path.dirname(cdir)
    m4a, info = scene_audio(S, adir)
    ass = ass_path(S, adir)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(cdir, "f_%05d.png"), "-i", m4a,
         "-vf", "ass=%s:fontsdir=%s" % (ass, E.FONTS), "-map", "0:v", "-map", "1:a"] + ENC + ["-c:a", "copy", "-t", "%.4f" % (S.frames / float(FPS)), "-movflags", "+faststart", out])
    print("wrote", out, probe(out))
    return out


def probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames,width,height,r_frame_rate:format=duration,size",
                        "-of", "json", p], capture_output=True, text=True)
    d = json.loads(r.stdout); s = d["streams"][0]
    return dict(frames=int(s["nb_read_frames"]), size="%sx%s" % (s["width"], s["height"]), fps=s["r_frame_rate"], seconds=round(float(d["format"]["duration"]), 3),
                mb=round(int(d["format"]["size"]) / 1e6, 2))


def master(hook, scenes, tier, W, H, out, base_size=None, name="comp", hook_tail=0.0, scene_mp4=None, work=None):
    """hook mezzanine + scenes -> one encode.  Scenes come from their finished frame sequences (captions burnt here), or
    from a scene mezzanine mp4 when --scene-mp4 names one.  Audio: hook audio + scene mixes at their scene gains, one
    static gain over the whole."""
    scene_mp4 = scene_mp4 or {}
    work = work or os.path.join(os.path.dirname(os.path.abspath(out)), "master_work"); os.makedirs(work, exist_ok=True)
    ins, vf, af, lab_v, lab_a = [], [], [], [], []
    report = dict(parts=[])
    n = 0
    hd = probe(hook)
    if hook_tail:
        ins += ["-sseof", "-%.3f" % hook_tail]
    ins += ["-i", hook]
    vf.append("[0:v]fps=%d,scale=%d:%d:flags=lanczos,setsar=1,format=yuv420p[v0]" % (FPS, W, H)); lab_v.append("[v0]")
    af.append("[0:a]aresample=48000,aformat=channel_layouts=stereo[a0]"); lab_a.append("[a0]")
    off = hook_tail or hd["seconds"]
    report["parts"].append(dict(part="hook", file=hook, seconds=round(off, 3)))
    all_ass = []
    n = 1
    for sc in scenes:
        S = E.Scene(sc); dur = S.frames / float(FPS)
        base, cdir = dirs(S, tier, W, H, base_size, name)
        if S.name in scene_mp4:
            ins += ["-i", scene_mp4[S.name]]
            vf.append("[%d:v]fps=%d,scale=%d:%d:flags=lanczos,setsar=1,format=yuv420p[v%d]" % (n, FPS, W, H, n))
            af.append("[%d:a]aresample=48000,aformat=channel_layouts=stereo[a%d]" % (n, n))
            n_in = 1; srcs = "mezzanine " + scene_mp4[S.name]
        else:
            have = len(glob.glob(os.path.join(cdir, "f_*.png")))
            if have != S.frames:
                raise SystemExit("master: %s has %d finished frames, the cut has %d" % (S.name, have, S.frames))
            adir = os.path.dirname(cdir)
            wav, what = scene_wav(S, adir); g, I, tp = static_gain(wav)
            ass = ass_path(S, adir)
            ins += ["-framerate", str(FPS), "-i", os.path.join(cdir, "f_%05d.png"), "-i", wav]
            vf.append("[%d:v]ass=%s:fontsdir=%s,setsar=1,format=yuv420p[v%d]" % (n, ass, E.FONTS, n))
            af.append("[%d:a]volume=%.2fdB,atrim=0:%.4f[a%d]" % (n + 1, g, dur, n))
            n_in = 2; srcs = "frames %s; audio %s at %.2f dB" % (cdir, what, g)
        lab_v.append("[v%d]" % n); lab_a.append("[a%d]" % n)
        all_ass += ass_lines(S, off)
        report["parts"].append(dict(part=S.name, t0=round(off, 3), seconds=round(dur, 3), frames=S.frames, source=srcs))
        off += dur; n += n_in
    N = len(lab_v)
    open(out[:-4] + ".ass", "w", encoding="utf-8").write(ASS_HEAD + "\n".join(all_ass) + "\n")       # the new scenes' captions on the episode clock (reference / soft subs)
    # pass 1: the joined audio, measured as a whole
    aj = os.path.join(work, "master_audio.wav")
    run(["ffmpeg", "-y", "-loglevel", "error"] + ins + ["-filter_complex", ";".join(af) + ";" + "".join(lab_a) + "concat=n=%d:v=0:a=1[aj]" % N, "-map", "[aj]", aj])
    g, I, tp = static_gain(aj)
    m4a = os.path.join(work, "master_audio.m4a")
    g, I2, tp2 = encode_audio(aj, m4a, g)
    # pass 2: picture, one encode
    run(["ffmpeg", "-y", "-loglevel", "error"] + ins + ["-i", m4a, "-filter_complex", ";".join(vf) + ";" + "".join(lab_v) + "concat=n=%d:v=1:a=0[vj]" % N,
         "-map", "[vj]", "-map", "%d:a" % n] + ENC + ["-r", str(FPS), "-c:a", "copy", "-t", "%.4f" % off, "-movflags", "+faststart", out])
    report.update(out=out, seconds=round(off, 3), audio=dict(gain_db=round(g, 2), joined_lufs=I, joined_tp=tp, lufs=I2, true_peak=tp2), video=probe(out))
    json.dump(report, open(out[:-4] + ".json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps(report, ensure_ascii=False, indent=1))
    return report


def sheet(S, video_path, out, th=320, t_off=0.0):
    """3 frames per shot (10 / 50 / 90 %) from a conformed clip, labelled with shot id, class and scene frame."""
    cap = cv2.VideoCapture(video_path)
    ims = []
    for row in S.shots:
        n = row["f1"] - row["f0"]
        for u in (0.1, 0.5, 0.9):
            k = row["f0"] + int(round(u * (n - 1)))
            cap.set(cv2.CAP_PROP_POS_FRAMES, k + int(round(t_off * FPS)))
            ok, f = cap.read()
            if not ok: continue
            im = Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))
            ims.append((row, k, im.resize((int(im.width * th / im.height), th), Image.LANCZOS)))
    tw = ims[0][2].width; cols = min(len(ims), 12 if tw < th else 6); lab = 22
    rows_ = (len(ims) + cols - 1) // cols
    Sh = Image.new("RGB", (cols * (tw + 4), rows_ * (th + lab + 4)), (14, 14, 18)); d = ImageDraw.Draw(Sh)
    f = ImageFont.truetype(E.C.WORKS, 13)
    for i, (row, k, im) in enumerate(ims):
        x = (i % cols) * (tw + 4); y = (i // cols) * (th + lab + 4)
        Sh.paste(im, (x, y + lab)); d.text((x + 3, y + 3), "%s %s f%d" % (row["id"], row["cls"], k), font=f, fill=(232, 232, 236))
    Sh.save(out); print("wrote", out, Sh.size)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode"); ap.add_argument("--scene", default=""); ap.add_argument("--scenes", default="")
    ap.add_argument("--tier", default="draft"); ap.add_argument("--size", default="720x1280"); ap.add_argument("--base-size", default="")
    ap.add_argument("--frames", default=""); ap.add_argument("--name", default="comp"); ap.add_argument("--worker", default="0/1")
    ap.add_argument("--out", default=""); ap.add_argument("--video", default=""); ap.add_argument("--sheet", default="")
    ap.add_argument("--hook", default=""); ap.add_argument("--hook-tail", type=float, default=0.0); ap.add_argument("--scene-mp4", action="append", default=[])
    a = ap.parse_args()
    W, H = [int(x) for x in a.size.lower().split("x")]
    bs = tuple(int(x) for x in a.base_size.lower().split("x")) if a.base_size else None
    if a.mode == "master":
        if not a.hook or not os.path.exists(a.hook): raise SystemExit("master needs --hook <the hook mezzanine mp4>")
        master(a.hook, [E.scene_name(x) for x in a.scenes.split(",") if x], a.tier, W, H, os.path.abspath(a.out), bs, a.name, a.hook_tail,
               dict(x.split("=", 1) for x in a.scene_mp4))
        return
    S = E.Scene(a.scene)
    fl = None
    if a.frames:
        x, y = a.frames.split(":"); fl = list(range(int(x), int(y)))
    out = os.path.abspath(a.out) if a.out else os.path.join(HERE, "%s_%s.mp4" % (S.name, a.tier))
    if a.mode == "missing": missing(S, a.tier, *(bs or (W, H)))
    if a.mode == "ass": print(ass_path(S, os.path.dirname(dirs(S, a.tier, W, H, bs, a.name)[1])))
    if a.mode in ("comp", "scene"): comp(S, a.tier, W, H, fl, bs, a.name, tuple(int(x) for x in a.worker.split("/")))
    if a.mode in ("video", "scene"): video(S, a.tier, W, H, out, bs, a.name)
    if a.mode == "sheet" or (a.mode == "scene" and a.sheet): sheet(S, a.video or out, os.path.abspath(a.sheet) if a.sheet else out[:-4] + "_sheet.png")


if __name__ == "__main__":
    main()
