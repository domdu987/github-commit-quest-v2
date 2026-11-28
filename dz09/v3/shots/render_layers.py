#!/usr/bin/env python3
"""render_layers.py -- for the frames that post.py streaks: a plate without the actors and a matte of the actors,
so that the set can be streaked along the camera motion while the characters stay sharp (reference: "the plate streaks
when it travels more than about 40 px per frame; characters stay sharp").

    python3 render_layers.py A|B <raw_dir> [--frames a:b] [--samples 12] [--threads 4]

  <raw_dir>/plate/f_%04d.png   the same 3D frame with the actor cards hidden from the camera only (their shadows stay)
  <raw_dir>/matte/f_%04d.png   RGBA, alpha = the actors as the camera sees them (the set is a holdout, so furniture in
                               front of an actor cuts the matte)
Frames come from post.streak_list() (camera faster than STREAK_MIN and not part of the whip pan) unless --frames is given.
"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("take"); ap.add_argument("raw")
    ap.add_argument("--frames", default=None); ap.add_argument("--samples", type=int, default=12); ap.add_argument("--threads", type=int, default=4)
    a = ap.parse_args()
    import bpy, film, post
    from probe import parse
    g0, g1 = film.TAKES[a.take]
    gs = parse(a.frames) if a.frames else [g for g, whip in post.streak_list() if not whip]
    gs = [g for g in gs if g0 <= g <= g1]
    if not gs:
        print("render_layers: nothing to do for take", a.take); return
    F = film.Film(a.take)
    F.pose(gs)
    sc = F.scene
    plate, matte = os.path.join(a.raw, "plate"), os.path.join(a.raw, "matte")
    R = film.render
    cards = [ac.card for ac in F.actors]
    decals = [ac.contact for ac in F.actors if getattr(ac, "contact", None) is not None]
    set_obs = [ob for ob in sc.objects if ob not in cards and ob.type in ("MESH", "CURVE") and not ob.name.endswith("_shadow")]
    for g in gs:
        f = g + 1
        # ---- plate: cards invisible to the camera, everything else as in the film frame
        for c in cards:
            c.visible_camera = False
        R.render_frames([f], plate, threads=a.threads, scene=sc, camera=F.cam, on_frame=F.on_frame, verbose=False, check=False)
        for c in cards:
            c.visible_camera = True
        # ---- matte: transparent film, the set as holdout, no compositor
        keep = (sc.render.film_transparent, sc.render.image_settings.color_mode, sc.render.use_compositing, sc.cycles.samples)
        sc.render.film_transparent = True; sc.render.image_settings.color_mode = "RGBA"; sc.render.use_compositing = False; sc.cycles.samples = 4
        hold = [(ob, ob.is_holdout) for ob in set_obs]
        for ob, _ in hold:
            ob.is_holdout = True
        hid = [(d, d.hide_render) for d in decals]
        for d, _ in hid:
            d.hide_render = True
        R.render_frames([f], matte, threads=a.threads, scene=sc, camera=F.cam, on_frame=F.on_frame, verbose=False, check=False)
        for ob, v in hold:
            ob.is_holdout = v
        for d, v in hid:
            d.hide_render = v
        sc.render.film_transparent, sc.render.image_settings.color_mode, sc.render.use_compositing, sc.cycles.samples = keep
        print("layers g %d" % g, flush=True)


if __name__ == "__main__":
    main()
