# "720 มื้อ ที่ครูซื้อเกิน": "ถ้า..." hook (take H), Puck narration at 1.2x, ครูสมศรี's own line (take T, a female voice
# at 1.1x), and the narrator saying the same line to the girl years later (take G). Each take is kept whole; scene keys are anchored to Whisper
# word timestamps, then snapped to the real speech onset. Writes story14/vo.js + segments.json.
import json
import numpy as np
import soundfile as sf
W = json.load(open('story14/vo/words.json'))
BND = json.load(open('story14/vo/bounds.json'))
KEYS = 'HABTCDEGF'
DB = {}
for k in KEYS:
    b, sr = sf.read(f'story14/vo/{k}44.wav'); f = int(sr * 0.01); n = len(b) // f
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
 'H': [('H0', 'ถ้าคุณ', None), ('H1', 'ที่ซื้อ', 'H0'), ('H2', 'ถ้าเขา', 'H1'), ('H3', 'กินช่วย', 'H2'), ('H4', 'คุณคิด', 'H3')],
 'A': [('A0', 'ตอน', None), ('A1', 'บ้านเรา', 'A0'), ('A2', 'พักเที่ยง', 'A1'), ('A3', 'อยู่หลัง', 'A2')],
 'B': [('B0', 'วันหนึ่ง', None), ('B1', 'ครูสม', 'B0'), ('B2', 'ถือข้าว', 'B1')],
 'T': [('T0', 'ครูซื้อ', None), ('T1', 'กินช่วย', 'T0')],
 'C': [('C0', 'หลังจาก', None), ('C1', 'ครูซื้อ', 'C0'), ('C2', '3', 'C1'), ('C3', 'ไม่เคย', 'C2')],
 'D': [('D0', 'วันนี้', None), ('D1', 'เมื่อวาน', 'D0'), ('D2', 'เราเห็น', 'D1'), ('D3', 'นั่งดื่ม', 'D2')],
 'E': [('E0', 'เราเลย', None), ('E1', 'แล้วบอก', 'E0')],
 'G': [('G0', 'ครูซื้อ', None), ('G1', 'กินช่วย', 'G0')],
 'F': [('F0', 'ความ', None), ('F1', 'ไม่ได้', 'F0'), ('F2', 'มันแค่', 'F1')],
}
GAP = {'H': 0.6, 'A': 0.45, 'B': 0.35, 'T': 0.75, 'C': 0.6, 'D': 0.45, 'E': 0.3, 'G': 1.3}   # C → title; G holds for the moment
P, segs, t = {}, [], 0.3
TITLE = 2.3; END = 3.0
for k in KEYS:
    an, first, last = anchors(k, spec[k])
    first = BND[k][0]; last = max(last, BND[k][1] - 0.04)
    an = {n: max(v, first) for n, v in an.items()}
    if k == 'D': t = P['title'] + TITLE
    off = t - first
    for n, v in an.items(): P[n] = round(v + off, 3)
    P[k + 'end'] = round(last + off, 3)
    segs.append({'file': f'story14/vo/{k}44.wav', 'src': [round(max(0, first - 0.05), 3), round(last + 0.12, 3)], 'on': round(t - 0.05, 3), 'name': k})
    t = last + off + GAP.get(k, 0.5)
    if k == 'C': P['title'] = round(last + off + GAP['C'], 3)
P['end'] = round(P['Fend'] + 1.0, 3)
P['DUR'] = round(P['end'] + END, 2)
for n in sorted(P, key=P.get): print(f'{n:5s} {P[n]:6.2f}')


def part(t_, s, a, b): return {'t': t_, 's': s, 'at': P[a], 'd': round(P[b] - P[a], 3)}


cues = [
 [part('ถ้าคุณเคยมีครู', 'w', 'H0', 'H1'), part('ที่ซื้อข้าวมาเกินทุกวัน', 'y', 'H1', 'H2')],
 [part('ถ้าเขาบอกว่า', 'w', 'H2', 'H3'), part(' "กินช่วยครูหน่อยนะ"', 'y', 'H3', 'H4')],
 [part('คุณคิดว่ามันบังเอิญไหม', 'r', 'H4', 'Hend')],
 [part('ตอน ป.4', 'y', 'A0', 'A1'), part(' บ้านเราไม่มีเงินให้มาโรงเรียน', 'w', 'A1', 'A2')],
 [part('พักเที่ยง เราเลยนั่งดื่มน้ำ', 'w', 'A2', 'A3'), part(' อยู่หลังห้องคนเดียว', 'y', 'A3', 'Aend')],
 [part('วันหนึ่ง ครูสมศรีเดินเข้ามา', 'w', 'B0', 'B2')],
 [part('ถือข้าวมา 2 ถุง', 'y', 'B2', 'Bend')],
 [part('"ครูซื้อมาเกิน', 'p', 'T0', 'T1'), part(' กินช่วยครูหน่อยนะ"', 'p', 'T1', 'Tend')],
 [part('หลังจากวันนั้น', 'w', 'C0', 'C1'), part(' ครูซื้อเกินทุกวัน', 'y', 'C1', 'C2')],
 [part('3 ปี จนเราจบ ป.6', 'w', 'C2', 'C3')],
 [part('ไม่เคยขาดสักวัน', 'r', 'C3', 'Cend')],
 [part('วันนี้ เราเป็นครูแล้ว', 'y', 'D0', 'D1')],
 [part('เมื่อวานตอนพักเที่ยง', 'w', 'D1', 'D2'), part(' เราเห็นเด็กคนหนึ่ง', 'w', 'D2', 'D3')],
 [part('นั่งดื่มน้ำอยู่หลังห้องคนเดียว', 'y', 'D3', 'Dend')],
 [part('เราเลยเดินไปซื้อข้าวมา 2 ถุง', 'w', 'E0', 'E1'), part(' แล้วบอกเขาว่า', 'w', 'E1', 'Eend')],
 [part('"ครูซื้อมาเกิน', 'y', 'G0', 'G1'), part(' กินช่วยครูหน่อยนะ"', 'r', 'G1', 'Gend')],
 [part('ความใจดีบางอย่าง', 'w', 'F0', 'F1'), part(' ไม่ได้จบที่เรา', 'w', 'F1', 'F2')],
 [part('มันแค่รอวันส่งต่อ', 'r', 'F2', 'Fend')],
]
CUES = []
for j, parts in enumerate(cues):
    a = parts[0]['at']; last_end = max(p['at'] + p['d'] for p in parts)
    nxt = cues[j + 1][0]['at'] if j + 1 < len(cues) else 99
    CUES.append({'a': round(a, 3), 'b': round(min(nxt - 0.04, last_end + 0.5), 3), 'parts': parts})
CUES[-1]['b'] = round(P['end'] - 0.05, 3)
open('story14/vo.js', 'w').write('// generated by story14/place14.py\nconst VO = ' + json.dumps({'P': P, 'CUES': CUES}, ensure_ascii=False) + ';\n')
json.dump(segs, open('story14/segments.json', 'w'), ensure_ascii=False, indent=1)
