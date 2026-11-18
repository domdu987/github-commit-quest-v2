import json, os, sys, glob, statistics
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
take = os.path.basename(HERE)
CFG = {
 "s09": dict(shots=[9, 10, 11], g0=619, g1=788, first_g=613, n=181, ranges={"9": [613, 674], "10": [675, 728], "11": [729, 793]},
   setups={"9": "hull_side DAY, high 3/4 from the quay over the scaffold, painter on the hanging plank, stripes 0.3 -> 1 (day 1 zigzags)",
           "10": "new angle: low from the bow side of the plank, DAY, stripes 1 -> 2 (day 2 staircases)",
           "11": "harbour_wide DUSK, lower crane view, stripes 2 -> 3 (day 3 full dazzle), painter steps back proud on the quay"},
   cues=[(20.63, "day 1: brush on the hull, scaffold creak, gulls"), (22.50, "day 2: paint bucket clank, brush strokes"), (24.30, "day 3 dusk: lamps, harbour hum, a satisfied sigh")],
   trans_in={"type": "cut", "frames": 0}, cuts=[675, 729]),
 "s12": dict(shots=[12, 13, 14], g0=788, g1=998, first_g=782, n=222, ranges={"12": [782, 863], "13": [864, 926], "14": [927, 1003]},
   setups={"12": "convoy_wide SEA_DAY, periscope foreground, convoy sailing (set_convoy s = g/30-35), slow drift",
           "13": "periscope_pov lens 50, one sweep from the left grey ship to the dazzle ship, stops with slow drift; overlay on, periscope head hidden",
           "14": "bridge_deck, camera carried with the flagship; admiral_shout, mouth only g 951-1000"},
   cues=[(26.27, "open sea, bow waves, engines, wind"), (28.80, "periscope hiss, a metallic creak"), (31.60, "the admiral shouts: 'เห็นมั้ย เป้าชัดแจ๋วเลย!'")],
   trans_in={"type": "cut", "frames": 0}, cuts=[864, 927])}
c = CFG[take]
cpu = []; wall = []
for j in glob.glob(os.path.join(HERE, "raw", "s*", "g_*.json")):
    d = json.load(open(j)); cpu.append(d.get("cpu", 0)); wall.append(d.get("wall", 0))
meta = dict(take=take, film=10, shots=c["shots"], g0=c["g0"], g1=c["g1"], first_g=c["first_g"], n_frames=c["n"], handle_in=6, handle_out=5,
            transition_in=c["trans_in"], transitions=[dict(at=x, type="cut") for x in c["cuts"]], shot_ranges=c["ranges"], setups=c["setups"],
            set="v3/set3d10/harbour.py", cast="v3/cast10", samples=12, resolution=[720, 1280], fps=30, dof="none",
            s_per_frame_wall_mean=round(statistics.mean(wall), 2), s_per_frame_cpu_mean=round(statistics.mean(cpu), 2))
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
json.dump(dict(take=take, fps=30, cues=[dict(time=round(g, 2), frame=int(round(g * 30)), kind="sfx", label=l) for g, l in c["cues"]]), open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)
gs = list(range(c["first_g"], c["first_g"] + c["n"], 10))
ims = [Image.open(os.path.join(HERE, "frames", "g_%04d.png" % g)).resize((180, 320)) for g in gs]
cols = 10; rows = (len(ims) + cols - 1) // cols
sh = Image.new("RGB", (cols * 180, rows * 320), (20, 20, 20))
for i, im in enumerate(ims): sh.paste(im, ((i % cols) * 180, (i // cols) * 320))
sh.save(os.path.join(HERE, "contact.jpg"), quality=85)
print(meta["s_per_frame_wall_mean"], meta["s_per_frame_cpu_mean"])
