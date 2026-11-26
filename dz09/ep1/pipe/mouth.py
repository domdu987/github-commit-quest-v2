"""mouth.py -- mouth envelope of a scene from its narration wav, and who it belongs to (no bpy).

    python3 mouth.py --scene sc02 --wav PROJ/audio/ep1/sc02/narr_final.wav      -> cut/mouth_sc02.json
    python3 mouth.py --scene sc02                                               synthetic envelope from the caption timing

Track (one value per scene frame):
    env      RMS of the wav in that frame, 0..1 (95th percentile of the voiced frames = 1), the wav starts narr0 into the scene
    level    the mouth drawing: 0, .25, .5, .75, 1  (the hook's mapping: floor 0.10, 0.25 + 0.75 * v ** 0.7, 5 steps)
    speakers [f0, f1, speaker, sentence id]: the frames of every sentence (first caption start .. last caption end)
Lip-sync assignment is by SPEAKER: Scene.mouth(actor, g) gives `level` only while the sentence at g is that actor's;
narrator sentences ("narr") and gaps move nobody.  A shot only poses the actors it stages, so a voice that is heard
but not seen (the phone) moves nobody either.
"""
import os, sys, json, math, wave, argparse
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import epcommon as E

FPS = E.FPS
FLOOR = 0.10


def read_wav(path):
    w = wave.open(path)
    sr, n, ch, sw = w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth()
    a = np.frombuffer(w.readframes(n), dtype={1: np.int8, 2: np.int16, 4: np.int32}[sw]).astype(np.float32)
    return a.reshape(-1, ch).mean(1) / float(2 ** (8 * sw - 1)), sr


def envelope(wav_path, n_frames, narr0):
    a, sr = read_wav(wav_path)
    hop = sr / float(FPS)
    env = np.zeros(n_frames, np.float32)
    for k in range(n_frames):
        i0 = int(round((k / float(FPS) - narr0) * sr)); i1 = int(round(i0 + hop))
        if i1 <= 0 or i0 >= len(a): continue
        seg = a[max(i0, 0):i1]
        env[k] = float(np.sqrt((seg * seg).mean())) if len(seg) else 0.0
    p = np.percentile(env[env > 0], 95) if (env > 0).any() else 1.0
    return np.clip(env / max(p, 1e-6), 0, 1)


def synthetic(caps, n_frames):
    """no recording yet: syllables at about 5 per second inside every caption (so a draft's mouths move on the words)."""
    env = np.zeros(n_frames, np.float32)
    for c in caps:
        a, b = int(round(c["t0"] * FPS)), int(round(c["t1"] * FPS))
        for k in range(max(a, 0), min(b, n_frames)):
            ph = (k / float(FPS) - c["t0"]) * 5.2
            env[k] = 0.35 + 0.65 * abs(math.sin(math.pi * ph)) * (0.7 + 0.3 * E.C.hash01(k, 3))
        if b - 1 < n_frames and b - 1 >= 0: env[b - 1] *= 0.4
    return env


def level(v):
    if v < FLOOR: return 0.0
    v = (v - FLOOR) / (1 - FLOOR)
    return round(max(0.0, min(1.0, 0.25 + 0.75 * v ** 0.7)) * 4) / 4.0


def speakers(caps):
    out = []
    for c in caps:
        a, b = int(round(c["t0"] * FPS)), int(round(c["t1"] * FPS))
        if out and out[-1][3] == c["id"]:
            out[-1][1] = b
        else:
            out.append([a, b, c.get("speaker", "narr"), c["id"]])
    return out


def caps_sig(S):
    """what a track was built against: the scene length, the lead-in and every caption's frames and speaker."""
    return E.sha(S.frames, S.narr0, [(c["id"], c["text"], round(c["t0"], 3), round(c["t1"], 3), c.get("speaker", "narr")) for c in S.caps])


def build(S, wav=None):
    """S = epcommon.Scene.  Returns the track dict (and does not write it)."""
    env = envelope(wav, S.frames, S.narr0) if wav else synthetic(S.caps, S.frames)
    return dict(scene=S.name, fps=FPS, frames=S.frames, source=os.path.abspath(wav) if wav else "synthetic (caption timing)",
                cut_source=S.d.get("source"), caps_sig=caps_sig(S), env=[round(float(x), 3) for x in env], level=[level(float(x)) for x in env], speakers=speakers(S.caps))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", required=True); ap.add_argument("--wav", default=""); ap.add_argument("--out", default="")
    a = ap.parse_args()
    S = E.Scene(a.scene)
    wav = a.wav or S.d.get("narration_wav") or None
    if wav and not os.path.isabs(wav): wav = os.path.join(E.PROJ, wav)
    tr = build(S, wav)
    out = a.out or os.path.join(os.path.dirname(S.path), "mouth_%s.json" % S.name)
    json.dump(tr, open(out, "w", encoding="utf-8"), ensure_ascii=False)
    sp = {}
    for f0, f1, who, sid in tr["speakers"]:
        lv = tr["level"][f0:f1]
        d = sp.setdefault(who, [0, 0]); d[0] += f1 - f0; d[1] += sum(1 for x in lv if x > 0)
    print("wrote", out, "source:", tr["source"])
    for who, (n, m) in sorted(sp.items()):
        print("  %-8s %5d frames spoken, mouth open on %d%s" % (who, n, m, "   (narrator: moves nobody)" if who == "narr" else ""))


if __name__ == "__main__":
    main()
