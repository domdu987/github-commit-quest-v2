import sys; sys.path.insert(0,'/home/user/github-commit-quest-v2/film/v3/set3d17'); sys.path.insert(0,'.')
import prefecture17 as P, bpy, bertillon as K, render_t6a as R
A=P.world_build('T6'); P.key_take('T6'); P.setup_render2((360,640),samples=8,threads=2)
G=int(sys.argv[-2]); bpy.context.scene.frame_set(G+1); P.stage_cast2('T6',G,R.assign_for(G))
mode=sys.argv[-1]
if mode=='hidebox':
    for o in K.STATE['anim']['box']['objs']: o.hide_render=True
if mode=='nobox2':
    r=K.STATE['anim']['box2']['root']
    for o in [r]+list(r.children_recursive): o.hide_render=True
if mode=='nocast':
    for a in bpy.data.objects:
        if a.name.startswith(('card_','act','Actor')) or 'bertillon' in a.name: print(a.name)

if mode=='nobox':
    for n in ('box',):
        r=K.STATE['anim'][n]['root']
        for o in [r]+list(r.children_recursive): o.hide_render=True
fp='/home/user/github-commit-quest-v2/film/v3/film17v2/T6a/probe_%s_%d.png'%(mode,G)
bpy.context.scene.render.filepath=fp; bpy.ops.render.render(write_still=True); P.grade2(fp)
