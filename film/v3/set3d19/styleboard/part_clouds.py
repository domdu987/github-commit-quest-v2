
# ---- clouds (copied from film 16)
def cloud_mat(P):
    """emission-only painted cloud: normal facing the sun -> cream/peach, facing away / down -> blue-violet (gradient across every puff)"""
    m = bpy.data.materials.new('cloudG'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); gm = N('ShaderNodeNewGeometry'); vm = N('ShaderNodeVectorMath'); vm.operation = 'DOT_PRODUCT'
    kd = Vector(P['key_dir']).normalized(); vm.inputs[1].default_value = (-kd.x, -kd.y, -kd.z); L(gm.outputs['Normal'], vm.inputs[0])
    mr = N('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = -0.35; mr.inputs['From Max'].default_value = 0.45; L(vm.outputs['Value'], mr.inputs['Value'])
    mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.inputs[6].default_value = hexc(P['cloud'][1]); mx.inputs[7].default_value = hexc(P['cloud'][0]); L(mr.outputs['Result'], mx.inputs[0])
    em.inputs['Strength'].default_value = P.get('cloud_k', 1.0); L(mx.outputs[2], em.inputs['Color']); L(em.outputs[0], out.inputs['Surface']); MATS['cloudG'] = m; return m

def clouds(P):
    mb = MB('clouds'); rr = rnd(P.get('cloud_seed', 9)); a = mat_emit('cloudA', P['cloud'][0], P.get('cloud_k', 1.0)); b = mat_emit('cloudB', P['cloud'][1], P.get('cloud_k', 1.0))
    if P.get('cloud_diffuse'):      # sun-lit clouds: warm cream tops, blue-violet undersides from the sky ambient + a faint violet self term
        a = cloud_mat(P); b = a
    for i in range(P.get('ncloud', 10)):
        cx = rr.uniform(-260, 260); cy = rr.uniform(300, 420); cz = rr.uniform(P.get('cloud_z', (60, 140))[0], P.get('cloud_z', (60, 140))[1]); sz = rr.uniform(25, 55) * (1.0 + cz / 160.0) * P.get('cloud_scale', 1.0)
        for j in range(rr.randint(4, 7)):
            ox = rr.uniform(-1.4, 1.4) * sz; oz = rr.uniform(0, 0.35) * sz
            mb.ell(b, (cx + ox, cy, cz + oz - 0.25 * sz), (sz * rr.uniform(0.6, 1.0), sz * 0.5, sz * 0.32), (18, 10))
            mb.ell(a, (cx + ox, cy - 6, cz + oz), (sz * rr.uniform(0.5, 0.9), sz * 0.45, sz * 0.27), (14, 8))
    mb.finish()

