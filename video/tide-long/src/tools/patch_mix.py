"""Long version (YouTube 16:9): each episode's own mix.py, re-pointed at its long-version schedule. Exact, asserted replacements.
  - EP.1: no choice or end card cues; the music (dipped since "again") fades out over the part's last second instead of the hard cut
  - EP.2: bridge A cues (brA, open, grab without a voice); the music fades out as the live dies; no choice or end card
  - EP.3: bridge B cues (brB, yai0, hook, cars without a voice); the ending as delivered (the music fades under "ตอนจบ")
  - all: one static gain to -14 LUFS (measured twice) instead of single-pass loudnorm, so vo_stem.wav and music_stem.wav are exactly
    what is summed into mix.wav (musiccheck needs that); a soft knee above -3 dBFS keeps peaks at or under -1 dBFS; MIXOUT = output dir.
suno1 restarts from 0 s in every part: its first second is near-silent, so each join is the outgoing music faded to nothing, then the
incoming theme coming up under the bridge narration (no overlap needed)."""
import os

W = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def sub(path, old, new, count=1):
    s = open(path).read()
    n = s.count(old)
    assert n == count, (path, old[:80], n)
    open(path, "w").write(s.replace(old, new))


TAIL_OLD = {
    1: '''peak = np.max(np.abs(mix))
if peak > 0.98:
    mix = np.tanh(mix / peak * 1.2) * 0.95
out = os.path.join(HERE, "mix_raw.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", out],
               input=mix.astype(np.float32).tobytes(), check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", os.path.join(HERE, "mix.wav")], check=True)
print("mix written", TOTAL)
''',
}
TAIL_OLD[2] = TAIL_OLD[3] = TAIL_OLD[1].replace(
    '''subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", os.path.join(HERE, "mix.wav")], check=True)''',
    '''# single-pass loudnorm lands ~0.8 dB under its target on this mix: aim at -13.2 to measure -14
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-af", "loudnorm=I=-13.2:TP=-1.5:LRA=11", "-ar", "48000", os.path.join(HERE, "mix.wav")], check=True)''')
TAIL_NEW = '''# ---- long version (YouTube 16:9): one static gain to -14 LUFS (measured twice) instead of single-pass loudnorm, so vo_stem.wav and
# music_stem.wav are exactly what is in mix.wav (musiccheck); a soft knee above -3 dBFS keeps the peaks at or under -1 dBFS ----
OUT = os.environ.get("MIXOUT", HERE)
os.makedirs(OUT, exist_ok=True)
mstem = mus * duck


def wr(path, x, codec="pcm_s16le"):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", "-c:a", codec, path],
                   input=x.astype(np.float32).tobytes(), check=True)


def integrated(path):
    o = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\\s+(-?[0-9.]+) LUFS", o)[-1])


def knee(x):
    ax = np.abs(x)
    return np.where(ax > 0.7, np.sign(x) * (0.7 + 0.19 * np.tanh((ax - 0.7) / 0.19)), x).astype(np.float32)


raw, g = os.path.join(OUT, "mix_raw.wav"), 1.0
for _ in range(3):   # the gain is measured through the knee, so the part lands on -14.0 with its peaks held under -1 dBFS
    wr(raw, knee(mix * g), "pcm_f32le"); g *= 10 ** ((-14.0 - integrated(raw)) / 20)
os.remove(raw)
mix, vo_s, mstem = knee(mix * g), vo * g, mstem * g
wr(os.path.join(OUT, "mix.wav"), mix)
wr(os.path.join(OUT, "vo_stem.wav"), vo_s, "pcm_f32le")
wr(os.path.join(OUT, "music_stem.wav"), mstem, "pcm_f32le")
print("mix written", TOTAL, "s · gain", round(20 * np.log10(g), 2), "dB · integrated", integrated(os.path.join(OUT, "mix.wav")), "LUFS · peak",
      round(20 * np.log10(float(np.max(np.abs(mix)))), 2), "dBFS")
'''

for ep in (1, 2, 3):
    p = os.path.join(W, f"ep{ep}", "mix.py")
    sub(p, "import json\nimport os\n", "import json\nimport os\nimport re\n")
    sub(p, TAIL_OLD[ep], TAIL_NEW)
    # the effects bus low-passed at ~4.5 kHz (skill A4 / hisscheck): synth.py's splashes, whooshes and roars are flat noise up there;
    # the delivered tide mixes failed hisscheck on this (flatness 0.66 / 0.72 / 0.48), the bus alone reads 0.80
    sub(p, "sfx = level(sfx, -27)\n",
        "sfx = np.frombuffer(subprocess.run([\"ffmpeg\", \"-v\", \"error\", \"-f\", \"f32le\", \"-ar\", str(SR), \"-ac\", \"1\", \"-i\", \"-\", \"-af\", \"lowpass=f=4500,lowpass=f=4500,highpass=f=40\",\n"
        "                                    \"-f\", \"f32le\", \"-\"], input=sfx.astype(np.float32).tobytes(), capture_output=True, check=True).stdout, np.float32).copy()\n"
        "sfx = level(np.pad(sfx, (0, max(0, N - len(sfx))))[:N], -27)   # long version: the effects bus low-passed at ~4.5 kHz (A4: no hiss)\n")

CHOICE_END = {
    1: '''    # the choice: ticks, the heartbeat quickens, the pull → black
    *tick3("choice", 0.0, 0.32), *beats("choice", 0.2, D["choice"] - 0.6, 0.55, 0.4), ("choice", D["choice"] - 1.3, "whoosh", 0.36), ("choice", D["choice"] - 1.2, "splash", 0.4),
    # the end card: the paper note flaps
    ("end", 0.15, "whoosh", 0.32), ("end", 0.5, "flap", 0.2), ("end", 1.2, "flap", 0.16), ("end", 0.8, "ding", 0.26),
''',
    2: '''    # the choice: ticks, the heartbeat quickens, the pull → black
    *tick3("choice", 0.0, 0.32), *beats("choice", 0.2, D["choice"] - 0.6, 0.55, 0.4), ("choice", D["choice"] - 1.3, "whoosh", 0.36), ("choice", D["choice"] - 1.2, "splash", 0.4),
    # the end card: the paper note flaps, the "ตอนจบ" sticker is stamped on
    ("end", 0.15, "whoosh", 0.32), ("end", 0.5, "flap", 0.2), ("end", 1.0, "thud", 0.26), ("end", 1.05, "ding", 0.24), ("end", 1.6, "flap", 0.16),
''',
}
CUT_OLD = '''cut, card = int(T("choice", -0.12) * SR), int(T("end", 0.1) * SR)
mix[cut - 240:cut] *= np.linspace(1, 0, 240)
mix[cut:card] = 0  # a beat of black and silence after the cliffhanger, then only the end card's own sounds
'''

# ================= EP.1 =================
p = os.path.join(W, "ep1", "mix.py")
sub(p, CHOICE_END[1], "    # long version: no choice and no end card; the film goes straight on into EP.2's bridge\n")
sub(p, 'dip(T("again", 0), T("choice", 0), 0.4)\n', 'dip(T("again", 0), TOTAL + 1, 0.4)   # long version: the dip runs to the end of the part\n')
sub(p, 'end = int(T("choice", -0.12) * SR)\nmus[end:] = 0  # hard cut to black and silence\n',
    'a = int((TOTAL - 1.0) * SR)\nmus[a:] *= np.linspace(1, 0, N - a)   # long version: the music fades out over the last second; EP.2\'s part starts suno1 again\n')
sub(p, CUT_OLD, "")

# ================= EP.2 =================
p = os.path.join(W, "ep2", "mix.py")
sub(p, '''    # the hook: a sound on frame 0 (the long breath of the sea still out), จูน's feet on the steps, her breath
    ("open", 0.0, "swell", 0.3), *[("open", 0.35 + i * 0.3, "steps", 0.09) for i in range(8)], ("open", 0.2, "pant", 0.14), *beats("open", 0.2, D["open"] - 0.2, 0.7, 0.2),
    # the old hand clamps her wrist on "อย่า": the sting, the grip, the sandal skids
    ("grab", vo_t("grab") - 0.02, "sting", 0.38), ("grab", vo_t("grab"), "snap", 0.3), ("grab", 0.3, "scrape", 0.2),
''', '''    # long version, bridge A: a sound on frame 0 (the long breath of the sea still out), จูน's heart as she makes up her mind, then she bolts
    ("brA", 0.0, "swell", 0.3), *beats("brA", 0.3, D["brA"] - 0.6, 0.7, 0.2), ("brA", D["brA"] - 0.4, "pant", 0.14), ("brA", D["brA"] - 0.3, "steps", 0.09),
    # her feet on the steps, her breath
    *[("open", 0.1 + i * 0.3, "steps", 0.09) for i in range(9)], ("open", 0.2, "pant", 0.14), *beats("open", 0.2, D["open"] - 0.2, 0.7, 0.2),
    # the old hand clamps her wrist 0.3 s in (no voice now): the sting, the grip, the sandal skids
    ("grab", 0.28, "sting", 0.38), ("grab", 0.3, "snap", 0.3), ("grab", 0.3, "scrape", 0.2),
''')
sub(p, CHOICE_END[2], "    # long version: no choice and no end card; the film goes on into EP.3's bridge\n")
sub(p, 'dip(T("wave3", 0), T("choice", 0), 0.4)\n', 'dip(T("wave3", 0), TOTAL + 1, 0.4)   # long version: the dip runs to the end of the part\n')
sub(p, 'end = int(T("choice", -0.12) * SR)\nmus[end:] = 0  # hard cut to black and silence\n',
    'a = int(T("close", vo_end("close", 1) - 0.22) * SR)   # long version: the stream dies on "ดับ" and the music goes with it\n'
    'b = a + int(0.5 * SR)\nmus[a:b] *= np.linspace(1, 0, b - a)\nmus[b:] = 0\n')
sub(p, CUT_OLD, "")

# ================= EP.3 =================
p = os.path.join(W, "ep3", "mix.py")
sub(p, '''    # the hook: a sound on frame 0, the tower's siren, people running for the cars, an engine
    ("hook", 0.0, "swell", 0.3), ("hook", 0.05, "siren", 0.16), *[("hook", 0.3 + i * 0.28, "steps", 0.08) for i in range(7)], ("hook", 1.4, "engine", 0.12),
''', '''    # long version, bridge B: back before the second wave — a sound on frame 0, the tower blaring, the hazards on the jammed road
    ("brB", 0.0, "swell", 0.3), ("brB", 0.05, "siren", 0.2), ("brB", 1.8, "siren", 0.16), *[("brB", 0.6 + i * 0.42, "blinker", 0.06) for i in range(6)],
    # ยาย at her shop with the old photo: the siren further off, a horn down the road
    ("yai0", 0.05, "siren", 0.1), ("yai0", 0.4, "swell", 0.16), ("yai0", 1.6, "beep", 0.1),
    # people running for the cars, an engine
    ("hook", 0.05, "siren", 0.12), *[("hook", 0.3 + i * 0.28, "steps", 0.08) for i in range(7)], ("hook", 1.4, "engine", 0.12),
''')
print("mix patched")
