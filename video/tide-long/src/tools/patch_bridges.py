"""Long version (YouTube 16:9): the bridge shots in EP.2 and EP.3's body.part. Each edit is an exact, asserted replacement.
Run once on fresh copies of video/tide/ep2 and video/tide/ep3 (tidelong/ep2, tidelong/ep3)."""
import os
import sys

W = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def sub(path, old, new, count=1):
    s = open(path).read()
    n = s.count(old)
    assert n == count, (path, old[:70], n)
    open(path, "w").write(s.replace(old, new))


# ================= EP.2: bridge A =================
p = os.path.join(W, "ep2", "body.part")
sub(p, '      // ---------- 1. hook: EP.1\'s last frame; จูน dashes for the steps down ----------\n',
     '''      // ---------- long version, bridge A: close on จูน on the hill (the framing of "how"); she makes up her mind and bolts ----------
      // "จูนตัดสินใจ… วิ่งลงไปตามยาย": the choice EP.1 ended on, answered; the cut to "open" picks up her run
      const HIb = TideCast.headPoint("idle"), faceB = [JUNE.x - HIb[0] * JUNE.s, JUNE.y + HIb[1] * JUNE.s];
      add("brA", {
        ...HILL("thA", { line: 1 }), blur: { sky: 5, far: 5, mid: 5, set: 3, fg: 8 },
        cam: { keys: [{ t: 0, ...fr(faceB[0], faceB[1], 2.3, 560, 640) }, { t: D("brA"), glide: D("brA"), ...fr(faceB[0], faceB[1], 2.5, 560, 640) }] },
        actors: [A("june", JUNE.x, JUNE.y, JUNE.s, [{ t: 0, mode: "idle", eyes: "wide", mouth: "o" }, { t: 1.0, mode: "idle", eyes: "sideAngry", mouth: "frown" },
          { t: D("brA") - 0.42, mode: "run", eyes: "sideAngry", mouth: "frown" }], { flip: true, moveTo: { x: JUNE.x - 260, y: JUNE.y, dur: 0.42, at: D("brA") - 0.42, ease: "power2.in" } })],
        captions: caps("brA"),
        fx(tl, id, t0) { Tide.land(tl, "thA", t0, D("brA"), { siren: false }); },
      });
      // ---------- 1. hook: EP.1's last frame; จูน dashes for the steps down ----------
''')
# the clamp no longer waits for a voice line: it lands 0.3 s in, as it did on "อย่า"
sub(p, 'fx(tl, id, t0) { Tide.grab(tl, "gb", t0, D("grab"), { at: vo("grab", 0) }); },',
     'fx(tl, id, t0) { Tide.grab(tl, "gb", t0, D("grab"), { at: 0.3 }); },   // long version: no voice in this insert; the clamp at 0.3 s as before')

# ================= EP.3: bridge B =================
p = os.path.join(W, "ep3", "body.part")
sub(p, '      // ---------- 1. hook: the second wave, ยาย\'s side: people run past her shop to the pickups on the beach road ----------\n',
     '''      // ---------- long version, bridge B: back before the second wave — EP.2's siren angle: the tower blaring over the hotel and
      // ยาย's shop, still standing, the jam on the beach road below ("ย้อนกลับไป… ก่อนคลื่นลูกที่สองจะมาถึง") ----------
      add("brB", {
        ...LAND("lvB"), blur: { sky: 1, far: 1.5, mid: 1, fg: 4 },
        cam: { keys: [{ t: 0, ...fr(860, 1150, 1.2, 540, 900) }, { t: D("brB"), glide: D("brB"), ...fr(860, 1110, 1.32, 540, 900) }] },
        shake: (t) => ({ x: 1.0 * Math.sin(t * 23), y: 0, r: 0 }),
        captions: caps("brB"),
        fx(tl, id, t0, L) {
          Tide.land(tl, "lvB", t0, D("brB"), { siren: true });
          road(L, tl, t0, D("brB"), "lvB");
          walkers(L, tl, t0, D("brB"), "lvB", [
            { x0: 1200, y0: 1700, x1: 900, y1: 1650, s0: 0.75, s1: 0.72, step: 0.12, flip: true, at: 0.6 }, { x0: 40, y0: 1695, x1: 330, y1: 1648, s0: 0.75, s1: 0.72, step: 0.13, at: 1.2 },
          ]);
        },
      });
      // ---------- long version, bridge B: ยาย at her shop hugging the old photo, the moment the film left her (closer than EP.2's shop shot) ----------
      add("yai0", {
        ...LAND("lvY"), blur: { sky: 2, far: 2, mid: 1.5 },
        cam: { keys: [{ t: 0, ...fr(YAI.x, 1450, 2.3, 540, 960) }, { t: D("yai0"), glide: D("yai0"), ...fr(YAI.x, 1440, 2.45, 540, 960) }] },
        actors: [A("yaiTideHug", YAI.x, YAI.y, YAI.s, [{ t: 0, mode: "hugPhoto", eyes: "worry", mouth: "frown" }], { flip: true })],
        captions: caps("yai0"),
        fx(tl, id, t0, L) { Tide.land(tl, "lvY", t0, D("yai0"), { siren: true }); road(L, tl, t0, D("yai0"), "lvY"); },
      });
      // ---------- 1. hook: the second wave, ยาย's side: people run past her shop to the pickups on the beach road ----------
''')
print("bridge shots patched")
