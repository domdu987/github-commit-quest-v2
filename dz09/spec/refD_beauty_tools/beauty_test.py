"""A/B test of the refD beauty settings on the v4 expressway set. Does not modify v4 files.
usage: python3 beauty_test.py <variant: base|beauty> <preset> <scale> <quality> <out_noext>"""
import sys, os, math, time, resource, json
P='/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09'
sys.path.insert(0, P+'/v4/set_expressway')
import bpy, expressway as X, standins
from mathutils import Vector
var, preset, scale, q, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4], sys.argv[5]
A = X.build(); X.setup_render(quality=q, threads=4)
acts = standins.place(A)
cam = X.use_camera(preset, "9:16", scale=scale); bpy.context.view_layer.update(); standins.pose_all(acts, cam)
sc = bpy.context.scene; cy = sc.cycles
popts = {}
if var == 'beauty':
    # 1) light transport: real bounce + AO from geometry
    cy.max_bounces = 4; cy.diffuse_bounces = 2; cy.glossy_bounces = 2; cy.sample_clamp_indirect = 3.0
    # 2) ambient emission fake: cut to 30 % (bounce + sky now do the fill)
    for m in bpy.data.materials:
        if not m.use_nodes: continue
        for n in m.node_tree.nodes:
            if n.type == 'BSDF_PRINCIPLED' and n.inputs['Emission Color'].is_linked and abs(n.inputs['Emission Strength'].default_value - 1.0) < 1e-6:
                n.inputs['Emission Strength'].default_value = 0.3
    # 3) sky dome lights diffuse too (cool fill), importance-sampled
    w = sc.world; nt = w.node_tree
    lp = [n for n in nt.nodes if n.type == 'LIGHT_PATH'][0]
    st = [l.to_node for l in lp.outputs['Is Diffuse Ray'].links][0]   # SUBTRACT(1, isDiffuse)
    st.inputs[0].default_value = 1.0; st.inputs[1].default_value = 0.0  # diffuse rays see the sky too
    w.cycles.sampling_method = 'MANUAL'; w.cycles.sample_map_resolution = 256
    # 4) moon key: cool sun, 3 deg, back-light from far end of the deck (shadows run toward camera)
    ld = bpy.data.lights.new('moon_key', 'SUN'); ld.energy = float(os.environ.get('MOON', '1.2')); ld.angle = math.radians(3.0)
    ld.color = (0.62, 0.74, 1.0)
    ob = bpy.data.objects.new('moon_key', ld); sc.collection.objects.link(ob); ob.visible_glossy = False
    d = Vector((0.35, -0.80, -0.48)).normalized()       # travel direction
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    # 5) rim from the sodium lamps keeps; flood key softer
    for L in bpy.data.lights:
        if L.name.startswith('flood_key'): L.shadow_soft_size = 0.35
        if L.name.startswith('sodium_'): L.shadow_soft_size = 0.4
    mul = [l.to_node for l in st.outputs[0].links][0]; mul.inputs[1].default_value = float(os.environ.get('SKY', '1.1'))
    popts = dict(fog_z0=450.0, bloom=0.45)
    if os.environ.get('NEWPOST', '1') == '1':
        import post, numpy as np
        post.FOG_BASE = np.array([0.010, 0.012, 0.024], np.float32)
        def grade(rgb):
            c = rgb * np.array([1.0, 1.0, 1.04], np.float32) * float(os.environ.get('EXPO', '1.25'))
            l = post.lum(c)[..., None]
            c = l + (c - l) * 1.15                                          # saturation
            sh = np.clip(1 - l / 0.06, 0, 1)                                 # shadow tint toward blue
            c = np.maximum(c - 0.004 * np.array([1.0, 0.8, 0.0], np.float32) * sh, 0) + sh * np.array([0, 0.001, 0.004], np.float32)
            k = 0.62                                                       # filmic shoulder (no hard clip)
            c = np.where(c > k, k + (1 - k) * (1 - np.exp(-(c - k) / (1 - k))), c)
            return np.maximum(c, 0)
        post.grade = grade
r0 = resource.getrusage(resource.RUSAGE_SELF); t0 = time.time()
res = X.render_still(out, frame=7, **({'post_opts': popts} if popts else {}))
r1 = resource.getrusage(resource.RUSAGE_SELF)
print(json.dumps(dict(var=var, preset=preset, q=q, cpu_render=res.get('cpu_render'), wall=res.get('wall_render'), cpu_post=res.get('cpu_post'), getr=round(r1.ru_utime-r0.ru_utime,1))))
