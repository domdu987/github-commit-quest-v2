"""make_dummy.py -- the dummy scene sc99 that proves the pipe: a 4-shot plan in the shape of shots_ep1.json /
narration_ep1.json, a "recorded" caption timing that differs from the plan's estimate, and placeholder audio
(numpy noise bursts on the captions: NOT a voice, nothing synthesised by a service)."""
import os, json, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))

# the plan's estimate (seconds on a pretend episode clock starting at 1000.0)
T = 1000.0
sent = [("s901", "narr", [("ฉากทดสอบ", 0.10, 0.55, None, None)]),
        ("s902", "kong", [("ฮัลโหล!", 0.60, 0.95, "ฮัลโหล!", "red"), ("ได้ยินไหม", 0.95, 1.20, None, None)]),
        ("s903", "narr", [("30 วินาที", 1.25, 1.80, "30 วินาที", "amber")]),
        ("s904", "narr", [("ภาพผ่านท่อ", 1.85, 2.15, None, None), ("ครบแล้ว", 2.15, 2.40, "ครบ", "amber")])]
shots = [("S901", "B", "X1", 0.0, 0.60, "(picture beat, no word)", [("s901", ["ฉากทดสอบ"])], "WIDE: the rescue zone, the hook's S02 crane position held"),
         ("S902", "A", "X1", 0.60, 1.25, "ฮัลโหล!", [("s902", ["ฮัลโหล!", "ได้ยินไหม"])], "MCU: Kong on the phone, HIS line: his mouth moves"),
         ("S903", "C1", "2D", 1.25, 1.85, "30 วินาที", [("s903", ["30 วินาที"])], "INSERT drawn: the wrist watch, one red second hand"),
         ("S904", "A", "X1", 1.85, 2.50, "ภาพผ่านท่อ", [("s904", ["ภาพผ่านท่อ", "ครบแล้ว"])], "MS: Kong with the cutter, NARRATOR line: nobody's mouth moves")]
fr = lambda t: int(round(t * 24))
sd = dict(episode=dict(fps=24, size="720x1280"), note="dummy scene 99 for the pipe proof",
          totals=dict(cpu_s_per_frame={"A": 68.2, "B": 36.6, "C2": 32.0, "C1": 2.0}),
          scenes=[dict(scene="99", t0=T, t1=T + 2.50, f0=fr(T), f1=fr(T + 2.5), frames=60)],
          shots=[dict(id=i, scene="99", t0=T + a, t1=T + b, f0=fr(T + a), f1=fr(T + b), frames=fr(T + b) - fr(T + a), cls=c, set=s, size="", action=act, cut_on=co,
                      narration=[dict(id=x, captions=y) for x, y in nar]) for i, c, s, a, b, co, nar, act in shots])
nd = dict(title="dummy narration", sentences=[
    dict(id=i, scene="99", speaker=sp, text=" ".join(c[0] for c in caps),
         captions=[dict(dict(text=tx, t0=T + a, t1=T + b), **(dict(emph=e, colour=col) if e else {})) for tx, a, b, e, col in caps]) for i, sp, caps in sent])
json.dump(sd, open(os.path.join(HERE, "shots_dummy.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(nd, open(os.path.join(HERE, "narration_dummy.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# the "recording": the same captions at other times (seconds from the start of the narration wav)
rec = [("s901", "ฉากทดสอบ", 0.00, 0.42), ("s902", "ฮัลโหล!", 0.50, 0.88), ("s902", "ได้ยินไหม", 0.88, 1.12),
       ("s903", "30 วินาที", 1.21, 1.72), ("s904", "ภาพผ่านท่อ", 1.80, 2.08), ("s904", "ครบแล้ว", 2.08, 2.30)]
json.dump([dict(id=i, text=t, t0=a, t1=b) for i, t, a, b in rec], open(os.path.join(HERE, "captions_timing.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

sr = 24000
rng = np.random.default_rng(9)
n = int(2.35 * sr); x = np.zeros(n, np.float32); tt = np.arange(n) / sr
for _i, _t, a, b in rec:                                       # 5 "syllables" per second of band-limited buzz inside each caption
    m = (tt >= a) & (tt < b)
    syl = np.abs(np.sin(np.pi * (tt - a) * 5.5)) ** 0.6
    x += m * syl * (0.22 * np.sin(2 * np.pi * 150 * tt) + 0.10 * np.sin(2 * np.pi * 300 * tt) + 0.05 * rng.standard_normal(n))


def save(p, a, sr):
    w = wave.open(p, "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()


save(os.path.join(HERE, "narr_placeholder.wav"), x, sr)
# placeholder mix: a rain bed (filtered noise) + the placeholder "voice" 0.10 s in, quiet
N = int(2.6 * sr); bed = rng.standard_normal(N).astype(np.float32)
bed = np.convolve(bed, np.ones(24) / 24.0, mode="same") * 0.20
mix = bed.copy(); o = int(0.10 * sr); mix[o:o + n] += x[:max(0, min(n, N - o))] * 0.5
save(os.path.join(HERE, "mix_placeholder.wav"), mix, sr)
print("wrote dummy plan, timing and placeholder audio in", HERE)
