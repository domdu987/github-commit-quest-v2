"""specs9.py -- EP.1 specs (Praew, Tos, James, the junior's states, Kong's EP.1 kit, the guard), the infected crowd
generator and static pose helpers.  Imported by draw9 (`from specs9 import *`)."""
import math, random
import draw8 as D
from draw8 import shade, tint, mix_hex, _spec, SPECS

INF_SKIN = "#c4cdb2"
HEIGHTS = dict(kong=2.86, crew=2.80, praew=2.60, james=2.61, tos=2.67, driver=2.70, guard=2.75)   # BU, soles to hair top (sheet ratios; Kong / crew as the hook)
__all__ = ["HEIGHTS", "pale", "wet9", "infected", "infected_crowd", "INF_ROLES", "check_unique9", "kong_ep1", "junior", "tos", "poses", "POSES",
           "press_wound", "tos_hold", "signature"]


def wet9(sp, name=None, darken=0.14):
    """rain-wet variant of a non-rescue spec: darker cloth, drooped hair with sheen, glossy card term."""
    w = dict(sp)
    w["name"] = name or sp["name"] + "_wet"
    w["wet"] = True
    c = dict(sp["col"])
    for k in ("shirt", "trouser", "trouser_dk", "jacket", "jacket_lo", "coat"):
        if k in c:
            c[k] = shade(c[k], darken * (0.35 if k in ("coat", "shirt") and sp.get("outfit9") in ("coat", "suit") else 1.0))
    w["col"] = c
    if "sleeve_col" in sp:
        w["sleeve_col"] = shade(sp["sleeve_col"], darken * (0.35 if sp.get("outfit9") == "coat" else 1.0))
    h = dict(sp["hair"])
    h.update(wet=True)
    if h["style"] in ("spiky", "crest"):
        h.update(top=h["top"] * 0.80, extent=h["extent"] * 1.06)
    w["hair"] = h
    return w


def pale(sp, level, name=None):
    """the bitten skin going grey: level 0 paper white .. 4 = the infected grey-green (continuity: three steps, the
    driver's colour is step four)."""
    k = max(0.0, min(4.0, float(level))) / 4.0
    p = dict(sp)
    p["skin"] = mix_hex(sp.get("skin", "#fdf6ed"), INF_SKIN, k)
    p["skin_dk"] = mix_hex("#d9cfc2", "#97a38a", k)
    p["name"] = name or "%s_p%d" % (sp["name"], round(level))
    return p


# ------------------------------------------------------------------------------------------------ Dr. Praew
SPECS["praew"] = _spec(
    name="praew", legs=1.81, torso=1.38, total_ref=4.48, head_ink_top=0.034, head_ink_side=0.050,
    hair=dict(style="praew", top=0.14, width=1.20, extent=1.2, n=6, fringe=0.2, seed=3, col="#231d1b"),
    shoulder=0.84, chest=0.74, belt_w=0.72, hip_w=0.68, leg_w=0.31, boot_h=0.31, sole_len=(0.36, 0.46, 0.56), boot_w=0.32,
    hand=0.25, forearm=0.13, sleeve="long", sleeve_w=0.21, upper_arm=0.56, fore_arm=0.50,
    outfit="dress", outfit9="coat", sleeve_col="#f6f5f1", pack=False, radio=False, flag=False, kneepads=False, thigh_pouch=False,
    hip_pouches=False, glove=True, shoe="sneaker",
    col=dict(shirt="#5f93cc", coat="#f6f5f1", trouser="#5f93cc", trouser_dk="#44709f", boot="#f2f2ee", sole="#cfd3d6", glove="#45a8dc", belt="#5f93cc"),
    face=dict(eye="oval", eye_w=0.085, eye_h=0.19, eye_sp=0.34, eye_y=0.03, brow_len=0.17, brow_th=0.038, brow_y=-0.20, mouth_y=0.27, mouth_w=0.19, stubble=False),
    default_expr="focused", exprs=("focused", "alarmed", "shouting", "doubtful", "calm", "neutral", "blink"))
SPECS["praew_wet"] = wet9(SPECS["praew"])
SPECS["praew_wet"]["hair"]["loose"] = 0.5
SPECS["praew_wet"]["knee_dirt"] = True

# ------------------------------------------------------------------------------------------------ Khun Tos
SPECS["tos"] = _spec(
    name="tos", legs=1.75, torso=1.27, total_ref=4.22, head_ink_top=0.034, head_ink_side=0.050,
    hair=dict(style="slick", top=0.135, width=1.17, extent=0.79, n=6, fringe=0.1, seed=7, col="#302a26"),
    shoulder=0.78, chest=0.66, belt_w=0.68, hip_w=0.66, leg_w=0.30, boot_h=0.30, sole_len=(0.36, 0.45, 0.56), boot_w=0.30,
    hand=0.20, forearm=0.15, sleeve="long", sleeve_w=0.205, upper_arm=0.56, fore_arm=0.50,
    outfit="office", outfit9="suit", sleeve_col="#323b4f", cuff_col="#f3f3ef", tie=False, torn=False, pack=False, radio=False, flag=False,
    kneepads=False, thigh_pouch=False, hip_pouches=False, glove=False, shoe="shoe",
    watch=dict(side="L", style="silver"),
    col=dict(shirt="#f6f6f2", shirt_dk="#c9ced6", jacket="#323b4f", trouser="#d0b190", trouser_dk="#a98c6c", boot="#383838", sole="#1c1c1c",
             belt="#6b4a33", buckle="#d9d4c6"),
    face=dict(eye="oval", eye_w=0.06, eye_h=0.125, eye_sp=0.35, eye_y=-0.05, brow_len=0.225, brow_th=0.042, brow_y=-0.215, mouth_y=0.24, mouth_w=0.19,
              stubble=False, glasses="tos"),
    default_expr="arrogant", exprs=("arrogant", "panicked", "shouting", "evasive", "neutral", "blink"))
SPECS["tos_wet"] = wet9(SPECS["tos"])


def tos(state="wet", side="L"):
    """Khun Tos by continuity state: "dry" (sheet), "wet" (scene 03: both sleeves whole), "torn" (from S112: the sleeve
    ripped, he clamps it), "soaked" (the cuff dark and wet, S120), "bleed" (scene 06: blood runs off the arm).
    side = the anatomical arm (continuity.md says left; the cast brief said right: pass "R" to switch)."""
    if state == "dry":
        return SPECS["tos"]
    sp = dict(SPECS["tos_wet"])
    lvl = {"wet": 0, "torn": 1, "soaked": 2, "bleed": 3}[state]
    sp["name"] = "tos_" + state + ("" if side == "L" else "_r")
    if lvl:
        sp["tear"] = dict(side=side, level=lvl)
        if side == "L":
            sp.pop("watch", None)                          # the watch arm is the torn one: the hand covers it
    return sp


for _st in ("torn", "soaked", "bleed"):
    SPECS["tos_" + _st] = tos(_st)

# ------------------------------------------------------------------------------------------------ James
SPECS["james"] = _spec(
    name="james", legs=1.74, torso=1.37, total_ref=4.49, head_ink_top=0.036, head_ink_side=0.054,
    hair=dict(style="crest", top=0.25, width=1.27, extent=0.90, n=8, fringe=0.36, seed=9),
    shoulder=0.80, chest=0.72, belt_w=0.74, hip_w=0.70, leg_w=0.31, boot_h=0.47, sole_len=(0.38, 0.47, 0.60), boot_w=0.34,
    hand=0.30, forearm=0.13, sleeve="long", sleeve_w=0.22, upper_arm=0.58, fore_arm=0.52,
    outfit="delivery", outfit9="rider", pack=False, box=False, radio=False, flag=False, kneepads=False, thigh_pouch=True, hip_pouches=False,
    glove=True, shoe="sneaker_high",
    col=dict(shirt="#52a753", jacket="#52a753", jacket_lo="#2c2c2c", trouser="#313131", trouser_dk="#202020", boot="#3c9a47", sole="#f4f4f0",
             glove="#2a2a2a", belt="#1b1b19", buckle="#8a8a86", vest="#1b1b19"),
    face=dict(eye="oval", eye_w=0.08, eye_h=0.18, eye_sp=0.40, brow_len=0.20, brow_th=0.046, brow_y=-0.165, mouth_y=0.20, mouth_w=0.27,
              stubble=False, brow_over_hair=True),
    default_expr="cheerful", exprs=("cheerful", "terrified", "shouting", "urgent", "neutral", "scared", "blink"))
_jh = dict(SPECS["james"])
_jh["name"] = "james_helmet"
_jh["hair"] = dict(style="helmet", top=0.165, width=1.23, extent=0.9, n=8, fringe=0.3, seed=9, shell="#f4f4f0", rim="#3fa34d", visor="up")
_jh["face"] = dict(SPECS["james"]["face"], brow_over_hair=False, brow_y=-0.13)
SPECS["james_helmet"] = _jh                                 # the EP.1 look: helmet on in every shot (continuity)
SPECS["james_wet"] = wet9(_jh, "james_wet")
SPECS["james_bare_wet"] = wet9(SPECS["james"], "james_bare_wet")

# ------------------------------------------------------------------------------------------------ the junior
def junior(state="bitten", pale_level=None, gauze=None, blood=1.0):
    """the junior rescue worker after the hook: "bitten" (wound open, blood down the chest), "treated" (gauze pad,
    soak 0..1 through `gauze`), "dying" (pale step 3, gauze soaked), "infected" (grey-green, white eyes with red pin
    pupils, same uniform and wound, dried blood on the collar, gloved claw hands).  The bite is on the ANATOMICAL LEFT
    side of the neck where it meets the shoulder (the side the hook's S21 / S23 cameras see)."""
    base = SPECS["crew_wet"]
    if state == "infected":
        sp = pale(base, 4, "crew_infected")
        sp["neck_wound"] = dict(side="L", blood=0.75, dried=True)
        sp["wounds"] = [dict(kind="collar_blood", side=1, seed=6)]
        sp["face"] = dict(base["face"], eye="zombie", eye_w=0.145, eye_h=0.135)
        sp["claws"] = True
        sp["default_expr"] = "searching"
        sp["exprs"] = ("snap_open", "searching", "lunging", "moan", "still", "bite")
        return sp
    lvl = {"bitten": 0, "treated": 1, "dying": 3}[state] if pale_level is None else pale_level
    sp = pale(base, lvl, "crew_%s%s" % (state, "" if pale_level is None else "_p%d" % pale_level))
    gz = gauze if gauze is not None else {"bitten": None, "treated": 0.35, "dying": 1.0}[state]
    sp["neck_wound"] = dict(side="L", blood=blood, gauze=gz)
    sp["default_expr"] = {"bitten": "pain", "treated": "pain", "dying": "fading"}[state]
    sp["exprs"] = ("pain", "fading", "out", "scared", "shouting", "neutral")
    return sp


for _st in ("bitten", "treated", "dying", "infected"):
    _j = junior(_st)
    SPECS[_j["name"]] = _j
for _lv in (1, 2, 3):
    _j = junior("treated", pale_level=_lv, gauze=0.3 + 0.23 * _lv)
    SPECS["crew_grey%d" % _lv] = dict(_j, name="crew_grey%d" % _lv)


# ------------------------------------------------------------------------------------------------ Kong in EP.1
def kong_ep1(scene="02", blood=None, crowbar=None, watch=True):
    """kong_wet with the EP.1 continuity kit.  scene "02" / "03": watch on the left wrist (first seen S26), the
    junior's blood on both gloves and the right forearm from S35 (blood=1; thinned by rain in 03: 0.5);
    "04" / "05" / "06": the crowbar through the pack's left loops, hook up over the left shoulder;
    "06b": the crowbar is in his hands (not on the pack)."""
    sp = dict(SPECS["kong_wet"])
    sp["name"] = "kong_ep1_" + scene
    sp["canvas_pad"] = (0.5, 1.5)
    if watch:
        sp["watch"] = dict(side="L", style="kong", blood=True)
    b = blood if blood is not None else {"02": 1.0, "03": 0.5, "04": 0.35, "05": 0.25, "06": 0.2, "06b": 0.2}[scene]
    if b:
        sp["blood_hands"] = b
        sp["blood_forearm"] = "R"
    cb = crowbar if crowbar is not None else scene in ("04", "05", "06")
    if cb:
        sp["crowbar_pack"] = True
    return sp


for _sc in ("02", "03", "04", "05", "06", "06b"):
    SPECS["kong_ep1_" + _sc] = kong_ep1(_sc)
SPECS["kong_ep1_clean"] = kong_ep1("02", blood=0)
SPECS["kong_ep1_clean"]["name"] = "kong_ep1_clean"

# ------------------------------------------------------------------------------------------------ the hospital guard
SPECS["guard"] = _spec(
    name="guard", legs=1.74, torso=1.36, total_ref=4.3,
    hair=dict(style="cap", top=0.14, width=1.14, extent=0.7, n=6, fringe=0.2, seed=4, col="#1b1b1b", cap_col="#1f2a44"),
    shoulder=1.02, chest=0.92, belt_w=0.92, hip_w=0.90, leg_w=0.36, boot_h=0.34, sole_len=(0.38, 0.46, 0.56), boot_w=0.34,
    hand=0.22, forearm=0.14, sleeve="short", sleeve_w=0.24, upper_arm=0.55, fore_arm=0.50,
    outfit="shirt", outfit9="guard", tie=True, pack=False, radio=False, flag=False, kneepads=False, thigh_pouch=False, hip_pouches=False,
    glove=False, shoe="shoe", skin="#f6e6d2",
    col=dict(shirt="#a9c7e6", trouser="#232b40", trouser_dk="#161c2c", boot="#1c1c1c", sole="#111111", belt="#15151a", buckle="#c9c9c4", tie="#1f2a44",
             stain="#6f5a44"),
    face=dict(eye="oval", eye_w=0.07, eye_h=0.15, eye_sp=0.36, brow_len=0.21, brow_th=0.046, brow_y=-0.10, mouth_y=0.25, mouth_w=0.21, stubble=False,
              moustache=True),
    default_expr="wary", exprs=("wary", "shouting", "scared", "neutral"))

# ------------------------------------------------------------------------------------------------ infected crowd
# role, base outfit, hair, colours, build (shoulder, chest, leg_w), face, wounds, idle arms, sprint style
INF_ROLES = [
    dict(role="office woman, blazer", outfit="blazer", hair="bob", hair_col="#2a1d18", col=dict(shirt="#f3f1ea", jacket="#7b2f45", trouser="#2e2f38", boot="#1f1f22"),
         skirt=True, shoe="shoe", build=(0.80, 0.70, 0.30), face=dict(eye_w=0.13, eye_h=0.12), skin_k=0.0,
         wounds=[dict(kind="mouth_blood"), dict(kind="shoulder_bite", side=1, seed=4)], arms=("claw", "hang"), run="reach", expr="lunging"),
    dict(role="older man, polo", outfit="polo", hair="grey_swept", hair_col="#9b9ea3", col=dict(shirt="#4f7fb8", trouser="#8c7a5e", boot="#5a3e2a"), shoe="shoe",
         build=(1.02, 0.96, 0.36), face=dict(eye_w=0.12, eye_h=0.10, wrinkles=True, moustache=True, glasses="round"), skin_k=0.25,
         wounds=[dict(kind="belly_blood", side=-1, seed=2), dict(kind="arm_bite", arm="L", at="fore", seed=7)], arms=("hang", "claw_up"), run="trail", expr="moan"),
    dict(role="student-age man, hoodie", outfit="hoodie", hair="messy", hair_col="#1a1414", col=dict(shirt="#5b6470", trouser="#3d5f8f", boot="#e9e9e4", sole="#f4f4f0"),
         shoe="sneaker_high", build=(0.88, 0.74, 0.31), face=dict(eye_w=0.15, eye_h=0.14), skin_k=-0.15,
         wounds=[dict(kind="cheek_bite", eye=1, seed=3), dict(kind="hand_blood", arm="R", seed=9)], arms=("claw_up", "claw"), run="flail", expr="lunging"),
    dict(role="auntie, tee", outfit="tee", hair="bun", hair_col="#2b2420", col=dict(shirt="#e7b23c", trouser="#4d4a6e", boot="#7d5b3f"), print="#c0392b", shoe="shoe",
         build=(1.04, 1.00, 0.38), face=dict(eye_w=0.12, eye_h=0.11), skin_k=0.35,
         wounds=[dict(kind="arm_bite", arm="R", at="fore", seed=5), dict(kind="chest_blood", side=-1, seed=8)], arms=("reach", "hang"), run="reach", expr="searching"),
    dict(role="taxi driver, cap", outfit="shirt", hair="cap", hair_col="#1b1b1b", col=dict(shirt="#8fb7d8", trouser="#363636", boot="#2a2a2a"), cap_col="#e0a21b",
         shoe="shoe", build=(1.00, 0.92, 0.36), face=dict(eye_w=0.13, eye_h=0.11, beard=True), skin_k=0.1,
         wounds=[dict(kind="collar_blood", side=-1, seed=12), dict(kind="knee_blood", leg="R")], arms=("claw", "claw"), run="trail", expr="lunging"),
    dict(role="student, ponytail", outfit="shirt", hair="ponytail", hair_col="#151111", col=dict(shirt="#ffffff", trouser="#1f2e5a", boot="#141414"), skirt=True,
         shoe="shoe", build=(0.82, 0.70, 0.29), tie=True, tie_col="#1f2e5a", face=dict(eye_w=0.15, eye_h=0.15), skin_k=-0.25,
         wounds=[dict(kind="chest_blood", side=1, seed=14), dict(kind="eye_shut", eye=-1)], arms=("hang", "hang"), run="flail", expr="moan"),
    dict(role="young man, tee and shorts", outfit="tee", hair="spiky", hair_col="#232020", col=dict(shirt="#2f7f7a", trouser="#41536b", boot="#b33a2e", sole="#f4f4f0"),
         shorts=True, shoe="sneaker", build=(0.92, 0.78, 0.32), face=dict(eye_w=0.14, eye_h=0.13), skin_k=0.0,
         wounds=[dict(kind="shin_blood", leg="L"), dict(kind="mouth_blood"), dict(kind="sleeve_torn", arm="L")], arms=("claw_up", "hang"), run="one_up", expr="lunging"),
    dict(role="office man, bald, tie", outfit="office", hair="bald", hair_col="#555555", col=dict(shirt="#f2f2ee", trouser="#22262f", boot="#1a1a1a", tie="#2c5e9e"),
         tie=True, shoe="shoe", build=(1.06, 1.04, 0.38), face=dict(eye_w=0.12, eye_h=0.12, glasses="rect"), skin_k=0.3, torn=True,
         wounds=[dict(kind="brow_cut", eye=1), dict(kind="belly_blood", side=1, seed=16)], arms=("reach", "claw"), run="reach", expr="searching"),
    dict(role="woman, long hair", outfit="tee", hair="long", hair_col="#3a261b", col=dict(shirt="#c86aa0", trouser="#d7c4a4", boot="#f0f0ec"), shoe="sneaker",
         build=(0.84, 0.72, 0.31), face=dict(eye_w=0.14, eye_h=0.12), skin_k=-0.1,
         wounds=[dict(kind="shoulder_bite", side=-1, seed=18), dict(kind="knee_blood", leg="L")], arms=("hang", "claw"), run="trail", expr="moan"),
    dict(role="motorbike-taxi rider, vest", outfit="polo", hair="mop", hair_col="#16130f", col=dict(shirt="#e8662a", trouser="#5a5d63", boot="#30302f"),
         shoe="sneaker", build=(0.96, 0.84, 0.34), face=dict(eye_w=0.13, eye_h=0.13, moustache=True), skin_k=0.2,
         wounds=[dict(kind="arm_bite", arm="L", at="upper", seed=19), dict(kind="mouth_blood")], arms=("claw", "claw_up"), run="flail", expr="lunging"),
    dict(role="office man, rolled sleeves", outfit="office", hair="flat", hair_col="#2b2118", col=dict(shirt="#cdb9e6", trouser="#4a3f36", boot="#2a211b", tie="#5d2a6e"),
         tie=True, shoe="shoe", build=(0.90, 0.80, 0.32), face=dict(eye_w=0.14, eye_h=0.11), skin_k=-0.05, torn=True,
         wounds=[dict(kind="cheek_bite", eye=-1, seed=21), dict(kind="hand_blood", arm="L", seed=22)], arms=("hang", "reach"), run="one_up", expr="searching"),
    dict(role="student-age woman, curls", outfit="hoodie", hair="curly", hair_col="#3b1f14", col=dict(shirt="#d9d2c2", trouser="#2d4a3a", boot="#c9c2b0", sole="#f4f4f0"),
         shoe="sneaker_high", build=(0.82, 0.72, 0.30), face=dict(eye_w=0.15, eye_h=0.13), skin_k=0.15,
         wounds=[dict(kind="collar_blood", side=1, seed=24), dict(kind="shin_blood", leg="R")], arms=("claw_up", "claw_up"), run="reach", expr="lunging"),
    dict(role="lorry driver, vest top", outfit="tee", hair="swept", hair_col="#4a3a2a", col=dict(shirt="#8d9a6a", trouser="#2f3a55", boot="#6a4b2e"), shoe="shoe",
         build=(1.10, 1.06, 0.40), face=dict(eye_w=0.12, eye_h=0.12, beard=True), skin_k=0.4,
         wounds=[dict(kind="chest_blood", side=1, seed=26), dict(kind="arm_bite", arm="R", at="upper", seed=27)], arms=("claw", "hang"), run="trail", expr="moan"),
    dict(role="office woman, bun, blouse", outfit="shirt", hair="praew", hair_col="#5a3a22", col=dict(shirt="#3f8f8a", trouser="#1e1e24", boot="#8a2f3a"), shoe="shoe",
         build=(0.80, 0.70, 0.29), face=dict(eye_w=0.13, eye_h=0.14), skin_k=-0.2,
         wounds=[dict(kind="mouth_blood"), dict(kind="brow_cut", eye=-1), dict(kind="sleeve_torn", arm="R")], arms=("reach", "claw_up"), run="flail", expr="lunging"),
]


def infected(i=0, seed=0):
    """infected crowd figure i (0..13): its own face, hair, clothes, wounds, idle arms and sprint style."""
    R = INF_ROLES[i % len(INF_ROLES)]
    rnd = random.Random(seed * 1000 + i * 37 + 5)
    sh, ch, lw = R["build"]
    legs = rnd.uniform(1.60, 1.82)
    torso = rnd.uniform(1.27, 1.42)
    k = R.get("skin_k", 0.0)
    skin = mix_hex(INF_SKIN, "#a8b89a" if k > 0 else "#d5d8c4", abs(k))
    col = dict(shirt="#888888", trouser="#444444", trouser_dk="#333333", boot="#2a2a2a", sole="#1c1c1c", belt="#2b2b2b", buckle="#c9c9c4",
               tie=R.get("tie_col", "#9b2a2a"), stain="#6f5a44", jacket="#555555", jacket_lo="#2c2c2c", glove="#333333")
    col.update(R["col"])
    for kk in ("shirt", "jacket", "trouser"):                # grimy: every cloth colour a little greyer
        col[kk] = mix_hex(col[kk], "#5c6058", 0.14)
    col["trouser_dk"] = shade(col["trouser"], 0.3)
    style = {"messy": "swept", "grey_swept": "swept"}.get(R["hair"], R["hair"])
    hair = dict(style=style, top=rnd.uniform(0.12, 0.2), width=rnd.uniform(1.12, 1.26), extent=rnd.uniform(0.62, 0.8), n=6 + i % 3,
                fringe=rnd.uniform(0.2, 0.32), seed=200 + i, col=R["hair_col"], messy=R["hair"] in ("messy", "swept"), cap_col=R.get("cap_col", "#2f5fa8"))
    if style == "praew":
        hair.update(top=0.14, width=1.2, loose=1.0)
    face = dict(eye="zombie", eye_w=0.13, eye_h=0.11, eye_sp=rnd.uniform(0.31, 0.40), brow_len=rnd.uniform(0.15, 0.22),
                brow_th=rnd.uniform(0.030, 0.045), brow_y=-rnd.uniform(0.17, 0.21), mouth_y=rnd.uniform(0.21, 0.26), mouth_w=rnd.uniform(0.17, 0.24), stubble=False)
    face.update(R["face"])
    sp = _spec(name="inf%02d" % i, role=R["role"], legs=legs, torso=torso, hair=hair, hair_col=R["hair_col"],
               shoulder=sh, chest=ch * 0.95, belt_w=ch * 0.98, hip_w=ch, leg_w=lw, boot_h=0.30 if R.get("shoe") in ("shoe", "sneaker") else 0.45,
               sole_len=(0.36, 0.44, 0.54), boot_w=0.32, hand=0.22, forearm=0.13, sleeve="short" if R["outfit"] in ("tee", "polo") else "long",
               sleeve_w=0.21, upper_arm=0.55, fore_arm=0.50, outfit=R["outfit"], col=col, glove=False, claws=True, shoe=R.get("shoe", "shoe"),
               tie=R.get("tie", False), print=R.get("print"), shorts=R.get("shorts", False), skirt=R.get("skirt", False), torn=R.get("torn", False),
               skin=skin, skin_dk=shade(skin, 0.24), face=face, default_expr=R["expr"], wounds=[dict(w) for w in R["wounds"]],
               extra_pose=dict(arm_r=R["arms"][0], arm_l=R["arms"][1]), run_style=R["run"], infected=True)
    if sp["skirt"]:
        sp["legwear"] = skin
    return sp


def signature(sp):
    return dict(face=(round(sp["face"]["eye_w"], 3), round(sp["face"]["eye_h"], 3), sp["default_expr"],
                      tuple(sorted(k for k in sp["face"] if k in ("glasses", "moustache", "beard", "wrinkles")))),
                hair=(sp["hair"]["style"], sp["hair"].get("col"), bool(sp["hair"].get("messy"))),
                clothes=(sp["outfit"], sp["col"].get("shirt"), sp["col"].get("jacket"), sp["col"]["trouser"], bool(sp.get("skirt")), bool(sp.get("shorts"))),
                wounds=tuple(sorted((w["kind"], str(w.get("side", w.get("arm", w.get("leg", w.get("eye", ""))))) ) for w in sp.get("wounds", ()))),
                skin=sp["skin"], build=(sp["shoulder"], sp["leg_w"]))


def check_unique9(specs):
    """raises unless every pair differs in face, hair, clothes AND wounds; returns the per-key value lists."""
    sig = [signature(s) for s in specs]
    out = {}
    for k in ("face", "hair", "clothes", "wounds"):
        vals = [s[k] for s in sig]
        out[k] = vals
        if len(set(vals)) != len(vals):
            dup = [v for v in set(vals) if vals.count(v) > 1]
            raise ValueError("infected not unique in %s: %s" % (k, dup))
    return out


def infected_crowd(n=14, seed=0):
    """n distinct infected (n <= 14 are all different designs; beyond that use the silhouettes of stage9)."""
    if n > len(INF_ROLES):
        raise ValueError("only %d distinct infected designs: fill the rest with stage9.Sil silhouettes" % len(INF_ROLES))
    specs = [infected(i, seed) for i in range(n)]
    check_unique9(specs)
    return specs


# ------------------------------------------------------------------------------------------------ static pose helpers
def press_wound(view="q", s=-1, side="L"):
    """pose keys for the hand pressed to the neck wound (the OTHER hand comes across; layer raised in front)."""
    if view in ("front", "back"):
        sg = 1 if side == "L" else -1
        key = "arm_r" if side == "L" else "arm_l"
        return {key: dict(fig_rel="neck", _neck=(sg * 0.17, 0.34), hand_shape="press", elbow=-sg), "z": {key: 2.7}}
    near_is_wound = (side == "L") == (s < 0)
    key = "arm_f" if near_is_wound else "arm_n"
    return {key: dict(fig_rel="neck", _neck=(-s * 0.08, 0.40), hand_shape="press", elbow=-s), "z": {key: 2.7}}


def tos_hold(view="front", s=1, side="L"):
    """Tos clamping the torn forearm: the torn arm folded across the belly, the other hand closed over its cuff."""
    if view == "front":
        torn, hold = ("arm_l", "arm_r") if side == "L" else ("arm_r", "arm_l")
        return {torn: dict(hand=(-0.50, 0.50), elbow=None), hold: dict(grab=dict(arm=torn[-1].upper(), t=0.86), hand_shape="grip"), "z": {hold: 2.6}}
    near_torn = (side == "L") == (s < 0)                    # facing screen-left shows the left arm
    torn, hold = ("arm_n", "arm_f") if near_torn else ("arm_f", "arm_n")
    p = {torn: dict(hand=(0.30, 0.56), elbow=None), hold: dict(grab=dict(arm=torn[-1], t=0.86), hand_shape="grip")}
    p["z"] = {"arm_f": 2.42, "arm_n": 2.5} if near_torn else {"arm_f": 2.42, "arm_n": 2.6}
    if near_torn:
        p["z"] = {"arm_n": 2.42, "arm_f": 2.6}
    return p


def _sit(sp, s=1, slump=0.0, legs_out=1.0):
    """seated on the ground against a wheel / wall behind the back: pelvis on the deck, legs out in front, back leaning."""
    sp = D.get_spec(sp)
    hy = sp["legs"] + 0.06 - 0.30
    reach = (sp["legs"] + 0.06 - min(sp["boot_h"] * 0.42, 0.24))
    return dict(view="side", s=s, hip=(0.0, hy), lean=-7 - 7 * slump,
                legs=dict(foot_n=(s * reach * (0.80 + 0.14 * legs_out), 0.0), foot_f=(s * reach * (0.60 + 0.10 * legs_out), 0.0), toe_n=-62, toe_f=-50),
                head=(0, 10 + 16 * slump, 0.03 * slump, 0.03 * slump))


def poses(sp, name, s=1, view=None, **kw):
    """named static poses -> pose dict for draw9.build / Actor.pose.  See POSES."""
    sp_ = D.get_spec(sp)
    if name == "sit_wheel":                                 # the junior against the truck's rear wheel
        p = _sit(sp_, s, kw.get("slump", 0.3))
        p.update(expr=kw.get("expr", "pain"), arm_f="lap", arm_n="lap")
        if kw.get("limp"):
            p.update(arm_n=dict(hand=(0.12, 0.80), elbow=None, hand_shape="open"), expr=kw.get("expr", "out"))
        else:
            p.update(press_wound("side", s))
        return p
    if name == "crouch_hide":                               # behind cover, knees deep, a glove over the mouth
        v = view or "q"
        return dict(view=v, s=s, expr=kw.get("expr", "alarmed"), legs="crouch", hip=(0.0, 0.62), lean=16, head=(0, 6, 0.02, 0.02),
                    arm_n=dict(fig_rel="mouth", hand_shape="press", elbow=-1), arm_f=dict(hand=(0.30, 0.52), elbow=None), z={"arm_n": 2.7})
    if name == "seated_cab":                                # in the truck cab: role "driver" / "front" / "rear"
        role = kw.get("role", "driver")
        v = view or "front"
        p = dict(view=v, s=s, legs=dict(seated=True), expr=kw.get("expr"), lean=2)
        if role == "driver":
            p.update(arm_r=dict(hand=(-0.22, 0.42), elbow=None, hand_shape="grip"), arm_l=dict(hand=(0.22, 0.42), elbow=None, hand_shape="grip")) if v == "front" else \
                p.update(arm_n="wheel", arm_f="wheel")
        elif role == "front":
            p.update(arm_r="lap", arm_l=dict(hand=(0.55, 0.05), elbow=None, hand_shape="open")) if v == "front" else p.update(arm_n="lap", arm_f=dict(hand=(0.6, 0.2), elbow=None, hand_shape="open"))
        else:
            p.update(arm_r="lap", arm_l="lap") if v == "front" else p.update(arm_n="lap", arm_f="lap")
        return p
    if name == "bang_glass":                                # one frame of the slam loop (use gait9.bang for the loop)
        return dict(view=view or "q", s=s, expr="lunging", legs="step", lean=14, arm_n=dict(hand=(0.62, -0.42), elbow=None, hand_shape="fist_side"),
                    arm_f=dict(hand=(0.55, -0.10), elbow=None, hand_shape="claw"))
    if name == "pulled":                                    # Tos dragged out by the arms: stage the card rolled ~80 deg
        return dict(view="q", s=s, expr=kw.get("expr", "panicked"), legs=dict(foot_n=(s * 0.10, 0.0), foot_f=(-s * 0.12, 0.0)), lean=0,
                    arm_n=dict(hand=(0.25, -1.02), elbow=None, hand_shape="open"), arm_f=dict(hand=(0.05, -1.05), elbow=None, hand_shape="open"), head=(0, -8, 0, 0))
    if name == "pull":                                      # the rescuer: both hands low and forward, weight back
        return dict(view="side", s=s, expr=kw.get("expr", "shouting"), legs="lunge", lean=-16 + kw.get("k", 0.0) * 10, hip=(0.0, 0.30),
                    arm_n=dict(hand=(0.80, 0.42), elbow=None, hand_shape="grip"), arm_f=dict(hand=(0.74, 0.52), elbow=None, hand_shape="grip"))
    if name == "phone_chest":                               # the lit phone hidden against the chest
        return dict(view=view or "front", s=s, expr=kw.get("expr", "grief"), arm_l=dict(hand=(-0.42, 0.40), elbow=None, hand_shape="press"),
                    prop_l=dict(type="phone", glow=kw.get("glow", 1.0)), arm_r="hold_cutter")
    if name == "tos_cross":
        p = dict(view=view or "front", s=s, expr=kw.get("expr", "arrogant"))
        p.update(tos_hold(p["view"], s, kw.get("side", "L")))
        return p
    raise KeyError(name)


POSES = ("sit_wheel", "crouch_hide", "seated_cab", "bang_glass", "pulled", "pull", "phone_chest", "tos_cross")
