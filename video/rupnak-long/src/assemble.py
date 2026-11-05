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
    if n == 2:  # 16:9 band: keep พ่อใหญ่สิน's face in the valve reveal (auto band crops his head)
        assert body.count('add("valve", { ') == 1
        body = body.replace('add("valve", { ', 'add("valve", { land: { y0: 0 }, ')
    blocks.append(f"      {{ // ======== EP.{n} ========\n        const P = \"e{n}_\";\n{SHIM}{helpers}{body}\n      }}\n")
ep2 = rd(f"{U}/ep2/body.part"); hdr = ep2[:ep2.index("      add(")]
hdr = hdr[: hdr.rfind("\n      //") + 1] if "\n      //" in hdr else hdr
blocks.append("      { // ======== bridges ========\n        const P = \"\";\n" + SHIM + hdr + rd(os.path.join(HERE, "bridge.part")) + "\n      }\n")
open(OUT, "w").write(head + sig + helpers + "".join(blocks) + foot)
print("template", len(head + sig + helpers + "".join(blocks) + foot))
