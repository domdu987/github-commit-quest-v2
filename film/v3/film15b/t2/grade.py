import numpy as np
def rgb2hsv(a):
    mx = a.max(-1); mn = a.min(-1); d = mx - mn + 1e-6; r, g, b = a[..., 0], a[..., 1], a[..., 2]
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60.0
    return h % 360, d / (mx + 1e-6), mx
def hsv2rgb(h, s, v):
    c = v * s; hp = (h % 360) / 60.0; x = c * (1 - np.abs(hp % 2 - 1)); z = np.zeros_like(c)
    conds = [(hp < 1), (hp < 2), (hp < 3), (hp < 4), (hp < 5), (hp >= 5)]
    rr = np.select(conds, [c, x, z, z, x, c]); gg = np.select(conds, [x, c, c, x, z, z]); bb = np.select(conds, [z, z, x, c, c, x]); m = v - c
    return np.stack([rr + m, gg + m, bb + m], -1)
def grade(a, gain=1.0, sat=1.12, shade=0.35, gamma=1.0):
    """a float RGB 0..1. gain/gamma set the luma, sat boosts saturation, shade pulls dark areas toward blue-violet (hue 250)."""
    a = np.clip(a, 0, 1) ** gamma * gain
    h, s, v = rgb2hsv(np.clip(a, 0, 1)); Y = (0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2])
    m = np.clip((0.50 - Y) / 0.50, 0, 1) ** 1.3 * shade
    dh = ((250.0 - h + 180) % 360) - 180                         # shortest way to hue 250
    win = np.clip(np.minimum(h - 110, 300 - h) / 40.0, 0, 1)         # only cool / green shadows move; reds, maroon and ambers keep their hue
    h2 = h + dh * m * np.clip(s * 3, 0, 1) * win
    s2 = np.clip(s * sat + 0.10 * m * win, 0, 1)
    # magenta guard: pull hues 285..345 toward 270
    mag = (h2 > 285) & (h2 < 330); h2 = np.where(mag, 270 + (h2 - 270) * 0.3, h2)
    return np.clip(hsv2rgb(h2, s2, v), 0, 1)
def stats(a):
    h, s, v = rgb2hsv(a); Y = (0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2])
    sh = Y < np.percentile(Y, 30)
    return dict(sat=float(s.mean()), vivid=float((s > 0.5).mean() * 100), luma=float((Y * 255).mean()), magenta=float(((h > 285) & (h < 345) & (s > 0.25)).mean() * 100), shade_hue=float(np.degrees(np.angle((np.exp(1j * np.radians(h[sh & (s > 0.15)]))).mean()))) % 360 if (sh & (s > 0.15)).any() else 0)
