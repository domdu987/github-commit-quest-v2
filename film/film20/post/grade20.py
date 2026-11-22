"""Film 20: apply the v1.1 grade (film/COLOUR_SPEC.md section 5; grade_v11.py = film/skill/.../out_v11/grade.py, unchanged)
to conformed frames, BEFORE captions. Only the global look is used (DEFAULT params: S-curve, sat x1.18, hot-spot bloom,
red/white protection, ceiling 0.985, vignette); film 1's per-shot table and clock are cleared.
Usage: python3 grade20.py <frames_dir> <pattern f_%04d.png> <N> [procs]   (in place; symlinks replaced by files)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grade_v11 as G
G.TAKES = [("all", 0)]; G.JOINS = []; G.SHOT = {}
from PIL import Image

def one(a):
    d, pat, g = a
    p = os.path.join(d, pat % g)
    if not os.path.exists(p): return 0
    im = Image.open(p).convert("RGB")
    out = G.grade_frame(im, g)
    if os.path.islink(p): os.remove(p)
    out.save(p); return 1

if __name__ == "__main__":
    d, pat, N = sys.argv[1], sys.argv[2], int(sys.argv[3]); procs = int(sys.argv[4]) if len(sys.argv) > 4 else os.cpu_count()
    import multiprocessing as mp
    with mp.Pool(procs) as pool:
        n = sum(pool.imap_unordered(one, [(d, pat, g) for g in range(N)], chunksize=8))
    print("grade20: graded", n, "frames (v1.1 global look)")
