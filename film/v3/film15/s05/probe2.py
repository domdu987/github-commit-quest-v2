import sys; import shot as S; from shot import *
n=int(sys.argv[1]); g=int(sys.argv[2]); W=S.setup(n); W.sc.frame_set(g); bpy.context.view_layer.update()
for a in sys.argv[3:]:
    x,y=[float(v) for v in a.split(',')]; p=W.ground_at(x,y); print(a,'->',[round(c,2) for c in p], screen(p))
