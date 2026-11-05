"""มือพราย long version (YouTube 16:9): every edit to the three fresh working copies (phrailong/ep1..3, from tools/fresh.sh).
Exact, asserted replacements; run once on fresh copies.

The joins:
  - EP.1 loses its choice ("ปลุกยาย / ตามไปเอง") and its end card; "call" is held a beat longer.
  - Bridge A: EP.2 opens on its own recap shot (EP.1's last image: โต้ง at the foot of the steps, the krathong waiting), now with the
    narrator's b01 "แพรวไม่ปลุกยาย… เธอไปคนเดียว" (EP.1's choice, answered as the possessed pick did), then straight into "follow"
    ("ตีสอง แพรวตามโต้งลงไปที่ท่าน้ำ"). EP.2's hook (the flash-forward with the "EP.2 อย่าอุ้มพาดบ่า" title) is cut: its rule comes back
    in the body ("no", "dont").
  - Bridge B: EP.2's last shot "swim" (แพรว's head above the water, the pale face rising, "ว่ายมาสิ… แพรว…") gets the narrator's b02
    "กลางแม่น้ำ… ฝั่งอยู่ไกล"; EP.2's choice and end card are cut. EP.3 starts at "swim" ("แพรวเป็นนักกีฬาว่ายน้ำ…"): its recap would
    repeat EP.2's last frame one-for-one, and its hook (title "EP.3 ให้นอนหงาย") is cut; the rule comes back in the body.
  - EP.3 ends as delivered: the cut to black and silence, then the "ตอนจบ" pier sign.
  - Every part ends on a multiple of 0.25 s (15 frames at 60 fps, 12000 samples at 48 kHz) so picture and sound join exactly.
The mixes: no cues for the cut shots; the music fades out over each part's last second (suno1 restarts at 0 s in the next part, and
its first second is near-silent); the effects bus low-passed at ~4.5 kHz (the delivered mixes fail hisscheck: flatness 0.49 / 0.43 /
0.50); one static gain to -14 LUFS through a soft knee instead of single-pass loudnorm, so vo_stem.wav and music_stem.wav are exactly
what is summed into mix.wav (musiccheck); MIXOUT = output dir; each episode runs its own synth.py."""
import json
import os
import shutil

W = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def sub(path, old, new, count=1):
    s = open(path).read()
    n = s.count(old)
    assert n == count, (path, old[:80], n)
    open(path, "w").write(s.replace(old, new))


def cut(path, start, end, new=""):
    """Replace the text from marker `start` (included) up to marker `end` (kept); both must occur exactly once."""
    s = open(path).read()
    assert s.count(start) == 1 and s.count(end) == 1, (path, start[:60], s.count(start), end[:60], s.count(end))
    a, b = s.index(start), s.index(end)
    assert a < b, (path, start[:60])
    open(path, "w").write(s[:a] + new + s[b:])


# ================= bridge lines: b01 → EP.2, b02 → EP.2 =================
B = {ln["id"]: ln for ln in json.load(open(os.path.join(W, "bridge", "lines.json")))}
BD = json.load(open(os.path.join(W, "bridge", "vo", "durations.json")))
d = os.path.join(W, "ep2")
L = [ln for ln in json.load(open(os.path.join(d, "lines.json"))) if ln["id"] not in B] + [B["b01"], B["b02"]]
json.dump(L, open(os.path.join(d, "lines.json"), "w"), ensure_ascii=False, indent=1)
du = json.load(open(os.path.join(d, "vo", "durations.json")))
for i in ("b01", "b02"):
    du[i] = BD[i]
    for f in os.listdir(os.path.join(W, "bridge", "vo")):
        if f.startswith(i + "."):
            shutil.copy(os.path.join(W, "bridge", "vo", f), os.path.join(d, "vo", f))
json.dump(du, open(os.path.join(d, "vo", "durations.json"), "w"), indent=1)

# ================= timing =================
p = os.path.join(W, "ep1", "timing.py")
sub(p, '    ("call", ["r02"], 0.3, 0.5, 4.4),                 # โต้ง walking down the steps to the water, a krathong waiting\n'
       '    ("choice", [], 0.0, 0.0, 3.4),                    # wake ยาย / follow him yourself\n'
       '    ("next", [], 0.0, 0.0, 2.6),                      # end card: the pier sign\n',
    '    ("call", ["r02"], 0.3, 0.9, 4.4),                 # โต้ง walking down the steps to the water, a krathong waiting (long: held a beat)\n'
    '    # long version (YouTube 16:9): the choice and the end card are cut; the film goes on into EP.2\'s recap with bridge A\n')
p = os.path.join(W, "ep2", "timing.py")
sub(p, '    ("recap", [], 0.0, 0.0, 2.0),                     # EP.1\'s last image: โต้ง at the foot of the river steps, the krathong waiting\n'
       '    ("hook", ["n01", ("n02", 0.15)], 0.3, 0.6, 6.0),  # top-down: โต้ง on the planks, not breathing; ยาย\'s arms come to lift him — stamped out · EP.2\n',
    '    # long version (YouTube 16:9), bridge A: the recap shot carries the narrator\'s b01; the hook (flash-forward + EP.2 title) is cut\n'
    '    ("recap", ["b01"], 0.3, 0.45, 2.6),               # EP.1\'s last image: โต้ง at the foot of the river steps, the krathong waiting\n')
sub(p, '    ("swim", ["r02"], 0.3, 0.4, 3.6),                 # in the water: แพรว\'s head above the surface, a pale face rising behind\n'
       '    ("choice", [], 0.0, 0.0, 3.4),                    # swim for it / float on your back\n'
       '    ("next", [], 0.0, 0.0, 2.6),                      # end card: the pier sign\n',
    '    ("swim", ["r02", ("b02", 0.45)], 0.3, 0.6, 3.6),  # in the water: แพรว\'s head above the surface, a pale face rising behind; then bridge B\n'
    '    # long version: the choice and the end card are cut; EP.3 starts at its "swim"\n')
p = os.path.join(W, "ep3", "timing.py")
sub(p, '    ("recap", [], 0.0, 0.0, 2.0),                     # EP.2\'s last image: แพรว\'s head above the river, the pale face rising behind her\n'
       '    ("hook", ["n01", ("n02", 0.15)], 0.3, 0.6, 6.0),  # top-down: thrashing far out, the bank a line of lights — stamped out · EP.3\n',
    '    # long version (YouTube 16:9): the recap (EP.2\'s last frame again) and the hook (EP.3 title) are cut; the film comes in on "swim"\n')
for ep in (1, 2, 3):
    sub(os.path.join(W, f"ep{ep}", "timing.py"),
        '    json.dump({"total": round(t, 3), "shots": out}, open(os.path.join(HERE, "schedule.json"), "w"), ensure_ascii=False, indent=1)\n',
        '    # long version: hold the last shot so the part ends on a multiple of 0.25 s (15 frames at 60 fps, 12000 samples at 48 kHz)\n'
        '    end = -(-round(t, 3) // 0.25) * 0.25\n'
        '    out[-1]["dur"] = round(out[-1]["dur"] + end - t, 3)\n'
        '    t = end\n'
        '    json.dump({"total": round(t, 3), "shots": out}, open(os.path.join(HERE, "schedule.json"), "w"), ensure_ascii=False, indent=1)\n')

# ================= picture (body.part) =================
p = os.path.join(W, "ep1", "body.part")
cut(p, "      // ---------- 33. the choice: wake ยาย / follow him yourself ----------\n", "      shots.forEach((sh) => {",
    "      // long version (YouTube 16:9): the choice and the end card are cut\n\n")
p = os.path.join(W, "ep2", "body.part")
sub(p, '        fx(tl, id, t0) { Fx.heart(tl, t0, D("recap"), 0.38, 0.7); Fx.glitch(tl, `#${id}`, t0 + D("recap") - 0.35, 0.35, 22, 601); },\n',
    '        captions: caps("recap"),   // long version, bridge A: "แพรวไม่ปลุกยาย… เธอไปคนเดียว"\n'
    '        fx(tl, id, t0) { Fx.heart(tl, t0, D("recap"), 0.38, 0.7); Fx.glitch(tl, `#${id}`, t0 + D("recap") - 0.35, 0.35, 22, 601); },\n')
cut(p, "      // ---------- 1. top-down: โต้ง on the planks, not breathing", "      // ---------- 2. wide, from the water:",
    "      // long version: the hook (top-down flash-forward with the EP.2 title) is cut\n\n")
sub(p, '        captions: caps("swim", undefined, { quote: true }),\n',
    '        captions: [...caps("swim", [0], { quote: true }), ...caps("swim", [1])],   // the voice under the water, then the narrator\'s b02\n')
cut(p, '      add("choice", SWIM("pd27", {', "      shots.forEach((sh) => {", "      // long version (YouTube 16:9): the choice and the end card are cut\n\n")
p = os.path.join(W, "ep3", "body.part")
cut(p, "      // ---------- 0. EP.2's last image:", "      // ---------- 2. top-down close, tracking:",
    "      // long version (YouTube 16:9): the recap and the hook (EP.3 title) are cut\n\n")
# 16:9: the shots' own water overlays were sized to run past the 9:16 frame's right edge; widened to the new world edge (x 3500)
sub(os.path.join(W, "ep1", "body.part"), '<rect x="640" y="${G + 230}" width="1600" height="1200" fill="#1d2640" opacity=".55"/>',
    '<rect x="640" y="${G + 230}" width="2860" height="1200" fill="#1d2640" opacity=".55"/>')
sub(os.path.join(W, "ep2", "body.part"), '<rect x="640" y="${G + 330}" width="1600" height="900" fill="#2b3656" opacity=".5"/>',
    '<rect x="640" y="${G + 330}" width="2860" height="900" fill="#2b3656" opacity=".5"/>')
sub(os.path.join(W, "ep3", "body.part"), '<rect x="-900" y="1480" width="2900" height="1200" fill="#1d2640" opacity=".55"/>',
    '<rect x="-2400" y="1480" width="5900" height="1200" fill="#1d2640" opacity=".55"/>')

# ================= sound (mix.py) =================
TAIL_OLD = '''peak = np.max(np.abs(mix))
if peak > 0.98:
    mix = np.tanh(mix / peak * 1.2) * 0.95
out = os.path.join(HERE, "mix_raw.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", out],
               input=mix.astype(np.float32).tobytes(), check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", os.path.join(HERE, "mix.wav")], check=True)
print("mix written", TOTAL)
'''
TAIL_NEW = '''# ---- long version (YouTube 16:9): one static gain to -14 LUFS (measured through the limiter) instead of single-pass loudnorm, so
# vo_stem.wav and music_stem.wav are what is summed into mix.wav (musiccheck); a look-ahead limiter keeps peaks under -1 dBFS ----
OUT = os.environ.get("MIXOUT", HERE)
os.makedirs(OUT, exist_ok=True)
mstem = mus * duck


def wr(path, x, codec="pcm_s16le"):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", "-c:a", codec, path],
                   input=x.astype(np.float32).tobytes(), check=True)


def integrated(path):
    o = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\\s+(-?[0-9.]+) LUFS", o)[-1])


def knee(x):   # a smooth look-ahead limiter (-1.1 dBFS): a waveshaping knee here bent the voice peaks into noise-like HF (hisscheck 0.41)
    y = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af",
                                      "alimiter=limit=0.88:attack=5:release=80:level=false:latency=1", "-f", "f32le", "-"],
                                     input=x.astype(np.float32).tobytes(), capture_output=True, check=True).stdout, np.float32).copy()
    return np.pad(y, (0, max(0, len(x) - len(y))))[:len(x)]


raw, g = os.path.join(OUT, "mix_raw.wav"), 1.0
for _ in range(3):
    wr(raw, knee(mix * g), "pcm_f32le"); g *= 10 ** ((-14.0 - integrated(raw)) / 20)
os.remove(raw)
mix, vo_s, mstem = knee(mix * g), vo * g, mstem * g
wr(os.path.join(OUT, "mix.wav"), mix)
wr(os.path.join(OUT, "vo_stem.wav"), vo_s, "pcm_f32le")
wr(os.path.join(OUT, "music_stem.wav"), mstem, "pcm_f32le")
print("mix written", TOTAL, "s · gain", round(20 * np.log10(g), 2), "dB · integrated", integrated(os.path.join(OUT, "mix.wav")), "LUFS · peak",
      round(20 * np.log10(float(np.max(np.abs(mix)))), 2), "dBFS")
'''
LOWPASS_OLD = "sfx = level(sfx, -27)\n"
LOWPASS_NEW = ("sfx = np.frombuffer(subprocess.run([\"ffmpeg\", \"-v\", \"error\", \"-f\", \"f32le\", \"-ar\", str(SR), \"-ac\", \"1\", \"-i\", \"-\", \"-af\", os.environ.get(\"SFXAF\", \"lowpass=f=4500,lowpass=f=4500,highpass=f=40\"),\n"
               "                                    \"-f\", \"f32le\", \"-\"], input=sfx.astype(np.float32).tobytes(), capture_output=True, check=True).stdout, np.float32).copy()\n"
               "sfx = level(np.pad(sfx, (0, max(0, N - len(sfx))))[:N], -27)   # long version: the effects bus low-passed at ~4.5 kHz (A4: no hiss)\n")
FADE = ""   # long version: no fade or cut at a part's end; the theme runs on into the next part (MUSOFF, tools/mixall.sh)
MUSIC_OLD = '''mus = load(os.path.join(HERE, "..", "music", "suno1.mp3"))
while len(mus) < N:
'''
MUSIC_NEW = '''mus = load(os.path.join(HERE, "..", "music", "suno1.mp3"))
# long version: one fixed theme gain for every part (MUSLVL dB RMS for the undipped track), so the level never steps at a join; and the
# theme continues from where the previous part left it (MUSOFF s into suno1, set by tools/mixall.sh), so the film has one unbroken score
MUSG = 10 ** ((float(os.environ.get("MUSLVL", "-31.5")) - rms_db(mus)) / 20)
k = int(float(os.environ.get("MUSOFF", "0")) * SR) % len(mus)
mus = np.concatenate([mus[k:], mus[:k]])
while len(mus) < N:
'''
for ep in (1, 2, 3):
    p = os.path.join(W, f"ep{ep}", "mix.py")
    sub(p, "import json\nimport os\n", "import json\nimport os\nimport re\n")
    sub(p, TAIL_OLD, TAIL_NEW)
    sub(p, LOWPASS_OLD, LOWPASS_NEW)
    sub(p, 'subprocess.run(["python3", os.path.join(HERE, "..", "synth.py"),', 'subprocess.run(["python3", os.path.join(HERE, "synth.py"),')
    # the ทะเลลด recipe's horror dips are x0.4-0.55 and its theme sits at -30 dB RMS; this series dipped the theme to x0.2-0.35 under
    # dense narration, so between lines it all but vanished (musiccheck on the first long mix: -41 LUFS between lines, 64 % missing).
    # The long version floors every dip at the recipe's x0.55 (DIPFLOOR) and gives the theme one fixed gain (MUSLVL, see MUSIC_NEW)
    sub(p, "def dip(t0, t1, lvl, ramp=0.25):\n",
        "def dip(t0, t1, lvl, ramp=0.25):\n    lvl = max(lvl, float(os.environ.get(\"DIPFLOOR\", \"0.55\")))   # long version: never deeper than the ทะเลลด recipe's dips\n")
    sub(p, MUSIC_OLD, MUSIC_NEW)
    sub(p, "mus = level(mus, -30)\n", "mus = mus * MUSG   # long version: the fixed theme gain (no per-part RMS levelling)\n")
    # hisscheck reads the TTS fricatives as hiss (flatness 0.41-0.43 with no bed at all: pause floor -83 dBFS). A gentle de-ess on every
    # line (high shelf, VOXAF) and the พราย's whispered lines (r01, r02: the voice from under the water, the breathiest takes, flatness
    # 0.32-0.44 each) muffled like a voice under the water
    sub(p, '''        x = load(os.path.join(HERE, "vo", f"{v['id']}.wav"))\n''',
        '''        x = load(os.path.join(HERE, "vo", f"{v['id']}.wav"))\n'''
        '''        af = os.environ.get("VOXAF", "highshelf=f=7000:g=-5")   # long version: a gentle de-ess on every line
        if v["id"].startswith("r"):
            af += ",lowpass=f=5000,lowpass=f=5000"                 # the voice under the water, muffled
        x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", af,
                                          "-f", "f32le", "-"], input=x.astype(np.float32).tobytes(), capture_output=True, check=True).stdout, np.float32).copy()\n''')

CHOICE_NEXT = '''    *beats("choice", 0.0, D["choice"] - 0.3, 0.38, 1.0), *[("choice", 0.05 + k * 1.0, "tick", 1.0) for k in range(3)], ("choice", 1.0, "glitch", 0.6),
    ("choice", D["choice"] - 2.2, "riser", 1.0), ("choice", D["choice"] - 0.62, "sting", 1.0), ("choice", D["choice"] - 0.6, "glitch", 0.8), ("choice", D["choice"] - 0.6, "boom", 0.7),
    ("next", 0.3, "whoosh", 0.5), ("next", 0.45, "drip", 0.6), ("next", 0.8, "sting", 0.7), *beats("next", 0.9, D["next"] - 0.9, 0.7, 0.5),
'''
CUT_CHOICE = '''cut, card = int(T("choice", -0.2) * SR), int(T("next", 0.3) * SR)
mix[cut - 240:cut] *= np.linspace(1, 0, 240)
mix[cut:card] = 0  # a beat of black and silence after the cliffhanger, then only the end card's own sounds
'''
# ---- EP.1 ----
p = os.path.join(W, "ep1", "mix.py")
sub(p, CHOICE_NEXT, "    # long version: no choice and no end card\n")
sub(p, 'dip(T("choice", 0), T("choice", -0.3), 0.5)\n', "")
# the night dip runs on to the end of the part, so the theme crosses into EP.2's recap at the same level it starts there (x0.55)
sub(p, 'dip(T("night", 0), T("call", -0.05), 0.3)\n', 'dip(T("night", 0), TOTAL + 1, 0.3)   # long version: on to the join\n')
sub(p, 'end = int(T("choice", -0.2) * SR)\nmus[end:] = 0  # hard cut to black and silence\n', FADE)
sub(p, CUT_CHOICE, "")
# ---- EP.2 ----
p = os.path.join(W, "ep2", "mix.py")
sub(p, 'H2 = frag("hook", 1, 0)\n', "")
sub(p, '''    ("hook", 0.0, "swell", 0.4), ("hook", 0.3, "sting", 0.6), ("hook", 0.4, "drip", 0.5), ("hook", 1.2, "drip", 0.4), *beats("hook", 0.5, D["hook"] - 0.5, 0.5, 0.4),
    ("hook", H2 - 0.7, "whoosh", 0.5), ("hook", H2 + 0.18, "slam", 0.8), ("hook", H2 + 0.18, "glitch", 0.6),
''', "    # long version: the hook is cut\n")
sub(p, CHOICE_NEXT, "    # long version: no choice and no end card\n")
sub(p, 'dip(T("swim", 0), T("choice", -0.3), 0.4)\n', 'dip(T("swim", 0), TOTAL + 1, 0.4)   # long version: the dip runs to the end of the part\n')
sub(p, 'end = int(T("choice", -0.2) * SR)\nmus[end:] = 0  # hard cut to black and silence\n', FADE)
sub(p, CUT_CHOICE, "")
# ---- EP.3 ----
p = os.path.join(W, "ep3", "mix.py")
sub(p, 'H2 = frag("hook", 1, 0)\n', "")
sub(p, '''    *beats("recap", 0.0, D["recap"], 0.38, 0.8), ("recap", D["recap"] - 0.35, "glitch", 0.7),
    ("hook", 0.0, "swell", 0.4), ("hook", 0.3, "sting", 0.6), *strokes("hook", 0.2, D["hook"], 0.6), *beats("hook", 0.5, D["hook"] - 0.5, 0.5, 0.4),
    ("hook", H2 - 0.7, "whoosh", 0.5), ("hook", H2 + 0.18, "slam", 0.8), ("hook", H2 + 0.18, "glitch", 0.6),
''', '    # long version: the recap and the hook are cut; a swell on the first frame of "swim" (the cut in from EP.2)\n    ("swim", 0.0, "swell", 0.35),\n')
sub(p, 'dip(0.0, T("recap", -0.05), 0.3, 0.05)\n',
    'dip(0.0, 0.0, 0.55, 1.0)   # long version: EP.2 hands over at x0.55; the theme swells back to full over the first second of "swim"\n')
# the film's ending: the cut to black stays a hole of silence; then the theme comes back under the "ตอนจบ" card (held 4 s now) and fades
# out over its last 0.8 s (the recipe's finale "fade over the end card"; delivered, the card had only its own sounds)
sub(p, 'end = int(T("last", -0.15) * SR)\nmus[end:] = 0  # hard cut to black and silence\n',
    'end, card0 = int(T("last", -0.15) * SR), int(T("end", 0.3) * SR)\n'
    'mus[end:card0] = 0  # the cut to black: a hole of silence, as delivered\n'
    'f0 = N - int(0.8 * SR)\nmus[f0:] *= np.linspace(1, 0, N - f0)   # long version: the theme back under the end card, fading out at the very end\n')
sub(os.path.join(W, "ep3", "timing.py"), '    ("end", [], 0.0, 0.0, 2.8),                       # end card: the pier sign, ตอนจบ\n',
    '    ("end", [], 0.0, 0.0, 4.0),                       # end card: the pier sign, ตอนจบ (long version: held 4 s, the theme under it)\n')
print("long version patched")
