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
# review 6 Nov (long only): B4 the ambulance ~2.4 m (it was ~0.9 m beside a 1.65 m rider), parked behind the people (set layer), its
# lights a glow around the vehicle instead of the whole frame flashing (M11); M6 the side-glass card lights the film on 1 of 3 cars (AAA)
AMB = [('put(L.act, `<g transform="translate(${x},${RY + 26})"><g id="${id}">',
        'put(L.set, `<g transform="translate(${x + AMB_DX},${RY + 26}) scale(${AMB_S})"><g id="${id}"><defs><radialGradient id="${id}-gr"><stop offset="0" stop-color="#ff2a1a" stop-opacity=".6"/><stop offset="1" stop-color="#ff2a1a" stop-opacity="0"/></radialGradient><radialGradient id="${id}-gb"><stop offset="0" stop-color="#2a5aff" stop-opacity=".6"/><stop offset="1" stop-color="#2a5aff" stop-opacity="0"/></radialGradient></defs><ellipse id="${id}-wr" cx="-40" cy="-200" rx="330" ry="190" fill="url(#${id}-gr)" opacity="0"/><ellipse id="${id}-wb" cx="-40" cy="-200" rx="330" ry="190" fill="url(#${id}-gb)" opacity="0"/>'),
       ('        put(L.light, `<rect id="${id}-wr" width="1080" height="1920" fill="#ff2a1a" opacity="0"/><rect id="${id}-wb" width="1080" height="1920" fill="#1a4aff" opacity="0"/>`);\n', ''),
       ('tl.set(`#${id}-wr`, { opacity: 0.16 }, t0 + k); tl.set(`#${id}-wb`, { opacity: 0 }, t0 + k);', 'tl.set(`#${id}-wr`, { opacity: 1 }, t0 + k); tl.set(`#${id}-wb`, { opacity: 0 }, t0 + k);'),
       ('tl.set(`#${id}-wr`, { opacity: 0 }, t0 + k + 0.25); tl.set(`#${id}-wb`, { opacity: 0.16 }, t0 + k + 0.25);', 'tl.set(`#${id}-wr`, { opacity: 0 }, t0 + k + 0.25); tl.set(`#${id}-wb`, { opacity: 1 }, t0 + k + 0.25);'),
       ('${car(1, 720, true)}${car(2, 1020, true)}', '${car(1, 720, false)}${car(2, 1020, true)}'),
       ('[1, 2].forEach((k, j) => tl.fromTo(`#${id}-f${k}`', '[2].forEach((k, j) => tl.fromTo(`#${id}-f${k}`')]
for a, b in AMB:
    assert shared.count(a) == 1, a[:60]; shared = shared.replace(a, b)
shared += rd(os.path.join(HERE, "pry.part"))   # M6: the headrest pry card and the float-and-shoe beat (long only)
shared = "      const AMB_S = 2.6, AMB_DX = 270;\n" + shared
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
SIGN = {("e", 3): [('sub: "EP.3 ช่วยจากบนฝั่ง · ตอนจบ"', 'sub: "ฉบับเต็ม"'),
                   # r2 B5: the cold open pushes in on ขิม (head ~1/4 of the frame), a warm street-lamp pool lifts it, and under the water the
                   # sunken car's cabin glows with a column of bubbles where ต้น still is; the bike still rolls in on the road behind her
                   ('cam: { keys: [{ t: 0, ...fr(460, 1060, 1.25, 540, 960) }, { t: D("hook"), glide: D("hook"), ...fr(480, 1075, 1.32, 540, 960) }] },',
                    'cam: { keys: [{ t: 0, ...fr(316, 1270, 3.9, 290, 1100) }, { t: D("hook"), glide: D("hook"), ...fr(316, 1268, 4.25, 290, 1100) }] },'),
                   ('inWater(L, tl, t0, D("hook"), "h0");',
                    'inWater(L, tl, t0, D("hook"), "h0"); put(L.set, `<radialGradient id="coWarm"><stop offset="0" stop-color="#ffd9a0" stop-opacity=".9"/><stop offset=".6" stop-color="#ffc070" stop-opacity=".35"/><stop offset="1" stop-color="#ffc070" stop-opacity="0"/></radialGradient><ellipse cx="380" cy="1240" rx="230" ry="120" fill="url(#coWarm)" opacity=".45"/>`); put(L.act, `<radialGradient id="coCabG"><stop offset="0" stop-color="#bff4ff" stop-opacity=".95"/><stop offset="1" stop-color="#9fe8ff" stop-opacity="0"/></radialGradient><ellipse id="coCab" cx="470" cy="${WY + 46}" rx="120" ry="44" fill="url(#coCabG)" style="mix-blend-mode:screen"/><ellipse cx="316" cy="${WY + 4}" rx="300" ry="46" fill="url(#coWarm)" opacity=".55" style="mix-blend-mode:screen"/>`); tl.fromTo("#coCab", { opacity: 1 }, { opacity: 0.75, duration: 0.2, yoyo: true, repeat: Math.ceil(D("hook") / 0.2), ease: "steps(1)", immediateRender: false }, t0 + 0.6); bubbles(L, tl, "h0cb", t0, D("hook"), 480, WY + 10, 22, 50); { const ck = L.set.closest(".clip"); if (ck) ck.style.filter = "brightness(1.5) saturate(1.08)"; }')], ("e", 1): ('sub: "EP.1 อย่าเพิ่งโทรหาใคร"', 'sub: "บทที่ 1 · อย่าเพิ่งโทรหาใคร"'),
        ("x", 3): [('title: { x: 300, sub: "EP.3 ช่วยจากบนฝั่ง · ตอนจบ" }', "title: false"),
                   ('captions: caps("kim", undefined, QUO),', 'captions: [...caps("kim", [0], QUO), ...caps("kim", [1])],')],   # M4: the narrator's x02 line without quote marks
        ("x", 2): [('captions: caps("surface", undefined, QUO),', 'captions: caps("surface"),'),
                   # M5: the bridge copy starts with her already up (no second surfacing splash) and the camera drifts to the car's bubbles
                   ('path: [{ t: 0, x: 540, y: 2300 }, { t: 0.24, x: 540, y: 1890 }]', 'path: [{ t: 0, x: 540, y: 1890 }]'),
                   ('          Canal.splash(L, tl, "sf0s", 540, 1206, t0 + 0.12);\n', '          bubbles(L, tl, "sf0cb", t0, D("surface"), 860, 1214, 26, 160); bubbles(L, tl, "sf0cc", t0 + 0.4, D("surface"), 900, 1214, 18, 120);\n'),
                   ('cam: { keys: [{ t: 0, ...fr(540, 1110, 1.9, 540, 980) }, { t: D("surface"), glide: D("surface"), ...fr(540, 1100, 2.05, 540, 980) }] },',
                    'cam: { keys: [{ t: 0, ...fr(560, 1110, 1.9, 540, 980) }, { t: D("surface"), glide: D("surface"), ...fr(760, 1150, 1.7, 540, 980) }] },')],
        ("x", 1): [('captions: caps("flicker"),', 'captions: caps("flicker", undefined, QUO),'),
                   ('flickerOut(L, tl, "cc3", t0, D("flicker"));', '')]}   # bridge A: the lights hold while she speaks (no black-out)   # bridge A: ขิม's own line on the dark-car shot   # bridge B puts narration on her shot: no quote marks
for pre, label in (("e", "EP"), ("x", "bridge copy of EP")):
    for n in (1, 2, 3):
        body = rd(f"{V}/sink-ep{n}/production/body.part")
        if (pre, n) in SIGN:
            reps = SIGN[(pre, n)]; reps = [reps] if isinstance(reps[0], str) else reps
            for a0, b0 in reps: assert body.count(a0) == 1, a0; body = body.replace(a0, b0)
        if n == 2:   # M6: the headrest shot teaches the DDC way (rod into the groove, pry) instead of "a bad choice"
            i0 = body.index('      split("headrest", HS, {'); i1 = body.index("      // ---------- 11.")
            body = body[:i0] + """      add("headrest", {
        dark: 0, light: false,
        cam: { keys: [{ t: 0, ...fr(540, 960, 1.0, 540, 960), drift: { s: 0 } }] },
        captions: caps("headrest"),
        fx(tl, id, t0, L) { SinkUI.pry(tl, L.light, t0, D("headrest"), { at: F("headrest", 0, 1) + 0.35 }); },
      });
""" + body[i1:]
        if pre == "e" and n == 3:   # M6: the shoe beat: the foot slips out (picture only), then he floats and lets the other shoe go
            a0 = """        fx(tl, id, t0, L) { shoeOff(L, tl, "fi0", t0 + 0.7); bubbles(L, tl, "fi0bb", t0, D("shoe"), 500, 1200, 16, 600); },
      });"""
            assert body.count(a0) == 1
            i0 = body.index('      add("shoe", {')
            body = body[:i0] + """      const SS = F("shoe", 0, 1) - 0.05;
      split("shoe", SS, {
        set: "footIns", setOpts: { id: "fi0" }, dark: 0.1, light: false, grade: GWATER,
        cam: { keys: [{ t: 0, ...fr(560, 1000, 1.0, 540, 960) }, { t: SS, glide: SS, ...fr(560, 980, 1.08, 540, 960) }] },
        captions: caps("shoe"),
        fx(tl, id, t0, L) { shoeOff(L, tl, "fi0", t0 + 0.25); bubbles(L, tl, "fi0bb", t0, SS, 500, 1200, 16, 600); },
      }, {
        ...BANK("cnf"),
        cam: { keys: [{ t: 0, ...fr(KW.x + 80, 1180, 1.9, 540, 900) }, { t: D("shoe") - SS, glide: D("shoe") - SS, ...fr(KW.x + 120, 1170, 2.05, 540, 900) }] },
        actors: [A("tonJ", KW.x, KW.y - 10, KW.s, [{ t: 0, mode: "idle", eyes: "worry", mouth: "o" }])],
        captions: capsFrom("shoe", SS),
        fx(tl, id, t0, L) { noShadows(tl, id, 1); Klong.life(tl, "cnf", t0, D("shoe") - SS); inWater(L, tl, t0, D("shoe") - SS, "fl0"); floatShoe(L, tl, "fs0", t0, D("shoe") - SS, KW.x + 60, WY - 10); },
      });""" + body[body.index(a0) + len(a0):]
        if pre == "e" and n == 3:   # B4: the hospital shot pulls back so the full-size ambulance fits beside them
            a0 = 'cam: { keys: [{ t: 0, ...fr(600, 940, 1.35, 540, 960) }, { t: D("hosp"), glide: D("hosp"), ...fr(620, 930, 1.45, 540, 960) }] },'
            assert body.count(a0) == 1; body = body.replace(a0, 'cam: { keys: [{ t: 0, ...fr(700, 900, 1.0, 540, 960) }, { t: D("hosp"), glide: D("hosp"), ...fr(710, 895, 1.06, 540, 960) }] },')
        if n == 3:   # B4: the twist push-in was framed for the old bike size: keep the same framing on the dark headlight
            a0 = "fr(BIKE.x - 0.3 * 283, BIKE.y - 0.3 * 430, 3.4, 540, 900)"; assert body.count(a0) == 1
            body = body.replace(a0, "fr(BIKE.x - BIKE.s * 283, BIKE.y - BIKE.s * 430, 3.4 * 0.3 / BIKE.s, 540, 900)")
        if n == 3:   # B4 (r2): the bike's scale per shot: ~1.1 m beside the rider in the close bank shots (and moved clear of him), the wide
            # shots keep the old 0.3 (there the rider rides far up the road)
            for a0, b0 in (('parkedBike(L, "bk2", BIKE.x, BIKE.y, BIKE.s)', 'parkedBike(L, "bk2", BIKE.x, BIKE.y, 0.58)'),
                           ('parkedBike(L, "bk4", BIKE.x, BIKE.y, BIKE.s)', 'parkedBike(L, "bk4", BIKE.x + 280, BIKE.y, 0.58)'),
                           ('parkedBike(L, "bk5", BIKE.x, BIKE.y, BIKE.s)', 'parkedBike(L, "bk5", BIKE.x + 280, BIKE.y, 0.58)'),
                           ('parkedBike(L, "bk6", BIKE.x, BIKE.y, BIKE.s)', 'parkedBike(L, "bk6", BIKE.x + 280, BIKE.y, 0.58)'),
                           ('parkedBike(L, "bk8", BIKE.x + 120, BIKE.y, BIKE.s)', 'parkedBike(L, "bk8", BIKE.x + 120, BIKE.y, 0.58)')):
                assert body.count(a0) == 1, a0; body = body.replace(a0, b0)
        body = prefix_ids(body, f"{pre}{n}")
        blocks.append(f"      {{ // ======== {label}.{n} ========\n        const P = \"{pre}{n}_\";\n{SHIM}{hl}{body}\n      }}\n")
blocks.append("      { // ======== cold-open gap ========\n        const P = \"\";\n" + SHIM + hl + rd(os.path.join(HERE, "bridge.part")) + "\n      }\n")
html = head + sig + helpers + shared + "".join(blocks) + foot
open(OUT, "w").write(html)
print("template", len(html))
