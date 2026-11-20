import sys; sys.path.insert(0,'.')
import render_t4 as R, t4lib as L
from t4lib import bpy, P, Vector, actors
A=L.setup(); g=int(sys.argv[1]); out=sys.argv[2]
print(R.render(g,out))
