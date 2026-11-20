s = open('shot.py').read()

# ---------------- (b) head tighten kick on "ระดับนี้" (g1343)
s = s.replace("    loc = (loc[0] + 0.10 * math.sin(g * 0.11), loc[1], loc[2] + 0.025 * math.sin(g * 0.17))",
"""    loc = (loc[0] + 0.10 * math.sin(g * 0.11), loc[1], loc[2] + 0.025 * math.sin(g * 0.17))
    kick = max(0.0, 1.0 - abs(g - 1344.5) / 2.2)                      # 2-3 frame tighten on "ระดับนี้" (g1343): a small push-in
    loc = (loc[0] + (look[0] - loc[0]) * 0.16 * kick, loc[1] + (look[1] - loc[1]) * 0.16 * kick, loc[2] + (look[2] - loc[2]) * 0.16 * kick)""")

# ---------------- slide_of: wide jaws on the skull, squeeze on the kick
s = s.replace("    return 0.50 - 0.04 * math.sin(g * 0.4)", "    return 0.0 + 0.05 * max(0.0, 1.0 - abs(g - 1344.5) / 2.2) + 0.012 * math.sin(g * 0.5)      # head: jaws open to the skull's width, squeeze on the kick")

# ---------------- (c) head mode: jaws ACROSS the skull (anchor calipers_r on the brow line), ears drawn
s = s.replace('''            _, dp = pose_with("dupont_innocent", g, expr="worried", phase=1.0, sway=0.6)
            dp["legs"] = "stand"
            if m == "finger":''', '''            _, dp = pose_with("dupont_innocent", g, expr="worried", phase=1.0, sway=0.6)
            dp["legs"] = "stand"
            if m == "head":
                dp["ears17"] = True
            if m == "finger":''')
old_a = s.index('            if m == "head":\n                u0 = seg(g, FIRST, 1350')
old_b = s.index('            else:\n                an = self.anch[(da.name, f)]')
s = s[:old_a] + '''            if m == "head":
                u0 = seg(g, FIRST, 1350, lambda x: 1 - (1 - x) ** 2)            # calipers rise from low and close across the skull by g1350, then hold
                bp["prop_r"] = dict(bp["prop_r"], scale=1.35, angle=0)
                bp["yaw"] = 0.35
                hw = Vector((0.70, 2.08, K.HEAD_Z["chair"] + 0.05 - 0.55 * (1 - u0)))      # jaw midpoint: brow level of the head
                hw.x += 0.35 * (1 - u0)
                tgt = actors.world_to_local(ba, self.cam, tuple(hw), f)
                bp2 = cast17.hand_for_anchor("bertillon", bp, "r", "calipers_r", tgt)
                ba.pose(f, bp2, camera=self.cam)
                continue
''' + s[old_b:]
# the generic 'else' branch below stays for finger/ear; remove the now-dead second 'ba.pose' for head: it is after the if/else, keep for others
s = s.replace("            ba.pose(f, bp, hands=hands, camera=self.cam)\n        self.sprites_group(ba, gs, 320, 512, hand_overlay=True)", "            ba.pose(f, bp, hands=hands, camera=self.cam)\n        self.sprites_group(ba, gs, 320, 512, hand_overlay=True)")
s = s.replace('"finger": (-0.15, 2.0)', '"finger": (-0.15, 2.0)').replace('"head": (bpos[0], bpos[1])', '"head": (0.58, 1.84)')

# ---------------- finger insert: camera on the hand (re-keyed from dupont's drawn hand), >= 40 % of the frame width
s = s.replace("        self.sprites_group(da, gs, 320, 512)\n", """        self.sprites_group(da, gs, 320, 512)
        for g in gs:
            if mode_of(g) != "finger":
                continue
            f = g - FIRST + 1
            self.scene.frame_set(f)
            hw = actors.local_to_world(da, self.anch[(da.name, f)]["hand_l"], f, camera=self.cam)
            u = seg(g, G_FING[0], G_FING[1] + 1, lambda x: 0.3 * sine(x) + 0.7 * x)
            off = Vector((lerp(0.62, 0.46, u), lerp(-0.62, -0.50, u), lerp(0.18, 0.10, u)))
            camrig.key_camera(f, hw + off, hw + Vector((-0.02, 0.0, 0.0)), cam=self.cam, lens=LENS, interp="LINEAR", easing="AUTO")
""")

# ---------------- (d) boxes: six boxes of the same size in a grid, hero scaled to match
a = s.index('DARK_AT = {'); b = s.index('LAMP_DB, LAMP_CARD')
s = s[:a] + '''BS = 0.7                                                      # the hero box is scaled to the size of the others
BW, BD, BH = 0.34 * BS, 0.24 * BS, 0.28 * BS
SLOT = {"hero": (-0.28, -0.14), "bxA": (0.0, -0.14), "bxB": (0.28, -0.14), "bxC": (-0.28, -0.38), "bxD": (0.0, -0.38), "bxE": (0.28, -0.38)}
DARK_AT = {"bxA": 1422, "bxB": 1426, "bxC": 1430, "bxD": 1434, "bxE": 1438}      # hard switch-off, one every 4 frames; the hero box stays lit
EXTRA = {k: (SLOT[k], BW, BD, BH, 5 + i) for i, k in enumerate(("bxA", "bxB", "bxC", "bxD", "bxE"))}


''' + s[b:]
a = s.index("    def build_extras(self):"); b = s.index("        B = K.Batch(21)")
s = s[:a] + '''    def build_extras(self):
        slide = K.STATE["anim"]["big"]["slide"]
        self.twin = {}
        for nm in ("box2",):                                    # the old second box and the ledger riser go away
            for o in K.STATE["anim"][nm]["objs"]:
                o.hide_render = True
        for o in bpy.data.objects:
            if o.name.startswith("riser"):
                o.hide_render = True
        root = K.STATE["anim"]["box"]["root"]
        root.scale = (BS, BS, BS)
        root.location = (SLOT["hero"][0], SLOT["hero"][1], -0.175)
        root.rotation_euler = (0, 0, 0)
        hero = K.STATE["anim"]["hero"]["root"]
        hero.scale = (1.0 / BS,) * 3
        for nm, (xy, w, d, h, seed) in EXTRA.items():
            K.card_box(nm, (xy[0], xy[1], -0.175), rot_z=0, w=w, d=d, h=h, lid=0.0, cards=8, seed=seed, parent=slide, mat="box_ochre", lining="walnut")
            K.card_box(nm + "_d", (xy[0], xy[1], -0.175), rot_z=0, w=w, d=d, h=h, lid=0.0, cards=8, seed=seed, parent=slide, mat="dark", lining="dark")
        K.point((0.2, 1.0, 1.9), color=(1.0, 0.82, 0.55), watts=45, radius=0.1, name="box_fill", flicker=False)
''' + s[b:]
# key_boxes: no box2
s = s.replace('        for nm in ("box2",):\n            K.set_box_lid(nm, 0.0, frame=f)\n', '')
# lid grip on the scaled hero box
a = s.index("    def lid_grip(self, t):"); b = s.index("    def key_hand(self, g, f):")
s = s[:a] + '''    def lid_grip(self, t):
        """world point of the hero box's lid front edge (+ a little in front) for lid-open amount t."""
        th = math.radians(110 * t)
        px, py, pz = 0.15 + SLOT["hero"][0], 0.78 + SLOT["hero"][1], 1.2 - 0.175
        hy, hz = py - BD / 2, pz + BH
        return Vector((px, hy + BD * math.cos(th) + 0.03, hz + BD * math.sin(th) + 0.015))

''' + s[b:]
# hero lift in the scaled box space
a = s.index("    def key_hero(self, g, f):"); b = s.index("    # ---- part R: bertillon at the drawer")
s = s[:a] + '''    def key_hero(self, g, f):
        t = lift_t(g)
        a = K.STATE["anim"]["hero"]["root"]
        a.location = (0.03 * t / BS, (0.02 + 0.14 * t) / BS, (0.12 + 0.45 * t) / BS)         # box-local units (the box root is scaled by BS)
        a.rotation_euler = (math.radians(22 * t), 0, math.radians(-9 * t))
        a.keyframe_insert("location", frame=f); a.keyframe_insert("rotation_euler", frame=f)

''' + s[b:]
# hero starts hidden below the rim: world top must be under BH
s = s.replace('K.STATE["hero_z0"] = 0.12', 'K.STATE["hero_z0"] = 0.12')

# ---------------- (6) drawer yank: stronger lean, shorter step (beard margin)
s = s.replace("ba.place(f, (-0.47, 1.12 + 0.36 * t, 0.0)", "ba.place(f, (-0.47, 1.12 + 0.22 * t, 0.0)")
s = s.replace('bp["lean"] = bp.get("lean", 0) - 9 * min(1.0, t * 1.5)', 'bp["lean"] = bp.get("lean", 0) - 16 * min(1.0, t * 1.5) + 2.5 * math.sin(g * 0.8) * (1.0 if g < 1406 else 0.0)')
open('shot.py', 'w').write(s)
