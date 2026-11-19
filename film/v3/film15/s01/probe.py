import sys; sys.path.insert(0,'.')
import shot as S, c15 as C
from c15 import *
n=int(sys.argv[1]); g=int(sys.argv[2])
st=S.Stage(g,'preview')
print('cam',[round(c,2) for c in st.cl], 'bar',tuple(st.bar))
for k in ('takeoff','bar_centre','landing','dick_mark','boy_wait_a','boy_wait_b','boy_c','coach_end','pile','runup_start'):
    print(k,[round(c,1) for c in st.M[k]], C.screen(st.M[k]))
for i,p in enumerate(st.M['runup_path']): print('path',i,[round(c,1) for c in p],C.screen(p))
print('barL', C.screen((-2.0/0.54,st.bar.y,st.bar.z)), C.screen((2.0/0.54,st.bar.y,st.bar.z)))
