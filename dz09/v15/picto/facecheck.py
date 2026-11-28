"""facecheck.py -- tmp/faces_*.png: top 400 px of the frame every 0.25-0.5 s while a pictogram is up, over the clean draft (finish.py's comp_frame)."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw
import picto15 as C
sys.path.insert(0, os.path.join(C.PROJ, "v10", "film"))
import finish as FN
FN._IC["m"] = C
base = FN.base_dir("draft", 360, 640)
def sheet(ts, name, cols=6, hcrop=400, sc=0.5):
    w, h = int(720 * sc), int(hcrop * sc)
    S = Image.new("RGB", (cols * w, ((len(ts) + cols - 1) // cols) * (h + 16)), (0, 0, 0)); d = ImageDraw.Draw(S)
    for i, t in enumerate(ts):
        g = int(round(t * 24)); im = FN.comp_frame(base, g, 720, 1280).crop((0, 0, 720, hcrop)).resize((w, h), Image.LANCZOS)
        x, y = (i % cols) * w, (i // cols) * (h + 16); S.paste(im, (x, y + 16)); d.text((x + 3, y + 2), "%.2f %s f%d" % (t, C.shot_of(g), g), fill=(255, 255, 255))
    S.save(os.path.join(C.HERE, "tmp", name))
if __name__ == "__main__":
    sheet([0.3 + x / 4.0 for x in range(0, 26)], "faces_0.png")
    sheet([16 + x / 4.0 for x in range(0, 30)], "faces_1.png")
    sheet([23.5 + x / 2.0 for x in range(0, 14)] + [30.5 + x / 4.0 for x in range(0, 11)], "faces_2.png")
    sheet([33.7 + x / 2.0 for x in range(0, 25)], "faces_3.png")
    sheet([46.5 + x / 3.0 for x in range(0, 18)], "faces_4.png")
    C.close()
