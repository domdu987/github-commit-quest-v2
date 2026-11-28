import sys, os, time, resource, json
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
import bpy, expressway as X, standins
A = X.build(haze_cards=False); X.setup_render(quality="final", threads=2)
for o in bpy.data.objects:
    if o.get("fx") == "cone": o.hide_render = True; acts = standins.place(A)
cam = X.use_camera("eye", "9:16", scale=1.0); bpy.context.view_layer.update(); standins.pose_all(acts, cam)
sc = bpy.context.scene; cy = sc.cycles
def cpu(): r = resource.getrusage(resource.RUSAGE_SELF); return r.ru_utime + r.ru_stime
def run(tag):
    c0 = cpu(); w0 = time.time(); bpy.ops.render.render(write_still=False); print(tag, round(cpu()-c0,1), round(time.time()-w0,1), flush=True)
variants = sys.argv[1].split(",")
for v in variants:
    if v == "sync": p = sc.render.resolution_percentage; sc.render.resolution_percentage = 2; run(v); sc.render.resolution_percentage = p
    elif v == "base": run(v)
    elif v == "tb6": cy.transparent_max_bounces = 6; run(v)
    elif v == "nodn": cy.use_denoising = False; run(v); cy.use_denoising = True
    elif v == "fx":
        hid=[o for o in bpy.data.objects if o.name.startswith(("cone_","flood_beam","steam","smoke","haze","plume")) and not o.hide_render]
        for o in hid: o.hide_render=True
        run(v+str(len(hid)))
        for o in hid: o.hide_render=False
    elif v.startswith("vis"):
        fx=[o for o in bpy.data.objects if o.name.startswith(("cone_","flood_beam","steam","smoke","haze","plume"))]
        print([ (o.name,o.visible_shadow,o.visible_glossy,o.visible_diffuse) for o in fx][:6])
        for o in fx:
            o.visible_shadow=False; o.visible_diffuse=False; o.visible_transmission=False
            if v=="vis2": o.visible_glossy=False
        run(v)
    elif v.startswith("only_"):
        pre=v[5:]
        hid=[o for o in bpy.data.objects if o.name.startswith(pre) and not o.hide_render]
        for o in hid: o.hide_render=True
        run(v+str(len(hid)))
        for o in hid: o.hide_render=False
    elif v == "mb2": cy.max_bounces = 2; run(v)
    elif v == "noglossy": cy.glossy_bounces = 0; run(v); cy.glossy_bounces = 1
    elif v.startswith("thr"): cy.adaptive_threshold = float(v[3:]); run(v)
    elif v.startswith("spp"): cy.samples = int(v[3:]); run(v)
    elif v == "s8": cy.samples = 8; run(v)
