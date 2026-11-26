"""finish.py -- after the set's post: shot joins, radio static, bite flash, the title plate, then the flat v13 status
strip + title mark (v13/icons, drawn sharp at the output size after all blur); then captions (libass, Kanit Black,
captions_ohm.ass made from narr_ohm/captions_timing.json) + mix_ohm_v2.wav at one static gain (about -14 LUFS, true
peak <= -1 dBTP), and the contact sheet.

    python3 finish.py comp  --tier draft --size 360x640 [--frames a:b]     -> out/<tier>_<size>/comp/f_####.png
    python3 finish.py video --tier draft --size 360x640 --out draft_v1.mp4
    python3 finish.py sheet --video draft_v1.mp4 --out draft_sheet.png
    python3 finish.py all   --tier draft --size 360x640 --out draft_v1.mp4 --sheet draft_sheet.png
    python3 finish.py comp  --tier draft --size 720x1280 --base-size 360x640 --name comp_v3 --worker 0/4   (x4 in parallel)
    python3 finish.py video --tier draft --size 720x1280 --base-size 360x640 --name comp_v3 --out draft_v3.mp4
    python3 finish.py missing --tier draft --size 360x640                   list frames not rendered yet
"""
import os, sys, json, math, argparse, subprocess
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C
import cues as Q
from common import PROJ, FPS, NF, fr

MIX = os.path.join(C.AUDIO, "mix_ohm_v3.wav")             # v3: Ohm narration, final mix (narration starts 0.30 s in)


def base_dir(tier, W, H):
    return os.path.join(HERE, "out", "%s_%dx%d" % (tier, W, H))


def src(base, g):
    return os.path.join(base, C.shot_of(g), "f_%04d.png" % (g + 1))


def font(path, sz):
    return ImageFont.truetype(path, int(sz), layout_engine=ImageFont.Layout.RAQM)


# ------------------------------------------------------------------------------------------------ joins
def zoom_blur(a, amount, n=18):
    """radial push blur: mean of n copies scaled 1 .. 1 + amount about the centre."""
    if amount <= 0.002:
        return a
    h, w = a.shape[:2]
    acc = np.zeros_like(a, np.float32)
    for i in range(n):
        s = 1.0 + amount * i / (n - 1)
        M = np.float32([[s, 0, (1 - s) * w / 2], [0, s, (1 - s) * h / 2]])
        acc += cv2.warpAffine(a, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return acc / n


JOIN = [0.04, 0.09, 0.15]                                   # last three frames out, mirrored for the first three in


def join_amount(g):
    sid = C.shot_of(g)
    g0, g1 = C.shot_range(sid)
    i = C.SHOT_IDS.index(sid)
    amt = 0.0
    if i + 1 < len(C.SHOT_IDS) and C.SHOT_IDS[i + 1] not in Q.HARD_CUTS and g1 - g <= 3:
        amt = JOIN[3 - (g1 - g)]
    if i > 0 and sid not in Q.HARD_CUTS and g - g0 < 3:
        amt = max(amt, JOIN[2 - (g - g0)])
    return amt


# ------------------------------------------------------------------------------------------------ icons (v13/icons)
_IC = {}


def icons():
    """the flat v13 status strip (top-left row) and its title mark: drawn at the output size, laid over last."""
    if "m" not in _IC:
        os.environ.setdefault("DZ09_NARR", "narr_ohm")
        sys.path.insert(0, os.path.join(PROJ, "v13", "icons"))
        import noicons                                    # user: NO status icons at all; only the title mark (noicons.py)
        _IC["m"] = noicons
    return _IC["m"]


def icons_over(im, g):
    """PIL RGB(A) frame -> RGB with the v13 icon layer of film frame g on top."""
    rgb = np.asarray(im.convert("RGB"))
    H, W = rgb.shape[:2]
    return Image.fromarray(icons().over(rgb, g, "916" if H > W else "169"))


TITLE_FS, TITLE_TEXT_Y, TITLE_DIM = 124, 612, 0.45         # title text size / centre y (of 1280); how far the picture sinks to navy under it (v2 0.62)

# ------------------------------------------------------------------------------------------------ captions, mix
# key words in the captions are coloured (user: "does the caption emphasise words?"): amber = the fact to remember,
# red = the threat.  (caption text, the part to colour, colour).  A coloured caption also pops 12 % for 3 frames.
AMBER_ASS, RED_ASS = "&H03B7FF&", "&H4F45F5&"       # the v14 cards' amber #ffb703 and (a little brighter) red
EMPH = [("คนเจ็บไม่ตอบสนอง", "ไม่ตอบสนอง", RED_ASS), ("เฮ้ย!", "เฮ้ย!", RED_ASS), ("ก็เงียบไป", "เงียบไป", RED_ASS),
        ("ฝนถล่มกรุงเทพฯ", "ฝนถล่ม", AMBER_ASS), ("รถชนกันเป็นแพ", "ชนกันเป็นแพ", AMBER_ASS), ("ก้อง", "ก้อง", AMBER_ASS),
        ("เจ้าหน้าที่กู้ภัย", "กู้ภัย", AMBER_ASS), ("เครื่องตัดไร้สาย", "เครื่องตัดไร้สาย", AMBER_ASS), ("แบตเต็ม 3 ขีด", "3 ขีด", AMBER_ASS),
        ("4 สาย", "4 สาย", RED_ASS), ("น้ำเหนือ", "น้ำเหนือ", AMBER_ASS), ("วันนี้พ่อสัญญา", "สัญญา", AMBER_ASS),
        ("ทุกครั้งเลย...", "ทุกครั้งเลย...", RED_ASS), ("แล้วก็วางสาย", "วางสาย", RED_ASS), ("ไม่ขยับเลยสักนิด", "ไม่ขยับ", RED_ASS),
        ("เงยหน้าขึ้น", "เงยหน้าขึ้น", RED_ASS), ("มันพุ่ง", "มันพุ่ง", RED_ASS), ("เข้ากัดทันที", "กัด", RED_ASS),
        ("อีก 60 วินาที", "60 วินาที", AMBER_ASS), ("จะไม่ใช่คน", "ไม่ใช่คน", RED_ASS)]


def emph(text):
    for full, part, col in EMPH:
        if text.strip() == full and part in text:
            a, b = text.split(part, 1)
            return "{\\fscx112\\fscy112\\t(0,125,\\fscx100\\fscy100)}%s{\\c%s}%s{\\c&HFFFFFF&}%s" % (a, col, part, b)
    return text


def ass_path():
    """captions_ohm.ass: the Cap / Title styles and the title line of the approved .ass, the caption lines from
    narr_ohm/captions_timing.json (+0.30 s)."""
    p = os.path.join(HERE, "captions_ohm.ass")
    src = open(os.path.join(C.AUDIO_V1, "preview_v2.ass"), encoding="utf-8").read().split("\n")
    head = [l for l in src if l.strip() and not l.startswith("Dialogue:")]
    # v3 title: the text block is about 70 % of the frame width (libass size 124 -> about 500 px; it was 96 -> 390 px), under the 236 px v13 mark
    title = ["Dialogue: 0,%s,%s,Title,,0,0,0,,{\\pos(360,%d)\\fs%d}เขตปิดตาย 09\\N{\\fs%d\\c&HFFFFFF&}DEAD ZONE 09"
             % ("0:00:50.72", "0:00:53.32", TITLE_TEXT_Y, TITLE_FS, int(TITLE_FS * 0.62))]
    ts = lambda t: "%d:%02d:%05.2f" % (t // 3600, (t % 3600) // 60, t % 60)
    lines = ["Dialogue: 0,%s,%s,Cap,,0,0,0,,{\\pos(360,900)}%s" % (ts(c["t0"] + C.NARR0), ts(c["t1"] + C.NARR0), emph(c["text"])) for c in C.CAPS]
    txt = "\n".join(head + lines + title) + "\n"
    if not os.path.exists(p) or open(p, encoding="utf-8").read() != txt:
        open(p, "w", encoding="utf-8").write(txt)
    return p


def loudness(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-map", "0:a", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    tail = r[r.rindex("Summary:"):]
    I = float(tail.split("I:")[1].split("LUFS")[0]); tp = float(tail.split("Peak:")[1].split("dBFS")[0])
    return I, tp


def mix_path(target=-14.0, ceil=-1.0):
    """mix_ohm_v2.wav as AAC (320 kb/s) with ONE static gain, so the balance is untouched: as close to -14 LUFS as a
    true peak <= -1 dBTP of the ENCODED track allows (the encoder overshoots by 0.2-0.8 dB, so the gain is stepped
    down until the decoded track measures <= -1).  Writes mix_ohm_v2_norm.m4a + .json."""
    p = os.path.join(HERE, "mix_ohm_v3_norm.m4a")
    I, tp = loudness(MIX)
    gain = min(target - I, ceil - tp)
    for _ in range(8):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", MIX, "-af", "volume=%.2fdB" % gain, "-c:a", "aac", "-b:a", "320k", p], check=True)
        I2, tp2 = loudness(p)
        if tp2 <= ceil: break
        gain -= max(0.1, tp2 - ceil)
    json.dump(dict(source=MIX, gain_db=round(gain, 2), source_lufs=I, source_tp=tp, lufs=I2, true_peak=tp2, codec="aac 320k"), open(p[:-4] + ".json", "w"), indent=1)
    print("mix: gain %.2f dB -> %.1f LUFS, true peak %.1f dBTP (encoded)" % (gain, I2, tp2))
    return p


def comp_frame(base, g, W, H, tmp=None):
    p = src(base, g)
    if not os.path.exists(p):
        return None
    a = cv2.imread(p, cv2.IMREAD_COLOR).astype(np.float32) / 255.0
    if a.shape[1] != W or a.shape[0] != H:
        a = cv2.resize(a, (W, H), interpolation=cv2.INTER_AREA if a.shape[1] > W else cv2.INTER_LANCZOS4)
    t = g / float(FPS)
    a = zoom_blur(a, join_amount(g))
    # the radio dies: three frames of static over the picture
    if fr(Q.STATIC[0]) <= g < fr(Q.STATIC[1]):
        n = np.random.default_rng(g).random((H // 2, W // 2)).astype(np.float32)
        n = cv2.resize(n, (W, H), interpolation=cv2.INTER_NEAREST)[..., None]
        a = a * 0.5 + n * 0.5
    # the lunge: ONE frame, white in the middle going to red at the edges
    if g == int(math.ceil(Q.LUNGE_FLASH * FPS - 1e-6)):
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H * 0.42) / (H / 2)) ** 2)[..., None]
        col = np.float32([235, 240, 255])[None, None] / 255.0 * np.clip(1.15 - 0.55 * r, 0, 1) + np.float32([30, 30, 230])[None, None] / 255.0 * np.clip(0.55 * r - 0.15, 0, 1)
        a = a * 0.35 + col * 0.65
    # the bite: a 2-frame red flash, then a red cast that drains away
    gb = fr(Q.BITE)
    if gb <= g < gb + 2:
        a = a * 0.42 + np.float32([30, 40, 226])[None, None] / 255.0 * 0.58
    elif gb + 2 <= g < fr(45.303):
        k = 0.26 * max(0.0, 1 - (t - Q.BITE - 0.08) / 1.4)
        a = a * (1 - k) + np.float32([10, 10, 160])[None, None] / 255.0 * k
    # title plate: the picture sinks to navy under the title
    if t >= Q.TITLE:
        k = TITLE_DIM * min(1.0, (t - Q.TITLE) / 0.5)
        a = a * (1 - k) + np.float32([26, 10, 6])[None, None] / 255.0 * k
    im = Image.fromarray(cv2.cvtColor((np.clip(a, 0, 1) * 255).astype(np.uint8), cv2.COLOR_BGR2RGB))
    return icons_over(im, g)                               # v13 flat strip + title mark: last, sharp, at the output size


def comp(tier, W, H, frames=None, force=True, base_size=None, name="comp", worker=(0, 1)):
    """base_size = (w, h) of the rendered frames when they differ from the output (e.g. a 360x640 draft finished at
    720x1280: the picture is scaled, the icons are drawn at the output size).  worker = (i, n): every n-th frame."""
    base = base_dir(tier, *(base_size or (W, H)))
    odir = base if not base_size else base_dir(tier + "_from%dx%d" % tuple(base_size), W, H)
    out = os.path.join(odir, name)
    os.makedirs(out, exist_ok=True)
    miss = []
    for g in (frames or range(NF)):
        if g % worker[1] != worker[0]: continue
        im = comp_frame(base, g, W, H)
        if im is None:
            miss.append(g); continue
        im.save(os.path.join(out, "f_%04d.png" % (g + 1)), compress_level=1)
    icons().close()
    print("comp done -> %s; missing %d frames" % (out, len(miss)), miss[:20])
    return miss


def video(tier, W, H, out, base_size=None, name="comp"):
    base = base_dir(tier, W, H) if not base_size else base_dir(tier + "_from%dx%d" % tuple(base_size), W, H)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(base, name, "f_%04d.png"), "-i", mix_path(),
           "-vf", "ass=%s:fontsdir=%s" % (ass_path(), C.FONTS), "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "15", "-tune", "animation",
           "-pix_fmt", "yuv420p", "-c:a", "copy", "-t", "%.3f" % C.DUR, "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    print("wrote", out, "loudness (LUFS, dBTP) of the encoded track:", loudness(out))


def grab(video_path, g, out):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video_path, "-vf", "select=eq(n\\,%d)" % g, "-frames:v", "1", out], check=True)
    return out


def sheet(video_path, out, per=3, th=320):
    """3 frames per shot (10 / 50 / 90 % of its length) + the title, labelled with shot id and film time."""
    tmp = os.path.join(HERE, "tmp", "sheet"); os.makedirs(tmp, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    items = []
    for sid in C.SHOT_IDS:
        g0, g1 = C.shot_range(sid)
        if sid == "S24": g1 = fr(Q.TITLE)
        for u in (0.1, 0.5, 0.9):
            items.append((sid, g0 + int(round(u * (g1 - g0 - 1)))))
    for u in (0.15, 0.5, 0.9):
        items.append(("TITLE", fr(Q.TITLE) + int(u * (NF - 1 - fr(Q.TITLE)))))
    ims = []
    for sid, g in items:
        cap.set(cv2.CAP_PROP_POS_FRAMES, g)
        ok, f = cap.read()
        if not ok: continue
        im = Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))
        tw = int(im.width * th / im.height)
        ims.append((sid, g, im.resize((tw, th), Image.LANCZOS)))
    tw = ims[0][2].width
    cols = 15 if tw < th else 6
    lab = 22
    rows = (len(ims) + cols - 1) // cols
    S = Image.new("RGB", (cols * (tw + 4), rows * (th + lab + 4)), (14, 14, 18)); d = ImageDraw.Draw(S)
    f = font(C.WORKS, 13)
    for i, (sid, g, im) in enumerate(ims):
        x = (i % cols) * (tw + 4); y = (i // cols) * (th + lab + 4)
        S.paste(im, (x, y + lab))
        d.text((x + 3, y + 3), "%s  %.2fs  f%d" % (sid, g / float(FPS), g), font=f, fill=(232, 232, 236))
    S.save(out); print("wrote", out, S.size)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode"); ap.add_argument("--tier", default="draft"); ap.add_argument("--size", default="360x640")
    ap.add_argument("--frames", default=""); ap.add_argument("--out", default=os.path.join(HERE, "draft_v1.mp4"))
    ap.add_argument("--sheet", default=os.path.join(HERE, "draft_sheet.png")); ap.add_argument("--video", default="")
    ap.add_argument("--base-size", default="", help="size of the rendered frames when it differs from --size (e.g. 360x640)")
    ap.add_argument("--name", default="comp", help="name of the finished-frames folder (default comp)")
    ap.add_argument("--worker", default="0/1", help="comp only: i/n = every n-th frame starting at i (run n in parallel)")
    a = ap.parse_args()
    W, H = [int(x) for x in a.size.lower().split("x")]
    fl = None
    if a.frames:
        x, y = a.frames.split(":"); fl = list(range(int(x), int(y)))
    out = a.out if os.path.isabs(a.out) else os.path.join(HERE, a.out)
    sh = a.sheet if os.path.isabs(a.sheet) else os.path.join(HERE, a.sheet)
    if a.mode == "missing":
        base = base_dir(a.tier, W, H)
        m = [g for g in range(NF) if not os.path.exists(src(base, g))]
        print(len(m), "missing", m[:40])
    bs = tuple(int(x) for x in a.base_size.lower().split("x")) if a.base_size else None
    if a.mode in ("comp", "all"): comp(a.tier, W, H, fl, base_size=bs, name=a.name, worker=tuple(int(x) for x in a.worker.split("/")))
    if a.mode in ("video", "all"): video(a.tier, W, H, out, base_size=bs, name=a.name)
    if a.mode in ("sheet", "all"): sheet(a.video or out, sh if a.mode == "all" or a.sheet else sh)


if __name__ == "__main__":
    main()
