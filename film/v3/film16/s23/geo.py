import sys
sys.argv=['x','probe','1500']
sys.path.insert(0,'.')
import shot as S
Tk=S.Take("preview")
for nm in ("pole","wood"):
    m=S.TG.STATE["M"][nm]
    print(nm,[ (n.type,n.name,n.label) for n in m.node_tree.nodes])
