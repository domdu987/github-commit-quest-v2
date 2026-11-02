# "128 ช่อ ที่ไม่ใช่ของเรา": "ถ้า..." hook (take H), Puck narration at 1.2x as the rider, and his wife's own line (take W,
# a female voice at 1.1x). Each take is kept whole; scene keys are anchored to Whisper word timestamps (Whisper writes
# วาเลนไทน์ as วาเลนไทย and ร้อยยี่สิบแปด as "รอ 28"; the words were checked with a second recogniser), then snapped to the
# real speech onset. Writes story17/vo.js + segments.json.
import json
import numpy as np
import soundfile as sf
W = json.load(open('story17/vo/words.json'))
BND = json.load(open('story17/vo/bounds.json'))
KEYS = 'HABCDEFWGL'
DB = {}
for k in KEYS:
    b, sr = sf.read(f'story17/vo/{k}44.wav'); f = int(sr * 0.01); n = len(b) // f
    r = np.sqrt((b[:n * f].reshape(n, f) ** 2).mean(1)); DB[k] = 20 * np.log10(r / r.max() + 1e-9)


def snap(k, a, b):
    """Speech onset inside [a, b): the end of the last silent run (>= 80 ms below -38 dB) in that window."""
    db = DB[k]; i0, i1 = int(a * 100), min(int(b * 100) + 6, len(db))
    quiet = db[i0:i1] < -38; best = None; run = 0
    for i, q in enumerate(quiet):
        run = run + 1 if q else 0
        if run >= 8: best = i0 + i + 1
    return a if best is None else max(a, best * 0.01 - 0.02)


def anchors(k, specs):
    toks = W[k]; txt = ''; idx = []
    for i, (w, a, b) in enumerate(toks):
        for _ in w: idx.append(i)
        txt += w
    out = {}
    for name, sub, after in specs:
        start = txt.find(sub, out[after][1] + 1 if after else 0)
        assert start >= 0, (k, name, sub, txt)
        while txt[start] == ' ': start += 1
        i = idx[start]
        a = toks[i][1]; nxt = toks[min(i + 2, len(toks) - 1)][1]
        out[name] = (round(snap(k, a, nxt), 3), start)
    return {n: v[0] for n, v in out.items()}, toks[0][1], toks[-1][2]


spec = {
 'H': [('H0', 'ถ้าคุณ', None), ('H1', 'ทั้งวัน', 'H0'), ('H2', 'ถ้าคน', 'H1'), ('H3', 'ไม่ได้', 'H2'), ('H4', 'เขาจะ', 'H3')],
 'A': [('A0', 'วาเลน', None), ('A1', 'เราขี่', 'A0'), ('A2', 'ตั้งแต่', 'A1')],
 'B': [('B0', 'ฝนตก', None), ('B1', 'เอาตัว', 'B0'), ('B2', 'ไม่ให้', 'B1')],
 'C': [('C0', 'ส่งไป', None), ('C1', 'ทุกคน', 'C0')],
 'D': [('D0', 'แต่ช่อ', None), ('D1', 'เราซื้อ', 'D0'), ('D2', 'ไม่ไหว', 'D1')],
 'E': [('E0', '4', None), ('E1', 'แอป', 'E0'), ('E2', 'ดอกไม้', 'E1'), ('E3', 'ปลายทาง', 'E2'), ('E4', 'บ้านเรา', 'E3')],
 'F': [('F0', 'เราเคาะ', None), ('F1', 'เมียเปิด', 'F0'), ('F2', 'เรายื่น', 'F1')],
 'W': [('W0', 'ทั้งวัน', None), ('W1', 'ช่อนี้', 'W0')],
 'G': [('G0', 'ส่งดอก', None), ('G1', 'เพิ่งรู้', 'G0'), ('G2', 'มันรู้สึก', 'G1')],
 'L': [('L0', 'วาเลน', None), ('L1', 'ส่งความ', 'L0'), ('L2', 'ทั้งวัน', 'L1')],
}
GAP = {'H': 0.55, 'A': 0.4, 'B': 0.4, 'C': 0.4, 'D': 0.6, 'E': 0.55, 'F': 0.4, 'W': 0.7, 'G': 0.6}   # D → title; W, G hold
P, segs, t = {}, [], 0.3
TITLE = 2.3; END = 3.0
for k in KEYS:
    an, first, last = anchors(k, spec[k])
    first = BND[k][0]; last = max(last, BND[k][1] - 0.04)
    an = {n: max(v, first) for n, v in an.items()}
    if k == 'E': t = P['title'] + TITLE
    off = t - first
    for n, v in an.items(): P[n] = round(v + off, 3)
    P[k + 'end'] = round(last + off, 3)
    segs.append({'file': f'story17/vo/{k}44.wav', 'src': [round(max(0, first - 0.05), 3), round(last + 0.12, 3)], 'on': round(t - 0.05, 3), 'name': k})
    t = last + off + GAP.get(k, 0.5)
    if k == 'D': P['title'] = round(last + off + GAP['D'], 3)
P['end'] = round(P['Lend'] + 1.0, 3)
P['DUR'] = round(P['end'] + END, 2)
for n in sorted(P, key=P.get): print(f'{n:5s} {P[n]:6.2f}')


def part(t_, s, a, b): return {'t': t_, 's': s, 'at': P[a], 'd': round(P[b] - P[a], 3)}


cues = [
 [part('ถ้าคุณส่งดอกไม้ให้คนอื่น', 'w', 'H0', 'H1'), part(' ทั้งวันวาเลนไทน์', 'y', 'H1', 'H2')],
 [part('ถ้าคนที่บ้าน', 'w', 'H2', 'H3'), part(' ไม่ได้สักช่อ', 'y', 'H3', 'H4')],
 [part('เขาจะน้อยใจไหม', 'r', 'H4', 'Hend')],
 [part('วาเลนไทน์ปีนี้', 'y', 'A0', 'A1'), part(' เราขี่มอไซค์ส่งดอกไม้', 'w', 'A1', 'A2')],
 [part('ตั้งแต่หกโมงเช้า', 'y', 'A2', 'Aend')],
 [part('ฝนตก', 'w', 'B0', 'B1'), part(' ก็ต้องเอาตัวบังดอกไม้ไว้', 'w', 'B1', 'B2')],
 [part('ไม่ให้ช้ำสักกลีบ', 'y', 'B2', 'Bend')],
 [part('ส่งไป 128 ช่อ', 'y', 'C0', 'C1'), part(' ทุกคนที่ได้ยิ้มหมด', 'w', 'C1', 'Cend')],
 [part('แต่ช่อละห้าร้อย', 'w', 'D0', 'D1')],
 [part('เราซื้อให้เมีย', 'w', 'D1', 'D2'), part(' ไม่ไหวสักช่อ', 'r', 'D2', 'Dend')],
 [part('สี่ทุ่ม', 'y', 'E0', 'E1'), part(' แอปเด้งออเดอร์สุดท้าย', 'w', 'E1', 'E2')],
 [part('ดอกไม้หนึ่งช่อ', 'w', 'E2', 'E3'), part(' ปลายทาง…', 'w', 'E3', 'E4'), part(' บ้านเราเอง', 'r', 'E4', 'Eend')],
 [part('เราเคาะประตูบ้านตัวเอง', 'w', 'F0', 'F1')],
 [part('เมียเปิดมารับ', 'w', 'F1', 'F2'), part(' แล้วยื่นช่อนั้นคืนให้เรา', 'y', 'F2', 'Fend')],
 [part('"ทั้งวันส่งให้คนอื่นแล้ว', 'p', 'W0', 'W1'), part(' ช่อนี้ของเธอนะ"', 'p', 'W1', 'Wend')],
 [part('ส่งดอกไม้มาทั้งวัน', 'w', 'G0', 'G1'), part(' เพิ่งรู้ว่าตอนได้รับ', 'y', 'G1', 'G2')],
 [part('มันรู้สึกแบบนี้นี่เอง', 'y', 'G2', 'Gend')],
 [part('วาเลนไทน์นี้', 'w', 'L0', 'L1'), part(' ส่งความรักให้คนที่ส่งให้คนอื่น', 'w', 'L1', 'L2')],
 [part('ทั้งวันบ้างนะ', 'r', 'L2', 'Lend')],
]
CUES = []
for j, parts in enumerate(cues):
    a = parts[0]['at']; last_end = max(p['at'] + p['d'] for p in parts)
    nxt = cues[j + 1][0]['at'] if j + 1 < len(cues) else 99
    CUES.append({'a': round(a, 3), 'b': round(min(nxt - 0.04, last_end + 0.5), 3), 'parts': parts})
CUES[-1]['b'] = round(P['end'] - 0.05, 3)
open('story17/vo.js', 'w').write('// generated by story17/place17.py\nconst VO = ' + json.dumps({'P': P, 'CUES': CUES}, ensure_ascii=False) + ';\n')
json.dump(segs, open('story17/segments.json', 'w'), ensure_ascii=False, indent=1)
