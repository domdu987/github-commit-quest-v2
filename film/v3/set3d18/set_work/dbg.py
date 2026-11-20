import sys; sys.path.insert(0,'/home/user/github-commit-quest-v2/film/v3/set3d18')
import jimo as J, bpy
A=J.build('jimo_in','jimo_in','NIGHT'); sc=bpy.context.scene
J.MN.setup_render(sc,'preview'); sc.cycles.samples=6
mode=sys.argv[1]
if mode=='nolights':
    for o in J.STATE['LIGHTS'].objects:
        if o.data.type=='POINT': o.data.energy=0
if mode=='nowarm':
    for ob in J.STATE['SET'].objects:
        if 'warm' in ob.data.attributes if ob.type=='MESH' else False:
            for d in ob.data.attributes['warm'].data: d.value=0
J.make_camera(dict(loc=(40,26,9),look_at=(10,0,6),lens=22)); J.T.render('/tmp/claude-0/dbg_%s.png'%mode)
