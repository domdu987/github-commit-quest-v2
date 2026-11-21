import numpy as np
def tighten(x, sr, t0, t1, max_gap=0.12, keep=0.08, thr=0.012):
    win = int(0.02 * sr); env = np.sqrt(np.convolve(x ** 2, np.ones(win) / win, "same")); sil = env < thr
    cuts, i, n = [], 0, len(x)
    while i < n:
        if sil[i]:
            j = i
            while j < n and sil[j]: j += 1
            if i == 0: cuts.append((0, max(0, j - int(0.03 * sr))))
            elif j == n: cuts.append((min(n, i + int(0.08 * sr)), n))
            elif (j - i) / sr > max_gap: cuts.append((i + int(keep * sr / 2), j - int(keep * sr / 2)))
            i = j
        else: i += 1
    km = np.ones(n, bool)
    for a, b in cuts: km[a:b] = False
    rb = np.cumsum(~km)
    rm = lambda t: (min(n - 1, max(0, int(t * sr))) - rb[min(n - 1, max(0, int(t * sr)))]) / sr
    return x[km], [rm(t) for t in t0], [rm(t) for t in t1], sum(b - a for a, b in cuts) / sr

