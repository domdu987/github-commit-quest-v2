# "9 ผ้าพันคอที่ไม่เคยได้ใช้": "ถ้า..." hook (take H), then Puck narration at 1.2x. Each take is kept whole; scene keys are
# anchored to Whisper word timestamps, then snapped to the real speech onset (Whisper stretches a word's start back over the
# pause before it). Writes story12/vo.js + segments.json.
import json
import numpy as np
import soundfile as sf
W = json.load(open('story12/vo/words.json'))
BND = json.load(open('story12/vo/bounds.json'))
DB = {}
for k in 'HABCDE':
    b, sr = sf.read(f'story12/vo/{k}44.wav'); f = int(sr * 0.01); n = len(b) // f
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
 'H': [('H0', 'ถ้าคุณ', None), ('H1', 'จากใคร', 'H0'), ('H2', 'ถ้าปีนี้', 'H1'), ('H3', 'ไม่เสร็จ', 'H2'), ('H4', 'คุณจะ', 'H3')],
 'A': [('A0', '9', None), ('A1', 'ที่ยาย', 'A0'), ('A2', 'ถักผ้า', 'A1'), ('A3', 'ส่งมา', 'A2'), ('A4', 'ทุกหน้า', 'A3')],
 'B': [('B0', 'แต่', None), ('B1', 'ผ้าพันคอ', 'B0'), ('B2', 'เลยนอน', 'B1'), ('B3', 'ไม่เคยได้', 'B2')],
 'C': [('C0', 'ปีนี้', None), ('C1', 'ข้างใน', 'C0'), ('C2', 'แค่ครึ่ง', 'C1'), ('C3', 'กับโน้ต', 'C2'), ('C4', 'มือยาย', 'C3'), ('C5', 'หลานทำ', 'C4')],
 'D': [('D0', 'เราขึ้น', None), ('D1', 'พันผ้า', 'D0'), ('D2', 'ยายขำ', 'D1'), ('D3', 'แล้วสอน', 'D2'), ('D4', 'จนเสร็จ', 'D3')],
 'E': [('E0', 'ของบาง', None), ('E1', 'ไม่ได้ส่ง', 'E0'), ('E2', 'แต่ส่ง', 'E1'), ('E3', 'มีคน', 'E2'), ('E4', 'อยู่ทุก', 'E3')],
}
GAP = {'H': 0.7, 'A': 0.5, 'B': 0.7, 'C': 0.6, 'D': 1.5}   # after each take; C → title; D → E holds for the wrap
P, segs, t = {}, [], 0.3
TITLE = 2.3; END = 3.0
for k in 'HABCDE':
    an, first, last = anchors(k, spec[k])
    first = BND[k][0]; last = max(last, BND[k][1] - 0.04)
    an = {n: max(v, first) for n, v in an.items()}
    if k == 'D': t = P['title'] + TITLE
    off = t - first
    for n, v in an.items(): P[n] = round(v + off, 3)
    P[k + 'end'] = round(last + off, 3)
    segs.append({'file': f'story12/vo/{k}44.wav', 'src': [round(max(0, first - 0.05), 3), round(last + 0.12, 3)], 'on': round(t - 0.05, 3), 'name': k})
    t = last + off + GAP.get(k, 0.5)
    if k == 'C': P['title'] = round(last + off + GAP['C'], 3)
P['end'] = round(max(P['Eend'] + 0.8, P['E3'] + 2.0), 3)
P['DUR'] = round(P['end'] + END, 2)
for n in sorted(P, key=P.get): print(f'{n:5s} {P[n]:6.2f}')


def part(t_, s, a, b): return {'t': t_, 's': s, 'at': P[a], 'd': round(P[b] - P[a], 3)}


cues = [
 [part('ถ้าคุณได้ผ้าพันคอ', 'w', 'H0', 'H1'), part('จากใครสักคนทุกหน้าหนาว', 'y', 'H1', 'H2')],
 [part('ถ้าปีนี้เขาถักให้', 'w', 'H2', 'H3'), part('ไม่เสร็จ', 'y', 'H3', 'H4')],
 [part('คุณจะทำยังไง', 'r', 'H4', 'Hend')],
 [part('9 ปีแล้ว', 'y', 'A0', 'A1'), part(' ที่ยายที่เชียงราย', 'w', 'A1', 'A2')],
 [part('ถักผ้าพันคอ', 'w', 'A2', 'A3'), part(' ส่งมาให้เราที่กรุงเทพฯ', 'w', 'A3', 'A4')],
 [part('ทุกหน้าหนาว', 'y', 'A4', 'Aend')],
 [part('แต่กรุงเทพฯ ไม่เคยหนาวพอ', 'w', 'B0', 'B1')],
 [part('ผ้าพันคอของยาย', 'w', 'B1', 'B2'), part(' เลยนอนพับอยู่ในลิ้นชัก', 'y', 'B2', 'B3')],
 [part('ไม่เคยได้ใช้สักครั้ง', 'r', 'B3', 'Bend')],
 [part('ปีนี้กล่องของยายมาช้า', 'w', 'C0', 'C1')],
 [part('ข้างในมีผ้าพันคอ', 'w', 'C1', 'C2'), part(' แค่ครึ่งผืน', 'y', 'C2', 'C3')],
 [part('กับโน้ตว่า', 'w', 'C3', 'C4')],
 [part('"มือยายสั่นแล้ว', 'y', 'C4', 'C5')],
 [part('หลานทำต่อให้ยายหน่อยนะ"', 'r', 'C5', 'Cend')],
 [part('เราขึ้นเหนือไปหายาย', 'w', 'D0', 'D1')],
 [part('พันผ้าพันคอของยายไปทั้งหมด', 'y', 'D1', 'D2')],
 [part('ยายขำจนน้ำตาไหล', 'w', 'D2', 'D3')],
 [part('แล้วสอนเราถักต่อ', 'w', 'D3', 'D4'), part(' จนเสร็จ', 'y', 'D4', 'Dend')],
 [part('ของบางอย่าง', 'w', 'E0', 'E1'), part(' ไม่ได้ส่งมาให้เราใช้', 'w', 'E1', 'E2')],
 [part('แต่ส่งมาบอกว่า', 'w', 'E2', 'E3')],
 [part('มีคนคิดถึงเรา', 'y', 'E3', 'E4'), part('อยู่ทุกปี', 'r', 'E4', 'Eend')],
]
CUES = []
for j, parts in enumerate(cues):
    a = parts[0]['at']; last_end = max(p['at'] + p['d'] for p in parts)
    nxt = cues[j + 1][0]['at'] if j + 1 < len(cues) else 99
    CUES.append({'a': round(a, 3), 'b': round(min(nxt - 0.04, last_end + 0.5), 3), 'parts': parts})
CUES[-1]['b'] = round(P['end'] - 0.05, 3)
open('story12/vo.js', 'w').write('// generated by story12/place11.py\nconst VO = ' + json.dumps({'P': P, 'CUES': CUES}, ensure_ascii=False) + ';\n')
json.dump(segs, open('story12/segments.json', 'w'), ensure_ascii=False, indent=1)
