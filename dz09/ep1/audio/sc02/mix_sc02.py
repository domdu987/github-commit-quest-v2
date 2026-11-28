"""mix_sc02.py -- the sound of SCENE 02 (film 53.333 .. 127.333 s = scene frames 0..1776), sample 0 = scene frame 0.

    python3 mix_sc02.py            -> mix_sc02.wav (48 kHz stereo float), stems/*.wav, mix_sc02_report.json

Voice   ep1/audio/narr_ep1.wav (film clock), unprocessed, centre, +4 dB as the hook (mix_ohm_v3.py).
Music   the user's Suno tracks, placed so their own hits land on picture beats (measured, work/fine_hits.py):
        Rain_on_the_Concrete (tension bed, hits every 8 s at 2.03 + 8k s of the file)
          A  from the cut: its 10.03 hit on the ram (S027, film 56.862), its 18.03 hit under the support walk (S031)
          B  crossfaded in under s22 so its 34.03 hit lands on the tick and '30 วินาที' (S036, 73.795); it stops on
             'หยุดนิ่ง' (S041, the hand stops, the heart stops): S042-S047 are rain only, as the plan asks
        Brutal_Pursuit (chase): enters on the eye-open (S048) low and climbing, its 47.142 / 47.966 hits land on the hard cut
          of S050 (the launch) and on the junior landing on the cutter; the track's own break (64-66 s) falls under S061.
Effects synthesised by code (sfx_synth.py): rain on metal, beacon hum, heartbeat pulse, watch ticks on the real second
        hand (bite 43.795 + n), car alarm locked to the lamps' 10-frame cycle, impacts, footsteps, breaths, snarls, roof
        bangs, windscreen crack, claws, glass, horns, crowd, sub-bass swell.
        Recorded beds reused from the hook for continuity across the join: rain_heavy_road and sirens_city_far (looped
        with crossfades), and man_scream_bite (S025's scream continues the hook's, pitched; also far screams in S057 / S059 / S060).
Ducking as the hook (bed -9 dB, effects -10 dB under the voice), then a per-window guarantee: in every 0.4 s window
        where the voice speaks, the bed is pulled down until the voice is at least FLOOR_DB over it.
"""
import os, sys, json, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sfx_synth as X
PROJ = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EP1 = os.path.join(PROJ, "ep1")
SR = 48000
FPS = 24
CUT = json.load(open(os.path.join(EP1, "pipe", "cut", "sc02.json"), encoding="utf-8"))
F0 = CUT["film_f0"] / float(FPS)                 # 53.333: film time of sample 0
DUR = CUT["frames"] / float(FPS)                 # 74.000
N = int(round(DUR * SR))
FLOOR_DB = 14.0                                  # the guarantee aims 2 dB above the 12 dB rule
HOOK_SFX = os.path.join(PROJ, "audio", "ep1_hook", "sfx")
SUNO = os.path.join(PROJ, "audio", "suno")
db = lambda d: 10 ** (d / 20.0)
rms = lambda x: float(np.sqrt(np.mean(np.asarray(x) ** 2)) + 1e-12)


def load(f, ch=2):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ar", str(SR), "-ac", str(ch), "-f", "f64le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float64).reshape(-1, ch).copy()


def W(text, sid=None, end=False):
    c = [c for c in CUT["captions"] if c["text"] == text and (sid is None or c["id"] == sid)][0]
    return F0 + (c["t1"] if end else c["t0"])


def shot(sid):
    s = [s for s in CUT["shots"] if s["id"] == sid][0]
    return F0 + s["f0"] / float(FPS), F0 + s["f1"] / float(FPS)


def I(t):
    return int(round((t - F0) * SR))


def put(buf, x, t, gain_db=0.0, pan=None, fin=0.0, fout=0.0):
    x = np.asarray(x, np.float64)
    if x.ndim == 1: x = X.st(x, 0.0 if pan is None else pan)
    elif pan is not None: x = X.st(x.mean(1), pan)
    x = x * db(gain_db)
    if fin: k = min(len(x), int(fin * SR)); x[:k] *= np.linspace(0, 1, k)[:, None]
    if fout: k = min(len(x), int(fout * SR)); x[-k:] *= np.linspace(1, 0, k)[:, None]
    i = I(t)
    if i < 0: x = x[-i:]; i = 0
    j = min(N, i + len(x))
    if j > i: buf[i:j] += x[:j - i]


def loop_bed(f, t0, t1, xf=0.5):
    """a recorded bed looped with crossfades from film t0 to t1."""
    x = load(f); n = I(t1) - I(t0); k = int(xf * SR); out = np.zeros((n + len(x), 2)); i = 0
    ramp_in = np.linspace(0, 1, k)[:, None]; ramp_out = 1 - ramp_in
    while i < n:
        y = x.copy()
        if i > 0: y[:k] *= ramp_in
        y[-k:] *= ramp_out
        out[i:i + len(y)] += y; i += len(x) - k
    return out[:n]


def music_seg(f, t_film, t_src, dur, fin=0.05, fout=0.05):
    x = load(os.path.join(SUNO, f)); a = int(round(t_src * SR)); n = min(int(dur * SR), len(x) - a)
    y = x[a:a + n].copy()
    k = int(fin * SR); y[:k] *= np.linspace(0, 1, k)[:, None]
    k = int(fout * SR); y[-k:] *= np.linspace(1, 0, k)[:, None]
    out = np.zeros((N, 2)); i = I(t_film); j = min(N, i + n); out[i:j] += y[:j - i]
    return out


def curve(pts):
    """gain curve over the scene in dB from (film t, dB) points, linear between them."""
    t = F0 + np.arange(N) / SR
    return db(np.interp(t, [p[0] for p in pts], [p[1] for p in pts]))


def main():
    os.makedirs(os.path.join(HERE, "stems"), exist_ok=True)
    T = {}                                                      # every cue used, for the report
    # ================================================================== voice
    v = load(os.path.join(EP1, "audio", "narr_ep1.wav"), 1)[:, 0]
    a = int(round(F0 * SR)); v = v[a:a + N]; v = np.concatenate([v, np.zeros(N - len(v))])
    voice = X.st(v) * db(4.0)
    # ================================================================== beds
    amb = np.zeros((N, 2)); fx = np.zeros((N, 2)); mus = np.zeros((N, 2))
    rain = loop_bed(os.path.join(HOOK_SFX, "rain_heavy_road.wav"), F0, F0 + DUR)
    sir = loop_bed(os.path.join(HOOK_SFX, "sirens_city_far.wav"), F0, F0 + DUR, 1.0)
    amb += rain + 0.35 * sir
    # rain on metal: always a little; up close in S032 (rain on the truck), S033-S037 under the truck's side
    rm = X.st(X.rain_metal(DUR, 70, seed=21), 0.2, 0.6)
    rmc = curve([(F0, -8), (shot("S032")[0] - 0.2, -8), (shot("S032")[0], 0), (shot("S037")[1], -2), (shot("S040")[0], -10), (F0 + DUR, -10)])
    amb += 0.25 * rm * rmc[:, None]
    # beacons: the light bar's hum, very low, louder near the truck
    bh = X.st(X.beacon_hum(DUR, F0), 0.0, 0.5)
    amb += 0.05 * bh
    amb *= db(-36.0) / rms(amb[: int(30 * SR)])                 # the hook's loud-rain level (-36 dB RMS before ducking)
    # ---- the rain is wide in S040 and gone for 6 frames on the eye-open
    t_open = F0 + 48.75                                         # S048: on_twos(W('ก็ลืมตา') + 0.20) on the stage clock = scene 48.750
    T["eye_open"] = t_open
    ambc = curve([(F0, 0), (shot("S040")[0], 0), (shot("S040")[0] + 0.3, 2), (shot("S040")[1], 2), (shot("S041")[0], 0), (shot("S046")[0], 0),
                  (shot("S046")[0] + 0.2, 1.5), (shot("S047")[1], 1.5), (shot("S048")[0], 0), (F0 + DUR, 0)])
    amb *= ambc[:, None]
    # ================================================================== music
    # Rain_on_the_Concrete A: hit 10.03 on the ram (film 56.862)
    t_ram = W("กระแทกมันกระเด็น") + 3 / 24.0; T["ram"] = t_ram
    offA = 10.03 - t_ram
    t_xf = W("น้องพยักหน้า") - 0.2                               # crossfade A -> B under s22 (narration, ducked)
    mus += music_seg("Rain_on_the_Concrete.mp3", F0, F0 + offA, t_xf + 1.5 - F0, fin=0.02, fout=1.5)
    # B: hit 34.03 on the 30-second tick (film 43.795 + 30 = 73.795), stops on 'หยุดนิ่ง'
    t30 = 43.795 + 30.0; T["tick30"] = t30
    offB = 34.032 - t30
    t_stop = W("หยุดนิ่ง") + 0.10; T["heart_stop"] = t_stop
    mus += music_seg("Rain_on_the_Concrete.mp3", t_xf, t_xf + offB, t_stop - t_xf, fin=1.5, fout=0.45)
    T["bed_A_src_at_film_0"] = round(F0 + offA, 3); T["bed_B_src"] = round(t_xf + offB, 3)
    # Brutal_Pursuit: 47.142 on the hard cut of S050, 47.966 on the landing; in low from the eye-open
    t50 = shot("S050")[0]; T["S050_cut"] = t50
    offC = 47.142 - t50
    chase = music_seg("Brutal_Pursuit.mp3", t_open, t_open + offC, F0 + DUR - t_open, fin=0.30, fout=1.2)
    t59 = shot("S059")[0]; t61 = shot("S061")[0]
    cc = curve([(F0, -60), (t_open, -60), (t_open + 0.3, -13), (t50 - 0.25, -6), (t50 - 0.02, -6), (t50, 0), (t59 - 0.1, 0), (t59, 1.5), (shot("S060")[1], 1.5),
                (t61 + 0.4, -2.5), (F0 + DUR, -2.5)])
    mus += chase * cc[:, None]
    T["chase_src_at_eye_open"] = round(t_open + offC, 3)
    mus *= db(-27.5) / rms(mus[I(F0 + 2): I(F0 + 30)])            # the hook's bed level for the tension track
    # ================================================================== effects
    # S025: the junior screams on (the hook's bite scream continued, pitched up), the driver's teeth growl under it
    scr = load(os.path.join(HOOK_SFX, "man_scream_bite.wav"))
    def pitch(x, semi):
        r = 2 ** (semi / 12.0)
        return X.ff(x, "asetrate=%d,aresample=%d" % (int(SR * r), SR))
    put(fx, pitch(scr, 1.0)[int(0.18 * SR):], F0 + 0.02, -5.0, pan=0.1, fout=0.3)
    put(fx, pitch(scr, -0.7)[int(0.35 * SR):], F0 + 1.45, -10.0, pan=0.1, fout=0.4)
    put(fx, X.growl(t_ram - F0 - 0.05, 78, seed=1, hard=0.7), F0, -12.0, pan=0.15)
    # heartbeat pulse: 96 bpm, faster from 'ลมหายใจน้อง' (S037) to 128 by S038, weaker through S041, stops before 'หยุดนิ่ง'
    hb_t = []
    t = F0 + 0.35
    t_fast0 = W("ลมหายใจน้อง"); t_fast1 = shot("S038")[0]; t_weak = shot("S041")[0]
    while t < t_stop - 0.35:
        bpm = np.interp(t, [F0, t_fast0, t_fast1, t_weak, t_stop], [96, 100, 128, 124, 84])
        g = np.interp(t, [F0, t_weak, t_stop], [0.0, 0.0, -9.0])
        hb_t.append((round(t, 3), round(float(bpm), 1)))
        put(fx, X.heartbeat(seed=len(hb_t)), t, -4.0 + g)
        t += 60.0 / bpm
    T["heartbeats"] = len(hb_t); T["last_heartbeat"] = hb_t[-1]
    # the watch: one dry tick per second of the real count, in the four inserts only
    ticks = []
    for sid in ("S026", "S036", "S044", "S047"):
        a_, b_ = shot(sid)
        k = int(np.ceil(a_ - 43.795 - 0.06))
        while 43.795 + k < b_ + 0.3:
            tk = 43.795 + k
            if tk >= a_ - 0.06:
                put(fx, X.tick(seed=k), tk, -1.0, pan=0.05); ticks.append(round(tk, 3))
            k += 1
    T["ticks"] = ticks
    # S027: the ram, the cloth, the driver flying off (a whoosh)
    put(fx, X.thud_ram(), t_ram, -7.0, pan=0.0)                # under the word: the voice rule wins
    put(fx, X.growl(0.35, 95, seed=3, hard=1.0), t_ram + 0.02, -11.0, pan=0.3)
    put(fx, X.burst(0.5, 300, 3000, a=0.12, d=0.25, seed=5) , t_ram + 0.05, -14.0, pan=0.5)
    # S028: the driver slams the taxi's tail, the car rocks; the alarm starts a quarter second before it is named
    t_slam = shot("S028")[0] + 6 / 24.0; T["taxi_slam"] = t_slam
    put(fx, X.body_panel(seed=2, big=1.0), t_slam, 0.0, pan=-0.2)
    put(fx, X.car_rock(), t_slam + 0.05, -12.0, pan=-0.2)
    t_alarm = W("สัญญาณกันขโมย") - 0.25; T["alarm_on"] = t_alarm
    al = X.st(X.car_alarm(F0 + DUR - t_alarm, t_alarm), -0.45, 0.3)
    alc = curve([(t_alarm, -5), (shot("S030")[1], -5), (shot("S031")[0], -9), (shot("S031")[1], -13), (shot("S032")[0], -16), (shot("S040")[0], -16),
                 (shot("S040")[0] + 0.5, -13), (shot("S040")[1], -14), (shot("S041")[0], -24), (shot("S049")[1], -24), (shot("S050")[0], -17), (shot("S058")[1], -17),
                 (shot("S059")[0], -12), (shot("S060")[0] - 0.05, -12), (shot("S060")[0], -3), (shot("S060")[1], -3), (shot("S061")[0], -15), (F0 + DUR, -15)])
    alarm = np.zeros((N, 2)); put(alarm, al, t_alarm, -6.0)
    alarm_far = X.far(alarm, 0.7)                               # the walk away: duller
    wfar = np.clip((np.log10(np.maximum(alc, 1e-6)) * 20 + 6) / -10, 0, 1)   # 0 near .. 1 far
    fx += (alarm * (1 - wfar)[:, None] + alarm_far * wfar[:, None]) * alc[:, None]
    # S030: the snarl on the light, the lunge, hands slapping the bonnet
    t_lunge = W("หันไปหาเสียง") + 6 / 24.0; T["S030_lunge"] = t_lunge
    put(fx, X.growl(1.2, 88, seed=4, hard=1.0, rise=0.15), W("มันทิ้งเหยื่อ") + 0.1, -10.0, pan=-0.2, fout=0.2)
    put(fx, X.hand_slap(4), t_lunge + 0.05, -8.0, pan=-0.35); put(fx, X.hand_slap(5), t_lunge + 0.27, -10.0, pan=-0.4)
    # S031: the support walk: Kong's boots and the junior's dragging foot
    a_, b_ = shot("S031"); t = a_ + 0.12; k = 0
    while t < b_ - 0.1:
        put(fx, X.footstep(seed=40 + k), t, -9.0, pan=-0.1)
        if k % 2 == 1: put(fx, X.drag(0.34, seed=60 + k), t + 0.06, -13.0, pan=0.1)
        t += 0.47; k += 1
    # S033-S035: breaths, the pad pressed, the wet cloth
    a_, b_ = shot("S033"); put(fx, X.breath(0.45, "in", 1, f=1100), a_ + 0.05, -16.0); put(fx, X.breath(0.5, "out", 2, f=1000), a_ + 0.5, -16.0)
    a_, b_ = shot("S034"); put(fx, X.cloth_press(b_ - a_ + 0.3, 3), a_ + 0.05, -12.0); put(fx, X.breath(0.4, "out", 4), a_ + 0.6, -17.0)
    a_, b_ = shot("S035"); put(fx, X.cloth_press(b_ - a_, 5), a_, -10.0)
    # S037: short breaths, 3 Hz, 4.2 Hz from 'ถี่ขึ้น', the jacket shivering
    a_, b_ = shot("S037"); t = a_ + 0.05; k = 0; tq = W("ถี่ขึ้น")
    while t < b_:
        hz = 3.0 if t < tq else 4.2
        put(fx, X.breath(0.5 / hz, "pant", 70 + k, f=1300), t, -15.0); t += 1.0 / hz; k += 1
    put(fx, X.shiver_cloth(b_ - a_, 6), a_, -22.0)
    # S041: his last breaths, then nothing
    a_, b_ = shot("S041")
    for k, (dt, g) in enumerate(((0.10, -18), (0.62, -20), (1.15, -23))):
        if a_ + dt < t_stop - 0.2: put(fx, X.breath(0.32, "out", 90 + k, f=1000), a_ + dt, g)
    # S045: Kong shakes him: cloth and body at 3.2 pulls a second from 'เฮ้ย!'
    t = W("เฮ้ย!"); b_ = shot("S045")[1]; k = 0
    while t < b_:
        put(fx, X.burst(0.18, 300, 2500, a=0.01, d=0.06, seed=100 + k), t, -14.0 - 1.5 * k / 3.0); t += 1 / 3.2; k += 1
    # S048: sub-bass swell to the eye-open, the open, the rain gone for 6 frames
    a_ = shot("S048")[0]
    put(fx, X.sub_swell(t_open - a_), a_, -3.0)
    drop = np.ones(N); i0, i1 = I(t_open), I(t_open + 6 / 24.0)
    k = int(0.01 * SR); drop[i0:i1] = 0.0; drop[i1:i1 + k] = np.linspace(0, 1, k)
    # S049: the infected inhale; the growl comes up with the fangs
    put(fx, X.inhale_infected(1.1), shot("S049")[0] + 0.30, -8.0)
    put(fx, X.growl(1.6, 74, seed=12, hard=0.6, rise=0.2), W("ไม่ใช่ตาคนแล้ว") + 0.05, -12.0, fout=0.4)
    # S050: snarl and launch, Kong's planted step back, the landing on the cutter
    put(fx, X.growl(1.1, 96, seed=13, hard=1.2, rise=0.1), t50 + 0.12, -3.0, pan=0.25, fout=0.15)
    put(fx, X.burst(0.35, 400, 3500, a=0.08, d=0.12, seed=14), t50 + 0.20, -12.0, pan=0.2)
    put(fx, X.footstep(seed=15, heavy=1.2), t50 + 0.48, -7.0, pan=-0.3)
    t_land = t50 + (47.966 - 47.142); T["S050_land"] = t_land
    put(fx, X.clank(16), t_land, -2.0, pan=-0.1); put(fx, X.body_panel(seed=17, big=0.5), t_land + 0.01, -10.0, pan=-0.1)
    # S051: teeth on the steel
    a_, b_ = shot("S051")
    put(fx, X.clank(18), a_ + 0.05, -6.0); put(fx, X.scrape(b_ - a_ - 0.2, 19), a_ + 0.15, -8.0)
    put(fx, X.growl(b_ - a_, 90, seed=20, hard=0.9), a_, -9.0, fout=0.2)
    # S052: the shove, the body on the truck's panel, Kong's two steps
    a_, b_ = shot("S052")
    put(fx, X.breath(0.25, "pant", 21, f=900), a_ + 0.18, -8.0)
    put(fx, X.body_panel(seed=22, big=1.0), a_ + 0.45, -5.0, pan=0.35)
    put(fx, X.footstep(seed=23), a_ + 0.70, -9.0, pan=-0.3); put(fx, X.footstep(seed=24), a_ + 1.05, -10.0, pan=-0.35)
    # S053: Kong backs round the corner: two planted steps, his breath
    a_, b_ = shot("S053")
    put(fx, X.footstep(seed=25, heavy=0.8), a_ + 0.25, -11.0); put(fx, X.footstep(seed=26, heavy=0.8), a_ + 0.70, -12.0)
    for k in range(3): put(fx, X.breath(0.45, "out" if k % 2 else "in", 27 + k, f=900), a_ + 0.1 + 0.5 * k, -13.0)
    # S054: short searching breaths
    a_, b_ = shot("S054")
    for k, dt in enumerate((0.15, 0.62, 1.10)): put(fx, X.sniff(30 + k), a_ + dt, -11.0, pan=0.3)
    # S055-S057: the roof chase: hollow bangs, the windscreen, claws, a far scream
    a_, b_ = shot("S055")
    put(fx, X.roof_bang(31), a_ + 0.10, -4.0, pan=-0.5)
    t = a_ + 0.42; k = 0
    while t < b_ - 0.25:
        put(fx, X.roof_bang(32 + k), t, -9.0 + (3.0 if k == 5 else 0.0), pan=-0.5 + 0.9 * (t - a_) / (b_ - a_)); t += 0.27; k += 1
    put(fx, X.growl(0.4, 92, seed=45, hard=0.8), a_ + 0.42, -9.0, pan=0.0)
    a_, b_ = shot("S056")
    put(fx, X.windscreen_crack(46), a_ + 0.22, -3.0, pan=0.2)
    for k, dt in enumerate((0.50, 0.75)): put(fx, X.roof_bang(47 + k), a_ + dt, -8.0, pan=0.4)
    a_, b_ = shot("S057")
    put(fx, X.roof_bang(49), a_ + 0.45, -3.0, pan=-0.1); put(fx, X.claws_metal(1.0, 50), a_ + 0.50, -6.0, pan=-0.05)
    put(fx, X.far(pitch(scr, 3.0), 0.8), a_ + 0.9, -12.0, pan=0.6)
    # S058: Kong's one step out of the nook
    put(fx, X.footstep(seed=51, heavy=0.8), shot("S058")[0] + 0.2, -12.0)
    # S059: the expressway: crowd left and right, screams, horns
    a_, b_ = shot("S059")
    put(fx, X.st(X.crowd_roar(b_ - a_ + 2.5, 52), -0.6, 0.8), a_, -6.0, fin=0.08, fout=1.5)
    put(fx, X.st(X.crowd_roar(b_ - a_ + 2.5, 62), 0.6, 0.8), a_, -6.0, fin=0.08, fout=1.5)
    for k, (dt, semi, pn, g) in enumerate(((0.05, 2.0, -0.7, -8), (0.45, 4.0, 0.6, -10), (0.9, -1.0, -0.4, -11), (1.5, 5.0, 0.75, -12), (2.0, 1.0, -0.8, -13))):
        put(fx, X.far(pitch(scr, semi), 0.6), a_ + dt, g, pan=pn)
    for k, (dt, f, pn) in enumerate(((0.25, (352.0, 440.0), 0.7), (0.8, (311.0, 392.0), -0.6), (1.35, (370.0, 466.0), 0.5))):
        put(fx, X.far(X.horn(0.65 + 0.2 * k, f, k), 0.4), a_ + dt, -9.0, pan=pn)
    # S060: at the alarm taxi: the slam on the rear door, the glass, the bite, the man's scream
    a_, b_ = shot("S060")
    t_s60 = a_ + 0.26; T["S060_slam"] = t_s60
    put(fx, X.body_panel(seed=70, big=0.9), t_s60, -6.0, pan=0.25)
    put(fx, X.glass_burst(71), t_s60 + 0.03, -8.0, pan=0.55)
    put(fx, X.growl(0.9, 100, seed=72, hard=1.1), t_s60 + 0.10, -11.0, pan=0.2)
    put(fx, pitch(scr, -2.0), t_s60 + 0.25, -12.0, pan=0.3, fout=0.3)
    # S061: Kong's breathing settles; the crowd is far now
    a_, b_ = shot("S061")
    put(fx, X.far(X.st(X.crowd_roar(b_ - a_, 80), 0.0, 0.9), 0.9), a_, -20.0, fin=0.5, fout=1.0)
    for k in range(5): put(fx, X.breath(0.5, "in" if k % 2 == 0 else "out", 81 + k, f=950), a_ + 0.2 + 0.62 * k * (1 + 0.15 * k), -15.0 - 1.5 * k)
    fx *= db(-7.0)                                              # the hook's effects trim
    # ================================================================== ducking (the hook's) + the guarantee
    env = np.convolve(np.abs(v), np.ones(int(0.12 * SR)) / int(0.12 * SR), "same")
    duck = db(-9.0 * np.clip(env / 0.02, 0, 1)); fxduck = db(-10.0 * np.clip(env / 0.02, 0, 1))
    bed = (amb * duck[:, None] + mus * duck[:, None] + fx * fxduck[:, None]) * drop[:, None]
    # the eye-open hit sits outside the drop (it IS the open)
    oh = np.zeros((N, 2)); put(oh, X.open_hit(), t_open, -1.0 - 7.0); bed += oh * fxduck[:, None]
    speak = env > 0.012
    win = int(0.4 * SR); hop = int(0.1 * SR)
    gfix = np.ones(N)
    vv = voice.mean(1)
    for i in range(0, N - win, hop):
        m = speak[i:i + win]
        if m.mean() < 0.5: continue
        r = 20 * np.log10(rms(vv[i:i + win][m]) / rms(bed[i:i + win].mean(1)[m]))
        if r < FLOOR_DB:
            gfix[i:i + win] = np.minimum(gfix[i:i + win], db(r - FLOOR_DB))
    # smooth the corrections (no pumping clicks): on a 10 ms grid, min-filter over +-0.15 s, average over +-0.15 s, back to samples
    from numpy.lib.stride_tricks import sliding_window_view as swv
    D = 480; gd = gfix[::D]; k = 15
    gm = swv(np.pad(gd, (k, k), mode="edge"), 2 * k + 1).min(1)
    gd2 = np.convolve(np.pad(gm, (k, k), mode="edge"), np.ones(2 * k + 1) / (2 * k + 1), "valid")
    gs = np.interp(np.arange(N), np.arange(len(gd2)) * D, gd2)
    bed *= gs[:, None]
    np.save(os.path.join(HERE, "work", "guarantee_gain.npy"), gs[::480].astype(np.float32))      # 10 ms steps, for the report
    from numpy.lib.stride_tricks import sliding_window_view as swv
    cut = 20 * np.log10(gs[::4800] + 1e-9)
    T["guarantee_cuts_over_3db"] = [(round(F0 + i * 0.1, 1), round(float(c), 1)) for i, c in enumerate(cut) if c < -3.0]
    T["guarantee_max_cut_db"] = round(float(20 * np.log10(gs.min())), 1)
    # ================================================================== measure, limit, write
    rep = measure(voice, bed, speak)
    rep["cues"] = T
    mix = voice + bed
    k = int(0.004 * SR)
    g = np.minimum(1, db(-1.5) / np.maximum(np.abs(mix).max(1), 1e-9)); g = swv(np.pad(g, (k, k), mode="edge"), 2 * k + 1).min(1)
    mix *= g[:, None]
    rep["limiter_max_db"] = round(float(20 * np.log10(g.min())), 2)
    write(os.path.join(HERE, "mix_sc02.wav"), mix)
    for nm, x in (("voice", voice), ("bed", bed), ("music", mus * duck[:, None] * drop[:, None] * gs[:, None]), ("amb", amb * duck[:, None] * drop[:, None] * gs[:, None]),
                  ("fx", fx * fxduck[:, None] * drop[:, None] * gs[:, None])):
        write(os.path.join(HERE, "stems", nm + ".wav"), x)
    I_, tp = loud(os.path.join(HERE, "mix_sc02.wav"))
    rep.update(mix_lufs=I_, mix_true_peak=tp, voice_lufs=loud(os.path.join(HERE, "stems", "voice.wav"))[0], bed_lufs=loud(os.path.join(HERE, "stems", "bed.wav"))[0])
    json.dump(rep, open(os.path.join(HERE, "mix_sc02_report.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in rep.items() if k not in ("windows", "sentences", "cues")}, indent=1, ensure_ascii=False))


def measure(voice, bed, speak):
    """voice over bed: whole (voiced samples), per 0.4 s window (hop 0.1 s) where the voice speaks >= 50 %, per sentence."""
    vv = voice.mean(1); bb = bed.mean(1)
    out = dict(rule="voice RMS over bed RMS on the voiced samples; windows 0.4 s, hop 0.1 s, counted when the voice is active in >= 50 % of the window")
    out["overall_db"] = round(20 * np.log10(rms(vv[speak]) / rms(bb[speak])), 1)
    win = int(0.4 * SR); hop = int(0.1 * SR); W_ = []
    for i in range(0, N - win, hop):
        m = speak[i:i + win]
        if m.mean() < 0.5: continue
        W_.append((round(F0 + i / SR, 2), round(20 * np.log10(rms(vv[i:i + win][m]) / rms(bb[i:i + win][m])), 1)))
    r = np.array([w[1] for w in W_])
    out.update(windows_n=len(W_), window_min_db=float(r.min()), window_p5_db=round(float(np.percentile(r, 5)), 1), window_mean_db=round(float(r.mean()), 1),
               window_median_db=round(float(np.median(r)), 1), worst_windows=sorted(W_, key=lambda w: w[1])[:8])
    sents = {}
    for c in CUT["captions"]:
        s = sents.setdefault(c["id"], [F0 + c["t0"], F0 + c["t1"]]); s[1] = F0 + c["t1"]
    per = []
    for sid, (a, b) in sents.items():
        i, j = I(a), I(b); m = speak[i:j]
        if m.sum() < SR * 0.05: continue
        per.append((sid, round(20 * np.log10(rms(vv[i:j][m]) / rms(bb[i:j][m])), 1)))
    out["sentences"] = per
    out["sentence_min"] = min(per, key=lambda p: p[1])
    out["windows"] = W_
    return out


def write(p, x):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f64le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_f32le", p], input=np.asarray(x, np.float64).tobytes(), check=True)


def loud(p):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", p, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    tail = r[r.rindex("Summary:"):]
    I_ = float(tail.split("I:")[1].split("LUFS")[0]); tp = tail.split("Peak:")[1].split("dBFS")[0].strip()
    return I_, (float(tp) if tp not in ("-inf", "inf") else -120.0)


if __name__ == "__main__":
    main()
