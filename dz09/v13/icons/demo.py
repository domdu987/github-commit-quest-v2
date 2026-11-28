"""demo.py -- demo.mp4: the whole film at 720x1280, icons over the newest draft frames, ohm captions, mix_ohm_v2.wav.
    python3 demo.py frames i/n     # render every n-th frame starting at i (run n of these in parallel)
    python3 demo.py video"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
import icons13 as I, base
OUT = os.path.join(I.HERE, "tmp", "demo")
def ass():
    src = open(os.path.join(I.PROJ, "audio", "narr_v1", "preview_v2.ass"), encoding="utf-8").read().split("\n")
    head = [l for l in src if not l.startswith("Dialogue:")]
    title = [l for l in src if l.startswith("Dialogue:") and ",Title," in l]
    ts = lambda t: "%d:%02d:%05.2f" % (t // 3600, (t % 3600) // 60, t % 60)
    caps = json.load(open(os.path.join(I.PROJ, "audio", "narr_ohm", "captions_timing.json"), encoding="utf-8"))
    lines = ["Dialogue: 0,%s,%s,Cap,,0,0,0,,{\\pos(360,900)}%s" % (ts(c["t0"] + 0.3), ts(c["t1"] + 0.3), c["text"]) for c in caps]
    p = os.path.join(I.HERE, "tmp", "ohm.ass")
    open(p, "w", encoding="utf-8").write("\n".join([l for l in head if l.strip()] + lines + title) + "\n")
    return p
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    if sys.argv[1] == "frames":
        i, n = [int(x) for x in sys.argv[2].split("/")]
        last = None
        for g in range(i, I.NF, n):
            p, d = base.frame_path(g)
            im = np.asarray(Image.open(p).convert("RGB").resize((720, 1280), Image.LANCZOS)) if p else last
            last = im
            if g / 24.0 >= I.T.TITLE:                                    # finish.py's navy title plate
                k = 0.62 * min(1.0, (g / 24.0 - I.T.TITLE) / 0.5)
                im = (im * (1 - k) + np.float32([6, 10, 26]) * k).astype(np.uint8)
            Image.fromarray(I.over(im, g)).save(os.path.join(OUT, "f_%04d.jpg" % g), quality=93)
    else:
        a = ass()
        subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-framerate", "24", "-i", os.path.join(OUT, "f_%04d.jpg"), "-i",
                               os.path.join(I.PROJ, "audio", "narr_ohm", "mix_ohm_v2.wav"), "-vf", "ass=%s:fontsdir=%s" % (a, os.path.join(I.PROJ, "fonts")),
                               "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest",
                               os.path.join(I.HERE, "demo.mp4")])
