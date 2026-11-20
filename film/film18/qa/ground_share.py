"""Film 18 shared plain-ground metric (director, 2026-11-20). usage: python3 ground_share.py take.mkv first_g g0 g1 [step]
Plain = below the horizon (first row from the top where >50 % of pixels are non-sky... approximated as the top of the lowest
contiguous band of low-sky-blue rows), HSV sat < 0.35, value 0.12-0.75, local 9x9 luma std < 6. Share of the WHOLE frame."""
import sys, subprocess, numpy as np
from scipy.ndimage import uniform_filter  # noqa
def frames(v, first_g, g0, g1, step):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", v, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, 1280, 720, 3)
    for g in range(g0, g1, step): yield g, a[g - first_g].astype(np.float32) / 255
def share(x):
    mx = x.max(-1); mn = x.min(-1); s = (mx - mn) / (mx + 1e-4); y = x @ [0.299, 0.587, 0.114]
    m1 = uniform_filter(y * 255, 9); m2 = uniform_filter((y * 255) ** 2, 9); sd = np.sqrt(np.clip(m2 - m1 ** 2, 0, None))
    plain = (s < 0.35) & (mx > 0.12) & (mx < 0.75) & (sd < 6)
    plain[:int(0.40 * 1280)] = False  # the horizon never sits above y 0.40 in film 18 ground shots
    return plain.mean()
if __name__ == "__main__":
    v, fg, g0, g1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]); st = int(sys.argv[5]) if len(sys.argv) > 5 else 10
    r = [(g, share(x)) for g, x in frames(v, fg, g0, g1, st)]
    print(" ".join(f"g{g}:{s:.2f}" for g, s in r)); print(f"max {max(s for _, s in r):.3f} median {np.median([s for _, s in r]):.3f}")
