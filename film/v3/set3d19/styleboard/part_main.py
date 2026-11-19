
# ================================================================== render + run
def render(mode, out, samples, draft):
    sc = bpy.context.scene; P = PRESETS[mode]
    sc.render.engine = 'CYCLES'; cy = sc.cycles; cy.device = 'CPU'; cy.use_denoising = True; cy.denoiser = 'OPENIMAGEDENOISE'
    cy.denoising_input_passes = 'RGB_ALBEDO_NORMAL'; cy.max_bounces = 4; cy.diffuse_bounces = P.get('dbounce', 1); cy.glossy_bounces = P.get('gloss', 1); cy.transmission_bounces = 0; cy.transparent_max_bounces = 6
    cy.use_light_tree = True; cy.filter_width = 1.2; sc.render.threads = 4
    sc.render.resolution_x = W // (2 if draft else 1); sc.render.resolution_y = H // (2 if draft else 1); sc.render.resolution_percentage = 100
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = P.get('exposure', 0.0)
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
    if os.environ.get('CROP'):      # debug: render only a fractional region x0,y0,x1,y1 (y from top)
        x0, y0, x1, y1 = [float(v) for v in os.environ['CROP'].split(',')]; sc.render.use_border = True; sc.render.border_min_x = x0; sc.render.border_max_x = x1; sc.render.border_min_y = 1 - y1; sc.render.border_max_y = 1 - y0
    A = _rd(sc, out + '_A.png', samples, True)[..., :3]
    # shade mask for the hue check (not used for grading): sun-only render with a white override, no bounces, sky hidden; cast shadow = sun blocked
    for l in bpy.data.lights:
        if l.name != 'key': l.energy = 0.0
    wbgs = [n for n in bpy.data.worlds['sky'].node_tree.nodes if n.bl_idname == 'ShaderNodeBackground']
    for n in wbgs: n.inputs['Strength'].default_value = 0.0
    for o in bpy.data.objects:
        if o.name.startswith(('clouds', 'glass', 'sun_', 'shafts', 'flame', 'skyobj')): o.hide_render = True
    wm = bpy.data.materials.new('ovr'); wm.use_nodes = True; bs = wm.node_tree.nodes['Principled BSDF']; bs.inputs['Base Color'].default_value = (1, 1, 1, 1)
    bs.inputs['Roughness'].default_value = 1.0; bs.inputs['Specular IOR Level'].default_value = 0.0
    cy.max_bounces = 0; cy.diffuse_bounces = 0; cy.glossy_bounces = 0; bpy.context.view_layer.material_override = wm
    D = _rd(sc, out + '_D.png', 24, False, True)
    bpy.context.view_layer.material_override = None
    lD = 0.3 * D[..., 0] + 0.59 * D[..., 1] + 0.11 * D[..., 2]
    vs = [(o, o.visible_shadow) for o in bpy.data.objects if o.type == 'MESH']
    for o, _ in vs: o.visible_shadow = False
    D2 = _rd(sc, out + '_D2.png', 8, False, True)
    for o, v in vs: o.visible_shadow = v
    lD2 = 0.3 * D2[..., 0] + 0.59 * D2[..., 1] + 0.11 * D2[..., 2]
    cast = (D[..., 3] > 0.99) & (lD < 0.02) & (lD2 > 0.08)
    Image.fromarray((cast * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).save(out + '_shade.png')
    a = grade(A, P)
    Image.fromarray((a * 255 + 0.5).astype(np.uint8)).save(out + '.jpg', quality=93)

NAMES = {'shop': 'sb1_workshop', 'ship': 'sb2_ship', 'hall': 'sb3_hall'}
def run(mode, draft=False):
    t = time.time(); bpy.ops.wm.read_factory_settings(use_empty=True); MATS.clear(); P = PRESETS[mode]
    if mode == 'shop':
        flat_world('#7a82ff', 0.0); build_shop(P); lights_shop(P)
    elif mode == 'ship':
        build_ship(P); lights_ship(P)
    else:
        flat_world('#7a82ff', 0.0); build_hall(P); lights_hall(P)
    setup_camera(P)
    out = os.path.join(HERE, ('d_' if draft else '') + NAMES[mode])
    render(mode, out, 24 if draft else P.get('samples', 100), draft)
    for f in os.listdir(HERE):
        if f.startswith(os.path.basename(out)) and f.endswith(('_A.png', '_D.png', '_D2.png')): os.remove(os.path.join(HERE, f))
    print(mode, 'done %.0fs' % (time.time() - t)); return time.time() - t

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != 'draft']; draft = 'draft' in sys.argv
    for m in (['shop', 'ship', 'hall'] if (not args or args[0] == 'all') else args): run(m, draft)
