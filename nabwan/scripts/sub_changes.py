import sys, cv2, numpy as np
cap = cv2.VideoCapture(sys.argv[1]); fps = cap.get(cv2.CAP_PROP_FPS)
prev = None; i = 0; diffs = []
while True:
    ok, f = cap.read()
    if not ok: break
    band = f[785:885, 60:660]
    # subtitle pixels: very bright (white text), yellow text, or saturated red box
    hsv = cv2.cvtColor(band, cv2.COLOR_BGR2HSV)
    white = (hsv[...,2] > 225) & (hsv[...,1] < 40)
    yellow = (hsv[...,0] > 15) & (hsv[...,0] < 35) & (hsv[...,1] > 110) & (hsv[...,2] > 180)
    red = ((hsv[...,0] < 8) | (hsv[...,0] > 172)) & (hsv[...,1] > 120) & (hsv[...,2] > 150)
    m = np.stack([white, yellow, red]).astype(np.uint8)
    if prev is not None:
        d = float(np.mean(m != prev))
        diffs.append((i/fps, d, int(white.sum()), int(yellow.sum()), int(red.sum())))
    prev = m; i += 1
ds = np.array([d for _, d, *_ in diffs])
thr = max(0.02, np.percentile(ds, 97))
last = -1
for t, d, w, y, r in diffs:
    if d >= thr and t - last > 0.25:
        style = "red" if r > 2000 else ("yellow" if y > w else "white")
        print(f"{t:6.2f}s  diff={d:.3f}  white={w} yellow={y} red={r} -> {style}")
        last = t
