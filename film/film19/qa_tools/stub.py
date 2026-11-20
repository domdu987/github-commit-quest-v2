import sys,types,math,os,numpy as np
class Vector:
    def __init__(s,v): s.v=np.array(list(v),float)
    def __add__(s,o): return Vector(s.v+o.v)
    def __sub__(s,o): return Vector(s.v-o.v)
    def __mul__(s,k): return Vector(s.v*k)
    __rmul__=__mul__
    def __neg__(s): return Vector(-s.v)
    def __truediv__(s,k): return Vector(s.v/k)
    def __getitem__(s,i): return s.v[i]
    def __len__(s): return 3
    def __iter__(s): return iter(s.v)
    x=property(lambda s:s.v[0]); y=property(lambda s:s.v[1]); z=property(lambda s:s.v[2])
    @property
    def length(s): return float(np.linalg.norm(s.v))
    def normalized(s): return Vector(s.v/np.linalg.norm(s.v))
    def dot(s,o): return float(s.v@o.v)
    def cross(s,o): return Vector(np.cross(s.v,o.v))
m=types.ModuleType('mathutils'); m.Vector=Vector; m.Matrix=object; sys.modules['mathutils']=m
c=types.ModuleType('c19')
class _T: pass
c.__getattr__=lambda n: (_T if n=='Take' else (lambda *a,**k: None))
c.clamp=lambda x,a=0.0,b=1.0: max(a,min(b,x))
c.lerp=lambda a,b,t: a+(b-a)*t
sys.modules['c19']=c
for nm in ['puppet','bpy']:
    mm=types.ModuleType(nm); mm.__getattr__=lambda n: (lambda *a,**k: None); sys.modules[nm]=mm
SHOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../v3/film19/s02'); sys.path.insert(0,SHOT)
import builtins
src=open(os.path.join(SHOT,'shot.py')).read().split('if __name__ == "__main__":')[0]
g={'__name__':'shotmod','__file__':os.path.join(SHOT,'shot.py')}
exec(compile(src,'shot.py','exec'),g)
for gg in range(118,166):
    tau=g['_tau_of'](gg); s=g['_umap'](min(tau,182)); u=g['_u_of_s'](s)
    loc,look=g['_land'](tau)
    print(gg,'tau=%.2f s=%.4f u=%.4f loc=(%.2f,%.2f,%.2f) look=(%.2f,%.2f,%.2f)'%(tau,s,u,*loc.v,*look.v))
