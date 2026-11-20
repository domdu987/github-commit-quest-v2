s = open('shot.py').read()

# ---------------- finger: dupont raises one finger UP, jaws close on it
s = s.replace('''                dp["arm_l"] = dict(hand=(lerp(-0.74, -0.88, u), lerp(0.60, 0.30, u)), bend=0.4, shape="point", sharp=1.0, layer="front")''',
              '''                dp["arm_l"] = dict(hand=(lerp(-0.74, -0.86, u), lerp(0.60, 0.34, u)), bend=0.4, shape="ball", layer="front")''')
a = s.index("def finger_dir(an):"); b = s.index("def hand_svg(an):")
s = s[:a] + '''FING_LEN = 0.40


def finger_tip(an, ln=0.40):
    """local point on the raised finger, ln up from the hand anchor."""
    return an["hand_l"][0], an["hand_l"][1] - ln


def finger_svg(an):
    """one distinct extended index finger pointing UP from the fist (skin, inked)."""
    hx, hy = an["hand_l"]; tx, ty = hx, hy - FING_LEN
    return ('<g><path d="M%.3f,%.3f L%.3f,%.3f" stroke="#3a2832" stroke-width="0.14" stroke-linecap="round" fill="none"/>'
            '<path d="M%.3f,%.3f L%.3f,%.3f" stroke="#f4d4cb" stroke-width="0.10" stroke-linecap="round" fill="none"/></g>' % (hx, hy - 0.03, tx, ty, hx, hy - 0.03, tx, ty))


''' + s[b:]
s = s.replace("        return lerp(0.30, 0.50, seg(g, G_FING[0] + 2, G_FING[0] + 12))", "        return lerp(0.46, 0.60, seg(g, G_FING[0] + 3, G_FING[0] + 12))")

# camera + bertillon placement for the finger frames
a = s.index("        for g in gs:\n            if mode_of(g) != \"finger\":\n                continue\n            f = g - FIRST + 1")
b = s.index("        for g in gs:                                              # bertillon: jaws pinned")
s = s[:a] + '''        for g in gs:
            if mode_of(g) != "finger":
                continue
            f = g - FIRST + 1
            self.scene.frame_set(f)
            an = self.anch[(da.name, f)]
            u = seg(g, G_FING[0], G_FING[1] + 1, lambda x: 0.3 * sine(x) + 0.7 * x)
            for _ in range(2):                                         # the card turns with the camera: two passes
                hw = actors.local_to_world(da, (an["hand_l"][0], an["hand_l"][1] - 0.20), f, camera=self.cam)
                off = Vector((lerp(0.34, 0.26, u), lerp(-0.70, -0.52, u), lerp(0.14, 0.10, u)))
                loc = hw + off
                look = hw + Vector((0.0, 0.0, 0.03))
                camrig.key_camera(f, loc, look, cam=self.cam, lens=LENS, interp="LINEAR", easing="AUTO")
                self.scene.frame_set(f)
            fwd = (look - loc).normalized(); rt = fwd.cross(Vector((0, 0, 1))).normalized()
            c = Vector((loc.x - hw.x, loc.y - hw.y, 0)).normalized()
            bpos = Vector((hw.x, hw.y, 0)) + c * 0.45 - rt * 0.40       # Bertillon stands between the lens and dupont's hand, to the left
            ba.place(f, (bpos.x, bpos.y, 0.0), scale=bsc)
''' + s[b:]
# bertillon finger target: far end of the beam beside the finger
s = s.replace('''                    hx, hy = finger_tip(an, 0.20)
                    k = 1.0 - seg(g, G_FING[0], G_FING[0] + 7)
                    loc_t = (hx - 0.5 * k, hy + 0.9 * k + 0.012 * math.sin(g * 0.9))
                    ang, psc = -4, 0.9''', '''                    fx, fy = an["hand_l"]
                    k = 1.0 - seg(g, G_FING[0], G_FING[0] + 7)
                    gap = (0.775 - slide_of(g)) * 0.9
                    loc_t = (fx + 0.045 * 0.9 + 0.5 * gap - 0.5 * k, fy - 0.42 + 0.9 * k + 0.008 * math.sin(g * 0.9))
                    ang, psc = 0, 0.9''')

# ---------------- dark twin material + fill light keys
s = s.replace('''        K.point((0.2, 1.0, 1.9), color=(1.0, 0.82, 0.55), watts=45, radius=0.1, name="box_fill", flicker=False)''', '''        self.fill = K.point((0.2, 1.0, 1.9), color=(1.0, 0.82, 0.55), watts=45, radius=0.1, name="box_fill", flicker=False)
        tm = bpy.data.materials.new("twin_dark")                  # unlit near-black emission: the switched-off boxes are <= 35 luma whatever the lamps do
        tm.use_nodes = True; nt = tm.node_tree; nt.nodes.clear()
        em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (0.045, 0.035, 0.05, 1.0); em.inputs["Strength"].default_value = 1.0
        out = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], out.inputs[0])
        for nm in list(DARK_AT) + ["box2"]:
            if nm + "_d" not in K.STATE["anim"]:
                continue
            for o in K.STATE["anim"][nm + "_d"]["objs"]:
                for i, m in enumerate(o.data.materials):
                    if m is not None and m.name.startswith("dark"):
                        o.data.materials[i] = tm''')
s = s.replace('''                self.key_boxes(g, f)''', '''                self.key_boxes(g, f)
                self.fill.data.energy = (72.0 if 1420 <= g <= 1458 else 45.0) * K.LAMP_W * K.STATE["P"]["lamp_k"]
                self.fill.data.keyframe_insert("energy", frame=f)''')

# ---------------- card shot: no pull-out, slow push-in, shorter lift (card just clears the rim)
a = s.index("    e = seg(g, G_CARD, G_CARD + SNAP, lambda x: ease_peak(x, 2.0))           # card shot")
b = s.index("# measuring-room inserts")
s = s[:a] + '''    u = seg(g, G_CARD, 1516, lambda x: 0.25 * sine(x) + 0.75 * x)            # card shot: slow push-in from the box-beat framing to the close card framing
    loc, look = vlerp(R_BX1[0], R_CHE[0], u), vlerp(R_BX1[1], R_CHE[1], u)
    return (loc[0] + 0.012 * math.sin(g * 0.14), loc[1], loc[2]), look


''' + s[b:]
s = s.replace("R_CH1 = ((0.20, 1.32, 1.82), (-0.15, 0.68, 1.50))           # push-in ~9 %/s + slide", "R_CHE = ((0.0, 1.14, 1.62), (-0.10, 0.72, 1.44))          # end of the card push: card >= 70 % of the frame width, box rim in frame")
s = s.replace("a.location = (0.03 * t / BS, (0.02 + 0.14 * t) / BS, (0.12 + 0.45 * t) / BS)", "a.location = (0.03 * t / BS, (0.02 + 0.08 * t) / BS, (0.12 + 0.19 * t) / BS)")
open('shot.py', 'w').write(s)

p = open('post.py').read()
p = p.replace("    if g >= 1476:                                   # card shot", '''    if g >= 1476:                                   # warm pool on the card + box, surroundings -18 % (director round 3)
        hh, ww = im.shape[:2]
        yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
        r = np.hypot((xx - 0.5 * ww) / (0.55 * ww), (yy - 0.42 * hh) / (0.40 * hh))
        pool = np.clip(1.0 - r, 0.0, 1.0); pool = pool * pool * (3 - 2 * pool)
        k2 = 1.0 - 0.18 * (1.0 - pool) * min(1.0, (g - 1476) / 8.0)
        warm = np.stack([1.0 - 0.05 * pool, 1.0 + 0.0 * pool, 1.0 + 0.06 * pool], -1)[..., ::-1] if False else np.stack([1.0 + 0.06 * pool, 1.0 + 0.0 * pool, 1.0 - 0.05 * pool], -1)   # BGR: warm = less blue, more red
        im = np.clip(im.astype(np.float32) * k2[..., None] * warm, 0, 255).astype(np.uint8)
    if g >= 1476:                                   # card shot''', 1)
open('post.py', 'w').write(p)
