"""make_contact.py : contact.jpg = one 720x1280 FINAL (placeholder actors at the stand points) per preset x light (x hook variant), label UNDER each tile, cyan line at y 880, plus the
per-tile render cost, head pixels and the hue report (hue_report.txt, cost_report.txt). Ship tiles are skipped gracefully while h19_ship is missing.
usage:  python3 make_contact.py run [name ...]     render the missing tiles (2 worker processes) then the sheet     (FORCE=1: re-render all given names)
        python3 make_contact.py tile NAME           render one tile (h19_work/final/NAME.png + .json)
        python3 make_contact.py sheet               contact.jpg + hue_report.txt + cost_report.txt from final/*.json"""
import os, sys, json, time, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
FINAL = os.path.join(HERE, 'h19_work', 'final'); os.makedirs(FINAL, exist_ok=True)
TILES = [   # name, preset, light, hooks (python, run after build), label
    ('W01_shop_wide_DAY', 'shop_wide', 'DAY', "H.set_balance(0.3)", 'shop_wide / DAY (H1 on the bench)'),
    ('W02_shop_wide_NIGHT', 'shop_wide', 'NIGHT', "H.set_balance(0.3)", 'shop_wide / NIGHT (candles + moon)'),
    ('W03_shop_bench_DAY', 'shop_bench', 'DAY', "H.set_balance(0.5)", 'shop_bench / DAY'),
    ('W04_shop_bench_NIGHT', 'shop_bench', 'NIGHT', "H.set_candles(0.6)", 'shop_bench / NIGHT (stub burnt to 0.6)'),
    ('W05_shop_clock_DAY', 'shop_clock', 'DAY', "", 'shop_clock / DAY (H1 + H4 shrink reveal)'),
    ('W06_shop_clock_NIGHT', 'shop_clock', 'NIGHT', "H.set_clock(3); H.set_balance(0.4)", 'shop_clock / NIGHT (H3)'),
    ('W07_shop_door_DAY', 'shop_door', 'DAY', "", 'shop_door / DAY (mocker visiting)'),
    ('W08_shop_door_NIGHT', 'shop_door', 'NIGHT', "", 'shop_door / NIGHT'),
    ('W09_shop_bench_H2', 'shop_bench', 'DAY', "H.set_clock(2); H.set_balance(0.7)", 'shop_bench / DAY + H2 hook'),
    ('W10_shop_clock_H4', 'shop_clock', 'DAY', "H.set_clock(4)", 'shop_clock / DAY + H4 watch alone'),
    ('H01_hall_wide_DAY', 'hall_wide', 'DAY', "", 'hall_wide / DAY'),
    ('H02_hall_wide_EVENING', 'hall_wide', 'EVENING', "H.set_stubs(10)", 'hall_wide / EVENING (10 stubs)'),
    ('H03_hall_table_DAY', 'hall_table', 'DAY', "H.set_moneybag('full'); H.set_box('sealed'); H.set_stubs(4)", 'hall_table / DAY (bag, sealed box, 4 stubs)'),
    ('H04_hall_table_EVENING', 'hall_table', 'EVENING', "H.set_moneybag('half'); H.set_box('open'); H.set_stubs(10)", 'hall_table / EVENING (half bag, open box, 10 stubs)'),
    ('H05_hall_low_DAY', 'hall_low', 'DAY', "", 'hall_low / DAY'),
    ('H06_hall_low_EVENING', 'hall_low', 'EVENING', "", 'hall_low / EVENING'),
    ('H07_hall_window_DAY', 'hall_window', 'DAY', "", 'hall_window / DAY'),
    ('H08_hall_window_EVENING', 'hall_window', 'EVENING', "", 'hall_window / EVENING'),
    ('H09_hall_door_DAY', 'hall_door', 'DAY', "", 'hall_door / DAY'),
    ('H10_hall_door_EVENING', 'hall_door', 'EVENING', "H.set_regulator(True)", 'hall_door / EVENING'),
    ('S01_ship_hero_NOON', 'ship_hero', 'NOON', "H.set_sea(0.0); H.set_roll(0.0)", 'ship_hero / NOON'),
    ('S02_ship_aerial_NOON', 'ship_aerial', 'NOON', "H.set_sea(0.0)", 'ship_aerial / NOON'),
    ('S03_ship_deck_NOON', 'ship_deck', 'NOON', "H.set_sea(0.0); H.set_roll(0.0)", 'ship_deck / NOON'),
    ('S04_ship_deck_overhead', 'ship_deck', 'NOON', "H.set_sea(0.0); H.set_sun_overhead(1.0)", 'ship_deck / NOON + sun overhead'),
    ('S05_ship_rail_NOON', 'ship_rail', 'NOON', "H.set_sea(0.0); H.set_roll(0.0)", 'ship_rail / NOON'),
    ('S06_ship_rocks_STORM', 'ship_rocks', 'STORM_DUSK', "H.set_rain(True)", 'ship_rocks / STORM_DUSK (rain)'),
    ('S07_ship_coast_DAY', 'ship_coast', 'DAY', "H.set_sea(0.0)", 'ship_coast / DAY'),
]
BYNAME = {t[0]: t for t in TILES}

def ship_ok():
    try:
        import importlib.util; return importlib.util.find_spec('h19_ship') is not None
    except Exception: return False

def do_tile(name):
    import bpy, h19 as H
    t = BYNAME[name]; _, preset, light, hooks, label = t
    A = H.build(preset, light=light); sc = bpy.context.scene; H.setup_render(sc, 'final')
    cs = A['cam']; cam = H.make_camera(cs)
    exec(hooks, dict(H=H, bpy=bpy))
    H.stage_placeholders(A['cam_name'], cs['loc']); bpy.context.view_layer.update(); hp = H.head_pixels(A['cam_name'])
    png = os.path.join(FINAL, name + '.png'); w, c = H.render(png)
    hue = H.measure_hue(png)
    json.dump(dict(name=name, label=label, preset=preset, light=light, wall=round(w, 1), cpu=round(c, 1), samples=sc.cycles.samples, heads=hp, hue=hue, load=os.getloadavg()[0]), open(os.path.join(FINAL, name + '.json'), 'w'))
    print('%s: %.1f s wall, %.1f s cpu, heads %s, hue %s' % (name, w, c, hp, hue), flush=True)

def sheet():
    from PIL import Image, ImageDraw, ImageFont
    W, H, LB, C = 720, 1280, 64, 6
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26); F2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 21)
    have = [t for t in TILES if os.path.exists(os.path.join(FINAL, t[0] + '.json'))]; rows = (len(have) + C - 1) // C
    S = Image.new('RGB', (W * C, (H + LB) * rows), (16, 16, 20)); d = ImageDraw.Draw(S); lines = []; cost = []
    for i, t in enumerate(have):
        js = json.load(open(os.path.join(FINAL, t[0] + '.json'))); im = Image.open(os.path.join(FINAL, t[0] + '.png')).convert('RGB'); x, y = (i % C) * W, (i // C) * (H + LB)
        S.paste(im, (x, y)); d.line([(x, y + 880), (x + W, y + 880)], fill=(0, 230, 255), width=2)
        h = js['hue']; hs = 'shade hue %s mag %.1f%%' % (h['shade_hue'], h['magenta'])
        d.text((x + 10, y + H + 6), t[4], fill=(235, 235, 235), font=F); d.text((x + 10, y + H + 36), '%s | %.0f cpu s' % (hs, js['cpu']), fill=(170, 210, 255), font=F2)
        indoor = t[1].startswith(('shop', 'hall'))
        lines.append('%-26s %-10s shade-hue(cast-shadow px) %-6s median %-6s in 225-265: %-6s cast %5.1f%% | magenta %5.2f%% (<=10) | %s' % (t[0], t[2], h['shade_hue'], h.get('median'), h['in_band'], h['cast_pct'], h['magenta'],
                     ('OK' if h['ok'] else ('magenta OK, warm indoor shade by design' if indoor and h['magenta'] <= 10 else 'CHECK'))))
        cost.append('%-26s %6.1f cpu s  %6.1f wall s  %d spp  heads(role,y,px,chin) %s' % (t[0], js['cpu'], js['wall'], js['samples'], [(a[0], a[2], a[3], a[4]) for a in js['heads']]))
    S.save(os.path.join(HERE, 'contact.jpg'), quality=86); S.resize((S.width // 3, S.height // 3), Image.LANCZOS).save(os.path.join(HERE, 'contact_small.jpg'), quality=86)
    mx = max(json.load(open(os.path.join(FINAL, t[0] + '.json')))['cpu'] for t in have)
    open(os.path.join(HERE, 'hue_report.txt'), 'w').write('hue per tile: cast-shadow hue (method of styleboard/hue_check.py; outdoors band 225-265, client shade 240-260), magenta share of the frame (limit 10 %). Indoor tiles: warm shade by design (approved on the board).\n' + '\n'.join(lines) + '\n')
    open(os.path.join(HERE, 'cost_report.txt'), 'w').write('CPU seconds of the final 720x1280 render call per tile (two worker processes in parallel, 2 threads each; limit 40 cpu s). Maximum: %.1f\n' % mx + '\n'.join(cost) + '\n')
    print(S.size, len(have)); print('\n'.join(lines)); print('\n'.join(cost))

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'sheet'; args = sys.argv[2:]
    if cmd == 'tile': do_tile(args[0])
    elif cmd == 'run':
        names = args or [t[0] for t in TILES]
        if not ship_ok(): names = [n for n in names if not BYNAME[n][1].startswith('ship')]; print('h19_ship missing: ship tiles skipped')
        force = bool(os.environ.get('FORCE')); todo = [n for n in names if force or not os.path.exists(os.path.join(FINAL, n + '.json'))]
        procs = []; q = list(todo)
        while q or procs:
            procs = [p for p in procs if p.poll() is None]
            while q and len(procs) < 2:
                n = q.pop(0); print('start', n, flush=True); procs.append(subprocess.Popen([sys.executable, os.path.abspath(__file__), 'tile', n], stdout=open(os.path.join(FINAL, n + '.log'), 'w'), stderr=subprocess.STDOUT))
            time.sleep(2)
        sheet()
    else: sheet()
