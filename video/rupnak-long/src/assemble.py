"""Assemble the full-story template: upgrade kit head + sigcard + helpers, then one block per episode (keys prefixed e1_/e2_/e3_
through a shadowed SH and helpers; scene ids prefixed so the three episodes' DOM ids never collide), the bridge block, one foot."""
import os, re, sys
U, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
rd = lambda p: open(p).read()
head, sig, helpers = rd(f"{U}/build/head.part"), rd(f"{U}/build/sigcard.part"), rd(f"{U}/build/helpers.part")
foot = rd(f"{U}/build/foot2.part").replace("รูพญานาค · EP.2", "รูพญานาค")
CAPS = re.search(r"      function caps\(k, lines, o = \{\}\) \{.*?\n      \}\n", head, re.S).group(0).replace("function caps(k, lines, o = {}) {", "const caps = function (k, lines, o = {}) {", 1).rstrip() + ";\n"
BUB = re.search(r"      const bub = .*\n", head).group(0)
SHIM = """        // shots cut from the full story (EP.2/3 hooks, choice and end cards) still run their spec code: give them a stand-in
        const CUTV = { t: 0, dur: 1, frags: [0, 0.3, 0.6, 0.9], cap: "- / - / - / -" };
        const CUT = { start: -100, dur: 1, vo: new Proxy([], { get: (a, i) => (i === "length" ? 4 : i === "map" ? (f) => [0, 1, 2, 3].map((j) => f(CUTV, j)) : CUTV) }) };
        const SH = new Proxy({}, { get: (_, k) => _SH[P + k] || CUT, has: (_, k) => (P + k) in _SH });
        const vo = (k, i = 0) => SH[k].vo[i].t;
        const voEnd = (k, i = 0) => SH[k].vo[i].t + SH[k].vo[i].dur;
        const F = (k, i = 0, j = 0) => SH[k].vo[i].t + SH[k].vo[i].frags[j];
        const D = (k) => SH[k].dur;
        const add = (k, spec) => _add(P + k, spec);
""" + CAPS + BUB

def ids_of(b):
    return set(re.findall(r'id: "([a-z0-9]{1,4})"', b)) | set(re.findall(r'\((?:L|tl), "([a-z0-9]{1,4})"', b))

def prefix_ids(b, n):
    for i in sorted(ids_of(b), key=len, reverse=True):
        q = f"e{n}{i}"
        b = re.sub(r'(id: )"%s"' % i, r'\1"%s"' % q, b)
        b = re.sub(r'(\((?:L|tl), )"%s"' % i, r'\1"%s"' % q, b)
        b = re.sub(r'(["\'])([#.]?)%s-' % i, lambda m: f"{m.group(1)}{m.group(2)}{q}-", b)
    return b

helpers = helpers.replace("const split = (k, at, A, B) => {", "const split = (k, at, A, B) => { if (!(k in SH)) return;")
blocks = ["      const _SH = SH, _add = add;\n"]
for n in (1, 2, 3):
    body = prefix_ids(rd(f"{U}/ep{n}/body.part"), n)
    # 16:9 band (sh.land y0) for shots whose subject the automatic band cuts: พ่อใหญ่สิน's face and the valve wheel,
    # the naga in the mural, the fenced hole the family bows to from 100 m
    # review 6 Nov (B1–B3, M3, M4): the rule card off the heads, ต้นข้าว's whole head, the shrine in frame, the stray head out of the barn shot
    for ep, key, y0 in ((2, "valve", 190), (2, "sin2", 420), (3, "close", 130), (3, "rule", 220), (3, "num", 380), (3, "shrine", 250), (3, "barn", 450), (1, "rule", 450), (1, "notch", 480), (2, "sin3", 350)):
        if n == ep:
            pat = f'add("{key}", {{ '
            assert body.count(pat) == 1, key
            body = body.replace(pat, pat + f"land: {{ y0: {y0} }}, ")
    if n == 3:   # review r2 M3: the barn-door cut has มุก's hand and ต้นข้าว's hair at the bottom left in 16:9: they leave from that cut on
        a0 = 'captions: caps("barn", undefined, { quote: true }), fx(tl, id, t0, L) { Rup2.barn(L, "e3bab");'
        assert body.count(a0) == 1; body = body.replace(a0, a0 + ' [0, 1].forEach((k) => tl.set(`#${id}-a${k}`, { opacity: 0 }, t0 + vo("barn", 1) - 0.1));')
    if n == 2:   # review r2 B2: the cold open (EP.2 open) redone for the long: brighter, the bucket pours, a second cut at 1.5 s
        a0 = body[body.index('      add("open", {'):body.index('      // ---------- 2. the command')]
        body = body.replace(a0, prefix_ids(rd(os.path.join(HERE, "coldopen.part")), 2))
    blocks.append(f"      {{ // ======== EP.{n} ========\n        const P = \"e{n}_\";\n{SHIM}{helpers}{body}\n      }}\n")
ep2 = rd(f"{U}/ep2/body.part"); hdr = ep2[:ep2.index("      add(")]
hdr = hdr[: hdr.rfind("\n      //") + 1] if "\n      //" in hdr else hdr
blocks.append("      { // ======== bridges ========\n        const P = \"\";\n" + SHIM + hdr + rd(os.path.join(HERE, "bridge.part")) + "\n      }\n")
open(OUT, "w").write(head + sig + helpers + "".join(blocks) + foot)
print("template", len(head + sig + helpers + "".join(blocks) + foot))
