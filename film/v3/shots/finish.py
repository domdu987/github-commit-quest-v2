#!/usr/bin/env python3
"""finish.py -- finished frames -> MP4 with Thai captions (+ narration).

    python3 finish.py <frames_dir> <out_dir> [name=proto_v3]

1. writes <out_dir>/caps_burn.json from the Thai timing file: every phrase exactly as given, with the file's
   caption_style_prefix (libass override selecting Kanit Black at the reference weight) in front; hard swaps.
2. python3 proj/assemble.py <frames_dir> <out_dir>/<name>_silent.mp4 caps_burn.json 30   (captions burned last)
3. if the timing file names a narration WAV: muxes it, delayed by audio_offset, AAC 192k, video stream copied,
   into <out_dir>/<name>.mp4.  Without audio the silent file is copied to <name>.mp4.
"""
import json, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import timing

PROJ = timing.PROJ


def main(argv):
    frames, out = argv[0], argv[1]
    name = argv[2] if len(argv) > 2 else "proto_v3"
    T = timing.load()
    caps = [dict(t0=p["t0"], t1=p["t1"], text=T["caption_style_prefix"] + p["text"]) for p in T["phrases"]]
    caps_path = os.path.join(out, "caps_burn.json")
    json.dump(caps, open(caps_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    silent = os.path.join(out, name + "_silent.mp4")
    subprocess.run([sys.executable, os.path.join(PROJ, "assemble.py"), frames, silent, caps_path, "30"], check=True)
    final = os.path.join(out, name + ".mp4")
    dur = T["N"] / 30.0
    if T["audio"] and os.path.exists(T["audio"]):
        ms = int(round(T["audio_offset"] * 1000))
        af = ("adelay=%d:all=1," % ms if ms > 0 else "") + "apad"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", T["audio"], "-map", "0:v:0", "-map", "1:a:0",
                        "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "192k", "-t", "%.4f" % dur, "-movflags", "+faststart", final], check=True)
        print("finish: muxed %s (delay %d ms) -> %s" % (T["audio"], ms, final))
    else:
        shutil.copyfile(silent, final)
        print("finish: no narration in the timing file; %s is silent" % final)
    print(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "stream=codec_name,width,height,r_frame_rate,nb_frames,duration,bit_rate",
                                   "-of", "compact", final]).decode())
    return final


if __name__ == "__main__":
    main(sys.argv[1:])
