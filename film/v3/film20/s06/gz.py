import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import c20 as C
Tk=C.Take("cafe_wide",light="DAY",quality="preview")
for k,m in Tk.A["marks"].items():
    if k.startswith("artist") or k=="waiter": print(k, round(m[2],3), round(C.ground_z(m[0],m[1],top=1.5),3))
