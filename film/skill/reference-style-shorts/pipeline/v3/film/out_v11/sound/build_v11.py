"""v1.1 sound spec: copy of out/mix_film.json with the three changes of BRIEF_POLISH.md section 5.
1. voice gain x 10^(-1/20) (1 dB lower)
2. gust thump_jab at 48.1 s: peak -13 -> GUST_PK (so nothing but the voice is over -10 dBFS there)
3. the two rain_drizzle beds (31.6 s, 59.55 s): rms -41.5/-41.6 -> -34, played from a peak-limited copy of
   rain_drizzle.wav (out_v11/sound/rain_drizzle_lim.wav, crest <= 19.5 dB) so their peak stays under -14 dBFS.
"""
import json, sys, wave, numpy as np, os
P = '__PROJ__'
OUT11 = P + '/v3/film/out_v11'
sys.path.insert(0, P + '/audio'); import mixer
SR = mixer.SR
GUST_PK = float(sys.argv[1]) if len(sys.argv) > 1 else -15.0
CREST = float(sys.argv[2]) if len(sys.argv) > 2 else 16.0   # dB, peak (max of both channels) over mono RMS
LIM = OUT11 + '/sound/rain_drizzle_lim.wav'

def limit(x, crest_db):
    """sample-peak limiter with 3 ms look-ahead / 3 ms attack / 60 ms release; iterated so peak/RMS <= crest."""
    y = x.copy()
    for it in range(12):
        rms = np.sqrt((y.mean(1) ** 2).mean()); T = rms * 10 ** (crest_db / 20)
        a = np.abs(y).max(1)
        if a.max() <= T * 1.0001: break
        g = np.minimum(1.0, T * 0.995 / np.maximum(a, 1e-12))
        la = int(0.003 * SR)
        # look-ahead: minimum over the next la samples
        from numpy.lib.stride_tricks import sliding_window_view
        gp = np.concatenate([g, np.ones(la)])
        gmin = sliding_window_view(gp, la + 1).min(1)[:len(g)]
        # smooth: release (one-pole) forward, then attack backward
        rel = np.exp(-1 / (0.060 * SR)); att = np.exp(-1 / (0.003 * SR))
        s = np.empty_like(gmin); c = 1.0
        for i in range(len(gmin)):
            v = gmin[i]; c = v if v < c else rel * c + (1 - rel) * v; s[i] = c
        s2 = np.empty_like(s); c = 1.0
        for i in range(len(s) - 1, -1, -1):
            v = s[i]; c = v if v < c else att * c + (1 - att) * v; s2[i] = c
        y = y * np.minimum(s, s2)[:, None]
    return y

if __name__ == '__main__':
    src = mixer.load(P + '/audio/sfx/rain_drizzle.wav')
    y = limit(src, CREST)
    pk = np.abs(y).max(); y = y * (0.5 / pk)       # level does not matter (the mixer normalises to rms_db)
    w = wave.open(LIM, 'w'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((y * 32767).round().astype(np.int16).tobytes()); w.close()
    z = mixer.load(LIM)
    for a, b in ((0, 5.85), (0, 3.0)):
        s = z[int(a * SR):int(b * SR)]; r = np.sqrt((s.mean(1) ** 2).mean())
        print('limited drizzle %.2f-%.2f s: crest %.1f dB (stereo peak / mono rms), src crest %.1f' % (
            a, b, 20 * np.log10(np.abs(s).max() / r),
            20 * np.log10(np.abs(src[int(a*SR):int(b*SR)]).max() / np.sqrt((src[int(a*SR):int(b*SR)].mean(1) ** 2).mean()))))
    spec = json.load(open(P + '/v3/film/out/mix_film.json'))
    spec['out_wav'] = OUT11 + '/film_mix.wav'
    spec['video_in'] = OUT11 + '/film_silent_sharp.mp4'          # the sharp v1.1 picture (make_sharp.py)
    spec['video_out'] = P + '/deliver/film_v1_1_sharp_thai.mp4'
    spec['voice']['gain'] = spec['voice']['gain'] * 10 ** (-1 / 20)
    n_g = n_r = 0
    for e in spec['sfx']:
        if os.path.basename(e['file']) == 'thump_jab.wav' and abs(e['at'] - 48.1) < 1e-6:
            e['peak_db'] = GUST_PK; n_g += 1
        if os.path.basename(e['file']) == 'rain_drizzle.wav':
            e['file'] = LIM; e['rms_db'] = -34.0; n_r += 1
    assert n_g == 1 and n_r == 2, (n_g, n_r)
    json.dump(spec, open(OUT11 + '/mix_film.json', 'w'), indent=1, ensure_ascii=False)
    print('voice gain', spec['voice']['gain'], 'gust', GUST_PK, 'drizzle entries', n_r)
