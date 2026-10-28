import sys, cv2, numpy as np
video = sys.argv[1]
shots = [(0.0,3.43),(3.43,5.1),(5.1,7.23),(7.23,9.47),(9.47,12.2),(12.2,13.37),(13.37,16.0),(16.0,18.7),(18.7,20.83),(20.83,22.07),(22.07,24.43),(24.43,29.13),(29.13,31.67),(31.67,35.6),(35.6,38.07),(38.07,39.63),(39.63,42.0),(42.0,45.0),(45.0,47.8),(47.8,53.2),(53.2,55.37),(55.37,56.8),(56.8,62.73),(62.73,66.73)]
cap = cv2.VideoCapture(video)
def frame_at(t):
    cap.set(cv2.CAP_PROP_POS_MSEC, t*1000)
    ok, f = cap.read()
    return cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
orb = cv2.ORB_create(4000)
for i,(a,b) in enumerate(shots,1):
    t0, t1 = a+0.12, b-0.12
    f0, f1 = frame_at(t0), frame_at(t1)
    # mask: ignore subtitle band (y 760-900) to reduce text influence
    mask = np.full(f0.shape, 255, np.uint8); mask[740:900,:] = 0
    k0,d0 = orb.detectAndCompute(f0,mask); k1,d1 = orb.detectAndCompute(f1,mask)
    if d0 is None or d1 is None: print(i,"no features"); continue
    m = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).match(d0,d1)
    m = sorted(m, key=lambda x:x.distance)[:800]
    p0 = np.float32([k0[x.queryIdx].pt for x in m]); p1 = np.float32([k1[x.trainIdx].pt for x in m])
    # moving points only (exclude static UI): keep matches that moved > 1.5px, estimate on them
    disp = np.linalg.norm(p1-p0,axis=1)
    static_ratio = float(np.mean(disp<1.0))
    mv = disp>=1.0
    if mv.sum() >= 12:
        M, inl = cv2.estimateAffinePartial2D(p0[mv], p1[mv], method=cv2.RANSAC, ransacReprojThreshold=2.0)
        s = float(np.sqrt(M[0,0]**2+M[1,0]**2)); tx, ty = float(M[0,2]), float(M[1,2])
        print(f"S{i:02d} {a:5.2f}-{b:5.2f} static={static_ratio:.2f} moving_n={int(mv.sum())} inliers={int(inl.sum())} scale={s:.3f} tx={tx:.1f} ty={ty:.1f}")
    else:
        print(f"S{i:02d} {a:5.2f}-{b:5.2f} static={static_ratio:.2f} (no dominant motion)")
