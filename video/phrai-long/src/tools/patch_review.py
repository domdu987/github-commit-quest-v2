"""มือพราย long version: fixes from review round 1 (6 Nov, video/release/reviews). Run after patch_band.py (prepare.sh). Each
change is asserted, and a change already present is skipped, so the script can be re-run on a tree it has patched.

  B1 hook    the narrator's command came at 5.8 s (rule: by ~3 s; ทะเลลด's long: 3.08 s). A new opening line in Puck,
             "ถ้าวันหนึ่ง… คุณเห็นเหรียญลอยมาในกระทง" (src/hook: tempo 1.25, the "…" beat kept to 0.12 s, Whisper CER 0.00),
             replaces "ถ้าวันหนึ่ง… กระทงลอยมาตรงหน้า มีเหรียญส่องแสงอยู่ข้างใน", and the opener is cut from 5.3 s to 3.0 s,
             so "อย่าก้มลงไปเก็บ" (red box) starts at ~3.05 s on the POV of the coin krathong. The opener's own timeline
             (title letters, the ฉบับเต็ม stamp, the glide down to the river) is compressed to fit, and so are its sound cues.
  B2 shadow  ตาเหม's hat and face went out of the top of the band during the push-in while the caption names him (auto y0 570):
             band to y0 400 (the reflections, the point of the shot, still in frame).
  B3 cards   the knowledge cards sat top centre, over the faces of แพรว and โต้ง in 12 teaching shots (and under the caption in
             cpr). In 16:9 the HTML UI column (steps card + source chip) moves to the empty top left (landscape.js land.ui);
             cpr's card, drawn at the bottom of the 9:16 frame, goes to the left at mid height, clear of the caption.
  minor, in the same render:
  M1 swim    part 3's first shot: แพรว swam out of the top of the band while the captions said "เธอว่ายสุดแรง / ตรงเข้าหาฝั่ง":
             the camera now starts a little wider (zoom 0.8) and follows her up the river, so the whole swimmer stays in frame
             and the krathongs and the moon's reflection slide past (the water is drawn from world y −1200, so nothing ends)
  M3 flashes the three full-frame white flashes (#flashw 0.7 / 0.6 / 0.4) capped at .28 (V1b's ceiling)
  M5 edges   bend (โต้ง's raised hand), throw (แพรว's bun and hand) and almost (her head at the top edge): bands moved up
The delivered 9:16 episodes are untouched."""
import json
import os
import shutil

W = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
done = []


def sub(rel, old, new):
    p = os.path.join(W, rel)
    s = open(p).read()
    if new in s:
        return done.append(f"{rel}: already")
    assert s.count(old) == 1, (rel, old[:90], s.count(old))
    open(p, "w").write(s.replace(old, new))
    done.append(f"{rel}: ok")


# ---------- B1: the new opening line (lines, recording, duration) ----------
H = os.path.join(W, "hook")
new01 = json.load(open(os.path.join(H, "lines.json")))[0]
lp = os.path.join(W, "ep1", "lines.json")
L = json.load(open(lp))
L = [new01 if ln["id"] == "n01" else ln for ln in L]
json.dump(L, open(lp, "w"), ensure_ascii=False, indent=1)
for f in os.listdir(os.path.join(H, "vo")):
    if f.startswith("n01."):
        shutil.copy(os.path.join(H, "vo", f), os.path.join(W, "ep1", "vo", f))
dp = os.path.join(W, "ep1", "vo", "durations.json")
du = json.load(open(dp))
du["n01"] = json.load(open(os.path.join(H, "vo", "durations.json")))["n01"]
json.dump(du, open(dp, "w"), indent=1)
done.append(f"ep1 n01: {new01['text']} ({du['n01']} s)")

# ---------- B1: the opener is one line long, the command follows straight on the POV ----------
sub("ep1/timing.py",
    '    ("open", ["n01"], 0.4, 0.5, 4.4),                 # story opener: title in the night sky, the dive onto the river of krathongs\n'
    '    ("hook", ["n02"], 0.5, 0.7, 2.6),                 # POV down from the pier: a child\'s arm reaching for the coins, a pale hand rising\n',
    '    ("open", ["n01"], 0.1, 0.0, 2.6),                 # story opener: title in the night sky, the dive onto the river of krathongs (long: one line, 3.0 s)\n'
    '    ("hook", ["n02"], 0.05, 0.7, 2.6),                # POV down from the pier: a child\'s arm reaching for the coins, a pale hand rising (long: the command at ~3.05 s)\n')
# the opener's timeline: title letters in by 0.9 s, the tag stamped at 0.7 s, the glide 1.7 → 2.7 s, the cut at 3.0 s
sub("hf/lib1/openers.js",
    '      clip.querySelectorAll(`#${id}-op2 .t i`).forEach((el, k) => tl.fromTo(el, { opacity: 0, y: 70, filter: "blur(8px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.55, ease: "power2.out", immediateRender: false }, A(0.2 + k * 0.13)));\n'
    '      tl.fromTo(q(".ep"), { opacity: 0, scale: 1.9 }, { opacity: 1, scale: 1, duration: 0.14, ease: "power4.in", immediateRender: false }, A(0.95));\n',
    '      // o.tin = [first letter, step, duration] and o.epAt (the tag stamp): a short opener (long version: 3.0 s) brings them in sooner\n'
    '      const TIN = o.tin || [0.2, 0.13, 0.55];\n'
    '      clip.querySelectorAll(`#${id}-op2 .t i`).forEach((el, k) => tl.fromTo(el, { opacity: 0, y: 70, filter: "blur(8px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: TIN[2], ease: "power2.out", immediateRender: false }, A(TIN[0] + k * TIN[1])));\n'
    '      tl.fromTo(q(".ep"), { opacity: 0, scale: 1.9 }, { opacity: 1, scale: 1, duration: 0.14, ease: "power4.in", immediateRender: false }, A(o.epAt ?? 0.95));\n')
sub("ep1/body.part",
    '         kick: "ROD MAI CLUB", at: 1.9, glide: 1.8,',
    '         kick: "ROD MAI CLUB", at: 1.7, glide: 1.0, tin: [0.1, 0.08, 0.4], epAt: 0.7, // long: a 3.0 s opener (was at 1.9, glide 1.8)')
# its sound: OpenerWater.cues at 1.7 / 1.0 (riser at − 0.9, splash and glitch at − 0.2, whoosh at, boom and glitch at the landing),
# the tag's boom at 0.7; the plops and the sting stay with the rings and hands, which still rise at 1.15–1.63 s (review round 2, N1)
sub("ep1/mix.py",
    '    ("open", 0.0, "swell", 0.5), ("open", 0.1, "bubbles", 0.8), ("open", 0.95, "boom", 0.35), *[("open", 1.15 + i * 0.12, "plop", 0.55) for i in range(5)], ("open", 1.15, "sting", 0.8),\n'
    '    ("open", 1.0, "riser", 0.5), ("open", 1.7, "splash", 0.9), ("open", 1.7, "glitch", 0.5), ("open", 1.9, "whoosh", 0.6), ("open", 3.68, "boom", 0.8), ("open", 3.7, "glitch", 0.4),\n',
    '    # long: the 3.0 s opener (at 1.7 / glide 1.0)\n'
    '    ("open", 0.0, "swell", 0.5), ("open", 0.1, "bubbles", 0.8), ("open", 0.7, "boom", 0.35), *[("open", 1.15 + i * 0.12, "plop", 0.55) for i in range(5)], ("open", 1.15, "sting", 0.8),\n'
    '    ("open", 0.8, "riser", 0.5), ("open", 1.5, "splash", 0.9), ("open", 1.5, "glitch", 0.5), ("open", 1.7, "whoosh", 0.6), ("open", 2.68, "boom", 0.8), ("open", 2.7, "glitch", 0.4),\n')

# ---------- B2: shadow ----------
sub("ep1/body.part",
    '      add("shadow", {\n        set: "reflections", setOpts: { id: "rf30" }, dark: 0.1,\n',
    '      add("shadow", {\n        set: "reflections", setOpts: { id: "rf30" }, dark: 0.1, land: { y0: 400 }, // long: ตาเหม\'s hat in the band through the push-in\n')

# ---------- B3: the knowledge cards to the empty top left (cpr: left, mid height, above the caption) ----------
TL = "{ x: 24 }"
CARDS = {1: {"how": TL, "reach": TL},
         2: {"srt": TL, "dont": TL, "call": TL, "check": TL, "air": TL, "cpr": '{ x: 24, y: -400, sel: ".steps, .zsrc" }', "recover": TL},
         3: {"mouth": TL, "float": TL, "know": TL}}
for e, shots in CARDS.items():
    for k, ui in shots.items():
        sub(f"ep{e}/body.part", f'      add("{k}", {{\n',
            f'      add("{k}", {{\n        land: {{ ui: {ui} }}, // long: the card clear of the faces (16:9 top left)\n')

# ---------- M1: the swim, followed ----------
sub("ep3/body.part",
    'land: { y0: 0 }, // long: whole swimmer at the start\n'
    '        cam: { keys: [{ t: 0, ...fr(540, 1050, 0.95, 540, 1000), drift: { y: 160, s: 0.01 } }] },\n',
    'land: { y0: 0 }, // long: whole swimmer at the start\n'
    '        // long: wider (0.8) and following her 80 % of the way up (she swims 170 / 0.95 world px a second), so she stays whole in the band\n'
    '        cam: { keys: [{ t: 0, ...fr(540, 1014, 0.8, 540, 640) }, { t: D("swim"), glide: D("swim"), ease: "none", ...fr(540, 1014 - 0.8 * 170 * D("swim") / 0.95, 0.8, 540, 640) }] },\n')

# ---------- M3: the white flashes at V1b's ceiling ----------
sub("ep1/body.part",
    'tl.fromTo("#flashw", { opacity: 0.7 }, { opacity: 0, duration: 0.25, immediateRender: false }, t0 + D("hook") - 0.4);',
    'tl.fromTo("#flashw", { opacity: 0.28 }, { opacity: 0, duration: 0.25, immediateRender: false }, t0 + D("hook") - 0.4); // long: V1b ceiling (was 0.7)')
sub("ep1/body.part",
    'tl.fromTo("#flashw", { opacity: 0.6 }, { opacity: 0, duration: 0.2, immediateRender: false }, t0 + YANK + 0.3);',
    'tl.fromTo("#flashw", { opacity: 0.28 }, { opacity: 0, duration: 0.2, immediateRender: false }, t0 + YANK + 0.3); // long: V1b ceiling (was 0.6)')
sub("ep2/body.part",
    'tl.fromTo("#flashw", { opacity: 0.4 }, { opacity: 0, duration: 0.3, immediateRender: false }, t0 + F("almost", 0, 1)); },',
    'tl.fromTo("#flashw", { opacity: 0.28 }, { opacity: 0, duration: 0.3, immediateRender: false }, t0 + F("almost", 0, 1)); }, // long: V1b ceiling (was 0.4)')

# ---------- M5: heads and hands at the top edge ----------
sub("ep1/body.part",
    'set: "pierDeck", setOpts: { id: "pd19", kt: [[760, WS + 8, 0.6, 5]] }, dark: 0.25,',
    'set: "pierDeck", setOpts: { id: "pd19", kt: [[760, WS + 8, 0.6, 5]] }, dark: 0.25, land: { y0: 330 }, // long: his raised hand in the band (auto 485)')
sub("ep1/body.part",
    'set: "pierDeck", setOpts: { id: "pd25" }, dark: 0.14,',
    'set: "pierDeck", setOpts: { id: "pd25" }, dark: 0.14, land: { y0: 400 }, // long: her bun and throwing hand in the band (auto 570)')
sub("ep2/body.part",
    'set: "pierDeck", setOpts: { id: "pd6" }, dark: 0.2,',
    'set: "pierDeck", setOpts: { id: "pd6" }, dark: 0.2, land: { y0: 430 }, // long: headroom after the push-in (auto 570)')

# ---------- review round 2 (6 Nov): the last edges, and the "then" shot ----------
# lure: โต้ง's legs hang from the surface above the band (auto y0 285); out: แพรว's head at the top edge (503);
# grab: the พราย's hand left the bottom edge on "แล้วดึงลง" (0); then: the card sat on the gallon the caption names and the bank
# (ทางขึ้น) was above the band (570)
sub("ep2/body.part",
    'set: "underRiver", setOpts: { id: "ur3", surface: 300 }, dark: 0.12,',
    'set: "underRiver", setOpts: { id: "ur3", surface: 300 }, dark: 0.12, land: { y0: 150 }, // long: his legs from the surface in the band')
sub("ep2/body.part",
    'set: "pierDeck", setOpts: { id: "pd9" }, dark: 0.2,',
    'set: "pierDeck", setOpts: { id: "pd9" }, dark: 0.2, land: { y0: 400 }, // long: headroom for แพรว (auto 503)')
sub("ep3/body.part",
    'set: "ankleGrab", setOpts: { id: "ag5" }, dark: 0.1,',
    'set: "ankleGrab", setOpts: { id: "ag5" }, dark: 0.1, land: { y0: 570 }, // long: the hand stays in the band, above the caption, as it pulls down')
sub("ep3/body.part",
    '      add("then", {\n',
    '      add("then", {\n        land: { y0: 300, ui: { x: 24 } }, // long: the bank (ทางขึ้น) and the gallon in frame, the card top left\n')

# grab with the band at 570: the arm's fade-out box (phUnder, lighter teal at its top, hard edges) came into the band behind the
# caption; in the long it fades from clear to the deep's colour instead, so it has no edge
sub("hf/lib3/phrai3.js",
    '<rect x="560" y="1500" width="300" height="480" fill="url(#phUnder)" opacity=".8"/></g>`;',
    '${window.LANDSCAPE ? `<defs><linearGradient id="${id}-fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a1b1a" stop-opacity="0"/><stop offset=".5" stop-color="#0a1b1a" stop-opacity=".9"/><stop offset="1" stop-color="#030807"/></linearGradient></defs><rect x="520" y="1380" width="380" height="640" fill="url(#${id}-fade)"/>` : `<rect x="560" y="1500" width="300" height="480" fill="url(#phUnder)" opacity=".8"/>`}</g>`;')

print("\n".join(done))
