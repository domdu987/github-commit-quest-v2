import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import c20 as C
Tk=C.Take(sys.argv[1],light="DAY",quality="preview")
A=Tk.A
for k,v in A["marks"].items(): print(k,[round(x,2) for x in v])
for k,v in A["cams"].items(): print(k,{a:(tuple(round(x,2) for x in b) if hasattr(b,'__len__') else b) for a,b in v.items()})
print(A['hooks'].keys(), A['P'] if 0 else '')
