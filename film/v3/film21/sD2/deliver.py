import os, json, shutil, subprocess
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__)); FIRST, LAST = 642, 796
fr = os.path.join(H, "frames"); os.makedirs(fr, exist_ok=True)
for g in range(FIRST, LAST + 1): shutil.copyfile(os.path.join(H, "raw", "f_%04d.png" % g), os.path.join(fr, "g_%04d.png" % g))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(fr, "g_%04d.png"), "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", os.path.join(H, "take.mkv")], check=True)
sz = os.path.getsize(os.path.join(H, "take.mkv"))
if sz > 45e6: subprocess.run("split -b 40M take.mkv take.mkv.part", shell=True, cwd=H, check=True)
json.dump(dict(take="sD2", film=21, segment="D2", first_g=FIRST, n_frames=LAST - FIRST + 1, g0=642, g1=793, handle_in=0, handle_out=3,
  transition_in=dict(type="cut", frames=0, note="whip in rendered inside: g 642-647 fast pan settling"), transition_out=dict(type="D6 join at P_BANK", at=793, handle=[794, 796]),
  world="K.build_world(['camp_bank'])", end_pose="K.POSES['P_BANK'] exactly at g793", samples=32, resolution=[720, 1280], fps=30,
  events=dict(whip_in=[642, 647], tracking=[648, 750], stop=750, cu1_push=[756, 765], purse_slap=758, cu1=[765, 778], pull_out=[778, 793], lipsync=[642, 791])),
  open(os.path.join(H, "meta.json"), "w"), indent=1)
cues = [(642, 647, "whoosh", "fast whip pan in"), (648, 750, "foley", "heavy waddling footsteps on dry grass, robe rustle, a tired shuffle behind"), (756, 765, "sfx", "quick push-in whoosh"),
        (758, 762, "sfx", "slap on the leather coin purse, coins jingle"), (778, 793, "sfx", "soft pull-out swish, smug chuckle")]
json.dump(dict(take="sD2", fps=30, cues=[dict(time=round(a / 30, 3), duration=round((b - a + 1) / 30, 3), frame=a, end_frame=b, kind=k, label=l) for a, b, k, l in cues]), open(os.path.join(H, "cues.json"), "w"), indent=1)
gs = list(range(642, 797, 8))[:20]
S = Image.new("RGB", (180 * 10, 320 * 2))
for k, g in enumerate(gs):
    im = Image.open(os.path.join(fr, "g_%04d.png" % g)).convert("RGB"); ImageDraw.Draw(im).line([(0, 880), (720, 880)], fill=(0, 255, 255), width=3)
    S.paste(im.resize((180, 320), Image.LANCZOS), ((k % 10) * 180, (k // 10) * 320))
S.save(os.path.join(H, "contact.jpg"), quality=90); print("ok", sz / 1e6)
