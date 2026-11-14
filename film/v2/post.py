#!/usr/bin/env python3
"""post.py -- raw shot frames -> final frames out/frames/f_0001.png ... (stdlib + ffmpeg; nothing is drawn here).

    python3 post.py [out/manifest.json]

Outside the browser, with ffmpeg:
  * supersampled raw frames (1440x2560) are scaled to 720x1280 with a bilinear filter (edge softness matched to the
    reference, see out/METRICS.md); draft frames rendered at 720x1280 get a 0.45 px Gaussian instead;
  * the frames of a dissolve are mixed from the two shots with the smoothstep weight P*P*(3-2P), P = i / (n + 1)
    (camera_motion.md 1.4), in R'G'B' like a video mixer.
Captions are burned afterwards by assemble.py, so they never take part in a mix.
"""
import json, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))


def raw_path(p):
    """the raw frame as rendered: PNG, or the JPEG intermediate written by render.js --jpg."""
    if os.path.exists(p):
        return p
    j = os.path.splitext(p)[0] + ".jpg"
    if os.path.exists(j):
        return j
    raise SystemExit("missing raw frame " + p)


def main(argv):
    man_path = argv[0] if argv else os.path.join(HERE, "out", "manifest.json")
    out = os.path.dirname(os.path.abspath(man_path))
    man = json.load(open(man_path))
    W, H, fps = man["width"], man["height"], man["fps"]
    raw = dict(((f["shot"], f["g"]), f["out"]) for f in man["frames"])
    seq = os.path.join(out, "seq")
    shutil.rmtree(seq, ignore_errors=True)
    os.makedirs(seq)
    frames_dir = os.path.join(out, "frames")
    shutil.rmtree(frames_dir, ignore_errors=True)
    os.makedirs(frames_dir)
    ext = None
    for g, src in enumerate(man["timeline"]):
        a = raw_path(raw[tuple(src[0])])
        b = raw_path(raw[tuple(src[1])]) if len(src) == 3 else a
        e = os.path.splitext(a)[1]
        if ext not in (None, e) or os.path.splitext(b)[1] != e:
            raise SystemExit("raw frames mix .png and .jpg: render them again with one setting")
        ext = e
        os.symlink(a, os.path.join(seq, "a_%04d%s" % (g, e)))
        os.symlink(b, os.path.join(seq, "b_%04d%s" % (g, e)))
    # raw frames at 2x are scaled down (bilinear); draft frames rendered at 1x get a 0.45 px Gaussian instead, which gives
    # the same measured edge softness (1.59 px against 1.60 px), so a draft looks like the final
    first = raw_path(raw[tuple(man["timeline"][0][0])])
    w_in = int(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width", "-of", "csv=p=0", first]).decode().strip().strip(","))
    soften = ("scale=%d:%d:flags=bilinear" % (W, H)) if w_in != W else "gblur=sigma=0.45"
    # pass 1: every frame from its own shot
    thr = ["-threads", "2", "-filter_threads", "2", "-filter_complex_threads", "2"]
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + thr + ["-framerate", str(fps), "-start_number", "0", "-i", os.path.join(seq, "a_%04d" + ext),
                    "-vf", soften + ",format=rgb24", "-start_number", "1", os.path.join(frames_dir, "f_%04d.png")], check=True)
    # pass 2: the frames of each dissolve, mixed from both shots: weight of B = P*P*(3-2P), P = (N + 1) / (n + 1)
    notes = []
    for tr in man["transitions"]:
        if tr["kind"] != "dissolve":
            continue
        n0, n = tr["first"], tr["frames"]
        p = "((N+1)/%d)" % (n + 1)
        fc = ("[0:v]%s,format=gbrp[a];[1:v]%s,format=gbrp[b];"
              "[a][b]blend=all_expr='A+(B-A)*%s*%s*(3-2*%s)',format=rgb24[o]" % (soften, soften, p, p, p))
        subprocess.run(["ffmpeg", "-v", "error", "-y"] + thr + ["-framerate", str(fps), "-start_number", str(n0), "-i", os.path.join(seq, "a_%04d" + ext),
                        "-framerate", str(fps), "-start_number", str(n0), "-i", os.path.join(seq, "b_%04d" + ext),
                        "-filter_complex", fc, "-map", "[o]", "-frames:v", str(n), "-start_number", str(n0 + 1), os.path.join(frames_dir, "f_%04d.png")], check=True)
        notes.append("g %d-%d %s>%s %d-frame smoothstep" % (n0, n0 + n - 1, tr["a"], tr["b"], n))
    n = len([f for f in os.listdir(frames_dir) if f.endswith(".png")])
    shutil.rmtree(seq, ignore_errors=True)
    if n != man["n_frames"]:
        raise SystemExit("expected %d frames, wrote %d" % (man["n_frames"], n))
    print("wrote %d frames to %s (dissolves: %s)" % (n, frames_dir, "; ".join(notes) or "none"))


if __name__ == "__main__":
    main(sys.argv[1:])
