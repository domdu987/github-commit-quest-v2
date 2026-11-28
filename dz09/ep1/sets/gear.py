"""gear.py -- the equipment wall behind the rear bench of the rescue cab: a locker 3.3 D wide, 1.8 D high, 1 D deep
behind a roll shutter, two tiers of rescue gear told apart by SHAPE and pictogram (no brand, no logo); the shelf-edge
tape labels are plain Thai nouns.  Four things come out, the rest stays:

    G = gear.build(cab_root, coll)       G["items"] = {"cutter", "crowbar", "radio", "pouch"} -> root objects
    gear.take(name, taken=True)          hide (or put back) one of the four; its clips / hook / cradle stay, empty
    gear.shutter(t)                      0 closed .. 1 open (the slats run up into the roll housing); the strip lamp follows
    gear.lamp(on, energy)                the locker's own strip lamp
Stays behind (continuity sheet): the big orange trauma bag, defibrillator case, oxygen cylinder, folded stretcher, rope,
two helmets, extinguisher, the flare box, the charger with its slot EMPTY (there is no spare battery).
"""
import math, random
import bpy
from mathutils import Vector
import core as K
from core import V, kit, X
import cab as CB

_S = {}
LABELS = dict(rope="เชือก", oxygen="ออกซิเจน", firstaid="ปฐมพยาบาล", flare="พลุสัญญาณ", battery="แบตเตอรี่", ext="ถังดับเพลิง", helmet="หมวกนิรภัย", stretcher="เปลสนาม")


def _picto(name, kind, bg, fg=(245, 245, 240)):
    def fn(d, im):
        W, H = im.size
        d.rounded_rectangle((0, 0, W - 1, H - 1), 14, fill=bg + (255,))
        cx, cy = W / 2, H / 2
        if kind == "cross":
            d.rectangle((cx - 16, cy - 50, cx + 16, cy + 50), fill=fg + (255,)); d.rectangle((cx - 50, cy - 16, cx + 50, cy + 16), fill=fg + (255,))
        elif kind == "heart":                     # heart with a bolt: the defibrillator
            d.ellipse((cx - 52, cy - 46, cx, cy + 6), fill=fg + (255,)); d.ellipse((cx, cy - 46, cx + 52, cy + 6), fill=fg + (255,))
            d.polygon([(cx - 50, cy - 8), (cx + 50, cy - 8), (cx, cy + 56)], fill=fg + (255,))
            d.polygon([(cx + 5, cy - 14), (cx - 13, cy + 10), (cx - 1, cy + 10), (cx - 6, cy + 32), (cx + 14, cy + 4), (cx + 2, cy + 4)], fill=bg + (255,))
        elif kind == "flame":
            d.polygon([(cx, cy - 56), (cx + 34, cy + 6), (cx + 26, cy + 44), (cx, cy + 56), (cx - 26, cy + 44), (cx - 34, cy + 6), (cx - 12, cy - 10)], fill=fg + (255,))
            d.polygon([(cx, cy - 6), (cx + 14, cy + 26), (cx, cy + 46), (cx - 14, cy + 26)], fill=bg + (255,))
        elif kind == "battery":
            d.rectangle((cx - 50, cy - 26, cx + 42, cy + 26), outline=fg + (255,), width=8); d.rectangle((cx + 42, cy - 10, cx + 54, cy + 10), fill=fg + (255,))
            d.polygon([(cx + 2, cy - 20), (cx - 18, cy + 4), (cx - 4, cy + 4), (cx - 10, cy + 20), (cx + 12, cy - 4), (cx - 2, cy - 4)], fill=fg + (255,))
        elif kind == "o2":
            f = K.font(84); bb = d.textbbox((0, 0), "O", font=f)
            d.text((cx - 44 - (bb[0] + bb[2]) / 2 + 20, cy - (bb[1] + bb[3]) / 2 - 4), "O", font=f, fill=fg + (255,))
            f2 = K.font(46); d.text((cx + 14, cy + 2), "2", font=f2, fill=fg + (255,))
    return K.draw_tex("picto_" + name, (160, 160), fn)


def _label(name, c, root, x, z, y):
    import cab
    m = K.image_mat("glabel_" + name, cab._label_tex("g_" + name, LABELS[name], size=(320, 96), fs=58, tilt=random.Random(name).uniform(-2, 2)), rough=0.8, alpha=True)
    w = 0.30 + 0.022 * len(LABELS[name])
    return K.quad("gear_label_" + name, w, w * 0.30, (x, y, z), "+Y", m, root, c=c)


def build(root, c):
    F = CB.F; Yf = CB.Y0                         # the wall's face
    Z0, Z1 = F + 1.45, F + 3.25
    ZS = F + 2.32                                # the shelf between the tiers
    D = 1.0; HWd = 1.65
    st = X.m_steel("ep1_locker_steel", "#7b8087", 0.3); dk = K.simple("cab_trim_dark", "#141518", 0.7)
    inn = K.simple("locker_inner", "#3a3d44", 0.6, 0.5)
    ch = V.mat("chrome"); pl = V.mat("plastic")
    P = []
    add = P.append
    # carcass: back, sides, floor, shelf, top; the wall around the opening down to the cab floor and up to the roof
    add(K.box("gear_back", (2 * HWd + 0.2, 0.05, Z1 - Z0 + 0.2), (0, Yf - D, (Z0 + Z1) / 2), inn, root, c=c))
    for sx in (-1, 1):
        add(K.box("gear_side", (0.06, D, Z1 - Z0 + 0.2), (sx * (HWd + 0.03), Yf - D / 2, (Z0 + Z1) / 2), inn, root, c=c))
        add(K.box("gear_jamb", (CB.HW - HWd + 0.12, 0.10, CB.ZR - F), (sx * (CB.HW + HWd + 0.12) / 2, Yf - 0.05, (F + CB.ZR) / 2), dk, root, c=c))
        add(K.box("gear_track", (0.05, 0.06, Z1 - Z0), (sx * (HWd - 0.01), Yf + 0.01, (Z0 + Z1) / 2), st, root, c=c))
    add(K.box("gear_floor", (2 * HWd, D, 0.05), (0, Yf - D / 2, Z0 - 0.025), st, root, c=c))
    add(K.box("gear_shelf", (2 * HWd - 0.32, D - 0.08, 0.04), (0.16, Yf - D / 2 - 0.04, ZS), st, root, c=c))
    add(K.box("gear_shelf_lip", (2 * HWd - 0.32, 0.03, 0.09), (0.16, Yf - 0.03, ZS + 0.02), st, root, c=c))
    add(K.box("gear_sill", (2 * CB.HW, 0.10, Z0 - F), (0, Yf - 0.05, (F + Z0) / 2), dk, root, c=c))
    add(K.box("gear_housing", (2 * HWd + 0.2, 0.30, CB.ZR - Z1), (0, Yf - 0.12, (Z1 + CB.ZR) / 2), dk, root, bevel=0.03, c=c))
    # ---- stays: left column, the folded stretcher standing (two poles, orange canvas, straps)
    xs = -HWd + 0.17
    for dy in (-0.10, 0.10):
        add(K.cyl("gear_str_pole", 0.03, Z1 - Z0 - 0.1, (xs, Yf - 0.45 + dy, (Z0 + Z1) / 2), st, root, c=c, segs=8))
    add(K.box("gear_str_canvas", (0.20, 0.30, Z1 - Z0 - 0.45), (xs, Yf - 0.45, (Z0 + Z1) / 2), K.simple("stretcher_orange", "#d2571c", 0.8), root, bevel=0.06, c=c))
    for z in (Z0 + 0.45, Z1 - 0.45):
        add(K.box("gear_str_strap", (0.215, 0.315, 0.06), (xs, Yf - 0.45, z), pl, root, c=c))
    # ---- lower tier: trauma bag, defibrillator, oxygen, charger, flare box
    bag = K.simple("medic_orange2", "#e0611f", 0.6)
    bx = -0.62
    add(K.box("gear_bag", (1.10, 0.62, 0.70), (bx, Yf - 0.60, Z0 + 0.35), bag, root, bevel=0.12, c=c))
    add(K.box("gear_bag_flap", (1.12, 0.64, 0.10), (bx, Yf - 0.60, Z0 + 0.69), K.simple("medic_orange_dk", "#b84a17", 0.6), root, bevel=0.04, c=c))
    add(K.box("gear_bag_band", (1.11, 0.02, 0.07), (bx, Yf - 0.285, Z0 + 0.30), K.simple("refl_grey", "#c9cdd2", 0.3, 0.3), root, c=c))
    add(K.quad("gear_bag_cross", 0.30, 0.30, (bx, Yf - 0.284, Z0 + 0.50), "+Y", K.image_mat("picto_cross_w", _picto("cross_w", "cross", (250, 250, 245), (200, 40, 30)), rough=0.6), root, c=c))
    add(K.tube("gear_bag_handle", [(bx - 0.2, Yf - 0.60, Z0 + 0.74), (bx - 0.12, Yf - 0.60, Z0 + 0.84), (bx + 0.12, Yf - 0.60, Z0 + 0.84), (bx + 0.2, Yf - 0.60, Z0 + 0.74)], 0.022, pl, root, c=c, segs=6))
    dx = 0.30
    add(K.box("gear_defib", (0.56, 0.36, 0.62), (dx, Yf - 0.50, Z0 + 0.31), K.simple("defib_green", "#7fc21e", 0.45, 0.0, 0.3), root, bevel=0.07, c=c))
    add(K.quad("gear_defib_p", 0.34, 0.34, (dx, Yf - 0.318, Z0 + 0.33), "+Y", K.image_mat("picto_heart", _picto("heart", "heart", (127, 194, 30)), rough=0.5), root, c=c))
    add(K.tube("gear_defib_handle", [(dx - 0.14, Yf - 0.50, Z0 + 0.62), (dx - 0.08, Yf - 0.50, Z0 + 0.70), (dx + 0.08, Yf - 0.50, Z0 + 0.70), (dx + 0.14, Yf - 0.50, Z0 + 0.62)], 0.02, pl, root, c=c, segs=6))
    ox = 0.82
    add(K.lathe("gear_o2", [(0.001, 0.0), (0.13, 0.0), (0.13, 0.58), (0.09, 0.70), (0.04, 0.74), (0.04, 0.80), (0.001, 0.80)], K.simple("o2_green", "#1f7a46", 0.3, 0.2, 0.4), root, loc=(ox, Yf - 0.55, Z0), c=c, segs=14))
    add(K.lathe("gear_o2_shoulder", [(0.132, 0.50), (0.132, 0.585), (0.092, 0.705)], K.simple("o2_white", "#e6e6e0", 0.3), root, loc=(ox, Yf - 0.55, Z0), c=c, segs=14, cap=False))
    add(K.cyl("gear_o2_gauge", 0.06, 0.03, (ox + 0.08, Yf - 0.50, Z0 + 0.80), ch, root, rot=(math.pi / 2, 0, 0), c=c))
    add(K.box("gear_o2_strap", (0.30, 0.02, 0.05), (ox, Yf - 0.415, Z0 + 0.36), pl, root, c=c))
    add(K.quad("gear_o2_p", 0.16, 0.16, (ox, Yf - 0.416, Z0 + 0.22), "+Y", K.image_mat("picto_o2", _picto("o2", "o2", (31, 122, 70)), rough=0.5), root, c=c))
    cx = 1.20
    add(K.box("gear_charger", (0.44, 0.50, 0.30), (cx, Yf - 0.48, Z0 + 0.15), K.simple("charger", "#25272c", 0.5), root, bevel=0.03, c=c))
    add(K.box("gear_charger_slot", (0.20, 0.30, 0.06), (cx, Yf - 0.48, Z0 + 0.29), K.simple("slot_black", "#020203", 0.9), root, c=c))          # the EMPTY slot
    for k in range(2):
        add(K.box("gear_charger_contact", (0.03, 0.05, 0.02), (cx - 0.05 + k * 0.10, Yf - 0.56, Z0 + 0.31), ch, root, c=c))
    add(K.box("gear_charger_led", (0.03, 0.012, 0.03), (cx + 0.15, Yf - 0.228, Z0 + 0.20), K.emit("gear_charger_led", (1.0, 0.6, 0.05), 3.0), root, c=c))
    add(K.quad("gear_charger_p", 0.20, 0.20, (cx - 0.06, Yf - 0.228, Z0 + 0.15), "+Y", K.image_mat("picto_batt", _picto("batt", "battery", (37, 39, 44)), rough=0.5), root, c=c))
    add(K.tube("gear_charger_cord", [(cx + 0.18, Yf - 0.70, Z0 + 0.1), (cx + 0.3, Yf - 0.85, Z0 + 0.05), (cx + 0.3, Yf - 0.95, Z0 + 0.5)], 0.015, pl, root, c=c, segs=5))
    fx = 1.20
    add(K.box("gear_flarebox", (0.50, 0.30, 0.34), (fx, Yf - 0.42, Z0 + 0.50), K.simple("flare_red", "#b3261c", 0.5), root, bevel=0.02, c=c))
    add(K.quad("gear_flare_p", 0.19, 0.19, (fx - 0.12, Yf - 0.268, Z0 + 0.555), "+Y", K.image_mat("picto_flame", _picto("flame", "flame", (179, 38, 28)), rough=0.5), root, c=c))
    import cab as _cab
    fl_m = K.image_mat("glabel_flare", _cab._label_tex("g_flare", LABELS["flare"], size=(320, 96), fs=58, tilt=1.5), rough=0.8, alpha=True)
    add(K.quad("gear_label_flare", 0.42, 0.126, (fx, Yf - 0.267, Z0 + 0.397), "+Y", fl_m, root, c=c))
    flares = []
    for k in range(5):
        f = K.cyl(f"gear_flare_{k}", 0.035, 0.42, (fx - 0.16 + k * 0.08, Yf - 0.44, Z0 + 0.78), K.simple("flare_tube", "#c8281e", 0.5), root, c=c, segs=8)
        cp = K.cyl(f"gear_flare_cap_{k}", 0.038, 0.06, (fx - 0.16 + k * 0.08, Yf - 0.44, Z0 + 1.0 - 0.01), K.simple("flare_cap", "#e8e6dc", 0.5), root, c=c, segs=8)
        add(f); add(cp); flares.append((f, cp))
    # ---- upper tier: two helmets, rope coil, extinguisher
    for k, (hx, col) in enumerate(((-1.0, "#d9d9d4"), (-0.42, "#e2b21a"))):
        add(K.lathe(f"gear_helmet_{k}", [(0.001, 0.36), (0.20, 0.33), (0.30, 0.18), (0.32, 0.02), (0.36, 0.0), (0.30, 0.0)], K.simple(f"helmet_{k}", col, 0.3, 0.0, 0.5), root, loc=(hx, Yf - 0.50, ZS + 0.03), c=c, segs=16))
        add(K.box(f"gear_helmet_lamp_{k}", (0.12, 0.08, 0.08), (hx, Yf - 0.20, ZS + 0.22), pl, root, bevel=0.02, c=c))
        add(K.box(f"gear_helmet_band_{k}", (0.50, 0.02, 0.05), (hx, Yf - 0.195, ZS + 0.11), K.simple("refl_grey", "#c9cdd2", 0.3, 0.3), root, c=c))
    rx = 0.22
    rope_m = K.simple("rope", "#b9a877", 0.9)
    for k in range(6):
        add(K.lathe(f"gear_rope_{k}", [(0.25, -0.03), (0.29, 0.0), (0.25, 0.03), (0.21, 0.0)], rope_m, root, loc=(rx, Yf - 0.62 + k * 0.055, ZS + 0.42), c=c, segs=20, axis="Y", cap=False))
    add(K.cyl("gear_rope_peg", 0.03, 0.5, (rx, Yf - 0.70, ZS + 0.62), st, root, rot=(math.pi / 2, 0, 0), c=c, segs=8))
    add(K.tube("gear_carabiner", [(rx + 0.2, Yf - 0.38, ZS + 0.30), (rx + 0.26, Yf - 0.38, ZS + 0.20), (rx + 0.2, Yf - 0.38, ZS + 0.10), (rx + 0.14, Yf - 0.38, ZS + 0.20), (rx + 0.2, Yf - 0.38, ZS + 0.30)], 0.014, ch, root, c=c, segs=5))
    ex = 1.38
    red = K.simple("ext_red", "#c21f1a", 0.3, 0.1, 0.5)
    add(K.lathe("gear_ext", [(0.001, 0.0), (0.14, 0.0), (0.14, 0.54), (0.10, 0.63), (0.04, 0.66), (0.04, 0.72), (0.001, 0.72)], red, root, loc=(ex, Yf - 0.50, ZS + 0.02), c=c, segs=14))
    add(K.box("gear_ext_lever", (0.05, 0.22, 0.03), (ex, Yf - 0.44, ZS + 0.77), pl, root, c=c))
    add(K.tube("gear_ext_hose", [(ex + 0.05, Yf - 0.50, ZS + 0.70), (ex + 0.17, Yf - 0.50, ZS + 0.62), (ex + 0.17, Yf - 0.50, ZS + 0.25)], 0.022, pl, root, c=c, segs=6))
    add(K.box("gear_ext_band", (0.30, 0.02, 0.05), (ex, Yf - 0.355, ZS + 0.34), st, root, c=c))
    # labels on the shelf lip and the floor edge
    lab = [("helmet", -0.72, ZS + 0.02), ("rope", 0.22, ZS + 0.02), ("ext", 1.30, ZS + 0.02), ("stretcher", -1.42, Z0 + 0.0)]
    for nm, x, z in lab: add(_label(nm, c, root, x, z if nm != "stretcher" else Z0 - 0.07, Yf - 0.012 if nm != "stretcher" else Yf + 0.003))
    for nm, x in (("firstaid", -0.62), ("oxygen", 0.60), ("battery", 1.22)):
        add(_label(nm, c, root, x, Z0 - 0.07, Yf + 0.003))
    # ---- the four that leave: each a root with its own parts; its holder stays
    items = {}
    # (a) the cutter: the set's 3D tool, lying on the lower tier in front of the bag, D-handle to the right
    cu = V.cutter("gear_cutter3d", c, bars=3)
    cu.parent = root; cu.location = (bx + 0.05, Yf - 0.16, Z0 + 0.30); cu.rotation_euler = (0, 0, math.pi / 2)
    for o in K.tree(cu):
        if o.type == "MESH": o.pass_index = 4
    add(K.box("gear_cutter_cradle", (0.10, 0.20, 0.10), (bx - 0.30, Yf - 0.16, Z0 + 0.05), dk, root, c=c)); add(K.box("gear_cutter_cradle", (0.10, 0.20, 0.10), (bx + 0.55, Yf - 0.16, Z0 + 0.05), dk, root, c=c))
    items["cutter"] = cu
    # (b) the crowbar: in two spring clips across the top of the upper tier
    cb = K.empty("gear_crowbar", (0.45, Yf - 0.14, Z1 - 0.20), root, c)
    cbm = K.simple("crowbar_red2", "#a4231e", 0.35, 0.6)
    K.tube("gear_crowbar_bar", [(-0.86, 0, 0), (0.70, 0, 0), (0.80, 0, -0.03), (0.86, 0, -0.10), (0.84, 0, -0.17)], 0.032, cbm, cb, c=c, segs=8)
    K.box("gear_crowbar_chisel", (0.16, 0.07, 0.022), (-0.92, 0, 0), K.simple("crowbar_tip", "#8c9097", 0.25, 1.0), cb, c=c, rot=(0, 0.12, 0))
    for x in (-0.25, 1.05):
        add(K.box("gear_clip", (0.05, 0.10, 0.12), (x, Yf - 0.14, Z1 - 0.20), ch, root, c=c)); add(K.box("gear_clip_back", (0.08, 0.14, 0.03), (x, Yf - 0.14, Z1 - 0.12), ch, root, c=c))
    items["crowbar"] = cb
    # (c) the chest radio: in a charging cradle on the right jamb, LED on, a volume knob on top
    rd = K.empty("gear_radio", (HWd - 0.12, Yf - 0.12, ZS + 0.62 - 0.9 + 0.55), root, c)
    K.box("gear_radio_body", (0.17, 0.10, 0.34), (0, 0, 0), K.simple("radio_black", "#16171a", 0.45), rd, bevel=0.02, c=c)
    K.cyl("gear_radio_ant", 0.012, 0.34, (-0.05, 0, 0.33), pl, rd, c=c, segs=6)
    K.cyl("gear_radio_knob", 0.025, 0.05, (0.04, 0, 0.19), pl, rd, c=c, segs=8)
    K.box("gear_radio_grille", (0.12, 0.012, 0.12), (0, 0.052, 0.04), K.simple("radio_grille", "#34363b", 0.6, 0.4), rd, c=c)
    K.box("gear_radio_led", (0.02, 0.012, 0.02), (0.05, 0.052, 0.14), K.emit("gear_radio_led", (1.0, 0.15, 0.08), 6.0), rd, c=c)
    add(K.box("gear_radio_cradle", (0.22, 0.14, 0.12), (HWd - 0.12, Yf - 0.12, ZS + 0.05), dk, root, bevel=0.02, c=c))
    rd.location = (HWd - 0.12, Yf - 0.12, ZS + 0.05 + 0.20)
    rd.location.x = 0.80; add(K.box("gear_radio_cradle2", (0.22, 0.14, 0.12), (0.80, Yf - 0.12, ZS + 0.07), dk, root, bevel=0.02, c=c)); rd.location.z = ZS + 0.07 + 0.21
    items["radio"] = rd
    # (d) the small red first-aid pouch: on a hook at the right of the upper tier
    po = K.empty("gear_pouch", (0.80, Yf - 0.10, Z1 - 0.55), root, c)
    po.location = (-0.02, Yf - 0.10, Z0 + 0.98)
    K.box("gear_pouch_body", (0.34, 0.14, 0.26), (0, 0, 0), K.simple("pouch_red", "#c2231c", 0.6), po, bevel=0.05, c=c)
    K.quad("gear_pouch_cross", 0.15, 0.15, (0, 0.072, 0.0), "+Y", K.image_mat("picto_cross_r", _picto("cross_r", "cross", (194, 35, 28)), rough=0.6), po, c=c)
    K.tube("gear_pouch_loop", [(-0.06, 0, 0.12), (-0.04, 0, 0.22), (0.04, 0, 0.22), (0.06, 0, 0.12)], 0.012, pl, po, c=c, segs=5)
    add(K.tube("gear_pouch_hook", [(-0.02, Yf - 0.10, Z0 + 0.98 + 0.26), (-0.02, Yf - 0.10, Z0 + 0.98 + 0.20), (-0.02, Yf - 0.05, Z0 + 0.98 + 0.18)], 0.012, ch, root, c=c, segs=5))
    po.location = (0.30, Yf - 0.08, Z0 + 0.78)                     # it hangs on the defibrillator's handle hook, in front of it
    P[-1].location = Vector((0.32, 0.02, -0.20))
    items["pouch"] = po
    # ---- roll shutter (slats), its lift handle, the strip lamp under the housing
    sh = K.empty("gear_shutter", (0, Yf + 0.045, Z1), root, c)
    slat = K.simple("shutter", "#9aa0a8", 0.35, 0.7)
    n = 18; hs = (Z1 - Z0) / n
    for i in range(n):
        K.box("gear_slat", (2 * HWd - 0.06, 0.035, hs - 0.012), (0, 0, -hs * (i + 0.5)), slat, sh, bevel=0.008, c=c)
    K.box("gear_shutter_bar", (2 * HWd - 0.06, 0.06, 0.10), (0, 0, -(Z1 - Z0) + 0.05), st, sh, c=c)
    K.tube("gear_shutter_handle", [(-0.22, 0.03, -(Z1 - Z0) + 0.08), (-0.18, 0.10, -(Z1 - Z0) + 0.08), (0.18, 0.10, -(Z1 - Z0) + 0.08), (0.22, 0.03, -(Z1 - Z0) + 0.08)], 0.022, V.mat("chrome"), sh, c=c, segs=6)
    lm = K.emit("gear_strip", (0.86, 0.94, 1.0), 0.05)
    add(K.box("gear_strip", (2 * HWd - 0.5, 0.05, 0.03), (0, Yf - 0.10, Z1 - 0.02), lm, root, c=c))
    add(K.box("gear_strip2", (2 * HWd - 0.8, 0.05, 0.03), (0.16, Yf - 0.10, ZS - 0.04), lm, root, c=c))
    L = K.point("gear_lamp", (0, Yf - 0.25, Z1 - 0.12), 0.0, (0.86, 0.94, 1.0), 0.25, parent=root, glossy=False); L.hide_render = True
    L2 = K.point("gear_lamp2", (0.1, Yf - 0.16, ZS - 0.12), 0.0, (0.86, 0.94, 1.0), 0.25, parent=root, glossy=False); L2.hide_render = True
    for o in P + K.tree(sh) + [x for it in items.values() for x in K.tree(it)]:
        if o.type == "MESH" and o.pass_index == 0: o.pass_index = 4
    G = dict(parts=P, items=items, shutter=sh, lamp=L, lamp2=L2, strip=lm, flares=flares, span=Z1 - Z0,
             local=dict(face_y=Yf, z0=Z0, z1=Z1, shelf=ZS, half_w=HWd, bag=(bx, Yf - 0.29, Z0 + 0.45), flare_box=(fx, Yf - 0.27, Z0 + 0.6)))
    _S["G"] = G
    shutter(0.0)
    return G


def take(name, taken=True):
    it = _S["G"]["items"][name]
    for o in K.tree(it): o.hide_render = taken


def shutter(t):
    G = _S["G"]; t = max(0.0, min(1.0, t))
    sh = G["shutter"]
    sh.scale = (1, 1, max(0.02, 1.0 - 0.97 * t))            # the curtain is gathered into the housing above
    lamp(t > 0.15)


def lamp(on=True, energy=26.0):
    G = _S["G"]
    for k, e in (("lamp", energy), ("lamp2", energy * 0.7)):
        G[k].hide_render = not on; G[k].data.energy = e if on else 0.0
    K.set_emit(G["strip"], 3.5 if on else 0.05)


def world(local):
    import cab
    return tuple(cab._S["R"]["root"].matrix_world @ Vector(local))
