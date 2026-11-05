"""Long version, review fix B1 (review desk 6 Nov): ยาย at true scale in EP.3's road shots. Run after patch_bridges.py (it rewrites
the bridge shot yai0). Exact, asserted replacements in tidelong/ep3/body.part.

The fault (in the delivered EP.3 too, much plainer in the long's close yai0): in the "land" view ยาย stood on the beach just in front of
the road at rig scale 0.62, about 4-5x the height of the cars (Mok at 0.36) and of the people running past (Tide.fig at ~0.75), with her
head at the shop's roof; and in yai0 a car was drawn over her apron while her sarong and feet showed below it.

The fix:
  - hook, yai: ยาย stands on her shop's deck behind the road (the land view's shop is drawn at (830, 1560) scale 0.86; its deck top is
    at y ~1514), at rig scale 0.16 (~100 px: a 1.55 m woman at the cars' ~65 px/m), so cars, runners, tables and ยาย share one scale and
    the road is in front of her. "yai" starts close on her (zoom 4.6) before its pan up to the hotel, as before.
  - yai0 ("ยายยังอยู่ที่ร้าน… กอดรูปเก่าไว้"): inside the shop, in its own perspective room (Sets.tideShop "room", as EP.1's "acct"),
    behind the counter at Tide.SHOP.spots.yai, eerie light; the old photo is in her arms, so its place on the wall is bare (#shY-photo hidden).
"""
import os

W = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
p = os.path.join(W, "ep3", "body.part")


def sub(old, new, count=1):
    s = open(p).read()
    n = s.count(old)
    assert n == count, (old[:80], n)
    open(p, "w").write(s.replace(old, new))


sub('      const YAI = { x: 820, y: 1720, s: 0.62 }, HOTEL = { x: 300, y: 1060 };\n',
    '      // long version (review fix B1): ยาย on her shop\'s deck behind the road, at the cars\' and the runners\' scale (was x 820, y 1720, s 0.62:\n'
    '      // on the beach in front of the road and 4-5x their height)\n'
    '      const YAI = { x: 900, y: 1514, s: 0.16 }, HOTEL = { x: 300, y: 1060 };\n')

# yai0: the shop's perspective room instead of the land view
sub('''      add("yai0", {
        ...LAND("lvY"), blur: { sky: 2, far: 2, mid: 1.5 },
        cam: { keys: [{ t: 0, ...fr(YAI.x, 1450, 2.3, 540, 960) }, { t: D("yai0"), glide: D("yai0"), ...fr(YAI.x, 1440, 2.45, 540, 960) }] },
        actors: [A("yaiTideHug", YAI.x, YAI.y, YAI.s, [{ t: 0, mode: "hugPhoto", eyes: "worry", mouth: "frown" }], { flip: true })],
        captions: caps("yai0"),
        fx(tl, id, t0, L) { Tide.land(tl, "lvY", t0, D("yai0"), { siren: true }); road(L, tl, t0, D("yai0"), "lvY"); },
      });
''', '''      // (review fix B1: inside the shop, in its own perspective room as EP.1's "acct", behind the counter at Tide.SHOP.spots.yai; the old
      // photo is in her arms, so its place on the wall is bare)
      const YS = Tide.shopPos(...Tide.SHOP.spots.yai);
      add("yai0", {
        set: "tideShop", setOpts: { id: "shY", view: "room", time: "eerie" }, dark: 0.05, blur: { sky: 2, far: 2 }, light: EERIE, grade: GEERIE,
        cam: { keys: [{ t: 0, ...fr(YS.x + 30, YS.y - 290, 3.2, 540, 900) }, { t: D("yai0"), glide: D("yai0"), ...fr(YS.x + 28, YS.y - 292, 3.4, 540, 900) }] },
        actors: [A("yaiTideHug", YS.x, YS.y, YS.s, [{ t: 0, mode: "hugPhoto", eyes: "worry", mouth: "frown" }])],
        captions: caps("yai0"),
        fx(tl, id, t0) { tl.set("#shY-photo", { opacity: 0 }, t0); },
      });
''')

# yai: start close on her at the new spot, then the same pan up to the hotel
sub('cam: { keys: [{ t: 0, ...fr(YAI.x, YAI.y - 300, 1.3, 540, 1150) }, { t: D("yai"), glide: D("yai") - 0.6, ease: "power2.inOut", ...fr(HOTEL.x, HOTEL.y, 1.15, 540, 760) }] },',
    'cam: { keys: [{ t: 0, ...fr(YAI.x, YAI.y - 55, 4.6, 540, 1000) }, { t: D("yai"), glide: D("yai") - 0.6, ease: "power2.inOut", ...fr(HOTEL.x, HOTEL.y, 1.15, 540, 760) }] },')
print("scale fix patched")

# review note M4: the opener's sand still said "EP.1" under the title; the long version reads "ฉบับเต็ม" there
p1 = os.path.join(W, "ep1", "body.part")
s1 = open(p1).read()
old = 'setOpts: { id: "sd0", title: "ทะเลลด", sub: "EP.1" }'
assert s1.count(old) == 1, s1.count(old)
open(p1, "w").write(s1.replace(old, 'setOpts: { id: "sd0", title: "ทะเลลด", sub: "ฉบับเต็ม" }'))
print("opener sub patched")
