import os, glob, json, subprocess, shutil
H = os.path.dirname(os.path.abspath(__file__))
fr = os.path.join(H, "frames"); shutil.rmtree(fr, ignore_errors=True); os.makedirs(fr)
n = 0
for g in range(1633, 1849):
    for d in ("camp", "bank", "low"):
        p = os.path.join(H, "raw", d, "g_%04d.png" % g)
        if os.path.exists(p): os.symlink(p, os.path.join(fr, "g_%04d.png" % g)); n += 1; break
    else: raise SystemExit("missing %d" % g)
subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", "1633", "-i", fr + "/g_%04d.png",
                       "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", os.path.join(H, "take.mkv")])
json.dump(dict(g0=1640, g1=1848, first_g=1633, n_frames=216, transition_in=dict(type="dissolve", frames=11), internal_cuts=[1709, 1769, 1821]), open(os.path.join(H, "meta.json"), "w"), indent=1)
json.dump([dict(g=1677, cue="coin scale tip"), dict(g=1690, cue="chest lid slam"), dict(g=1709, cue="murmur, nose pinch"), dict(g=1783, cue="splash"), dict(g=1788, cue="splash"),
           dict(g=1793, cue="splash"), dict(g=1797, cue="splash"), dict(g=1802, cue="splash"), dict(g=1806, cue="splash"), dict(g=1821, cue="splash 1 (ตูม)"), dict(g=1830, cue="splash 2 (ตูม)"), dict(g=1839, cue="splash 3 (ตูม)")], open(os.path.join(H, "cues.json"), "w"), indent=1)
from PIL import Image
gs = [1640, 1662, 1680, 1692, 1712, 1735, 1760, 1780, 1795, 1810, 1825, 1848]
ims = [Image.open(os.path.join(fr, "g_%04d.png" % g)).resize((240, 427)) for g in gs]
m = Image.new("RGB", (240 * 6, 427 * 2))
for i, im in enumerate(ims): m.paste(im, ((i % 6) * 240, (i // 6) * 427))
m.save(os.path.join(H, "contact.jpg"), quality=88)
print("delivered", n, os.path.getsize(os.path.join(H, "take.mkv")) // 1000000, "MB")
