# "12 ฤดูฝน ที่ไหล่ของพ่อเปียก": "ถ้า..." hook (take H), then Puck narration at 1.2x. Each take is kept whole; scene keys are
# anchored to Whisper word timestamps, then snapped to the real speech onset (Whisper stretches a word's start back over the
# pause before it). Writes story11/vo.js + segments.json.
import json
import numpy as np
import soundfile as sf
W = json.load(open('story11/vo/words.json'))
BND = json.load(open('story11/vo/bounds.json'))
DB = {}
for k in 'HABCD':
    b, sr = sf.read(f'story11/vo/{k}44.wav'); f = int(sr * 0.01); n = len(b) // f
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
 'H': [('H0', 'ถ้าคุณ', None), ('H1', 'ใต้ร่ม', 'H0'), ('H2', 'ถ้าไหล่', 'H1'), ('H3', 'เปียก', 'H2'), ('H4', 'คุณเคยสังเกต', 'H3')],
 'A': [('A0', 'ตั้งแต่', None), ('A1', 'ฝนตก', 'A0'), ('A2', 'พ่อจะ', 'A1'), ('A3', 'กับร่ม', 'A2'), ('A4', 'เดินกลับ', 'A3'),
       ('A5', 'ถึงบ้าน', 'A4'), ('A6', 'ตัวเรา', 'A5')],
 'B': [('B0', 'เราเคย', None), ('B1', 'ทำไม', 'B0'), ('B2', 'พ่อบอก', 'B1'), ('B3', 'คันใหญ่มัน', 'B2'), ('B4', 'พ่อไม่ชอบ', 'B3')],
 'C': [('C0', 'ตอนนี้', None), ('C1', 'เดินช้า', 'C0'), ('C2', 'วันหนึ่ง', 'C1'), ('C3', 'เป็นครั้งแรก', 'C2'), ('C4', 'เราเอียง', 'C3'),
       ('C5', 'ไหล่ของเรา', 'C4')],
 'D': [('D0', 'สิบสอง', None), ('D1', 'พ่อเปียก', 'D0'), ('D2', 'โดยไม่เคย', 'D1'), ('D3', 'บางความรัก', 'D2'), ('D4', 'เราจะเข้าใจ', 'D3'),
       ('D5', 'ก็ตอนที่', 'D4')],
}
P, segs, t = {}, [], 0.3
TITLE = 2.3; END = 3.0
for k in 'HABCD':
    an, first, last = anchors(k, spec[k])
    first = BND[k][0]; last = max(last, BND[k][1] - 0.04)
    an = {n: max(v, first) for n, v in an.items()}
    if k == 'D': t = P['title'] + TITLE
    off = t - first
    for n, v in an.items(): P[n] = round(v + off, 3)
    P[k + 'end'] = round(last + off, 3)
    segs.append({'file': f'story11/vo/{k}44.wav', 'src': [round(max(0, first - 0.05), 3), round(last + 0.12, 3)], 'on': round(t - 0.05, 3), 'name': k})
    t = last + off + (0.6 if k == 'H' else 0.5)
    if k == 'C': P['title'] = round(last + off + 0.6, 3)
P['end'] = round(max(P['Dend'] + 0.8, P['D5'] + 2.0), 3)
P['DUR'] = round(P['end'] + END, 2)
for n in sorted(P, key=P.get): print(f'{n:5s} {P[n]:6.2f}')


def part(t_, s, a, b): return {'t': t_, 's': s, 'at': P[a], 'd': round(P[b] - P[a], 3)}


cues = [
 [part('ถ้าคุณเคยเดิน', 'w', 'H0', 'H1'), part('ใต้ร่มคันเดียวกับพ่อ', 'y', 'H1', 'H2')],
 [part('ถ้าไหล่ข้างหนึ่งของเขา', 'w', 'H2', 'H3'), part('เปียกทุกครั้ง', 'y', 'H3', 'H4')],
 [part('คุณเคยสังเกตไหม', 'r', 'H4', 'Hend')],
 [part('ตั้งแต่ ', 'w', 'A0', 'A1'), part('ป.1 จน ม.6', 'y', 'A0', 'A1')],
 [part('ฝนตกทีไร', 'w', 'A1', 'A2'), part(' พ่อจะมารอรับหน้าโรงเรียน', 'w', 'A2', 'A3')],
 [part('กับร่ม', 'w', 'A3', 'A4'), part('คันเดียว', 'y', 'A3', 'A4')],
 [part('เดินกลับบ้านด้วยกัน', 'w', 'A4', 'A5')],
 [part('ถึงบ้านทีไร', 'w', 'A5', 'A6'), part(' ตัวเราแห้งทุกครั้ง', 'y', 'A6', 'Aend')],
 [part('เราเคยถามพ่อว่า', 'w', 'B0', 'B1'), part(' ทำไมไม่ซื้อร่มคันใหญ่', 'y', 'B1', 'B2')],
 [part('พ่อบอกว่า', 'w', 'B2', 'B3'), part(' "คันใหญ่มันหนัก', 'y', 'B3', 'B4')],
 [part('พ่อไม่ชอบ"', 'r', 'B4', 'Bend')],
 [part('ตอนนี้พ่อ ', 'w', 'C0', 'C1'), part('67 แล้ว', 'y', 'C0', 'C1')],
 [part('เดินช้ากว่าเดิม', 'w', 'C1', 'C2')],
 [part('วันหนึ่งฝนตก', 'w', 'C2', 'C3')],
 [part('เป็นครั้งแรก', 'y', 'C3', 'C4'), part('ที่เราถือร่มให้พ่อ', 'w', 'C3', 'C4')],
 [part('เราเอียงร่มไปทางพ่อ', 'w', 'C4', 'C5'), part('นิดเดียว', 'y', 'C4', 'C5')],
 [part('ไหล่ของเรา', 'w', 'C5', 'Cend'), part('ก็เปียกทั้งข้าง', 'r', 'C5', 'Cend')],
 [part('12 ปีที่ผ่านมา', 'y', 'D0', 'D1')],
 [part('พ่อเปียกแบบนี้ทุกครั้ง', 'w', 'D1', 'D2')],
 [part('โดยไม่เคย', 'w', 'D2', 'D3'), part('บอกเราเลย', 'y', 'D2', 'D3')],
 [part('บางความรัก', 'w', 'D3', 'D4'), part(' เราจะเข้าใจ', 'w', 'D4', 'D5')],
 [part('ก็ตอนที่', 'w', 'D5', 'Dend'), part('ไหล่ของเราเปียกบ้าง', 'r', 'D5', 'Dend')],
]
CUES = []
for j, parts in enumerate(cues):
    a = parts[0]['at']; last_end = max(p['at'] + p['d'] for p in parts)
    nxt = cues[j + 1][0]['at'] if j + 1 < len(cues) else 99
    CUES.append({'a': round(a, 3), 'b': round(min(nxt - 0.04, last_end + 0.5), 3), 'parts': parts})
CUES[-1]['b'] = round(P['end'] - 0.05, 3)
open('story11/vo.js', 'w').write('// generated by story11/place11.py\nconst VO = ' + json.dumps({'P': P, 'CUES': CUES}, ensure_ascii=False) + ';\n')
json.dump(segs, open('story11/segments.json', 'w'), ensure_ascii=False, indent=1)
