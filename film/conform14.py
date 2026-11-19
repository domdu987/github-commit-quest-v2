"""Film 14 conform: frames (from conform_full.py) + captions + SFX + narration (+ music) -> mp4.
usage: FRAMES=<dir with f_%04d.png> python3 conform14.py <out_basename>
env: MUSICF (wav/mp3 path, optional; no music if unset), MUSIC_DB (-31), VOICE_DB (-14.4), NARR_DB (-17.2)
Times below are FILM seconds (narration is placed at +0.10 s). N = 2106, last frame g2105 is black (hard cut after g2104)."""
import sys, json, os, subprocess
import numpy as np
from PIL import Image
P = os.path.dirname(os.path.abspath(__file__)); out = sys.argv[1]; FPS = 30; OFF = 0.10; N = 2106; T = N / FPS
tmp = os.environ["FRAMES"]
for g in range(N):  # any missing frame (only g2105 by design) -> black
    f = f"{tmp}/f_{g:04d}.png"
    if not os.path.exists(f):
        if os.path.lexists(f): os.remove(f)
        Image.new("RGB", (720, 1280), (0, 0, 0)).save(f)
caps = json.load(open(P + "/film14/script/captions.json"))
ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 720", "PlayResY: 1280", "WrapStyle: 2", "", "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: Pop,Kanit Black,88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,5,0,5,30,30,0,1", "", "[Events]",
       "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
ts = lambda t: f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
TEND = 2105 / FPS  # captions end with the picture (hard cut to black)
for c in caps:
    a = max(0.0, c["t"] + OFF); b = min(c["end"] + OFF, TEND)
    if a >= TEND: continue
    ass.append(f"Dialogue: 0,{ts(a)},{ts(b)},Pop,,0,0,0,,{{\\pos(360,900)}}{c['text']}")
open(out + ".ass", "w").write("\n".join(ass))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-i", f"{tmp}/f_%04d.png", "-frames:v", str(N), "-vf", f"ass={out}.ass:fontsdir={P}/fonts",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", "-movflags", "+faststart", out + "_silent.mp4"], check=True)
B = P + "/film14/audio/sfx/"
sfx = []
def add(f, t, db, ln, fo=0.08):
    if t < TEND: sfx.append({"file": B + f + ".mp3", "at": t, "peak_db": db, "len": min(ln, TEND - t), "align": "onset", "fade_out": fo})
CUES = [
 # hook (DAY): farmer hangs the first hive, village laughs
 ("hammer_tie", 0.5, -20, 1.2), ("crowd_laugh", 1.1, -19, 2.4), ("crowd_laugh", 2.5, -20, 2.4), ("whoosh", 4.1, -28, 0.5),
 # pivot: Kenya dusk, herd eats maize at night, pots and torches
 ("whoosh", 6.03, -28, 0.5), ("elephant_step", 8.5, -18, 2.4), ("maize_crunch", 9.3, -18, 2.4),
 ("pots_torches", 10.85, -18, 2.9), ("maize_crunch", 12.4, -20, 1.2),
 # boss: uncle laughs, then quotes (keep quiet under the quote)
 ("big_laugh", 13.7, -16, 1.8),
 # nickname: village laughs along, kid bangs the pot (shot 10 g664-758)
 ("crowd_laugh", 22.2, -18, 2.4), ("pot_bang", 22.5, -20, 1.1), ("crowd_laugh", 23.6, -19, 1.7), ("pot_bang", 23.8, -21, 1.1),
 # count: day 1 / day 2 / day 3 wire / the ring
 ("hammer_tie", 25.7, -20, 1.2), ("whoosh", 27.36, -28, 0.5), ("ding", 27.6, -26, 0.9), ("wire_creak", 29.1, -24, 1.4), ("hammer_tie", 30.0, -22, 1.0),
 ("ding", 31.2, -26, 0.9),
 # false payoff: herd walks at night, matriarch at the fence, bees asleep, uncle shouts
 ("elephant_step", 33.5, -18, 2.4), ("elephant_step", 35.5, -17, 2.4), ("bees_sleep", 37.6, -24, 1.4),
 # attack: chest on the wire
 ("elephant_step", 40.9, -18, 1.5), ("wire_creak", 41.3, -17, 1.5), ("wire_creak", 43.6, -20, 1.5),
 # reveal: hives knock (s21 contact frames g1390/1410/1430), hive jolts, bees burst, swarm on eyes and trunk
 ("wood_knock", 1390 / 30, -13, 0.45), ("wood_knock", 1410 / 30, -13, 0.45), ("wood_knock", 1430 / 30, -12, 0.45), ("bee_zip", 48.1, -22, 0.5),
 ("wood_knock", 1458 / 30, -11, 0.45), ("bees_burst", 48.7, -13, 3.0), ("bees_swarm", 50.1, -15, 3.0), ("bees_swarm", 52.0, -16, 1.4),
 # aha: bees up the trunk, trumpet (g1653), herd flees, dawn
 ("bees_swarm", 53.3, -17, 1.8), ("elephant_trumpet", 1653 / 30, -10, 1.9), ("herd_run", 55.95, -14, 3.4), ("rooster", 59.1, -20, 1.9),
 # ending: uncle's field raided at night, morning ask, sting, swelling nose
 ("elephant_step", 61.4, -18, 1.2), ("maize_crunch", 61.9, -18, 1.4), ("stalks_fall", 62.6, -16, 1.9),
 ("whoosh", 63.79, -28, 0.5), ("hammer_tie", 65.6, -22, 0.8), ("bee_zip", 65.95, -18, 0.5), ("sting_pop", 66.33, -12, 0.6),
 ("nose_swell", 68.17, -14, 1.35),
]
for c in CUES: add(*c)
BEDS = [("savanna_day", 0, 6.03), ("village_dusk", 6.03, 8.40), ("night_crickets", 8.40, 13.64), ("savanna_day", 13.64, 22.13),
        ("village_dusk", 22.13, 25.30), ("savanna_day", 25.30, 28.80), ("village_dusk", 28.80, 33.38), ("night_crickets", 33.38, 58.81),
        ("savanna_day", 58.81, 61.34), ("night_crickets", 61.34, 63.79), ("savanna_day", 63.79, TEND)]
for n, a_, b_ in BEDS:
    t = a_
    while t < b_ - 0.3:
        sfx.append({"file": B + n + ".mp3", "at": t, "rms_db": -36, "len": min(5.5, b_ - t), "align": "start", "fade_in": 0.15, "fade_out": 0.3}); t += 5.4
# duck: SFX overlapping narration
_v = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", P + "/film14/audio/narration.wav", "-ac", "1", "-ar", "8000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
_env = np.sqrt(np.convolve(_v ** 2, np.ones(800) / 800, "same"))[::80]
def _talk(a, ln):
    seg = _env[max(0, int((a - OFF) * 100)):max(0, int((a - OFF + ln) * 100))]
    return seg.size > 0 and (seg > 0.02).mean() > 0.3
for x in sfx:
    if "peak_db" in x and _talk(x["at"], x["len"]): x["peak_db"] -= 6 if x["len"] < 3 else 3
spec = {"duration": T, "out_wav": out + ".wav", "video_in": out + "_silent.mp4", "video_out": out + ".mp4",
        "voice": {"file": P + "/film14/audio/narration.wav", "at": OFF, "gain": 10 ** ((float(os.environ.get("VOICE_DB", "-14.4")) - float(os.environ.get("NARR_DB", "-17.2"))) / 20)},
        "sfx": sfx}
if os.environ.get("MUSICF"):
    spec["music"] = {"file": os.environ["MUSICF"], "at": 0, "rms_db": float(os.environ.get("MUSIC_DB", "-31")), "fade_in": 0.3, "fade_out": 0.4}
json.dump(spec, open(out + "_mix.json", "w"), indent=1)
subprocess.run([sys.executable, P + "/audio/mixer.py", out + "_mix.json"], check=True)
