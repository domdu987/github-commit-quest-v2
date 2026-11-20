SLIDE = [0.46]

def _calipers_body(k):
    """cast17's calipers with an adjustable sliding jaw (SLIDE[0] = x of the jaw tip line; default 0.46) so the jaws can close."""
    c17 = cast17; dx = SLIDE[0] - 0.46
    g = c17._lin(k, "cb", c17.STEEL["light"], c17.STEEL["base"], c17.STEEL["dark"], 0, -0.05, 0, 0.05)
    o = ['<path d="M-0.12,-0.034 L0.88,-0.034 L0.88,0.034 L-0.12,0.034 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (g, k.ink)]
    tk = "".join("M%.3f,0.034 L%.3f,%.3f " % (x, x, 0.034 + (0.034 if i % 5 == 0 else 0.020)) for i, x in enumerate([0.02 + 0.04 * j for j in range(20)]))
    o.append('<path d="%s" stroke="%s" stroke-width="0.008" fill="none"/>' % (tk, k.c(c17.STEEL["deep"])))
    o.append('<path d="M-0.08,-0.018 L0.84,-0.018" stroke="#ffffff" stroke-width="0.008" opacity="0.7" stroke-linecap="round"/>')
    o.append('<path d="M0.80,0.030 L0.88,0.030 L0.88,0.30 L0.835,0.33 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (k.c(c17.STEEL["base"]), k.ink))
    o.append('<path d="M%.3f,-0.050 L%.3f,-0.050 L%.3f,0.30 L%.3f,0.33 L%.3f,0.034 L%.3f,0.034 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>'
             % (0.40 + dx, 0.52 + dx, 0.52 + dx, 0.485 + dx, 0.46 + dx, 0.40 + dx, k.c(c17.STEEL["light"]), k.ink))
    o.append('<circle cx="%.3f" cy="-0.075" r="0.036" fill="%s" stroke="%s" stroke-width="0.014"/>' % (0.46 + dx, k.c(c17.BRASS["base"]), k.ink))
    return "".join(o)
cast17._calipers_body = _calipers_body
_orig_svg = C.sprites.sprite_svg
def _svg(cast, pose, *a, **kw):
    g = (pose or {}).get("t", None)
    if g is not None and cast == "bertillon": SLIDE[0] = slide_of(int(round(g * 30)))
    return _orig_svg(cast, pose, *a, **kw)
C.sprites.sprite_svg = _svg


def theta_of(yaw): return math.radians(min(abs(yaw), 1.2) * 70.0)

def ear_local(an, g, name, s):
    """target for the caliper jaws (puppet-local D): the viewer-left ear (the near ear in profile).  Shot 1 approaches from below-left."""
    hx, hy = an["head"]
    yw = yaw_of(name, g)
    ex = hx - 0.52 * math.cos(theta_of(yw))
    u = clamp((g - 1) / 13.0) if s == 1 else 1.0
    k = 1.0 - sm(u)
    tap = 0.015 * math.sin(g * 0.8) * (1 if u >= 1 else 0)
    return (ex - 0.5 * k, hy + 0.02 + 1.0 * k + tap)

def ears_svg(pose):
    """cartoon ears (the puppet has none) -> (underlay, overlay) SVG, puppet-local D, y down.  Near ear in profile is drawn OVER the head."""
    yw = pose.get("yaw", 0.0); r = pose.get("head_roll", 0.0); dx = pose.get("head_dx", 0.0); dy = pose.get("head_dy", 0.0)
    ink, fill = "#3a2832", "#f4d4cb"
    c = math.cos(theta_of(yw)); prof = abs(yw) > 0.5
    def ear(x, sx, big):
        rx, ry = (0.19, 0.27) if big else 0.15, (0.25)
        if big: rx, ry = 0.19, 0.27
        else: rx, ry = 0.15, 0.25
        return ('<g transform="translate(%.3f %.3f) scale(%d 1)"><ellipse cx="0" cy="0.02" rx="%.3f" ry="%.3f" fill="%s" stroke="%s" stroke-width="0.035"/>'
                '<path d="M-0.05,-0.13 C0.05,-0.15 0.11,0.02 0.03,0.14" fill="none" stroke="%s" stroke-width="0.03" stroke-linecap="round"/></g>' % (x, 0, sx, rx, ry, fill, ink, ink))
    under = ear(0.52 * c, 1, False) + ear(-0.52 * c, 1, False) if not prof else ear(0.52 * c, 1, False)
    over = ear(-0.52 * c, 1, True) if prof else ""
    wrap = lambda g: '<g transform="rotate(%.2f %.3f %.3f) translate(%.3f %.3f)">%s</g>' % (r, dx, dy, dx, dy, g) if g else ""
    return wrap(under), wrap(over)

def hand_svg(an):
    """a visible forearm (lighter sleeve), white cuff and skin hand gripping the beam (puppet-local D, from the sprite's own anchors)."""
    ex, ey = an["elbow_r"]; hx, hy = an["hand_r"]
    dx, dy = hx - ex, hy - ey; L = math.hypot(dx, dy) or 1.0; ux, uy = dx / L, dy / L
    cx, cy = hx - ux * 0.13, hy - uy * 0.13
    return ('<g><path d="M%.3f,%.3f L%.3f,%.3f" stroke="#3a2832" stroke-width="0.17" stroke-linecap="round" fill="none"/>'
            '<path d="M%.3f,%.3f L%.3f,%.3f" stroke="#46598f" stroke-width="0.125" stroke-linecap="round" fill="none"/>'
            '<path d="M%.3f,%.3f L%.3f,%.3f" stroke="#3a2832" stroke-width="0.155" stroke-linecap="butt" fill="none"/>'
            '<path d="M%.3f,%.3f L%.3f,%.3f" stroke="#fbf3ee" stroke-width="0.115" stroke-linecap="butt" fill="none"/>'
            '<circle cx="%.3f" cy="%.3f" r="0.105" fill="#f4d4cb" stroke="#3a2832" stroke-width="0.03"/>'
            '<path d="M%.3f,%.3f q0.05,-0.02 0.09,0.03" stroke="#3a2832" stroke-width="0.02" fill="none"/></g>'
            % (ex, ey, hx, hy, ex, ey, hx, hy, cx - ux * 0.045, cy - uy * 0.045, cx + ux * 0.045, cy + uy * 0.045,
               cx - ux * 0.045, cy - uy * 0.045, cx + ux * 0.045, cy + uy * 0.045, hx, hy, hx - 0.04, hy - 0.01))

