import sys, cv2, numpy as np
video = sys.argv[1]
cap = cv2.VideoCapture(video)
def frame(t):
    cap.set(cv2.CAP_PROP_POS_MSEC, t*1000); ok, f = cap.read(); return f
regions = {
 "station_bg":      (0.6, (0, 0, 720, 300)),
 "bus_body":        (0.6, (60, 640, 640, 760)),
 "distance_card":   (2.6, (330, 70, 700, 300)),
 "map_bg_and_land": (4.6, (0, 300, 720, 1200)),
 "red_route_pin":   (4.6, (100, 150, 300, 600)),
 "subtitle_redbox": (4.6, (340, 820, 680, 880)),
 "split_day_room":  (6.5, (0, 0, 720, 600)),
 "chart1_bars":     (9.0, (60, 230, 560, 520)),
 "green_pill":      (9.0, (570, 580, 720, 650)),
 "night_highway":   (11.0, (0, 0, 720, 600)),
 "qmark_icon":      (11.0, (300, 380, 420, 500)),
 "calendar":        (13.2, (40, 60, 680, 560)),
 "waffle":          (18.4, (40, 60, 680, 600)),
 "day_room":        (20.2, (0, 0, 720, 1280)),
 "night_room":      (21.5, (0, 0, 720, 1280)),
 "phone_call":      (23.8, (150, 100, 570, 1150)),
 "chart2":          (28.6, (40, 60, 700, 560)),
 "image_vs_real":   (31.0, (40, 120, 700, 560)),
 "spotlight":       (37.9, (0, 300, 720, 1280)),
 "checklist":       (44.4, (40, 60, 470, 380)),
 "photo_wall":      (47.5, (100, 100, 700, 700)),
 "chart3":          (52.6, (40, 90, 700, 560)),
 "remote_closeup":  (56.2, (0, 0, 720, 1280)),
 "endcard":         (65.0, (0, 0, 720, 1280)),
 "logo":            (69.0, (200, 300, 520, 800)),
 "yellow_sub":      (8.0, (150, 800, 570, 880)),
}
for name,(t,(x0,y0,x1,y1)) in regions.items():
    f = frame(t)[y0:y1, x0:x1].reshape(-1,3).astype(np.float32)
    crit = (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 1.0)
    _, lab, cen = cv2.kmeans(f, 6, None, crit, 3, cv2.KMEANS_PP_CENTERS)
    cnt = np.bincount(lab.ravel(), minlength=6)/len(lab)
    order = np.argsort(-cnt)
    s = "  ".join(f"#{int(cen[i][2]):02x}{int(cen[i][1]):02x}{int(cen[i][0]):02x}:{cnt[i]*100:.0f}%" for i in order)
    print(f"{name:16s} t={t:5.1f}  {s}")
