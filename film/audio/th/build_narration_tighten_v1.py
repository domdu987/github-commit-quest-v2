import numpy as np
def tighten(x, sr, t0, t1, max_gap=0.26, keep=0.17, thr=0.012):
    """shorten silences longer than max_gap to keep seconds; trim head and tail; remap char times."""
    win = int(0.02 * sr); env = np.sqrt(np.convolve(x ** 2, np.ones(win) / win, "same")); sil = env < thr
    cuts = []  # (start, end) sample ranges to remove
    i, n = 0, len(x)
    while i < n:
        if sil[i]:
            j = i
            while j < n and sil[j]: j += 1
            dur = (j - i) / sr
            if i == 0: cuts.append((0, max(0, j - int(0.03 * sr))))
            elif j == n: cuts.append((min(n, i + int(0.08 * sr)), n))
            elif dur > max_gap:
                a = i + int(keep * sr / 2); b = j - int(keep * sr / 2); cuts.append((a, b))
            i = j
        else: i += 1
    keepmask = np.ones(n, bool)
    for a, b in cuts: keepmask[a:b] = False
    removed_before = np.cumsum(~keepmask)
    def remap(t):
        k = min(n - 1, max(0, int(t * sr))); return (k - removed_before[k]) / sr
    y = x[keepmask]
    # tiny fades at the joins are unnecessary: cuts are inside silence
    return y, [remap(t) for t in t0], [remap(t) for t in t1], sum(b - a for a, b in cuts) / sr
