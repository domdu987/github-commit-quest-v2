"""นาทีก่อนจม ฉบับเต็ม: the full-story template. EP.3's head + sigcard + helpers, the shared set/kit parts once (EP.3's copies are a
superset of EP.1/2's), then one block per episode body (keys prefixed e1_/e2_/e3_ through a shadowed SH and helpers; scene ids prefixed
so the three bodies' DOM ids never collide), the bridge block (bridge.part), and one foot.
usage: python3 assemble.py <video dir> <out ep.tmpl.html> [land.json]   (land.json: {"e2_fist": {"y0": 300, "ui": {"x": 24}}, ...})"""
import json, os, re, sys
V, OUT = sys.argv[1], sys.argv[2]
LAND = json.load(open(sys.argv[3])) if len(sys.argv) > 3 and os.path.exists(sys.argv[3]) else {}
HERE = os.path.dirname(os.path.abspath(__file__))
rd = lambda p: open(p).read()
P3 = f"{V}/sink-ep3/production"
head, sig, helpers = rd(f"{P3}/head.part"), rd(f"{P3}/sigcard.part"), rd(f"{P3}/helpers.part")
shared = "".join(rd(f"{P3}/{p}.part") for p in ("kit", "kit2", "hands", "kit3", "cut", "rich", "ep2", "ep3", "ep3b", "world", "sinkui"))
foot = rd(f"{P3}/foot.part").replace("นาทีก่อนจม · EP.3", "นาทีก่อนจม")
assert "นาทีก่อนจม</div>" in foot
CAPS = re.search(r"      function caps\(k, lines, o = \{\}\) \{.*?\n      \}\n", head, re.S).group(0).replace("function caps(k, lines, o = {}) {", "const caps = function (k, lines, o = {}) {", 1).rstrip() + ";\n"
BUB = re.search(r"      const bub = .*\n", head).group(0)
SHIM = """        // shots cut from the full story still run their spec code: give them a stand-in
        const _CUTV = { t: 0, dur: 1, frags: [0, 0.3, 0.6, 0.9], cap: "- / - / - / -" };
        const _CUT = { start: -100, dur: 1, vo: new Proxy([], { get: (a, i) => (i === "length" ? 4 : i === "map" ? (f) => [0, 1, 2, 3].map((j) => f(_CUTV, j)) : _CUTV) }) };
        // a re-used shot may read more voice lines than its bridge line gives it: missing indices get a silent stand-in at the shot's end
        const _W = {};
        const SH = new Proxy({}, { get: (_, k) => { const s = _SH[P + k]; if (!s) return _CUT;
          return _W[k] || (_W[k] = { ...s, vo: new Proxy(s.vo, { get: (a, i) => (i in a || !/^[0-9]+$/.test(i) ? a[i] : { t: Math.max(0, s.dur - 0.3), dur: 0.1, frags: [0, 0.03, 0.06, 0.09], cap: "" }) }) }); },
          has: (_, k) => (P + k) in _SH });
        const vo = (k, i = 0) => SH[k].vo[i].t;
        const voEnd = (k, i = 0) => SH[k].vo[i].t + SH[k].vo[i].dur;
        const F = (k, i = 0, j = 0) => SH[k].vo[i].t + SH[k].vo[i].frags[j];
        const D = (k) => SH[k].dur;
        const add = (k, spec) => { const L = LAND[P + k]; _add(P + k, L ? { ...spec, land: { ...(spec.land || {}), ...L } } : spec); };
""" + CAPS + BUB

def ids_of(b):
    # scene ids: id: "x", (L|tl, "x", and any short id-like literal with a digit ("h0", "kh2"…) handed to helpers such as inWater;
    # "a0"/"a1" are actor suffixes, not ids
    lit = set(re.findall(r'"([a-z]{1,3}[0-9][a-z0-9]{0,3})"', b)) - {"a0", "a1", "a2", "a3", "a4"}
    return set(re.findall(r'id: "([A-Za-z0-9]{1,6})"', b)) | set(re.findall(r'\((?:L|tl), "([A-Za-z0-9]{1,6})"', b)) | lit

def prefix_ids(b, tag):
    for i in sorted(ids_of(b), key=len, reverse=True):
        q = f"{tag}{i}"
        b = re.sub(r'(id: )"%s"' % i, r'\1"%s"' % q, b)
        b = re.sub(r'(\((?:L|tl), )"%s"' % i, r'\1"%s"' % q, b)
        b = re.sub(r'(["\'`])([#.]?)%s-' % i, lambda m: f"{m.group(1)}{m.group(2)}{q}-", b)
        b = re.sub(r'"%s"' % i, f'"{q}"', b)
    return b

hl = helpers.replace("const split = (k, at, A, B) => {", "const split = (k, at, A, B) => { if (!(k in SH)) return;")
assert hl != helpers
blocks = ["      const _SH = SH, _add = add, LAND = " + json.dumps(LAND, ensure_ascii=False) + ";\n"]
# the road signs in the hook shots: the cold open (EP.3 hook) names the full story, EP.1's names its chapter, the bridge copy has none
SIGN = {("e", 3): ('sub: "EP.3 ช่วยจากบนฝั่ง · ตอนจบ"', 'sub: "ฉบับเต็ม"'), ("e", 1): ('sub: "EP.1 อย่าเพิ่งโทรหาใคร"', 'sub: "บทที่ 1 · อย่าเพิ่งโทรหาใคร"'),
        ("x", 3): ('title: { x: 300, sub: "EP.3 ช่วยจากบนฝั่ง · ตอนจบ" }', "title: false"),
        ("x", 2): ('captions: caps("surface", undefined, QUO),', 'captions: caps("surface"),')}   # bridge B puts narration on her shot: no quote marks
for pre, label in (("e", "EP"), ("x", "bridge copy of EP")):
    for n in (1, 2, 3):
        body = rd(f"{V}/sink-ep{n}/production/body.part")
        if (pre, n) in SIGN:
            a0, b0 = SIGN[(pre, n)]; assert body.count(a0) == 1, a0; body = body.replace(a0, b0)
        body = prefix_ids(body, f"{pre}{n}")
        blocks.append(f"      {{ // ======== {label}.{n} ========\n        const P = \"{pre}{n}_\";\n{SHIM}{hl}{body}\n      }}\n")
blocks.append("      { // ======== cold-open gap ========\n        const P = \"\";\n" + SHIM + hl + rd(os.path.join(HERE, "bridge.part")) + "\n      }\n")
html = head + sig + helpers + shared + "".join(blocks) + foot
open(OUT, "w").write(html)
print("template", len(html))
