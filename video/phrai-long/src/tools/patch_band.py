"""มือพราย long version: what the 16:9 band cut off. Run after patch_libs.py (prepare.sh). Each change is asserted, and a change
already present is skipped, so the script can be re-run on a tree it has patched.

The band check (tools/fitcheck.sh: every shot's whole vertical frame with the 16:9 band outlined) found, in the long only:
  part 1  hook   the พราย's pale hand rising toward the child's hand sat at world y 1556+, below the band (auto y0 0): never seen.
                 The long places it at the krathong's lower right, reaching up-left (pierPOV option phL, used only when
                 window.LANDSCAPE is set) and lowers the band to y0 150, so it rises beside the centred caption.
          open   the opener's tag read "EP.1 · อย่าก้มคว้า"; the long reads "ฉบับเต็ม" (as ทะเลลด's long, review note M4).
          hug    the two sinking figures (the drowning one hugging the rescuer) had their heads and arms above the band (auto y0
                 490); band to y0 60, the surface at the top edge.
          call   part 1's last shot: the พราย's face below the steps fell under the band (y0 361, eyes at ~1740); the พราย 130 up and 50 right
                 (still under the water, below the krathong) and the band at y0 440, the sleepwalker's head still in frame.
  part 2  hands  the hull the hands push was a sliver at the top edge (y0 285); band to y0 180.
  part 3  swim   แพรว swims out of the top of the frame: with y0 270 she was half out from the first frame; y0 0 as the 9:16.
          land   the hospital's sign on its roof was above the band (y0 570); band to y0 400.
The delivered 9:16 episodes are untouched."""
import os

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


# part 1: the hook's pale hand
sub("hf/lib1/phrai.js",
    '<g id="${id}-phand" opacity="${o.phand ?? 0.6}">${paleHand(560, 1700, 1.5, 6)}</g>',
    '<g id="${id}-phand" opacity="${o.phand ?? 0.6}">${paleHand(...(window.LANDSCAPE && o.phL ? o.phL : [560, 1700, 1.5, 6]))}</g>')
sub("ep1/body.part",
    'set: "pierPOV", setOpts: { id: "pp1", phand: 0, faces: 0.15 }, dark: 0.15,',
    'set: "pierPOV", setOpts: { id: "pp1", phand: 0, faces: 0.15, phL: [900, 1350, 1.5, -40] }, dark: 0.15, land: { y0: 150 }, // long: hand in the 16:9 band')
# part 1: the opener's tag
sub("ep1/body.part",
    'const OP = { title: "มือพราย", ep: "EP.1", name: "อย่าก้มคว้า",',
    'const OP = { title: "มือพราย", ep: "ฉบับเต็ม", name: "", // long: the tag reads ฉบับเต็ม\n        ')
# part 1: hug
sub("ep1/body.part",
    'set: "underRiver", setOpts: { id: "ur22" }, dark: 0.1,',
    'set: "underRiver", setOpts: { id: "ur22" }, dark: 0.1, land: { y0: 60 }, // long: heads and arms in the band')
# part 1: call (the พราย up 130, the band at 440)
sub("ep1/body.part",
    '<g id="${k}-ph" opacity=".4">${Phrai.phraiBody(1240, G + 640, 0.7,',
    '<g id="${k}-ph" opacity=".4">${Phrai.phraiBody(1290, G + 510, 0.7, /* long: was 1240, G + 640 */')
sub("ep1/body.part",
    'set: "porch", setOpts: CALLSET("po32"), dark: 0.25,',
    'set: "porch", setOpts: CALLSET("po32"), dark: 0.25, land: { y0: 440 }, // long: the พราย\'s face in the band')
# part 2: hands
sub("ep2/body.part",
    'set: "hullHands", setOpts: { id: "hh23" }, dark: 0.1,',
    'set: "hullHands", setOpts: { id: "hh23" }, dark: 0.1, land: { y0: 180 }, // long: the whole hull in the band')
# part 3: swim and land
sub("ep3/body.part",
    '...RT("rt2", { pose: "prone", x: 540, y: 1150, rot: -3, s: 1.0, kt: [[180, 400, 0.8], [980, 1500, 0.9], [60, 1900, 0.7]] }),',
    '...RT("rt2", { pose: "prone", x: 540, y: 1150, rot: -3, s: 1.0, kt: [[180, 400, 0.8], [980, 1500, 0.9], [60, 1900, 0.7]] }), land: { y0: 0 }, // long: whole swimmer at the start')
sub("ep3/body.part",
    'props: Phrai3.hosp(G), lamps: false }, dark: 0.22,',
    'props: Phrai3.hosp(G), lamps: false }, dark: 0.22, land: { y0: 400 }, // long: the hospital sign in the band')
print("\n".join(done))
