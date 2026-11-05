"""Long version (YouTube 16:9): the schedules. EP.1 loses its choice and end card; EP.2 and EP.3 get the bridge lines in place of their
hook lines (b01 b02 → EP.2, b03 b04 b05 → EP.3, recorded in tidelong/bridge with voice.py). Asserted, exact replacements."""
import json
import os
import shutil

W = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
B = {ln["id"]: ln for ln in json.load(open(os.path.join(W, "bridge", "lines.json")))}
BD = json.load(open(os.path.join(W, "bridge", "vo", "durations.json")))


def sub(path, old, new, count=1):
    s = open(path).read()
    n = s.count(old)
    assert n == count, (path, old[:70], n)
    open(path, "w").write(s.replace(old, new))


for ep, ids in ((2, ("b01", "b02")), (3, ("b03", "b04", "b05"))):
    d = os.path.join(W, f"ep{ep}")
    L = [ln for ln in json.load(open(os.path.join(d, "lines.json"))) if ln["id"] not in ids] + [B[i] for i in ids]
    json.dump(L, open(os.path.join(d, "lines.json"), "w"), ensure_ascii=False, indent=1)
    du = json.load(open(os.path.join(d, "vo", "durations.json")))
    for i in ids:
        du[i] = BD[i]
        for f in os.listdir(os.path.join(W, "bridge", "vo")):
            if f.startswith(i + "."):
                shutil.copy(os.path.join(W, "bridge", "vo", f), os.path.join(d, "vo", f))
    json.dump(du, open(os.path.join(d, "vo", "durations.json"), "w"), indent=1)

p = os.path.join(W, "ep1", "timing.py")
sub(p, '    ("close", ["n21", ("n22", 0.25)], 0.3, 0.7, 3.8),   # wide: the bay drawn back, a white line on the horizon\n',
    '    ("close", ["n21", ("n22", 0.25)], 0.3, 1.0, 3.8),   # wide: the bay drawn back, a white line on the horizon (long version: held 1 s, then bridge A)\n')
sub(p, '    ("choice", [], 0, 0, 3.2),                   # the choice: วิ่งลงไปตามยาย / ตะโกนเรียกจากบนเขา, pulled toward the first → black\n',
    "    # long version (YouTube 16:9): the choice and the end card are cut; the film goes straight on into EP.2's bridge\n")
sub(p, '    ("end", [], 0, 0, 2.4),                      # the end card: the evacuation sign with a note "ตอนที่ 2 · คลื่นแรกไป"\n', '')

p = os.path.join(W, "ep2", "timing.py")
sub(p, '    ("open", ["n01"], 0.15, -0.3, 2.6),            # EP.1\'s last frame on the hill (the bay drawn back, the white line); จูน dashes for the steps down\n'
       '    ("grab", ["n02"], 0.3, 0.5, 1.8),             # insert: ตาจุ่น\'s old hand clamps จูน\'s wrist on "อย่า" (sting); her sandal skids\n',
    '    # long version (YouTube 16:9): bridge A (b01 b02, narrator) replaces the hook lines n01 n02\n'
    '    ("brA", ["b01"], 0.3, 0.35, 2.8),             # NEW จูน on the hill makes up her mind and bolts ("จูนตัดสินใจ… วิ่งลงไปตามยาย")\n'
    '    ("open", ["b02"], 0.1, 0.25, 2.6),            # EP.1\'s last frame on the hill (the bay drawn back, the white line); จูน dashes for the steps down\n'
    '    ("grab", [], 0, 0, 1.8),                      # insert: ตาจุ่น\'s old hand clamps จูน\'s wrist at 0.3 s (sting, no voice); her sandal skids\n')
sub(p, '    ("close", ["n13", ("n14", 0.25)], 0.3, 0.7, 3.8),   # the phone: the live freezes and ends\n'
       '    ("choice", [], 0, 0, 3.2),                     # the choice, pulled toward going down to the hotel → black\n'
       '    ("end", [], 0, 0, 2.4),                        # the end card: ตอนที่ 3 · หนีไม่ทัน (ตอนจบ)\n',
    '    ("close", ["n13", ("n14", 0.25)], 0.3, 1.2, 3.8),   # the phone: the live freezes and ends (long version: a held beat on the dead stream, then bridge B)\n'
    '    # long version: the choice and the end card are cut\n')

p = os.path.join(W, "ep3", "timing.py")
sub(p, '    ("hook", ["n01"], 0.15, -0.3, 2.6),            # back to the second wave, ยาย\'s side: people run past the shop to the pickups on the beach road\n'
       '    ("cars", ["n02"], 0.3, 0.5, 1.9),              # the jam: bumper to bumper, hazards blinking (the command at ~2.9 s)\n',
    '    # long version (YouTube 16:9): bridge B (b03 b04 b05, narrator) replaces the hook lines n01 n02\n'
    '    ("brB", ["b03"], 0.3, 0.4, 3.0),              # NEW back before the second wave: the tower blaring over the hotel and ยาย\'s shop (EP.2\'s siren angle)\n'
    '    ("yai0", ["b04"], 0.25, 0.4, 2.8),            # NEW ยาย at her shop hugging the old photo (the moment EP.2 left her)\n'
    '    ("hook", ["b05"], 0.15, 0.4, 2.6),            # back to the second wave, ยาย\'s side: people run past the shop to the pickups on the beach road\n'
    '    ("cars", [], 0, 0, 1.9),                      # the jam: bumper to bumper, hazards blinking, the horn (no voice)\n')
# every part ends on a whole number of 60 fps frames that is exact in binary floating point (a multiple of 0.25 s = 15 frames =
# 12000 samples at 48 kHz): HyperFrames counts frames with ceil(duration * fps), so the rendered video, mix.wav and the joins agree
for ep in (1, 2, 3):
    sub(os.path.join(W, f"ep{ep}", "timing.py"),
        '    json.dump({"total": round(t, 3), "shots": out}, open(os.path.join(HERE, "schedule.json"), "w"), ensure_ascii=False, indent=1)\n',
        '    # long version: hold the last shot so the part ends on a multiple of 0.25 s (15 frames at 60 fps, 12000 samples at 48 kHz)\n'
        '    end = -(-round(t, 3) // 0.25) * 0.25\n'
        '    out[-1]["dur"] = round(out[-1]["dur"] + end - t, 3)\n'
        '    t = end\n'
        '    json.dump({"total": round(t, 3), "shots": out}, open(os.path.join(HERE, "schedule.json"), "w"), ensure_ascii=False, indent=1)\n')
print("timing patched")
