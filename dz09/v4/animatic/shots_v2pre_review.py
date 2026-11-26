"""shots.py -- DEAD ZONE 09 EP.1 opening animatic: shot list, cameras, cast cards, props; renders Cycles frames.

    python3 shots.py                 render every shot   -> render/f_0001.png ... (global frame g -> f_{g+1})
    python3 shots.py --test          one middle frame per shot -> test/<shot>.png
    python3 shots.py --only S07,S08  subset
Times are film seconds (narration starts at 0.30 s; caption boundaries already shifted).
"""
import json, math, os, sys, time
import bpy
from mathutils import Vector, Euler, Quaternion, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import set_build as SB
from set_build import hexcol, KONG, CREW, DRIVER_SEAT, SEDAN

FPS = 24
W, H = 360, 640
SPR = os.path.join(HERE, "sprites")
META = json.load(open(os.path.join(SPR, "meta.json")))
ENV = json.load(open(os.path.join(HERE, "tex", "env.json")))
D = 0.5                                  # metres per puppet D

# ---------------------------------------------------------------------------------------------------- shot list
# cam keys: (t, loc, target, lens, roll_deg); interpolation smoothstep between keys; shake (amp_deg, hz, t_from)
K0 = (KONG[0], KONG[1])
CR = (CREW[0], CREW[1])
DS = DRIVER_SEAT

SHOTS = [
 dict(id="S01", t0=0.000, t1=3.525, angle="insert, low macro", what="radio on Kong's shoulder, LED pulses with the voice; snap push on 'เดี๋ยว!', flinch on 'เฮ้ย!'",
      cam=[(0.0, (0.15, 5.80, 1.07), (0.10, 6.20, 1.16), 35, -3), (2.17, (0.14, 5.86, 1.08), (0.10, 6.20, 1.16), 35, -3),
           (2.42, (0.12, 5.97, 1.11), (0.10, 6.20, 1.16), 35, -4)],
      shake=[(0.25, 1.0, 0.0), (2.0, 7.0, 2.636, 0.5)], radio=True, cast=[], door=0),
 dict(id="S02", t0=3.525, t1=5.384, angle="ground -> low crane", what="red light bar on the wet asphalt, crane up to the pile-up",
      cam=[(3.525, (1.3, -3.4, 0.22), (0.9, 3.0, -0.25), 22, 0), (4.10, (1.3, -3.9, 1.45), (-0.5, 40, 1.6), 22, 0),
           (5.384, (1.35, -4.2, 1.75), (-0.5, 40, 2.3), 22, 0)],
      shake=[(0.2, 1.0, 0.0)], cast=[("kong_cutter", K0, 0.0, False)], door=0),
 dict(id="S03", t0=5.384, t1=7.155, angle="high wide", what="Friday night, rain on Bangkok, expressway",
      cam=[(5.384, (11.0, -22.0, 16.0), (-1.0, 30.0, 0.0), 22, 0), (7.155, (10.2, -20.5, 15.3), (-1.0, 32.0, 0.0), 22, 0)],
      shake=[], cast=[("kong_cutter", K0, 0.0, False)], door=0),
 dict(id="S04", t0=7.155, t1=8.909, angle="eye level, along the barrier", what="'บนทางด่วน รถชนกันเป็นแพ': the pile-up",
      cam=[(7.155, (-7.6, -4.0, 1.3), (-2.5, 20.0, 1.0), 22, 0), (8.909, (-7.3, -1.6, 1.3), (-2.3, 20.0, 1.0), 22, 0)],
      shake=[(0.15, 1.0, 0.0)], cast=[("kong_cutter", K0, 0.0, False)], door=0),
 dict(id="S05", t0=8.909, t1=10.706, angle="top-down, rising", what="'ยาวจนมองไม่เห็นปลายทาง': gridlock to the horizon",
      cam=[(8.909, (0.0, 18.0, 20.0), (0.0, 26.0, 0.0), 22, 0), (10.706, (0.0, 24.0, 38.0), (0.0, 40.0, 0.0), 22, 0)],
      shake=[], cast=[("kong_cutter", K0, 0.0, False)], door=0),
 dict(id="S06", t0=10.706, t1=12.18, angle="low (strength)", what="'ก้อง เจ้าหน้าที่กู้ภัย': Kong with the cutter",
      cam=[(10.706, (1.05, 4.65, 0.38), (0.25, 6.4, 1.30), 22, 0), (12.18, (0.85, 4.95, 0.45), (0.25, 6.4, 1.35), 22, 0)],
      shake=[(0.3, 2.0, 0.0)], cast=[("kong_cutter", K0, 0.0, False, [(11.6, "kong_cutter_b"), (11.75, "kong_cutter")])], door=0),
 dict(id="S07", t0=12.18, t1=13.923, angle="eye level medium wide", what="'ยืนข้างรถที่ยับยู่ยี่': Kong beside the crushed sedan, crew works the door",
      cam=[(12.18, (1.9, 2.5, 1.65), (-0.9, 7.8, 0.9), 22, 0), (13.923, (1.6, 3.1, 1.6), (-0.9, 7.8, 0.9), 22, 0)],
      shake=[(0.2, 1.5, 0.0)], cast=[("kong_cutter", K0, 0.0, False), ("crew_lean", (CR[0] + 0.15, CR[1] - 0.3), 0.0, True)], door=0),
 dict(id="S08", t0=13.923, t1=15.682, angle="insert, low raking", what="'ในมือคือเครื่องตัดไร้สาย': the cordless cutter in his glove",
      cam=[(13.923, (1.35, 5.25, 0.52), (0.55, 6.05, 0.74), 35, 0), (15.682, (1.12, 5.45, 0.6), (0.55, 6.05, 0.74), 35, 0)],
      shake=[(0.25, 2.0, 0.0)], cutter=True, cast=[], door=0),
 dict(id="S09", t0=15.682, t1=16.950, angle="macro insert", what="'แบตเต็ม 3 ขีด': battery bars light 1-2-3",
      cam=[(15.682, (0.88, 5.66, 0.76), (0.607, 5.84, 0.665), 50, 0), (16.95, (0.82, 5.71, 0.74), (0.607, 5.84, 0.665), 50, 0)],
      shake=[(0.1, 1.0, 0.0)], cutter=True, cast=[], door=0),
 dict(id="S10", t0=16.950, t1=18.355, angle="eye level MCU", what="'โทรศัพท์สั่น': the phone buzzes, Kong looks down",
      cam=[(16.95, (0.85, 4.95, 1.40), (0.25, 6.4, 1.18), 22, 0), (18.355, (0.8, 5.05, 1.40), (0.25, 6.4, 1.18), 22, 0)],
      shake=[], cast=[("kong_cutter", K0, 0.0, False, [(17.55, "kong_phone")])], buzz=(16.95, 17.6), door=0),
 dict(id="S11", t0=18.355, t1=21.260, angle="high insert (phone, 50 mm)", what="'4 สายที่ไม่ได้รับ จากลูกสาว น้ำเหนือ'",
      cam=[(18.355, (0.47, 5.78, 1.40), (0.45, 6.02, 1.03), 50, 0), (21.26, (0.46, 5.85, 1.33), (0.45, 6.02, 1.03), 50, 0)],
      shake=[(0.08, 1.0, 0.0)], phone=("missed", (0.45, 6.02, 1.03), 55), cast=[], door=0),
 dict(id="S12", t0=21.260, t1=23.740, angle="high CU (the call makes him small), locked", what="Namnuea: 'พ่อ วันนี้พ่อสัญญาว่าจะมารับหนูไง'",
      cam=[(21.26, (0.78, 5.35, 2.30), (0.25, 6.4, 1.30), 22, 0), (23.74, (0.72, 5.45, 2.22), (0.25, 6.4, 1.30), 22, 0)],
      shake=[], cast=[("kong_call", K0, 0.0, False)], door=0),
 dict(id="S13", t0=23.740, t1=26.069, angle="eye level MCU, crew in depth", what="Kong: 'พ่อมีเคสด่วนลูก รออีกแป๊บเดียว'",
      cam=[(23.74, (-0.40, 4.55, 1.50), (0.20, 6.4, 1.32), 22, 0), (26.069, (-0.33, 4.7, 1.50), (0.20, 6.4, 1.32), 22, 0)],
      shake=[(0.1, 1.0, 0.0)], cast=[("kong_call", K0, 0.0, False, "talk"), ("crew_lean", (CR[0] + 0.1, CR[1]), 0.0, True)],
      talk=[(23.74, 26.0)], door=0),
 dict(id="S14", t0=26.069, t1=27.250, angle="high wide", what="Namnuea: 'ทุกครั้งเลย...': Kong small in the rain",
      cam=[(26.069, (-4.3, 1.2, 7.0), (0.1, 6.8, 0.6), 22, 0), (27.25, (-4.45, 0.95, 7.4), (0.1, 6.8, 0.6), 22, 0)],
      shake=[], cast=[("kong_tired", K0, 0.0, False), ("crew_lean", (CR[0] + 0.1, CR[1]), 0.0, True)], door=0),
 dict(id="S15", t0=27.250, t1=28.441, angle="low CU", what="Kong: 'เดี๋ยวพ่อโทรกลับนะ'",
      cam=[(27.25, (0.72, 5.55, 0.85), (0.25, 6.4, 1.42), 22, 0), (28.441, (0.66, 5.65, 0.88), (0.25, 6.4, 1.42), 22, 0)],
      shake=[(0.15, 1.0, 0.0)], cast=[("kong_call", K0, 0.0, False, "talk")], talk=[(27.25, 28.3)], door=0),
 dict(id="S16", t0=28.441, t1=30.838, angle="top-down insert, locked", what="'ปลายสายเงียบไป แล้วก็วางสาย': call ended",
      cam=[(28.441, (0.42, 6.04, 1.30), (0.42, 6.06, 1.0), 50, 0), (30.838, (0.42, 6.04, 1.25), (0.42, 6.06, 1.0), 50, 0)],
      shake=[], phone=("ended", (0.42, 6.05, 1.0), -2), cast=[], door=0),
 dict(id="S17", t0=30.838, t1=32.163, angle="eye level medium, handheld", what="crew: 'พี่ก้อง! เปิดได้แล้วครับ!' at the open door",
      cam=[(30.838, (0.95, 6.55, 1.55), (-0.3, 8.1, 1.35), 22, 0), (32.163, (0.85, 6.7, 1.55), (-0.3, 8.1, 1.35), 22, 0)],
      shake=[(0.6, 2.2, 0.0)], cast=[("crew_shout", (CR[0] + 0.25, CR[1] - 0.35), 0.0, False), ("driver_still", DS, 0.05, False)], door=70),
 dict(id="S18", t0=32.163, t1=34.721, angle="POV through the windscreen", what="'ในรถ คนขับนั่งนิ่ง ไม่ขยับเลยสักนิด'",
      cam=[(32.163, (-1.45, 11.2, 1.32), (-1.55, 8.3, 1.02), 28, 0), (34.721, (-1.48, 10.95, 1.3), (-1.55, 8.3, 1.02), 28, 0)],
      shake=[], cast=[("driver_still", DS, 0.05, False)], door=70),
 dict(id="S19", t0=34.721, t1=36.940, angle="over-the-shoulder (crew)", what="'น้องในทีมค่อยๆ ยื่นหน้าเข้าไปใกล้'",
      cam=[(34.721, (0.95, 6.35, 1.72), (-1.25, 8.4, 1.1), 22, 0), (36.94, (0.78, 6.6, 1.66), (-1.25, 8.4, 1.1), 22, 0)],
      shake=[(0.2, 1.2, 0.0)], cast=[("crew_lean", (CR[0] + 0.05, CR[1] - 0.15), 0.0, True), ("driver_still", DS, 0.05, False)], door=70),
 dict(id="S20", t0=36.940, t1=39.411, angle="Dutch 12 deg, windscreen CU", what="'แล้วคนขับก็ค่อยๆ เงยหน้าขึ้น'",
      cam=[(36.94, (-1.5, 10.75, 1.32), (-1.55, 8.35, 1.2), 30, 0), (37.6, (-1.5, 10.6, 1.31), (-1.55, 8.35, 1.2), 30, 12),
           (39.411, (-1.52, 10.3, 1.29), (-1.55, 8.35, 1.25), 30, 13)],
      shake=[], cast=[("driver_still", DS, 0.05, False, [(38.01, "driver_lift")])], door=70),
 dict(id="S21", t0=39.411, t1=41.261, angle="Dutch low, violent handheld", what="'มันพุ่งเข้ากัดทันที': the lunge and the bite",
      cam=[(39.411, (1.35, 6.55, 0.45), (-0.5, 8.3, 1.3), 22, -14), (41.261, (1.2, 6.7, 0.5), (-0.5, 8.3, 1.25), 22, -15)],
      shake=[(0.2, 1.0, 0.0), (3.0, 6.0, 39.70, 1.2)],
      cast=[("crew_alarmed", (CR[0] + 0.3, CR[1] - 0.25), 0.0, True, [(39.70, "crew_pain")]),
            ("driver_lift", DS, 0.05, False, [(39.70, None)]),
            ("driver_lunge", (CR[0] - 0.3, CR[1] - 0.15), 0.0, False, [(39.411, None), (39.70, "driver_lunge")])],
      door=70),
 dict(id="S22", t0=41.261, t1=42.262, angle="Dutch 8 deg, eye level", what="'ก้องยังไม่รู้เลยว่า': Kong, unaware, the attack behind him",
      cam=[(41.261, (1.75, 4.2, 1.5), (-0.1, 7.3, 1.3), 22, 8), (42.262, (1.7, 4.35, 1.5), (-0.1, 7.3, 1.3), 22, 8)],
      shake=[(0.2, 1.0, 0.0)],
      cast=[("kong_tired", K0, 0.0, False), ("crew_pain", (CR[0] + 0.3, CR[1] - 0.25), 0.0, True),
            ("driver_lunge", (CR[0] - 0.3, CR[1] - 0.15), 0.0, False)], door=70),
 dict(id="S23", t0=42.262, t1=43.451, angle="Dutch low CU", what="'อีก 60 วินาที': the bitten crew member, clock starts",
      cam=[(42.262, (0.55, 6.85, 0.75), (-0.3, 8.05, 1.3), 22, 10), (43.451, (0.5, 6.95, 0.78), (-0.3, 8.05, 1.3), 22, 11)],
      shake=[(0.5, 3.0, 0.0)],
      cast=[("crew_pain", (CR[0] + 0.3, CR[1] - 0.25), 0.0, True), ("driver_lunge", (CR[0] - 0.3, CR[1] - 0.15), 0.0, False)], door=70),
 dict(id="S24", t0=43.451, t1=48.500, angle="high -> top-down, rising above the expressway", what="'เพื่อนของเขาจะไม่ใช่คนอีกต่อไป' + title from 45.9",
      cam=[(43.451, (0.2, 4.0, 6.5), (-0.6, 9.0, 0.5), 22, 0), (45.9, (0.0, 6.0, 26.0), (-0.6, 16.0, 0.0), 22, 0),
           (48.5, (0.0, 8.0, 46.0), (-0.6, 24.0, 0.0), 22, 0)],
      shake=[],
      cast=[("kong_tired", K0, 0.0, False), ("crew_pain", (CR[0] + 0.3, CR[1] - 0.25), 0.0, True),
            ("driver_lunge", (CR[0] - 0.3, CR[1] - 0.15), 0.0, False)], door=70),
]


# ---------------------------------------------------------------------------------------------------- v2 retime
# The literal times above are the v1 cut. Every shot is remapped linearly onto its v2 slot (timing.NEW, cut on the
# new caption boundaries), then the beats that must land on a word or a sound cue are pinned explicitly.
import timing as TM


def _retime():
    for sh in SHOTS:
        o0, o1 = sh["t0"], sh["t1"]
        n0, n1, _ = TM.NEW[sh["id"]]
        m = lambda t, o0=o0, o1=o1, n0=n0, n1=n1: n0 + (t - o0) * (n1 - n0) / (o1 - o0)
        sh["t0"], sh["t1"] = n0, n1
        sh["cam"] = [(m(k[0]),) + tuple(k[1:]) for k in sh["cam"]]
        sh["shake"] = [(e[0], e[1], m(e[2]) if e[2] > 0 else 0.0) + tuple(e[3:]) for e in sh.get("shake", [])]
        cast = []
        for e in sh["cast"]:
            if len(e) > 4 and isinstance(e[4], list):
                e = tuple(e[:4]) + ([(m(t), sp) for t, sp in e[4]],)
            cast.append(e)
        sh["cast"] = cast
        if sh.get("talk"):
            sh["talk"] = [(m(a), m(b)) for a, b in sh["talk"]]
        if sh.get("buzz"):
            sh["buzz"] = (m(sh["buzz"][0]), m(sh["buzz"][1]))
    S = {sh["id"]: sh for sh in SHOTS}
    # S20: hold level, slow push; driver lifts his head on 'เงยหน้าขึ้น' (41.657); Dutch only after the lift
    S["S20"]["cam"] = [(40.281, (-1.5, 10.80, 1.32), (-1.55, 8.35, 1.2), 30, 0),
                       (41.657, (-1.5, 10.55, 1.31), (-1.55, 8.35, 1.2), 30, 0),
                       (42.10, (-1.51, 10.45, 1.30), (-1.55, 8.35, 1.23), 30, 12),
                       (43.445, (-1.53, 10.20, 1.29), (-1.55, 8.35, 1.25), 30, 13)]
    S["S20"]["cast"] = [("driver_still", DS, 0.05, False, [(41.657, "driver_lift")])]
    # S21: lunge sound at 43.445 -> lunge sprite 2 frames after the cut, scream/bite at 43.795
    S["S21"]["shake"] = [(0.2, 1.0, 0.0), (3.0, 6.0, 43.53, 1.2)]
    S["S21"]["cast"] = [("crew_alarmed", (CR[0] + 0.3, CR[1] - 0.25), 0.0, True, [(43.795, "crew_pain")]),
                        ("driver_lift", DS, 0.05, False, [(43.53, None)]),
                        ("driver_lunge", (CR[0] - 0.3, CR[1] - 0.15), 0.0, False, [(43.445, None), (43.53, "driver_lunge")])]
    # S24: rises through the last line, keeps rising under the title (50.72 -> end)
    S["S24"]["cam"] = [(47.778, (0.2, 4.0, 6.5), (-0.6, 9.0, 0.5), 22, 0), (50.72, (0.0, 6.0, 26.0), (-0.6, 16.0, 0.0), 22, 0),
                       (53.32, (0.0, 8.0, 46.0), (-0.6, 24.0, 0.0), 22, 0)]


_retime()


def fr(t):
    return int(round(t * FPS))


# ---------------------------------------------------------------------------------------------------- scene
def setup_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    c = sc.cycles
    c.device = "CPU"
    c.samples = int(os.environ.get("SAMPLES", "5"))
    c.use_adaptive_sampling = False
    c.max_bounces = 3
    c.diffuse_bounces = 1
    c.glossy_bounces = 2
    c.transmission_bounces = 2
    c.transparent_max_bounces = 12
    c.caustics_reflective = False
    c.caustics_refractive = False
    c.sample_clamp_indirect = 4.0
    c.filter_width = 1.5
    try:
        c.use_denoising = os.environ.get("DENOISE", "1") == "1"
        c.denoiser = "OPENIMAGEDENOISE"
        c.denoising_prefilter = os.environ.get("PREFILTER", "FAST")
        try:
            c.denoising_quality = os.environ.get("DQ", "FAST")
        except Exception as e:
            print("no denoising_quality", e)
        c.denoising_input_passes = "RGB_ALBEDO"
    except Exception as e:
        print("denoiser unavailable:", e)
        c.use_denoising = False
    r = sc.render
    r.resolution_x, r.resolution_y, r.resolution_percentage = W, H, 100
    r.fps = FPS
    r.threads_mode = "FIXED"
    r.threads = 2
    r.film_transparent = False
    r.use_persistent_data = True
    r.image_settings.file_format = "PNG"
    r.image_settings.color_mode = "RGB"
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sc.view_settings.exposure = 0.0
    r.use_compositing = False
    sc.frame_start, sc.frame_end = 1, 1280
    return sc


def make_camera(sc):
    cd = bpy.data.cameras.new("cam")
    cd.sensor_fit = "VERTICAL"
    cd.sensor_height = 36.0
    cd.sensor_width = 36.0 * W / H
    cd.clip_start = 0.03
    cd.clip_end = 2500
    cam = bpy.data.objects.new("cam", cd)
    sc.collection.objects.link(cam)
    sc.camera = cam
    return cam


def look_quat(loc, target, roll):
    d = Vector(target) - Vector(loc)
    q = d.to_track_quat("-Z", "Y")
    return q @ Quaternion((0, 0, 1), math.radians(roll))


def smooth(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def cam_state(shot, t):
    keys = shot["cam"]
    if t <= keys[0][0]:
        k = keys[0]
        return Vector(k[1]), Vector(k[2]), k[3], k[4]
    for a, b in zip(keys, keys[1:]):
        if a[0] <= t <= b[0]:
            u = (t - a[0]) / max(1e-6, b[0] - a[0])
            # first segment of a multi-key shot that is short = snap (smoothstep); long segments ease gently
            u = smooth(u) if (b[0] - a[0]) < 0.8 else 0.35 * u + 0.65 * smooth(u)
            return (Vector(a[1]).lerp(Vector(b[1]), u), Vector(a[2]).lerp(Vector(b[2]), u),
                    a[3] + (b[3] - a[3]) * u, a[4] + (b[4] - a[4]) * u)
    k = keys[-1]
    return Vector(k[1]), Vector(k[2]), k[3], k[4]


def shake_at(shot, t):
    """sum of sines handheld; entries (amp_deg, hz, t_from[, decay_s])."""
    yaw = pit = rol = 0.0
    for e in shot.get("shake", []):
        amp, hz, tf = e[0], e[1], e[2]
        if t < tf:
            continue
        k = 1.0
        if len(e) > 3:
            k = max(0.0, 1.0 - (t - tf) / e[3])
        w = 2 * math.pi * hz
        yaw += amp * k * (0.6 * math.sin(w * t + 1.1) + 0.4 * math.sin(2.3 * w * t + 0.3))
        pit += amp * k * (0.6 * math.sin(1.3 * w * t + 2.0) + 0.4 * math.sin(2.9 * w * t + 0.7))
        rol += 0.5 * amp * k * math.sin(0.7 * w * t + 0.4)
    return yaw, pit, rol


def key_camera(cam, shot, frames):
    for g in frames:
        t = g / FPS
        loc, tgt, lens, roll = cam_state(shot, t)
        yaw, pit, rol = shake_at(shot, t)
        q = look_quat(loc, tgt, roll + rol)
        q = q @ Euler((math.radians(pit), math.radians(yaw), 0), "XYZ").to_quaternion()
        cam.location = loc
        cam.rotation_mode = "QUATERNION"
        cam.rotation_quaternion = q
        cam.data.lens = lens
        cam.keyframe_insert("location", frame=g + 1)
        cam.keyframe_insert("rotation_quaternion", frame=g + 1)
        cam.data.keyframe_insert("lens", frame=g + 1)


# ---------------------------------------------------------------------------------------------------- cast cards
def card(name, sprite, feet_xy, z0, flip, cam):
    m = META[sprite]
    x0, y0, x1, y1 = m["canvas"]
    fy = m["feet_y"]
    w = (x1 - x0) * D
    top = (fy - y0) * D
    bot = (y1 - fy) * D
    me = bpy.data.meshes.new(name)
    v = [(x0 * D, 0, -bot), (x1 * D, 0, -bot), (x1 * D, 0, top), (x0 * D, 0, top)]
    me.from_pydata(v, [], [(0, 1, 2, 3)])
    uvl = me.uv_layers.new()
    for i, c in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]):
        uvl.data[i].uv = c
    me.materials.append(SB.card_material("card_" + sprite, os.path.join(SPR, sprite + ".png")))
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = (feet_xy[0], feet_xy[1], z0)
    if flip:
        ob.scale = (-1, 1, 1)
    ob.visible_shadow = False
    ob.visible_diffuse = False
    ob.visible_glossy = True          # shows in the wet road
    ob.visible_transmission = True
    con = ob.constraints.new("LOCKED_TRACK")
    con.target = cam
    con.track_axis = "TRACK_NEGATIVE_Y"
    con.lock_axis = "LOCK_Z"
    return ob


def build_cast(shot, cam, frames):
    """each cast entry: (sprite, feet_xy, z0, flip[, swaps]) where swaps is a list of (t, sprite|None) or "talk"."""
    objs = []
    for ci, e in enumerate(shot["cast"]):
        sprite, pos, z0, flip = e[:4]
        swaps = e[4] if len(e) > 4 else []
        # timeline of sprite per frame
        tl = {}
        for g in frames:
            t = g / FPS
            s = sprite
            if swaps == "talk":
                talking = any(a <= t < b for a, b in shot.get("talk", []))
                if talking and (g // 3) % 3 != 2 and ENV[min(g, len(ENV) - 1)] > 0.12:
                    s = sprite + "_talk" if sprite + "_talk" in META else sprite
            else:
                for (ts, sp) in swaps:
                    if t >= ts:
                        s = sp
            tl[g] = s
        sprites_used = sorted(set(v for v in tl.values() if v))
        for sp in sprites_used:
            ob = card("c%d_%s" % (ci, sp), sp, pos, z0, flip, cam)
            objs.append(ob)
            prev = None
            for g in frames:
                hide = tl[g] != sp
                if hide != prev:
                    ob.hide_render = hide
                    ob.keyframe_insert("hide_render", frame=g + 1)
                    prev = hide
            # phone buzz jitter
            if shot.get("buzz"):
                b0, b1 = shot["buzz"]
                for g in frames:
                    t = g / FPS
                    j = 0.012 * math.sin(t * 2 * math.pi * 15) if b0 <= t < b1 and ((t - b0) % 0.4) < 0.25 else 0.0
                    ob.location = (pos[0] + j, pos[1], z0)
                    ob.keyframe_insert("location", frame=g + 1)
    return objs


# ---------------------------------------------------------------------------------------------------- props
def radio_prop():
    objs = []
    body = SB.principled("radio_body", hexcol("#1d1e24"), rough=0.35)
    R = Vector((0.10, 6.20, 1.15))
    vestm = SB.principled("vest", hexcol("#6e2c0e"), rough=0.55)
    objs.append(SB.box("vest_block", (0.9, 0.16, 0.9), R + Vector((0, 0.12, -0.1)), vestm, 0.08))
    stripe = SB.principled("reflect", hexcol("#b5bcc6"), rough=0.25, metal=0.5)
    objs.append(SB.box("vest_stripe", (0.92, 0.03, 0.07), R + Vector((0, 0.035, -0.16)), stripe, 0.0))
    objs.append(SB.box("strap", (0.06, 0.03, 0.6), R + Vector((0.0, 0.04, 0.05)), SB.principled("strap", hexcol("#26262c"), 0.7), 0.0))
    objs.append(SB.box("radio", (0.065, 0.04, 0.13), R, body, 0.008))
    for i in range(5):
        objs.append(SB.box("grille%d" % i, (0.045, 0.004, 0.004), R + Vector((0, -0.021, 0.035 - i * 0.01)),
                           SB.principled("grille", hexcol("#0b0b0e"), 0.5), 0.0))
    objs.append(SB.cyl("antenna", 0.006, 0.12, R + Vector((-0.018, 0, 0.12)), body))
    led = SB.emission("radio_led", hexcol("#ff2015"), 1.0)
    objs.append(SB.box("led", (0.01, 0.006, 0.006), R + Vector((0.018, -0.021, 0.055)), led, 0.0))
    node = led.node_tree.nodes["Emission"].inputs["Strength"]
    for g in range(0, 86):
        e = ENV[g] if g < 82 else 0.0
        if 60 <= g < 82:                                  # stutter on 'เฮ้ย!'
            e = e if (g // 2) % 2 == 0 else 0.0
        node.default_value = 2.0 + 120.0 * e if g < 82 else 0.0
        node.keyframe_insert("default_value", frame=g + 1)
    return objs


def cutter_prop(t_bars=(16.30, 16.50, 16.70)):
    objs = []
    C = Vector((0.55, 6.05, 0.74))
    orange = SB.principled("cutter_orange", hexcol("#e06a1c"), rough=0.35)
    steel = SB.principled("steel", hexcol("#9aa0a8"), rough=0.25, metal=0.9)
    black = SB.principled("cutter_black", hexcol("#141418"), rough=0.5)
    glove = SB.principled("glove", hexcol("#18171c"), rough=0.8)
    objs.append(SB.box("cut_body", (0.12, 0.42, 0.14), C, orange, 0.03))
    objs.append(SB.box("cut_jaw1", (0.03, 0.28, 0.05), C + Vector((0.02, 0.32, 0.02)), steel, 0.01, rot=(0, 0, math.radians(6))))
    objs.append(SB.box("cut_jaw2", (0.03, 0.28, 0.05), C + Vector((-0.02, 0.32, 0.02)), steel, 0.01, rot=(0, 0, math.radians(-6))))
    objs.append(SB.box("cut_handle", (0.05, 0.22, 0.05), C + Vector((0, -0.25, 0.1)), black, 0.015))
    objs.append(SB.box("cut_batt", (0.11, 0.16, 0.1), C + Vector((0, -0.2, -0.08)), black, 0.015))
    objs.append(SB.box("glove", (0.11, 0.12, 0.1), C + Vector((0, -0.25, 0.13)), glove, 0.03))
    objs.append(SB.box("sleeve", (0.16, 0.5, 0.16), C + Vector((0.0, -0.55, 0.22)), SB.principled("vest", hexcol("#9a3c12"), 0.55), 0.05,
                       rot=(math.radians(-25), 0, 0)))
    for i, tb in enumerate(t_bars):
        m = SB.emission("bar%d" % i, hexcol("#2fdc3f"), 1.0)
        objs.append(SB.box("bar%d" % i, (0.005, 0.03, 0.018), C + Vector((0.057, -0.25 + i * 0.04, -0.08)), m, 0.0))
        s = m.node_tree.nodes["Emission"].inputs["Strength"]
        s.default_value = 0.05
        s.keyframe_insert("default_value", frame=1)
        s.default_value = 0.05
        s.keyframe_insert("default_value", frame=fr(tb))
        s.default_value = 18.0
        s.keyframe_insert("default_value", frame=fr(tb) + 1)
    return objs


def phone_prop(state, pos, tilt):
    objs = []
    P = Vector(pos)
    root = SB.empty("phone_root", P, (math.radians(tilt), 0, 0))
    objs.append(root)
    blk = SB.principled("phone_black", hexcol("#0c0c10"), rough=0.2, metal=0.3)
    b = SB.box("phone_body", (0.075, 0.155, 0.009), (0, 0, 0), blk, 0.006, parent=root)
    objs.append(b)
    scr = SB.image_emission_material("screen_" + state, os.path.join(HERE, "tex", "screen_%s.png" % state), 1.0, alpha=True)
    # plane in XZ -> rotate to XY (facing +Z)
    p = SB.plane("phone_screen", 0.068, 0.145, (0, 0, 0.0051), scr, rot=(math.radians(-90), 0, 0), parent=root)
    # flip so the image is upright when the phone top is +Y
    p.rotation_euler = (math.radians(90), 0, math.radians(180))
    p.scale = (-1, 1, 1)
    objs.append(p)
    glove = SB.principled("glove", hexcol("#18171c"), rough=0.8)
    objs.append(SB.box("phone_glove", (0.1, 0.1, 0.05), (0.0, -0.06, -0.03), glove, 0.025, parent=root))
    objs.append(SB.box("phone_sleeve", (0.13, 0.4, 0.13), (0.0, -0.3, -0.07), SB.principled("vest", hexcol("#9a3c12"), 0.55), 0.04, parent=root))
    return objs


# ---------------------------------------------------------------------------------------------------- render
def clear_keys(ob):
    if ob.animation_data:
        ob.animation_data_clear()


def main():
    args = sys.argv[1:]
    test = "--test" in args
    only = None
    if "--only" in args:
        only = set(args[args.index("--only") + 1].split(","))
    sc = setup_scene()
    SB.build(sc)
    SB.merge_static(sc)
    print("objects after merge:", len(sc.collection.objects), flush=True)
    cam = make_camera(sc)
    SB.rain_rig(sc, cam)
    hinge = bpy.data.objects["sedan_hinge"]
    out_dir = os.path.join(HERE, "test2" if test else "render_v2")
    os.makedirs(out_dir, exist_ok=True)
    log = []
    for shot in SHOTS:
        if only and shot["id"] not in only:
            continue
        g0, g1 = fr(shot["t0"]), fr(shot["t1"])
        frames = list(range(g0, g1))
        if test:
            frames = [(g0 + g1) // 2] if "--mid" not in args else [g0, (g0 + g1) // 2, g1 - 1]
        clear_keys(cam); clear_keys(cam.data)
        key_camera(cam, shot, frames)
        hinge.rotation_euler = (0, 0, math.radians(shot.get("door", 0)))
        temp = build_cast(shot, cam, frames)
        if shot.get("radio"):
            temp += radio_prop()
        if shot.get("cutter"):
            temp += cutter_prop()
        if shot.get("phone"):
            temp += phone_prop(*shot["phone"])
        t_start = time.time()
        for g in frames:
            sc.frame_set(g + 1)
            sc.render.filepath = os.path.join(out_dir, ("%s_%04d.png" % (shot["id"], g + 1)) if test else ("f_%04d.png" % (g + 1)))
            if not test and os.path.exists(sc.render.filepath) and "--force" not in args:
                continue
            t_f = time.time()
            bpy.ops.render.render(write_still=True)
            if "--timing" in args:
                print("FRAME", g + 1, round(time.time() - t_f, 2), flush=True)
        dt = time.time() - t_start
        log.append({"id": shot["id"], "frames": len(frames), "sec": round(dt, 1)})
        print("SHOT", shot["id"], len(frames), "frames", round(dt, 1), "s", flush=True)
        for ob in temp:
            bpy.data.objects.remove(ob, do_unlink=True)
    json.dump(log, open(os.path.join(out_dir, "_log.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
