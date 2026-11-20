s = open('shot.py').read()

# ---------------------------------------------------------------- A. timeline + cameras
a = s.index("# part R: reveal room.")
b = s.index("# ----------------------------------------------------------------------------- hooks (reveal)")
new_cams = '''# part R: reveal room.  wall y 0, camera side y > 0.  drawer front centre (0.15, 0, 1.2), pulls out toward +y (travel 0.78).
R_DB0 = ((-0.15, 3.0, 1.9), (-0.50, 0.5, 1.2))          # drawer_big start (landing of the whip)
R_DB1 = ((-0.22, 2.40, 1.8), (-0.48, 0.5, 1.2))           # drawer_big end
R_BX0 = ((0.24, 1.38, 1.84), (-0.02, 0.50, 1.20))         # box beat start: all the boxes in frame
R_BX1 = ((0.07, 1.03, 1.68), (-0.03, 0.58, 1.26))         # box beat end: the one lit box, hand at the lid
R_CH0 = ((0.30, 1.55, 1.78), (0.0, 0.70, 1.38))           # card_hero preset
R_CH1 = ((0.16, 1.22, 1.70), (0.0, 0.72, 1.47))           # push-in ~9 %/s + slide
G_WHIP_R = (1375, 1383)           # whip-on: pan settles into drawer_big
G_FING = (1406, 1419)             # insert: calipers on dupont's raised finger ("นิ้ว")   (measure room)
G_BOX = 1420                      # box beat starts (reveal room)
G_EAR = (1459, 1473)              # insert: calipers on dupont's ear ("หู")  (measure room)
G_CARD = 1474                     # card_hero: snap + card rises
SNAP = 10


def part_of(g):
    return "M" if (FIRST <= g <= G_M_END or G_FING[0] <= g <= G_FING[1] or G_EAR[0] <= g <= G_EAR[1]) else "R"


def mode_of(g):
    return "finger" if G_FING[0] <= g <= G_FING[1] else ("ear" if G_EAR[0] <= g <= G_EAR[1] else "head")


def cam_R(g):
    if g < G_FING[0]:                                                       # shot 24b: drawer_big
        u = seg(g, G_WHIP_R[0], G_FING[0], lambda x: 0.3 * sine(x) + 0.7 * x)
        loc, look = vlerp(R_DB0[0], R_DB1[0], u), vlerp(R_DB0[1], R_DB1[1], u)
        loc = (loc[0] + 0.05 * math.sin(g * 0.13), loc[1], loc[2])
        if g < G_WHIP_R[1]:                                                 # whip-on: start panned away to the left, brake into place
            w = 1 - seg(g, G_WHIP_R[0] - 1, G_WHIP_R[1], lambda x: 1 - (1 - x) ** 2.2)
            look = (look[0] - 3.4 * w, look[1] + 0.6 * w, look[2])
        return loc, look
    if g < G_CARD:                                                          # box beat: drift + slide, snap-push into the box at the end of the beat
        u = seg(g, G_BOX, G_EAR[0], lambda x: 0.3 * sine(x) + 0.7 * x)
        loc, look = vlerp(R_BX0[0], R_BX1[0], u), vlerp(R_BX0[1], R_BX1[1], u)
        return (loc[0] + 0.045 * math.sin(g * 0.15), loc[1], loc[2] + 0.02 * math.sin(g * 0.11)), look
    e = seg(g, G_CARD, G_CARD + SNAP, lambda x: ease_peak(x, 2.0))           # card shot: snap from the wide box view to card_hero, then push-in
    if g < G_CARD + SNAP:
        return vlerp(R_BX1[0], R_CH0[0], e), vlerp(R_BX1[1], R_CH0[1], e)
    u = seg(g, G_CARD + SNAP, 1521, lambda x: 0.2 * sine(x) + 0.8 * x)
    loc, look = vlerp(R_CH0[0], R_CH1[0], u), vlerp(R_CH0[1], R_CH1[1], u)
    return (loc[0] + 0.04 * math.sin(g * 0.14), loc[1], loc[2]), look


# measuring-room inserts (copied from team 1's approved S3A ear framing for the ear)
F_A = ((1.20, 1.18, 1.12), (0.46, 2.02, 1.08))
F_B = ((0.98, 1.38, 1.10), (0.46, 2.04, 1.08))
S3A = (((-0.58, 1.46, 1.02), (0.58, 2.20, 1.24)), ((-0.14, 1.80, 1.06), (0.74, 2.20, 1.24)))


def cam_ins(g):
    if mode_of(g) == "finger":
        u = seg(g, G_FING[0], G_FING[1] + 1, lambda x: 0.3 * sine(x) + 0.7 * x)
        a, b = F_A, F_B
    else:
        u = seg(g, G_EAR[0], G_EAR[1] + 1, lambda x: 0.25 * sine(x) + 0.75 * x)
        a, b = S3A
    return vlerp(a[0], b[0], u), vlerp(a[1], b[1], u)


'''
s = s[:a] + new_cams + s[b:]

# ---------------------------------------------------------------- B. hooks
a = s.index("def lid_t(g):")
b = s.index("LAMP_DB, LAMP_CARD")
s = s[:a] + '''def lid_t(g):
    return seg(g, 1442, 1457)


def lift_t(g):
    return seg(g, G_CARD + 2, 1500, lambda x: ease_peak(x, 1.6))


DARK_AT = {"box2": 1424, "bxA": 1429, "bxB": 1434, "bxC": 1439, "bxD": 1444, "bxE": 1449}      # lit box -> dark box, one by one; 'box' stays lit
EXTRA = {"bxA": ((0.30, -0.02), 0.16, 0.14, 0.12, 8), "bxB": ((0.33, -0.32), 0.14, 0.18, 0.13, 8),
         "bxC": ((-0.18, -0.46), 0.20, 0.14, 0.12, 5), "bxD": ((-0.38, 0.06), 0.14, 0.16, 0.12, 7), "bxE": ((-0.05, 0.05), 0.18, 0.15, 0.13, 9)}


''' + s[b:]
s = s.replace("return lerp(LAMP_DB, LAMP_CARD, seg(g, G_S26, G_S26 + SNAP + 8))", "return lerp(LAMP_DB, LAMP_CARD, seg(g, G_CARD, G_CARD + SNAP + 8))")

# ---------------------------------------------------------------- C. cam_M modes
s = s.replace("def cam_M(g):\n    u = seg(", "def cam_M(g):\n    if mode_of(g) != 'head':\n        return cam_ins(g)\n    u = seg(")

# ---------------------------------------------------------------- D. pose_frames
s = s.replace("            loc, look = (cam_M if self.part == \"M\" else cam_R)(g)", "            loc, look = (cam_M if self.part == \"M\" else cam_R)(g)")
s = s.replace('''                K.set_box_lid("box", lid_t(g) if g >= 1410 else 0.0, frame=f)
                K.set_card_lift(lift_t(g), frame=f)
''', '''                K.set_box_lid("box", lid_t(g), frame=f)
                self.key_boxes(g, f)
                self.key_hand(g, f)
                self.key_hero(g, f)
''')

# ---------------------------------------------------------------- E. new Take helpers + stage_M
a = s.index("    def stage_M(self, gs):")
b = s.index("    # ---- part R: bertillon at the drawer")
stage_m = r'''    # ---- measuring-room staging: three modes (head: calipers on the skull; finger: on the raised finger; ear: on the near ear)
    def stage_M(self, gs):
        d_cast, b_cast = "dupont", "bertillon"
        da, dpos, dsc = self.put("dup", d_cast, "chair", dy=-0.22)
        ba, bpos, bsc = self.put("ber", b_cast, "clerk", dx=-1.0, dy=-0.15)
        _, dpose0 = pose_with("dupont_innocent", 1)
        fx, fy = sprites.feet_of(d_cast, dpose0)
        dzz = K.HEAD_Z["chair"] - dsc * fy
        for g in gs:
            f = g - FIRST + 1
            m = mode_of(g)
            dp_xy = (0.70, 2.16) if m == "ear" else (dpos[0], dpos[1])
            bp_xy = {"head": (bpos[0], bpos[1]), "finger": (0.36, 1.86), "ear": (0.30, 2.42)}[m]
            da.place(f, (dp_xy[0], dp_xy[1], dzz), scale=dsc)
            ba.place(f, (bp_xy[0], bp_xy[1], 0.0), scale=bsc)
        for g in gs:                                              # dupont first (his anchors give the calipers' target)
            f = g - FIRST + 1
            self.scene.frame_set(f)
            m = mode_of(g)
            _, dp = pose_with("dupont_innocent", g, expr="worried", phase=1.0, sway=0.6)
            dp["legs"] = "stand"
            if m == "finger":                                       # the left hand (screen-left, toward Bertillon) comes up with one finger
                u = seg(g, G_FING[0], G_FING[0] + 6)
                dp["arm_l"] = dict(hand=(lerp(-0.74, -0.52, u), lerp(0.60, 0.30, u)), bend=0.4, shape="point", sharp=1.0)
                dp["ears17"] = True
            elif m == "ear":
                dp.update(yaw=0.88, pitch=0.0, gaze=(0.9, 0.05), arm_l=dict(preset="shrug"), arm_r=dict(preset="shrug"))
                dp["ears17"] = True
            da.pose(f, dp, camera=self.cam)
        self.sprites_group(da, gs, 320, 512)
        for g in gs:                                              # bertillon: jaws pinned
            f = g - FIRST + 1
            self.scene.frame_set(f)
            m = mode_of(g)
            bp_cast, bp = pose_with("bertillon_measuring", g, mirror=False, sway=0.5)
            bp["prop_r"] = dict(bp["prop_r"], angle=-10 + 6 * math.sin(g * 0.3)); bp["gaze"] = (0.95, 0.35); bp["pitch"] = 0.25
            bp["t"] = g / 30.0
            if m == "head":
                u0 = seg(g, FIRST, 1350, lambda x: 1 - (1 - x) ** 2)
                head_w = Vector((da.feet_at(f)[0] if False else 0.70, 2.08, K.HEAD_Z["chair"] + 0.03))
                tip = (head_w.x - 0.10 - 0.45 * (1 - u0), head_w.y - 0.05, head_w.z + 0.09 - 0.40 * (1 - u0) + 0.012 * math.sin(g * 0.9))
                hands = {"r": {"tip": tip, "prop": "calipers", "angle": -4}}
            else:
                an = self.anch[(da.name, f)]
                if m == "finger":
                    hx, hy = an["hand_l"]
                    k = 1.0 - seg(g, G_FING[0], G_FING[0] + 7)
                    loc_t = (hx - 0.02 - 0.5 * k, hy - 0.10 + 0.9 * k + 0.012 * math.sin(g * 0.9))
                    ang, psc = -4, 0.9
                else:
                    hx, hy = an["head"]
                    ex = hx - 0.52 * math.cos(theta_of(0.88))
                    k = 1.0 - seg(g, G_EAR[0], G_EAR[0] + 6)
                    loc_t = (ex - 0.5 * k, hy + 0.02 + 1.0 * k + 0.015 * math.sin(g * 0.8))
                    ang, psc = -4, 0.8
                w = actors.local_to_world(da, loc_t, f, camera=self.cam)
                hands = {"r": {"tip": w, "prop": "calipers", "angle": ang, "prop_scale": psc, "stretch": 1.15}}
            ba.pose(f, bp, hands=hands, camera=self.cam)
        self.sprites_group(ba, gs, 320, 512, hand_overlay=True)

    def sprites_group(self, a, gs, ppd_lo, ppd_hi, hand_overlay=False):
        lo = [g - FIRST + 1 for g in gs if mode_of(g) == "head"]
        hi = [g - FIRST + 1 for g in gs if mode_of(g) != "head"]
        for frames, ppd in ((lo, ppd_lo), (hi, ppd_hi)):
            if not frames:
                continue
            for f, r in zip(frames, a.render_sprites(ppd, frames=frames)):
                self.anch[(a.name, f)] = r["anchors"]
            if hand_overlay and frames is hi:
                ov = lambda f, pose: hand_svg(self.anch[(a.name, f)])
                a.render_sprites(ppd, frames=frames, overlay=ov)

    # ---- reveal-room runtime dressing: extra boxes (lit -> dark one by one), Bertillon's hand at the lid, the hero card
    def build_extras(self):
        slide = K.STATE["anim"]["big"]["slide"]
        self.twin = {}
        for nm, (xy, w, d, h, seed) in EXTRA.items():
            K.card_box(nm, (xy[0], xy[1], -0.175), rot_z=seed * 7 % 20 - 10, w=w, d=d, h=h, lid=0.0, cards=6, seed=seed, parent=slide, mat="box_ochre", lining="walnut")
            K.card_box(nm + "_d", (xy[0], xy[1], -0.175), rot_z=seed * 7 % 20 - 10, w=w, d=d, h=h, lid=0.0, cards=6, seed=seed, parent=slide, mat="dark", lining="dark")
        xy2 = (0.1, -0.3)
        K.card_box("box2_d", (xy2[0], xy2[1], -0.175), rot_z=6, w=0.28, d=0.22, h=0.17, lid=0.0, cards=8, seed=6, parent=slide, mat="dark", lining="dark")
        B = K.Batch(21)                                         # the hand: local +x points back along the forearm, the hand is at the origin
        B.cyl("cloth", (0.38, 0, 0), 0.048, 0.62, axis="x", seg=12)
        B.cyl("cream", (0.075, 0, 0), 0.052, 0.05, axis="x", seg=12)
        B.sphere("cardedge", (0.0, 0, 0), 0.05, scale=(1.0, 1.0, 0.8))
        for k in (-1, 0, 1):
            B.cyl("cardedge", (-0.065, 0.026 * k, 0.0), 0.012, 0.09, axis="x", seg=8)
        B.sphere("cardedge", (-0.02, -0.055, -0.01), 0.02)
        root = bpy.data.objects.new("hand_root", None)
        bpy.context.scene.collection.objects.link(root)
        B.finalize("hand", parent=root, ink_t=K.STATE["ink_t"] * 0.7)
        self.hand = root

    def objs_of(self, nm):
        a = K.STATE["anim"][nm]
        return list(a["objs"])

    def key_boxes(self, g, f):
        for nm, tg in DARK_AT.items():
            dark = g >= tg
            for o in self.objs_of(nm):
                o.hide_render = dark; o.keyframe_insert("hide_render", frame=f)
            for o in self.objs_of(nm + "_d"):
                o.hide_render = not dark; o.keyframe_insert("hide_render", frame=f)
        for nm in ("box2",):
            K.set_box_lid(nm, 0.0, frame=f)

    def lid_grip(self, t):
        """world point of the lit box's lid front edge (+ a little in front) for lid-open amount t."""
        th = math.radians(110 * t)
        return Vector((-0.03, 0.46 + 0.24 * math.cos(th) + 0.03, 1.385 + 0.24 * math.sin(th) + 0.015))

    def key_hand(self, g, f):
        t = lid_t(g)
        grip = self.lid_grip(t)
        arr = seg(g, 1430, 1442)                                # comes in from the right / back
        lv = seg(g, 1457, 1459)
        away = Vector((-0.65, 0.22, 0.16))                      # off-screen toward the right (-x), a little back and up
        pos = grip + away * ((1 - arr) + 0.35 * lv)
        self.hand.location = pos
        v = (away * -1.0)                                       # local +x points from the hand back along the forearm = toward 'away'
        self.hand.rotation_euler = (-1.0 * away).to_track_quat("-X", "Z").to_euler() if False else away.to_track_quat("X", "Z").to_euler()
        vis = 1430 <= g <= 1458
        for o in self.hand.children_recursive:
            o.hide_render = not vis; o.keyframe_insert("hide_render", frame=f)
        self.hand.keyframe_insert("location", frame=f); self.hand.keyframe_insert("rotation_euler", frame=f)

    def key_hero(self, g, f):
        t = lift_t(g)
        a = K.STATE["anim"]["hero"]["root"]
        a.location = (0.03 * t, 0.02 + 0.14 * t, 0.12 + 0.45 * t)
        a.rotation_euler = (math.radians(22 * t), 0, math.radians(-9 * t))
        a.keyframe_insert("location", frame=f); a.keyframe_insert("rotation_euler", frame=f)

'''
s = s[:a] + stage_m + s[b:]

# R init: extras after build
s = s.replace('''        if part == "R":
            self.lamp = bpy.data.objects["box_lamp"]''', '''        if part == "R":
            self.lamp = bpy.data.objects["box_lamp"]
            K.STATE["hero_z0"] = 0.12
            self.build_extras()''')

# bertillon leaves at the cut to the finger insert
s = s.replace("if g < 1411 else (60.0, 60.0, -60.0)", "if g < G_FING[0] else (60.0, 60.0, -60.0)")

# helpers from team 1 (ears + hand + closing jaws) placed before class Take
a = s.index("class Take(object):")
helpers = r'''SLIDE = [0.46]


def _calipers_body(k):
    """cast17's calipers with an adjustable sliding jaw (SLIDE[0]) so the jaws can close (copied from team 1 s01)."""
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
_orig_svg = sprites.sprite_svg


def slide_of(g):
    m = mode_of(g)
    if m == "ear":
        return lerp(0.30, 0.50, seg(g, G_EAR[0] + 2, G_EAR[0] + 12))
    if m == "finger":
        return lerp(0.30, 0.50, seg(g, G_FING[0] + 2, G_FING[0] + 12))
    return 0.50 - 0.04 * math.sin(g * 0.4)


def _svg(cast, pose, *a, **kw):
    t = (pose or {}).get("t", None)
    if t is not None and cast == "bertillon":
        SLIDE[0] = slide_of(int(round(t * 30)))
    return _orig_svg(cast, pose, *a, **kw)


sprites.sprite_svg = _svg


def theta_of(yaw):
    return math.radians(min(abs(yaw), 1.2) * 70.0)


def ears_svg(pose):
    """cartoon ears (the puppet has none) -> (underlay, overlay) SVG (team 1 s01)."""
    if not pose.get("ears17"):
        return "", ""
    yw = pose.get("yaw", 0.0); r = pose.get("head_roll", 0.0); dx = pose.get("head_dx", 0.0); dy = pose.get("head_dy", 0.0)
    ink, fill = "#3a2832", "#f4d4cb"
    c = math.cos(theta_of(yw)); prof = abs(yw) > 0.5

    def ear(x, sx, big):
        rx, ry = (0.19, 0.27) if big else (0.15, 0.25)
        return ('<g transform="translate(%.3f %.3f) scale(%d 1)"><ellipse cx="0" cy="0.02" rx="%.3f" ry="%.3f" fill="%s" stroke="%s" stroke-width="0.035"/>'
                '<path d="M-0.05,-0.13 C0.05,-0.15 0.11,0.02 0.03,0.14" fill="none" stroke="%s" stroke-width="0.03" stroke-linecap="round"/></g>' % (x, 0, sx, rx, ry, fill, ink, ink))
    under = ear(0.52 * c, 1, False) + ear(-0.52 * c, 1, False) if not prof else ear(0.52 * c, 1, False)
    over = ear(-0.52 * c, 1, True) if prof else ""
    wrap = lambda gg: '<g transform="rotate(%.2f %.3f %.3f) translate(%.3f %.3f)">%s</g>' % (r, dx, dy, dx, dy, gg) if gg else ""
    return wrap(under), wrap(over)


def hand_svg(an):
    """a visible forearm (lighter sleeve), white cuff and skin hand gripping the beam (team 1 s01)."""
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


'''
s = s[:a] + helpers + s[a:]

# mk_actor: dupont gets the ears underlay/overlay patch
s = s.replace('''    a.head_flip = True
    return a''', '''    a.head_flip = True
    if cast == "dupont":
        a.jobs = (lambda orig: (lambda px, frames=None, overlay=None: [dict(j, underlay=ears_svg(j["pose"])[0], overlay=ears_svg(j["pose"])[1]) for j in orig(px, frames, overlay)]))(a.jobs)
    return a''')

# main: frame partition
s = s.replace("gs = [g for g in parse(spec) if (FIRST <= g <= G_M_END if part == \"M\" else G_M_END < g <= LAST)]", "gs = [g for g in parse(spec) if FIRST <= g <= LAST and part_of(g) == part]")
open('shot.py', 'w').write(s)
