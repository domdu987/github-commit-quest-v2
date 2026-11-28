import sys; sys.path.insert(0,'.')
import post_d as PD
for g in range(1880,1932): PD.compose(g,'../s64/work','../s64/frames',vib=2.0,wb=(-2.0,3.5),sat=1.3,gamma=0.88)
