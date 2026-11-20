import os,sys
os.environ["CAML"]="(-5.0,-1.6,1.1)";os.environ["TILT"]="11"
sys.argv=["x"]
import shot as Sh
Tk=Sh.Take("preview")
Tk.pose([395,430,469])
for g in (395,430,469,430):
    f=Sh.bf(g); Tk.scene.frame_set(f)
    print(g,[round(v,3) for v in Tk.cam.matrix_world.translation],[round(v,3) for v in Tk.cam.rotation_euler], [round(v,3) for v in Tk.path.at(g)[0]])
