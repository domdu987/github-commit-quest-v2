import sys; import shot as S; from shot import *
n=int(sys.argv[1]); W=S.setup(n)
for g in [int(x) for x in sys.argv[2].split(',')]:
    W.sc.frame_set(g); bpy.context.view_layer.update()
    print('g',g,'cam',[round(c*DM,2) for c in W.sc.camera.location])
    for k,v in W.M.items():
        if isinstance(v,list): continue
        s=screen(v); 
        if -50<s[0]<770 and 0<s[1]<1330: print('  ',k,s)
