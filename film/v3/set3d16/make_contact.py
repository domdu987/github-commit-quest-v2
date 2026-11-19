"""make_contact.py : contact.jpg = one 720x1280 FINAL (placeholder actors at the stand points) per preset x light (x key state), label UNDER each tile, cyan line at y 880, plus the
per-tile render cost, head pixels and the hue report (hue_report.txt).
usage:  python3 make_contact.py run [name ...]     render the missing tiles (2 worker processes) then the sheet
        python3 make_contact.py tile NAME           render one tile (final/NAME.png + .json)
        python3 make_contact.py sheet               contact.jpg + hue_report.txt + cost table from final/*.json"""
import os, sys, json, time, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
FINAL = os.path.join(HERE, 'telegraph_work', 'final'); os.makedirs(FINAL, exist_ok=True)
TILES = [   # name, preset, light, hooks (python, run after build), staging override (role, mark) or None, label
    ('L01_line_close_AFTER_RAIN', 'line_close', 'AFTER_RAIN', '', None, 'line_close / AFTER_RAIN (ladder, drops)'),
    ('L02_line_close_DAY', 'line_close', 'DAY', "TG.set_wet(0.0)", None, 'line_close / DAY'),
    ('L03_line_close_RAIN', 'line_close', 'RAIN', "TG.set_rain(True); TG.set_leak('pole', 1.0)", None, 'line_close / RAIN (rain, pole sparks)'),
    ('L04_line_close_pulse', 'line_close', 'AFTER_RAIN', "TG.set_pulse(0.0105)", None, 'line_close / AFTER_RAIN + pulse bead'),
    ('L05_line_wide_DAY', 'line_wide', 'DAY', '', None, 'line_wide / DAY (train, poles)'),
    ('L06_line_wide_DUSK', 'line_wide', 'DUSK', '', None, 'line_wide / DUSK'),
    ('L07_line_wide_RAIN', 'line_wide', 'RAIN', "TG.set_poles('bare', 16); TG.set_rain(True)", None, 'line_wide / RAIN (bare poles, rain)'),
    ('L08_line_rail_DAY', 'line_rail', 'DAY', '', None, 'line_rail / DAY (train, station)'),
    ('L09_line_rail_pulse', 'line_rail', 'DAY', "TG.set_pulse(0.2)", None, 'line_rail / DAY + pulse'),
    ('L10_line_trench_DAY', 'line_trench', 'DAY', '', None, 'line_trench / DAY (plough, furrow)'),
    ('L11_line_trench_high_DUSK', 'line_trench_high', 'DUSK', "TG.set_light_mix('DAY', 'DUSK', 0.7)", None, 'line_trench_high / DAY->DUSK 0.7'),
    ('L12_line_trench_end_DUSK', 'line_trench_end', 'DUSK', '', None, 'line_trench_end / DUSK (key, coil)'),
    ('L13_line_trench_end_RAIN', 'line_trench_end', 'RAIN', "TG.set_rain(True)", None, 'line_trench_end / RAIN'),
    ('L14_trench_cut_DUSK', 'trench_cut', 'DUSK', '', None, 'trench_cut / DUSK (pipe, sparks)'),
    ('L15_line_road_DUSK', 'line_road', 'DUSK', '', None, 'line_road / DUSK (buggy)'),
    ('L16_line_wagon_AFTER_RAIN', 'line_wagon', 'AFTER_RAIN', '', None, 'line_wagon / AFTER_RAIN (bottles)'),
    ('S01_studio_wide_DAY', 'studio_wide', 'DAY', '', None, 'studio_wide / DAY'),
    ('S02_studio_easel_DAY', 'studio_easel', 'DAY', '', None, 'studio_easel / DAY'),
    ('S03_studio_door_DAY', 'studio_door', 'DAY', '', None, 'studio_door / DAY (door ajar, palette)'),
    ('S04_studio_window_DAY', 'studio_window', 'DAY', '', None, 'studio_window / DAY'),
    ('C01_chamber_wide_high_DAY', 'chamber_wide_high', 'DAY', '', None, 'chamber_wide_high / DAY'),
    ('C02_chamber_wide_high_NIGHT', 'chamber_wide_high', 'NIGHT', '', [('morse', 'morse_door')], 'chamber_wide_high / NIGHT'),
    ('C03_chamber_low_DAY', 'chamber_low', 'DAY', '', None, 'chamber_low / DAY (mail sacks)'),
    ('C04_chamber_low_NIGHT', 'chamber_low', 'NIGHT', "CH.set_mailsacks(False)", None, 'chamber_low / NIGHT'),
    ('C05_chamber_table_DAY', 'chamber_table', 'DAY', "CH.set_tape(0.55, 1)", None, 'chamber_table / DAY (tape, click)'),
    ('C06_chamber_table_money', 'chamber_table', 'DAY', "CH.set_moneybag(True)", None, 'chamber_table / DAY + money bag'),
    ('C07_chamber_table_NIGHT', 'chamber_table', 'NIGHT', "CH.set_tape(1.0, 0)", [('mocker', 'mocker_stool'), ('morse', 'morse_door')], 'chamber_table / NIGHT (candles, tape pile)'),
]
BYNAME = {t[0]: t for t in TILES}

def do_tile(name):
    import bpy, telegraph as TG, tg_chamber as CH, tg_studio as SD, tg_line as LN, tg_hue
    t = BYNAME[name]; _, preset, light, hooks, staging, label = t
    A = TG.build(None, preset, light=light); sc = bpy.context.scene; TG.setup_render(sc, 'final')
    exec(hooks, dict(TG=TG, CH=CH, SD=SD, LN=LN, SC=TG.SC, bpy=bpy))
    cs = A['cams'][A['cam_name']]; TG.make_camera(cs)
    if staging is not None: TG.STAGING['__tile'] = staging; nm = '__tile'
    else: nm = A['cam_name']
    TG.stage_placeholders(A, nm, cs['loc']); bpy.context.view_layer.update(); hp = TG.head_pixels(nm)
    png = os.path.join(FINAL, name + '.png'); w, c = TG.render(png)
    hue = tg_hue.measure(png)
    json.dump(dict(name=name, label=label, preset=preset, light=light, wall=round(w, 1), cpu=round(c, 1), samples=sc.cycles.samples, heads=hp, hue=hue, load=os.getloadavg()[0]), open(os.path.join(FINAL, name + '.json'), 'w'))
    print('%s: %.1f s wall, %.1f s cpu, heads %s, hue %s' % (name, w, c, hp, hue), flush=True)

def sheet():
    from PIL import Image, ImageDraw, ImageFont
    W, H, LB, C = 720, 1280, 64, 6
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26); F2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 21)
    have = [t for t in TILES if os.path.exists(os.path.join(FINAL, t[0] + '.png'))]; rows = (len(have) + C - 1) // C
    S = Image.new('RGB', (W * C, (H + LB) * rows), (16, 16, 20)); d = ImageDraw.Draw(S); lines = []; cost = []
    for i, t in enumerate(have):
        js = json.load(open(os.path.join(FINAL, t[0] + '.json'))); im = Image.open(os.path.join(FINAL, t[0] + '.png')).convert('RGB'); x, y = (i % C) * W, (i // C) * (H + LB)
        S.paste(im, (x, y)); d.line([(x, y + 880), (x + W, y + 880)], fill=(0, 230, 255), width=2)
        h = js['hue']; hs = 'shade hue %s mag %.1f%%' % (h['shade_hue'], h['magenta'])
        d.text((x + 10, y + H + 6), t[5], fill=(235, 235, 235), font=F); d.text((x + 10, y + H + 36), '%s | %.0f cpu s' % (hs, js['cpu']), fill=(170, 210, 255), font=F2)
        lines.append('%-30s %-8s shade-hue(cast-shadow px) %-6s median %-6s in 225-265: %-6s cast %5.1f%% | magenta %5.2f%% (<=10) | %s' % (t[0], t[2], h['shade_hue'], h.get('median'), h['in_band'], h['cast_pct'], h['magenta'], 'OK' if h['ok'] else ('n/a indoor / no shade' if t[1].startswith(('studio', 'chamber')) else 'CHECK')))
        cost.append('%-30s %6.1f cpu s  %6.1f wall s  %d spp  heads(y,px,chin) %s' % (t[0], js['cpu'], js['wall'], js['samples'], [(a[0], a[2], a[3], a[4]) for a in js['heads']]))
    S.save(os.path.join(HERE, 'contact.jpg'), quality=86); S.resize((S.width // 3, S.height // 3), Image.LANCZOS).save(os.path.join(HERE, 'contact_small.jpg'), quality=86)
    open(os.path.join(HERE, 'hue_report.txt'), 'w').write('hue per tile: cast-shadow hue (method of styleboard/hue_check.py; outdoors band 225-265, client shade 240-260), magenta share of the frame (limit 10 %)\n' + '\n'.join(lines) + '\n')
    open(os.path.join(HERE, 'cost_report.txt'), 'w').write('CPU seconds of the final 720x1280 render call per tile (two worker processes in parallel, 2 threads each)\n' + '\n'.join(cost) + '\n')
    print(S.size, len(have)); print('\n'.join(lines)); print('\n'.join(cost))

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'sheet'; args = sys.argv[2:]
    if cmd == 'tile': do_tile(args[0])
    elif cmd == 'run':
        names = args or [t[0] for t in TILES]; todo = [n for n in names if not os.path.exists(os.path.join(FINAL, n + '.json'))]
        # location-grouped, two workers
        procs = []; q = list(todo)
        while q or procs:
            procs = [p for p in procs if p.poll() is None]
            while q and len(procs) < 2:
                n = q.pop(0); print('start', n, flush=True); procs.append(subprocess.Popen([sys.executable, os.path.abspath(__file__), 'tile', n], stdout=open(os.path.join(FINAL, n + '.log'), 'w'), stderr=subprocess.STDOUT))
            time.sleep(2)
        sheet()
    else: sheet()
