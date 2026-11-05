"""มือพราย long version (YouTube 16:9): widen every set in phrai.js so no set edge shows in the 16:9 frame.

The episodes' sets were drawn for the 1080-wide vertical frame over world x -900…2000. In 16:9 the frame shows 2400/zoom world px
around the camera, and at the zooms these shots use (0.82…1.3) that reaches past -900 and 2000: the porch wall, the river, the far
bank, the sky, the pier decks and the near water then end in a hard edge inside the picture. Everything is widened to x -2400…3500:
  - full-width rects and paths: x -900 → -2400 and every width +1500 (+3000 for the full-width ones)
  - loops that lay planks, posts, lamps and rails start further left on the same grid (lamps, rails and the pier crowd keep their
    original positions; the crowd is still spread over the original span)
  - the near water in front of swimmers (#id-wfront) continues its swell to the right
  - the cprTop deck: its water edge moves from x 960 to 1900, out of the 16:9 frame, so the top-down CPR shots are all planks as in 9:16;
    the rescuer's knees (drawn to be cut by the 9:16 left edge) are left out
  - random scatter (stars, ripples, reflections, water drops) is spread over the wider world with the count scaled to keep its density
Applied to the long version's own copies (phrailong/hf/lib1..3/phrai.js); the delivered episodes are untouched.
usage: python3 patch_libs.py   (run once on fresh copies)"""
import os

W = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def patch(s):
    def sub(old, new, count=1):
        nonlocal s
        n = s.count(old)
        assert n == count, (old[:80], n)
        s = s.replace(old, new)

    # ---- specific first (they contain the generic patterns) ----
    sub('M-900,${SY}Q-600,${SY - 20} -300,${SY}T300,${SY}T900,${SY}T1500,${SY}T2100,${SY}',
        'M-2100,${SY}Q-1800,${SY - 20} -1500,${SY}T-900,${SY}T-300,${SY}T300,${SY}T900,${SY}T1500,${SY}T2100,${SY}T2700,${SY}T3300,${SY}')
    sub('T${E + 1300},${WS}V2600', 'T${E + 1300},${WS}T${E + 2000},${WS}T${E + 2700},${WS}T${E + 3400},${WS}V2600')
    sub('T${E + 1300},${WS}" stroke', 'T${E + 1300},${WS}T${E + 2000},${WS}T${E + 2700},${WS}T${E + 3400},${WS}" stroke')
    sub('if (o.rail) s += `<path d="M-900,${G - 150}H${E - 60}"', 'if (o.rail) s += `<path d="M-2400,${G - 150}H${E - 60}"')
    sub('Array.from({ length: 14 }, (_, k) => `<rect x="${-880 + k * 110}"', 'Array.from({ length: 28 }, (_, k) => `<rect x="${-880 + (k - 14) * 110}"')
    sub('.filter((_, k) => -880 + k * 110 < E - 60)', '.filter((_, k) => -880 + (k - 14) * 110 < E - 60)')
    sub('x0 = p.x0 ?? -900', 'x0 = p.x0 ?? -2400')
    sub('const cx = x0 + 120 + k * ((x1 - x0 - 160) / 8)', 'const cx0 = p.x0 ?? -900, cx = cx0 + 120 + k * ((x1 - cx0 - 160) / 8)')
    sub('for (let x = x0 + 100; x < x1; x += 260)', 'for (let x = (p.x0 ?? -900) + 100 - 260 * 6; x < x1; x += 260)')
    sub('for (let x = -500; x < E; x += 380)', 'for (let x = -500 - 380 * 4; x < E; x += 380)')
    sub('for (let k = 0; k < 2; k++) {\n        const x0 = -700 + k * 1300', 'for (let k = -1; k < 3; k++) {\n        const x0 = -700 + k * 1300')
    # the cprTop deck: its water edge out of the 16:9 frame
    sub('<rect x="960" y="-600" width="1200" height="3400" fill="url(#phWater)"/><rect x="940" y="-600" width="40"',
        '<rect x="1900" y="-600" width="1600" height="3400" fill="url(#phWater)"/><rect x="1880" y="-600" width="40"')
    sub('M${f1(1000 + r() * 400)}', 'M${f1(1940 + r() * 400)}')
    # the rescuer's knees were drawn to be cut by the 9:16 frame's left edge (only their tips showed); in 16:9 they float whole
    # beside the boy as two blue blobs, so the long version leaves them out
    sub('    put(L.set, `<g opacity=".95">${[880, 1180].map((y) => ', '    if (!window.LANDSCAPE) put(L.set, `<g opacity=".95">${[880, 1180].map((y) => ')
    # the porch's near water and the pier deck's near water reach the new right edge; their ripples spread with them
    sub('<rect x="640" y="${G + 230}" width="1600"', '<rect x="640" y="${G + 230}" width="2860"')
    sub('for (let k = 0; k < 14; k++) s += `<path class="rip" d="M${f1(700 + r() * 900)}', 'for (let k = 0; k < 40; k++) s += `<path class="rip" d="M${f1(700 + r() * 2700)}')
    sub('width="${2000 - E}"', 'width="${3500 - E}"')
    sub('for (let k = 0; k < 16; k++) s += `<path class="rip" d="M${f1(E + r() * 1300)}', 'for (let k = 0; k < 40; k++) s += `<path class="rip" d="M${f1(E + r() * 3300)}')
    # random scatter over the wider world, same density
    sub('for (let i = 0; i < 90; i++) s += `<circle cx="${f1(-700 + r() * 2500)}"', 'for (let i = 0; i < 200; i++) s += `<circle cx="${f1(-2200 + r() * 5500)}"')
    sub('for (let k = 0; k < 40; k++) s += `<path class="rip" d="M${f1(-700 + r() * 2500)}', 'for (let k = 0; k < 88; k++) s += `<path class="rip" d="M${f1(-2200 + r() * 5500)}')
    sub('for (let k = 0; k < 24; k++) s += `<path class="rip" d="M${f1(-700 + r() * 2500)}', 'for (let k = 0; k < 53; k++) s += `<path class="rip" d="M${f1(-2200 + r() * 5500)}')
    sub('for (let k = 0; k < 30; k++) m += `<path class="mrefl" d="M${f1(-200 + r() * 1500)}', 'for (let k = 0; k < 90; k++) m += `<path class="mrefl" d="M${f1(-1700 + r() * 4500)}')
    sub('for (let k = 0; k < 40; k++) s += `<ellipse cx="${f1(-200 + r() * 1500)}"', 'for (let k = 0; k < 120; k++) s += `<ellipse cx="${f1(-1700 + r() * 4500)}"')
    sub('for (let k = 0; k < 40; k++) m += `<path class="mrefl" d="M${f1(-200 + r() * 1500)}', 'for (let k = 0; k < 120; k++) m += `<path class="mrefl" d="M${f1(-1700 + r() * 4500)}')
    sub('for (let k = 0; k < 22; k++) s += `<path class="rip" d="M${f1(-500 + r() * 2000)}', 'for (let k = 0; k < 60; k++) s += `<path class="rip" d="M${f1(-2200 + r() * 5500)}')
    # ---- generic extents ----
    sub('width="${E + 900}"', 'width="${E + 2400}"', 2)
    sub('width="1660"', 'width="3160"', 2)
    sub('x="-900" y="${WL - 220}" width="1500"', 'x="-900" y="${WL - 220}" width="3000"')
    sub('x="-900" y="${WL - 30}" width="1300"', 'x="-900" y="${WL - 30}" width="2800"')
    sub('width="2900"', 'width="5900"', 21)
    sub('x="-900"', 'x="-2400"', 27)
    sub('M-900,', 'M-2400,', 7)
    sub('H-900Z', 'H-2400Z', 4)
    sub('H2000', 'H3500', 4)
    sub('L2000,', 'L3500,', 2)
    sub('let x = -900; x <= 2000', 'let x = -2400; x <= 3500', 2)
    sub('let x = -880; x < 2000', 'let x = -2380; x < 3500', 3)
    sub('let x = -900; x < 2000', 'let x = -2400; x < 3500')
    sub('let x = -880; x < 520', 'let x = -2380; x < 520')
    sub('let x = -880; x < E', 'let x = -2380; x < E')
    sub('let x = -820; x < E', 'let x = -2320; x < E')
    sub('let x = -840; x < 600', 'let x = -2340; x < 600')
    return s


def patch3(s):
    """EP.3's own sets (phrai3.js): the hospital ward (dawn, wake, tell, dead, whisper, marks: "dawn" pulls back to zoom 0.6, so the
    9:16 room showed black past both walls) and the full-screen backgrounds. The hospital building's exterior (hosp) keeps its size."""
    def sub(old, new, count=1):
        nonlocal s
        n = s.count(old)
        assert n == count, (old[:80], n)
        s = s.replace(old, new)

    sub('<rect x="-900" y="-600" width="2900" height="3400" fill="#1b2420"/>', '<rect x="-2400" y="-600" width="5900" height="3400" fill="#1b2420"/>')
    sub('<rect x="-900" y="-600" width="2900" height="${G + 600}" fill="url(#p3Wall)"/><rect x="-900" y="${G - 220}" width="2900" height="220" fill="#8fa89c"/><path d="M-900,${G - 220}H2000"',
        '<rect x="-2400" y="-600" width="5900" height="${G + 600}" fill="url(#p3Wall)"/><rect x="-2400" y="${G - 220}" width="5900" height="220" fill="#8fa89c"/><path d="M-2400,${G - 220}H3500"')
    sub('<rect x="-900" y="${G}" width="2900" height="1200" fill="#cfd8d2"/>${Array.from({ length: 30 }, (_, k) => `<path d="M${-900 + k * 120},${G}V${G + 1200}"',
        '<rect x="-2400" y="${G}" width="5900" height="1200" fill="#cfd8d2"/>${Array.from({ length: 50 }, (_, k) => `<path d="M${-2340 + k * 120},${G}V${G + 1200}"')
    sub('<path d="M-900,${G + 60 + k * 120}H2000"', '<path d="M-2400,${G + 60 + k * 120}H3500"')
    sub('<rect x="-900" y="-900" width="2900" height="3800" fill="url(#phSky)"/>', '<rect x="-2400" y="-900" width="5900" height="3800" fill="url(#phSky)"/>')
    sub('<rect x="-900" y="-1200" width="2900" height="5200" fill="#1c1009"/>', '<rect x="-2400" y="-1200" width="5900" height="5200" fill="#1c1009"/>')
    sub('<rect x="-900" y="-600" width="2900" height="3400" fill="#e8eeea"/>', '<rect x="-2400" y="-600" width="5900" height="3400" fill="#e8eeea"/>')
    sub('<rect x="-900" y="-600" width="2900" height="3400" fill="#ffd9a0" opacity=".12"/>', '<rect x="-2400" y="-600" width="5900" height="3400" fill="#ffd9a0" opacity=".12"/>')
    return s


for e in (1, 2, 3):
    p = os.path.join(W, "hf", f"lib{e}", "phrai.js")
    s = open(p).read()
    assert "patch_libs: widened" not in s, "already patched"
    open(p, "w").write("// patch_libs: widened to x -2400…3500 for the 16:9 long version\n" + patch(s))
p = os.path.join(W, "hf", "lib3", "phrai3.js")
s = open(p).read()
assert "patch_libs: widened" not in s, "already patched"
open(p, "w").write("// patch_libs: widened to x -2400…3500 for the 16:9 long version (the ward and the backgrounds)\n" + patch3(s))
print("phrai.js widened (lib1..3) · phrai3.js ward widened (lib3)")
