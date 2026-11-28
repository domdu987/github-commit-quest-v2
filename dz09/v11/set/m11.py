import sys,json,cv2
sys.path.insert(0,"analysis")
import meas
out={}
for n in ["s06","s09","s13","s18","s20","s24"]:
    for tag,p in (("v9",f"../../v9/set/look/out/{n}_916.png"),("v11",f"look/out/{n}_916.png")):
        s=meas.stats(cv2.imread(p)); out[f"{n}_{tag}"]=s
        if tag=="v11": print(n,tag,"L",s["L_mean"],"p5",s["L_p5"],"p50",s["L_p50"],"p95",s["L_p95"],"deep",s["deep"],"S",s["S_mean"],"hueSh",s["hue_shadow"],"vig",s["vign"],"ol",s["outline"],"ed",s["edge"])
json.dump(out,open("look/measure11.json","w"),indent=1)
