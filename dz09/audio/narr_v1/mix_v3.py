"""mix_v3: same cues and length as mix_v2, rain turned into a soft bed.

Changes against mix_v2.py (user: "less rain, the rain sound too"):
  - rain bed -21 -> -32 dBFS RMS (8-40 s), high shelf + low-pass so it is a soft bed, not hiss
  - rain ducked a further 4 dB under narration (music keeps its 5 dB duck)
  - sirens on their own stem, kept faint (-40 dBFS RMS)
  - rain_on_hood 0.8 -> 0.25 (-10 dB), same softening
  - first radio static 0.5 -> 0.8 (+4 dB, it sits under the radio voice); other story effects, music, narration unchanged; master trimmed to -14 LUFS, limiter ceiling for <= -1 dBTP
Writes mix_v3.wav, mix_v3_levels.json, ab_rain.mp3.  Does NOT touch mix.wav / narr_final.wav / timing json.
Run from this folder:  python3 mix_v3.py
"""
import numpy as np, subprocess, json, os, re, tempfile
from numpy.lib.stride_tricks import sliding_window_view as sw
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
SR = 48000; OFF = 0.30; DUR = 53.32; N = int(SR * DUR)
S = '../ep1_hook/sfx/'
RAIN_RMS_DB = -32.0      # was -21 (rain+sirens together)
RAIN_DUCK_DB = 4.0       # extra dip under narration
SIREN_RMS_DB = -40.0     # v2 sirens sat near -37 inside the bed
HOOD_GAIN = 0.25         # was 0.8
SOFT = 'highpass=f=70,highshelf=f=3000:g=-8,lowpass=f=9000'   # soft bed instead of hiss
TARGET_LUFS = -14.0; CEIL_DB = -1.6

def ff_pcm(args, data=None, ch=2):
    raw = subprocess.run(['ffmpeg', '-v', 'error'] + args + ['-ar', '48000', '-ac', str(ch), '-f', 'f32le', '-'],
                         input=data, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, ch).astype(float)
def load(f, af=None): return ff_pcm(['-i', f] + (['-af', af] if af else []))
rms = lambda x: np.sqrt((x ** 2).mean())
db = lambda x: 20 * np.log10(x + 1e-12)
def put(buf, f, t, g, loop_to=None, af=None):
    x = load(S + f, af) * g; i = int(t * SR); end = int(loop_to * SR) if loop_to else N
    while i < end:
        n = min(len(x), end - i); buf[i:i + n] += x[:n]
        if not loop_to: break
        i += n

def stems(v3):
    voice = np.zeros((N, 2)); rain = np.zeros((N, 2)); sir = np.zeros((N, 2)); fx = np.zeros((N, 2)); mus = np.zeros((N, 2)); hood = np.zeros((N, 2))
    v = load('narr_final.wav'); i = int(OFF * SR); voice[i:i + len(v)] = v[:N - i]
    a, b = int(OFF * SR), int(3.55 * SR)      # radio colour on the cold-open sentence
    r = ff_pcm(['-f', 'f32le', '-ar', '48000', '-ac', '2', '-i', '-', '-af',
                'highpass=f=450,lowpass=f=2800,volume=3,alimiter=limit=0.5,volume=1.7'], voice[a:b].astype(np.float32).tobytes())
    voice[a:b] = r[:b - a]
    put(fx, 'radio_static_cut.wav', 0.0, 0.8 if v3 else 0.5); put(fx, 'radio_static_cut.wav', 3.24, 0.9)
    put(rain, 'rain_heavy_road.wav', 5.49, 1.0, 50.72, SOFT if v3 else None)
    put(sir, 'sirens_city_far.wav', 6.14, 0.35, 50.72)
    put(fx, 'hydraulic_cutter.wav', 15.05, 0.7); put(fx, 'car_alarm_far.wav', 11.10, 0.15)
    put(fx, 'phone_vibrate.wav', 17.65, 0.4)
    put(hood, 'rain_on_hood.wav', 30.35, HOOD_GAIN if v3 else 0.8, af=SOFT if v3 else None)
    put(fx, 'car_door_pry.wav', 34.51, 0.75); put(fx, 'heartbeat_low.wav', 38.68, 0.8); put(fx, 'heartbeat_low.wav', 40.68, 0.9)
    put(fx, 'zombie_lunge.wav', 43.45, 1.0); put(fx, 'man_scream_bite.wav', 43.80, 0.75); put(fx, 'hit_trailer.wav', 50.72, 1.0)
    m = load('../ep1_hook/music/bed_temp.mp3'); a, b = int(17.25 * SR), int(40.08 * SR); seg = m[:b - a].copy()
    seg[:int(3 * SR)] *= np.linspace(0, 1, int(3 * SR))[:, None]; seg[-int(1.2 * SR):] *= np.linspace(1, 0, int(1.2 * SR))[:, None]; mus[a:b] = seg
    a2, b2 = int(45.10 * SR), int(50.72 * SR); seg2 = m[int(30 * SR):int(30 * SR) + (b2 - a2)].copy()
    seg2[:int(0.8 * SR)] *= np.linspace(0, 1, int(0.8 * SR))[:, None]; mus[a2:b2] = seg2
    w = slice(int(8 * SR), int(40 * SR))
    if v3:
        rain *= 10 ** (RAIN_RMS_DB / 20) / rms(rain[w]); sir *= 10 ** (SIREN_RMS_DB / 20) / rms(sir[w])
        f = int(0.25 * SR); rain[int(5.49 * SR):int(5.49 * SR) + f] *= np.linspace(0, 1, f)[:, None]   # no click at the rain cue
    else:
        k = 10 ** (-21 / 20) / rms((rain + sir)[w]); rain *= k; sir *= k
    mus *= 10 ** (-31 / 20) / rms(mus[int(20 * SR):int(36 * SR)])
    env = np.convolve(np.abs(voice.mean(1)), np.ones(int(0.12 * SR)) / int(0.12 * SR), 'same')
    act = np.clip(env / 0.03, 0, 1)
    duck5 = 10 ** (-5 / 20 * act); duckr = 10 ** (-RAIN_DUCK_DB / 20 * act) if v3 else duck5
    t = np.arange(N) / SR; drop = np.ones(N); m1 = (t >= 40.08) & (t < 43.45)
    drop[m1] = np.interp(t[m1], [40.08, 43.30, 43.45], [1, 10 ** (-20 / 20), 10 ** (-20 / 20)])
    return dict(voice=voice, rain=rain * (duckr * drop)[:, None], rain_static=rain, sir=sir * (duck5 * drop)[:, None],
                mus=mus * (duck5 * drop)[:, None], fx=fx, hood=hood, act=act)

def limit(mix, ceil_db, smooth=True):
    k = int(0.004 * SR)
    g = np.minimum(1, 10 ** (ceil_db / 20) / np.maximum(np.abs(mix).max(1), 1e-9))
    g = sw(np.pad(g, (k, k), mode='edge'), 2 * k + 1).min(1)
    if smooth: g = np.convolve(np.pad(g, (k // 2, k // 2), mode='edge'), np.ones(k + 1) / (k + 1), 'valid')[:len(g)]   # smooth the gain steps
    return mix * g[:, None]

def write(mix, name):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', '48000', '-ac', '2', '-i', '-', '-c:a', 'pcm_s16le', name],
                   input=mix.astype(np.float32).tobytes(), check=True)
def ebur(name):
    e = subprocess.run(['ffmpeg', '-nostats', '-i', name, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    e = e[e.rindex('Summary:'):]
    g = lambda k: float(re.search(k + r':\s+(-?[\d.]+)', e).group(1))
    return dict(lufs=g('I'), lra=g('LRA'), true_peak_dbtp=g('Peak'))

def levels(st, master=1.0, bed_master=1.0):
    """levels as they sit in the final file (master gain applied), limiter ignored (it only touches peaks)"""
    w = slice(int(8 * SR), int(40 * SR)); act = st['act'][w] > 0.9; gap = st['act'][w] < 0.1
    vo = st['voice'][w]; ra = st['rain'][w]; bed = (st['rain'] + st['sir'] + st['hood'])[w]
    hs = slice(int(30.35 * SR), int(36.35 * SR)); mv = 20 * np.log10(master); m = 20 * np.log10(bed_master)
    d = dict(rain_bed_rms_static_8_40=db(rms(st['rain_static'][w])) + m,
             rain_bed_rms_as_mixed_8_40=db(rms(ra)) + m,
             rain_bed_rms_under_narration=db(rms(ra[act])) + m,
             rain_bed_rms_in_gaps=db(rms(ra[gap])) + m if gap.sum() > SR // 10 else None,
             sirens_rms_as_mixed_8_40=db(rms(st['sir'][w])) + m,
             rain_on_hood_rms_30_36=db(rms(st['hood'][hs])) + m,
             narration_rms_while_speaking=db(rms(vo[act])) + mv,
             speaking_fraction_8_40=float(act.mean()))
    d['narration_to_rain_bed_db'] = d['narration_rms_while_speaking'] - d['rain_bed_rms_under_narration']
    d['narration_to_all_ambience_db'] = d['narration_rms_while_speaking'] - (db(rms(bed[act])) + m)
    return {k: (round(float(v), 2) if v is not None else None) for k, v in d.items()}

def hf_share(x):
    """share of energy above 4 kHz, in dB relative to the whole (how hissy the rain is)"""
    X = np.abs(np.fft.rfft(x.mean(1))) ** 2; f = np.fft.rfftfreq(len(x), 1 / SR)
    return round(float(10 * np.log10(X[f > 4000].sum() / X.sum())), 2)

if __name__ == '__main__':
    old = stems(False); new = stems(True)
    old_mix = limit(old['voice'] + old['rain'] + old['sir'] + old['mus'] + old['fx'] + old['hood'], -1.0, smooth=False)
    ref = load('mix.wav')
    rep = dict(old_rebuild_vs_mix_wav_max_abs_diff=float(np.abs(old_mix[:len(ref)] - ref[:N]).max()))   # ~1e-4 = the rebuilt v2 stems are the shipped mix
    fore = new['voice'] + new['mus'] + new['fx']; bed = new['rain'] + new['sir'] + new['hood']   # master trim on the foreground only,
    g = 1.0                                                                                      # so the bed keeps its absolute target
    for _ in range(4):                                   # trim master to the loudness target
        write(limit(fore * g + bed, CEIL_DB), 'mix_v3.wav'); e = ebur('mix_v3.wav')
        if abs(e['lufs'] - TARGET_LUFS) < 0.05: break
        g *= 10 ** ((TARGET_LUFS - e['lufs']) / 20)
    w = slice(int(8 * SR), int(40 * SR))
    rep.update(master_gain_db=round(20 * np.log10(g), 2),
               old=dict(levels(old), **ebur('mix.wav'), rain_energy_above_4k_db=hf_share(old['rain_static'][w])),
               new=dict(levels(new, g, 1.0), **e, rain_energy_above_4k_db=hf_share(new['rain_static'][w])))
    info = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', 'mix_v3.wav'], capture_output=True, text=True).stdout
    rep['mix_v3_duration_s'] = float(info)
    # per-effect check: effect stem level against everything else at its cue (new mix)
    other = (new['voice'] + new['mus']) * g + new['rain'] + new['sir'] + new['hood']
    oo = (old['voice'] + old['rain'] + old['sir'] + old['mus'] + old['hood'])
    cues = dict(radio_static_1=(0.39, 1.4), radio_static_2=(3.63, 4.7), car_alarm=(11.10, 15.0), cutter=(15.05, 18.0), phone_vibrate=(17.65, 19.6),
                door_pry=(34.51, 36.5), heartbeat_1=(38.68, 40.6), heartbeat_2=(40.68, 42.6), lunge=(43.45, 43.8), scream=(43.80, 45.5), title_hit=(50.72, 53.3))
    rep['fx_minus_rest_db'] = {k: dict(fx_rms=round(float(db(rms(new['fx'][int(a * SR):int(b * SR)])) + 20 * np.log10(g)), 1),
                                       old=round(float(db(rms(old['fx'][int(a * SR):int(b * SR)])) - db(rms(oo[int(a * SR):int(b * SR)]))), 1),
                                       new=round(float(db(rms(new['fx'][int(a * SR):int(b * SR)]) * g) - db(rms(other[int(a * SR):int(b * SR)]))), 1))
                               for k, (a, b) in cues.items()}
    json.dump(rep, open('mix_v3_levels.json', 'w'), indent=1); print(json.dumps(rep, indent=1))
    # A/B: 10 s of the old mix from 8 s, short gap, the same 10 s of the new mix
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '8', '-t', '10', '-i', 'mix.wav', '-ss', '8', '-t', '10', '-i', 'mix_v3.wav', '-filter_complex',
                    '[0:a]afade=t=in:d=0.05,afade=t=out:st=9.9:d=0.1[a];[1:a]afade=t=in:d=0.05,afade=t=out:st=9.9:d=0.1[b];[a][b]concat=n=2:v=0:a=1',
                    '-c:a', 'libmp3lame', '-b:a', '192k', 'ab_rain.mp3'], check=True)
