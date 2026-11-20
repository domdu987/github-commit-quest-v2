import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import c20 as C
Tk=C.Take("cafe_table_insert",light="DAY",quality="preview")
print(sorted(C.CO.STATE['M'].keys()))
print(Tk.A['marks'])
