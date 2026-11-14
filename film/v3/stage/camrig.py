"""camrig.py -- the v3 camera: one 22 mm lens, keyed poses, and the measured move grammar (bpy 5.3).

World convention: 1 unit = 1 D (head diameter), Z up, floor z = 0, map wall = plane y = 0, the room is at negative y.
Lens 22 mm on a 36 mm sensor, sensor fit AUTO, 720x1280: focal length 782.2 px, 49.4 deg horizontal, 78.6 deg vertical;
an object of size 1 D at planar depth z covers 782.2 / z px.

A camera "pose" is a dict: {"loc": (x, y, z), "rot": Euler} or {"loc": ..., "look_at": (x, y, z), "roll": deg}, optional
"lens": mm.  cam_for() returns such dicts; drift / snap / whip take them.

Every key is written through key() below: the per-keyframe-point helper of spec/camera_motion.md 3.3 (the user-preference
trick does nothing in 5.3 and action.fcurves is gone).  The interpolation of a key governs the segment that STARTS there.
"""
import math
import bpy
from mathutils import Euler, Matrix, Quaternion, Vector

LENS = 22.0
SENSOR = 36.0
RES_X, RES_Y = 720, 1280
FPS = 30
FOCAL_PX = max(RES_X, RES_Y) * LENS / SENSOR          # 782.22 px (AUTO fit: the sensor width lies along the long side)

_LAST_EULER = {}       # camera name -> last keyed Euler (keeps successive keys on the same branch, no 360 degree spins)


# ----------------------------------------------------------------------------- keys (camera_motion.md 3.3)
def fcurves_of(idblock):
    ad = idblock.animation_data
    out = []
    if ad is None or ad.action is None:
        return out
    for layer in ad.action.layers:
        for strip in layer.strips:
            cb = strip.channelbag(ad.action_slot)
            if cb:
                out += list(cb.fcurves)
    return out


def key(idblock, path, frame, value, interp="SINE", easing="EASE_IN_OUT"):
    """set `path` on an object / camera data block, insert a keyframe and stamp interpolation + easing on that keyframe
    point of every channel.  interp: CONSTANT LINEAR BEZIER SINE QUAD CUBIC QUART QUINT EXPO CIRC BACK; easing: AUTO
    EASE_IN EASE_OUT EASE_IN_OUT."""
    setattr(idblock, path, value)
    idblock.keyframe_insert(path, frame=frame)
    for fc in fcurves_of(idblock):
        if fc.data_path == path:
            pts = fc.keyframe_points
            for i in range(len(pts) - 1, -1, -1):          # the new key is usually the last one
                kp = pts[i]
                if abs(kp.co.x - frame) < 0.5:
                    kp.interpolation = interp
                    kp.easing = easing
                    break


def clear_keys(idblock):
    """remove every key of an object or data block (start a shot from scratch)."""
    if idblock.animation_data is not None:
        idblock.animation_data_clear()
    _LAST_EULER.pop(getattr(idblock, "name", None), None)


# ----------------------------------------------------------------------------- camera object
def make_camera(scene=None, name="StageCam", lens=LENS):
    """camera with the reference lens; becomes scene.camera; also sets 720x1280, 30 fps on the scene."""
    scene = scene or bpy.context.scene
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.sensor_width = SENSOR
    cd.sensor_fit = "AUTO"
    cd.clip_start = 0.05
    cd.clip_end = 500.0
    cd.dof.use_dof = False
    cam = bpy.data.objects.new(name, cd)
    cam.rotation_mode = "XYZ"
    scene.collection.objects.link(cam)
    scene.camera = cam
    scene.render.resolution_x, scene.render.resolution_y = RES_X, RES_Y
    scene.render.fps = FPS
    return cam


def _cam(cam):
    return cam if cam is not None else bpy.context.scene.camera


def focal_px(lens=LENS):
    return max(RES_X, RES_Y) * lens / SENSOR


def look_rotation(loc, look_at, roll=0.0):
    """Euler (XYZ) of a camera at `loc` looking at `look_at`, horizon level, then rolled by `roll` degrees."""
    d = Vector(look_at) - Vector(loc)
    if d.length < 1e-9:
        d = Vector((0.0, 1.0, 0.0))
    q = d.to_track_quat("-Z", "Y")
    if roll:
        q = q @ Quaternion((0.0, 0.0, 1.0), math.radians(roll))
    return q.to_euler("XYZ")


def basis_rotation(yaw_deg, pitch_deg, roll=0.0):
    """Euler of a camera whose view direction is yaw_deg clockwise from +Y (seen from above; positive looks toward +X)
    and pitch_deg above the horizon."""
    y, p = math.radians(yaw_deg), math.radians(pitch_deg)
    f = Vector((math.sin(y) * math.cos(p), math.cos(y) * math.cos(p), math.sin(p)))
    r = Vector((math.cos(y), -math.sin(y), 0.0))
    u = r.cross(f)
    m = Matrix((r, u, -f)).transposed()               # columns: camera X (right), Y (up), Z (backward)
    q = m.to_quaternion()
    if roll:
        q = q @ Quaternion((0.0, 0.0, 1.0), math.radians(roll))
    return q.to_euler("XYZ")


def _resolve(pose):
    """pose dict -> (Vector loc, Quaternion rot, lens or None)."""
    loc = Vector(pose["loc"])
    if pose.get("rot") is not None:
        r = pose["rot"]
        q = (r if isinstance(r, Euler) else Euler(tuple(r), "XYZ")).to_quaternion()
    elif pose.get("look_at") is not None:
        q = look_rotation(loc, pose["look_at"], pose.get("roll", 0.0)).to_quaternion()
    else:
        raise ValueError("camera pose needs 'rot' or 'look_at'")
    return loc, q, pose.get("lens")


def key_camera(frame, loc, look_at=None, rotation=None, lens=None, roll=0.0, cam=None, interp="SINE", easing="EASE_IN_OUT"):
    """key the camera on `frame`: position `loc` and either `look_at` (a world point; horizon level plus `roll` degrees)
    or `rotation` (Euler XYZ in radians, as camera.rotation_euler; a mathutils Euler or Quaternion given as the third
    positional argument is taken as the rotation too).  `lens` in mm keys the focal length too (leave None to
    stay on 22 mm).  interp / easing shape the move from this key to the next one."""
    cam = _cam(cam)
    if isinstance(look_at, (Euler, Quaternion)):            # key_camera(frame, loc, some_euler): a rotation, not a point
        rotation, look_at = look_at, None
    if isinstance(rotation, Quaternion):
        rotation = rotation.to_euler("XYZ")
    if rotation is not None:
        eul = Euler(tuple(rotation), "XYZ")
        if roll:
            eul = (eul.to_quaternion() @ Quaternion((0.0, 0.0, 1.0), math.radians(roll))).to_euler("XYZ")
    elif look_at is not None:
        eul = look_rotation(loc, look_at, roll)
    else:
        raise ValueError("key_camera needs look_at or rotation")
    prev = _LAST_EULER.get(cam.name)
    if prev is not None:
        eul.make_compatible(prev)
    _LAST_EULER[cam.name] = eul.copy()
    key(cam, "location", frame, Vector(loc), interp, easing)
    key(cam, "rotation_euler", frame, eul, interp, easing)
    if lens is not None:
        key(cam.data, "lens", frame, float(lens), interp, easing)
    return cam


def key_pose(frame, pose, cam=None, interp="SINE", easing="EASE_IN_OUT"):
    loc, q, lens = _resolve(pose)
    return key_camera(frame, loc, rotation=q.to_euler("XYZ"), lens=lens, cam=cam, interp=interp, easing=easing)


# ----------------------------------------------------------------------------- easing
def ease_sine(u):
    return 0.5 - 0.5 * math.cos(math.pi * u)


def ease_quintic(u):                 # smootherstep, peak speed 1.875 x mean
    return u * u * u * (u * (6.0 * u - 15.0) + 10.0)


def ease_septic(u):                  # peak speed 2.1875 x mean
    return u ** 4 * (35.0 - 84.0 * u + 70.0 * u * u - 20.0 * u ** 3)


def ease_peak(u, peak=1.7):
    """ease in-out whose peak speed is `peak` times its mean speed: 1.571 = sine, 1.875 = quintic, up to 2.19.
    The reference snaps measure 1.56 to 2.09 (median about 1.7)."""
    u = 0.0 if u < 0.0 else 1.0 if u > 1.0 else u
    a, b, c = math.pi / 2.0, 1.875, 2.1875
    if peak <= a:
        return ease_sine(u)
    if peak <= b:
        w = (peak - a) / (b - a)
        return (1.0 - w) * ease_sine(u) + w * ease_quintic(u)
    w = min(1.0, (peak - b) / (c - b))
    return (1.0 - w) * ease_quintic(u) + w * ease_septic(u)


def _mix_pose(p0, p1, e, pivot=None):
    l0, q0, z0 = p0
    l1, q1, z1 = p1
    q = q0.slerp(q1, e)
    if pivot is not None:
        pv = Vector(pivot)
        d0, d1 = l0 - pv, l1 - pv
        r0, r1 = max(d0.length, 1e-6), max(d1.length, 1e-6)
        r = r0 * (r1 / r0) ** e                                   # a push that looks even is exponential in distance
        dq = d0.normalized().rotation_difference(d1.normalized())
        loc = pv + (Quaternion().slerp(dq, e) @ d0.normalized()) * r
    else:
        loc = l0.lerp(l1, e)
    lens = None
    if z0 is not None or z1 is not None:
        a, b = (z0 or LENS), (z1 or LENS)
        lens = a * (b / a) ** e
    return loc, q, lens


def _bake(f0, f1, pose0, pose1, fn, cam, pivot=None):
    cam = _cam(cam)
    p0, p1 = _resolve(pose0), _resolve(pose1)
    n = max(1, int(f1) - int(f0))
    for i in range(n + 1):
        loc, q, lens = _mix_pose(p0, p1, fn(i / float(n)), pivot)
        key_camera(int(f0) + i, loc, rotation=q.to_euler("XYZ"), lens=lens, cam=cam, interp="LINEAR", easing="AUTO")
    return cam


# ----------------------------------------------------------------------------- the measured moves
def drift(f0, f1, pose0, pose1, ease="sine", cam=None):
    """the slow primary move of a shot (6 to 10 percent per second push or pull, 20 to 60 px per second slide), two keys.
    ease="sine": SINE in-out, velocity 0 at both ends (shot inside dissolves).  ease="cubic_out": already moving on f0 and
    settling to rest at f1 (shot that starts on a cut).  ease="linear" exists for tests only.  After f1 the camera holds.
    Template: f1 = last frame of the shot - 12."""
    interp, easing = {"sine": ("SINE", "EASE_IN_OUT"), "cubic_out": ("CUBIC", "EASE_OUT"), "quad_out": ("QUAD", "EASE_OUT"),
                      "linear": ("LINEAR", "AUTO")}[ease]
    key_pose(f0, pose0, cam, interp, easing)
    key_pose(f1, pose1, cam, interp, easing)
    return _cam(cam)


def snap(f0, f1, pose0, pose1, peak=1.7, pivot=None, cam=None):
    """snap push / pull / reframing over f0..f1 (14 to 24 frames): ease in-out between sine and quintic with peak speed
    `peak` x the mean (measured 1.56 to 2.09).  One key per frame (LINEAR between them) so the curve is exact.
    pivot = the subject's world point: the distance to it changes geometrically (an even-looking push) and the camera
    swings around it; without a pivot the position is interpolated on a straight line.  Rotation is slerped."""
    return _bake(f0, f1, pose0, pose1, lambda u: ease_peak(u, peak), cam, pivot)


def whip(f0, f1, pose0, pose1, cam=None):
    """whip pan between two poses, sine in-out (7 to 20 frames, 600 to 1300 px)."""
    return _bake(f0, f1, pose0, pose1, ease_sine, cam)


def _panned(pose, pan_deg):
    loc, q, lens = _resolve(pose)
    q2 = Quaternion((0.0, 0.0, 1.0), -math.radians(pan_deg)) @ q         # positive pan = the view turns toward +X (right)
    return {"loc": loc, "rot": q2.to_euler("XYZ"), "lens": lens}


def whip_off(f0, f1, pose, pan_deg, cam=None):
    """leave a shot: pan away by pan_deg (positive = to the right), accelerating (quadratic ease-in), 3 to 5 frames.
    Cut on f1 + 1 and start the next shot with whip_on in the same direction."""
    return _bake(f0, f1, pose, _panned(pose, pan_deg), lambda u: u * u, cam)


def whip_on(f0, f1, pose, pan_deg, cam=None):
    """enter a shot still travelling: start pan_deg short of `pose` and brake hard into it (quartic ease-out)."""
    return _bake(f0, f1, _panned(pose, -pan_deg), pose, lambda u: 1.0 - (1.0 - u) ** 4, cam)


def shake(f0, f1, amp_deg=0.45, every=3, seed=1, cam=None):
    """storm / wave shake: adds random pan and tilt keys every `every` frames on top of the pose the camera already has at
    those frames (5 Hz at every=3; 0.45 deg = about 12 px standard deviation at 782 px focal length)."""
    cam = _cam(cam)
    scene = bpy.context.scene
    s = (int(seed) * 2654435761 + 12345) & 0xFFFFFFFF

    def rnd():
        nonlocal s
        s = (s * 1664525 + 1013904223) & 0xFFFFFFFF
        return ((s >> 8) & 0xFFFF) / 32767.5 - 1.0
    poses = []
    for f in range(int(f0), int(f1) + 1, every):
        scene.frame_set(f)
        poses.append((f, cam.matrix_world.to_translation().copy(), cam.matrix_world.to_quaternion().copy()))
    for i, (f, loc, q) in enumerate(poses):
        k = 0.0 if i in (0, len(poses) - 1) else 1.0
        q2 = q @ Quaternion((1.0, 0.0, 0.0), math.radians(amp_deg * 1.7 * k * rnd())) @ Quaternion((0.0, 1.0, 0.0), math.radians(amp_deg * 1.7 * k * rnd()))
        key_camera(f, loc, rotation=q2.to_euler("XYZ"), cam=cam, interp="LINEAR", easing="AUTO")
    return cam


# ----------------------------------------------------------------------------- placement from the measured framing
HEIGHT_CLASSES = {
    # camera height rule, pitch of the view axis (deg, + = looking up), measured on the reference (LOOK_SPEC 5.2):
    "low":  dict(above="floor", h=1.20, pitch=13.5),      # a/t16.0: 1.16 D above the ground, pitched up 12 to 15 deg
    "eye":  dict(above="head", h=0.30, pitch=-3.0),       # a/t20.0: head-centre height + 0 to 0.3 D, 2 to 5 deg down
    "high": dict(above="head", h=None, pitch=-15.0),      # a/t58.5, b/t10.0, b/t42.0: 2 to 3.5 D above the head, 15 deg down
                                                          # (h = 0.417 x depth, clamped to 2 .. 3.5 D: head centre near 0.60 H)
    "top":  dict(above="head", h=None, pitch=-90.0),      # b/t52.0: straight down
}


def cam_for(subject_point, head_px, height_class="eye", yaw_deg=0.0, D=1.0, floor_z=0.0, screen_x=360.0,
            pitch_deg=None, cam_height=None, lens=LENS, screen_y=None):
    """Camera pose that shows a head of diameter D at `subject_point` (the head centre, world) `head_px` pixels wide:
    planar depth = 782.2 x D / head_px.

    height_class  "low"  camera 1.2 D above the floor, view axis pitched up 13.5 deg (figure against ceiling or sky)
                  "eye"  camera 0.3 D above the head centre, pitched 3 deg down (dialogue default)
                  "high" camera 2 to 3.5 D above the head centre (0.417 x depth: the head lands near 0.60 H at the
                         reference distances of 5 to 8 D), pitched 15 deg down
                  "top"  camera straight above, looking down
    yaw_deg       direction the camera looks, clockwise from +Y seen from above: 0 looks at the map wall square on,
                  +20 looks toward +X (the camera stands to the LEFT of the subject), -20 the opposite
    screen_x      pixel column where the head centre lands (360 = centred; a two-shot wants about 200 or 480)
    pitch_deg, cam_height   override the class (cam_height = absolute world z of the camera)
    screen_y      pixel row (from the top) where the head centre must land: the pitch is solved for it instead of taken
                  from the class (the camera height rule is kept).  Keep heads between y = 300 and 760; captions sit at 900.
    Returns {"loc", "rot" (Euler XYZ), "lens", "look_at" (point on the view axis at the subject's depth), "depth",
             "subject_px" (x, y from the top), "pitch_deg", "yaw_deg"}; pass it to key_pose / drift / snap."""
    S = Vector(subject_point)
    F = focal_px(lens)
    zd = F * D / float(head_px)
    hc = HEIGHT_CLASSES[height_class]
    pitch = hc["pitch"] if pitch_deg is None else float(pitch_deg)
    y, p = math.radians(yaw_deg), math.radians(pitch)
    X = (screen_x - RES_X / 2.0) * zd / F
    if abs(math.cos(p)) < 1e-4:                                  # straight down (or up): "up" on screen = the yaw direction
        sgn = -1.0 if p < 0 else 1.0
        f = Vector((0.0, 0.0, sgn))
        u = Vector((math.sin(y), math.cos(y), 0.0)) * (-sgn)
        r = f.cross(u)                                           # camera X = forward x up (right-handed: X x Y = Z = -forward)
        Y = 0.0
    else:
        f = Vector((math.sin(y) * math.cos(p), math.cos(y) * math.cos(p), math.sin(p)))
        r = Vector((math.cos(y), -math.sin(y), 0.0))
        u = r.cross(f)
        if cam_height is not None:
            cz = float(cam_height)
        elif hc["above"] == "floor":
            cz = floor_z + hc["h"] * D
        elif hc["h"] is None:                                    # "high"
            cz = S.z + max(2.0, min(3.5, 0.417 * zd / D)) * D
        else:
            cz = S.z + hc["h"] * D
        if screen_y is not None:                                 # solve the pitch: Y cos p + zd sin p = S.z - cz
            Yw = (RES_Y / 2.0 - float(screen_y)) * zd / F
            R = math.hypot(Yw, zd)
            p = math.asin(max(-1.0, min(1.0, (S.z - cz) / R))) - math.atan2(Yw, zd)
            pitch = math.degrees(p)
            f = Vector((math.sin(y) * math.cos(p), math.cos(y) * math.cos(p), math.sin(p)))
            u = r.cross(f)
        Y = (S.z - cz - zd * math.sin(p)) / math.cos(p)
    loc = S - r * X - u * Y - f * zd
    m = Matrix((r, u, -f)).transposed()
    return {"loc": loc, "rot": m.to_euler("XYZ"), "lens": lens, "look_at": loc + f * zd, "depth": zd,
            "subject_px": (screen_x, RES_Y / 2.0 - F * Y / zd), "pitch_deg": pitch, "yaw_deg": yaw_deg,
            "height_class": height_class}


def dolly(pose, right=0.0, up=0.0, forward=0.0, pan_deg=0.0, tilt_deg=0.0):
    """a pose moved in its own axes (D units): right, up (world Z), forward (along the horizontal view direction), then
    panned (deg, + = right) and tilted (deg, + = up).  For the sideways truck that gives parallax."""
    loc, q, lens = _resolve(pose)
    m = q.to_matrix()
    r = Vector((m[0][0], m[1][0], 0.0))
    if r.length < 1e-6:
        r = Vector((1.0, 0.0, 0.0))
    r.normalize()
    fwd = Vector((0.0, 0.0, 1.0)).cross(r)
    loc2 = loc + r * right + Vector((0.0, 0.0, up)) + fwd * forward
    q2 = Quaternion((0.0, 0.0, 1.0), -math.radians(pan_deg)) @ q @ Quaternion((1.0, 0.0, 0.0), math.radians(tilt_deg))
    return {"loc": loc2, "rot": q2.to_euler("XYZ"), "lens": lens}
