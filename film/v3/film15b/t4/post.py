"""post: fill the leftover black void behind the stand crowd (stands frames only), then nothing else (whips are blurred in shot.py)."""
import sys, os, numpy as np, cv2
d = sys.argv[1]
for g in range(1205, 1273):
    p = os.path.join(d, 'g_%04d.png' % g)
    if not os.path.exists(p): continue
    im = cv2.imread(p); lum = im.max(2)
    m = (lum < 16).astype(np.uint8); m[int(im.shape[0] * 0.5):] = 0
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, connectivity=4)
    out = np.zeros_like(m)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 1500: out[lab == i] = 1
    if not out.any(): continue
    out = cv2.dilate(out, np.ones((3, 3), np.uint8))
    h = im.shape[0]; yy = np.linspace(0, 1, h)[:, None, None]
    fill = (np.array([70, 36, 26], np.float32) * (1 - yy * 0.4) + 0 * yy)            # BGR deep stand blue-violet, a touch lighter lower down
    fill = np.broadcast_to(fill, im.shape).astype(np.float32)
    a = cv2.GaussianBlur(out.astype(np.float32), (0, 0), 1.2)[..., None]
    cv2.imwrite(p, np.clip(im * (1 - a) + fill * a, 0, 255).astype(np.uint8))
print('post done')
