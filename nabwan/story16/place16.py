# "50 กุหลาบ ที่ยายจำไม่ได้": "ถ้า..." hook (take H), Puck narration at 1.2x, ตาบุญ's two lines (T, K: an old man's
# voice at 1.1x with its longest pause shortened, then 1.09x / 1.12x to fit 60 s) and ยายแก้ว's line (Y, 1.1x then 1.09x).
# Each take is kept whole; scene keys are anchored to Whisper word timestamps (Whisper writes ตาบุญ as ตะบุญ; the words
# were checked with a second recogniser), then snapped to the real speech onset. Writes story16/vo.js + segments.json.
import json
import numpy as np
import soundfile as sf
W = json.load(open('story16/vo/words.json'))
BND = json.load(open('story16/vo/bounds.json'))
KEYS = 'HABCDETGYKL'
DB = {}
for k in KEYS:
    b, sr = sf.read(f'story16/vo/{k}44.wav'); f = int(sr * 0.01); n = len(b) // f
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
 'H': [('H0', 'ถ้าคุณ', None), ('H1', 'ทุกวาเลน', 'H0'), ('H2', 'ถ้าวัน', 'H1'), ('H3', 'จำไม่ได้', 'H2'), ('H4', 'คุณจะ', 'H3')],
 'A': [('A0', 'ตะบุญ', None), ('A1', 'ปีละ', 'A0'), ('A2', '49', 'A1')],
 'B': [('B0', 'ยายทับ', None), ('B1', 'แล้วเขียน', 'B0')],
 'C': [('C0', '2', None), ('C1', 'ยายเริ่ม', 'C0'), ('C2', 'ลืมกุญแจ', 'C1'), ('C3', 'จนวัน', 'C2'), ('C4', 'ยายจำ', 'C3')],
 'D': [('D0', 'หลาน', None), ('D1', 'ไม่ต้อง', 'D0')],
 'E': [('E0', 'แต่เช้า', None), ('E1', 'ตาก็', 'E0'), ('E2', 'ซื้อ', 'E1'), ('E3', 'เหมือน', 'E2')],
 'T': [('T0', 'สวัสดี', None), ('T1', 'ผมชื่อ', 'T0'), ('T2', 'เป็นแฟน', 'T1')],
 'G': [('G0', 'ยายเปิด', None), ('G1', 'เจอ', 'G0'), ('G2', 'กับลาย', 'G1')],
 'Y': [('Y0', 'คนคน', None), ('Y1', 'คงรัก', 'Y0')],
 'K': [('K0', 'เธอ', None), ('K1', 'ไม่เป็น', 'K0'), ('K2', 'ฉันจำ', 'K1')],
 'L': [('L0', 'ความรัก', None), ('L1', 'ไม่ต้อง', 'L0'), ('L2', 'แค่เรา', 'L1')],
}
GAP = {'H': 0.5, 'A': 0.35, 'B': 0.35, 'C': 0.5, 'D': 0.3, 'E': 0.45, 'T': 0.4, 'G': 0.35, 'Y': 0.55, 'K': 0.6}   # C → title; Y, K hold
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
    segs.append({'file': f'story16/vo/{k}44.wav', 'src': [round(max(0, first - 0.05), 3), round(last + 0.12, 3)], 'on': round(t - 0.05, 3), 'name': k})
    t = last + off + GAP.get(k, 0.5)
    if k == 'C': P['title'] = round(last + off + GAP['C'], 3)
P['end'] = round(P['Lend'] + 0.8, 3)
P['DUR'] = round(P['end'] + END, 2)
for n in sorted(P, key=P.get): print(f'{n:5s} {P[n]:6.2f}')


def part(t_, s, a, b): return {'t': t_, 's': s, 'at': P[a], 'd': round(P[b] - P[a], 3)}


cues = [
 [part('ถ้าคุณให้กุหลาบคนรัก', 'w', 'H0', 'H1'), part(' ทุกวาเลนไทน์', 'y', 'H1', 'H2')],
 [part('ถ้าวันหนึ่ง', 'w', 'H2', 'H3'), part(' เขาจำไม่ได้ว่าคุณเป็นใคร', 'y', 'H3', 'H4')],
 [part('คุณจะยังให้อยู่ไหม', 'r', 'H4', 'Hend')],
 [part('ตาบุญให้กุหลาบยายแก้ว', 'w', 'A0', 'A1'), part(' ปีละหนึ่งดอก ทุกวาเลนไทน์', 'y', 'A1', 'A2')],
 [part('มา 49 ปี', 'r', 'A2', 'Aend')],
 [part('ยายทับดอกไม้ไว้ในสมุดทุกดอก', 'w', 'B0', 'B1')],
 [part('แล้วเขียนกำกับไว้ทุกหน้า', 'y', 'B1', 'Bend')],
 [part('สองปีก่อน', 'w', 'C0', 'C1'), part(' ยายเริ่มลืม', 'y', 'C1', 'C2')],
 [part('ลืมกุญแจ ลืมชื่อหลาน', 'w', 'C2', 'C3')],
 [part('จนวันหนึ่ง', 'w', 'C3', 'C4'), part(' ยายจำตาไม่ได้', 'r', 'C4', 'Cend')],
 [part('หลานบอกว่า', 'w', 'D0', 'D1'), part(' "ไม่ต้องซื้อแล้วก็ได้นะตา"', 'p', 'D1', 'Dend')],
 [part('แต่เช้าวันวาเลนไทน์', 'w', 'E0', 'E1'), part(' ตาก็ยังไปตลาด', 'y', 'E1', 'E2')],
 [part('ซื้อกุหลาบมาหนึ่งดอก', 'w', 'E2', 'E3'), part(' เหมือนทุกปี', 'y', 'E3', 'Eend')],
 [part('"สวัสดีครับ', 'p', 'T0', 'T1'), part(' ผมชื่อบุญ', 'p', 'T1', 'T2')],
 [part('เป็นแฟนคุณครับ"', 'p', 'T2', 'Tend')],
 [part('ยายเปิดสมุดเล่มนั้น', 'w', 'G0', 'G1'), part(' เจอกุหลาบ 49 ดอก', 'y', 'G1', 'G2')],
 [part('กับลายมือตัวเองทุกหน้า', 'y', 'G2', 'Gend')],
 [part('"คนคนนี้', 'p', 'Y0', 'Y1'), part(' คงรักฉันมากเลยนะคะ"', 'p', 'Y1', 'Yend')],
 [part('"เธอจำไม่ได้', 'p', 'K0', 'K1'), part(' ไม่เป็นไรนะ', 'p', 'K1', 'K2')],
 [part('ฉันจำแทนเธอเอง"', 'r', 'K2', 'Kend')],
 [part('ความรักบางเรื่อง', 'w', 'L0', 'L1'), part(' ไม่ต้องให้อีกคนจำได้', 'w', 'L1', 'L2')],
 [part('แค่เรายังจำได้ก็พอ', 'r', 'L2', 'Lend')],
]
CUES = []
for j, parts in enumerate(cues):
    a = parts[0]['at']; last_end = max(p['at'] + p['d'] for p in parts)
    nxt = cues[j + 1][0]['at'] if j + 1 < len(cues) else 99
    CUES.append({'a': round(a, 3), 'b': round(min(nxt - 0.04, last_end + 0.5), 3), 'parts': parts})
CUES[-1]['b'] = round(P['end'] - 0.05, 3)
open('story16/vo.js', 'w').write('// generated by story16/place16.py\nconst VO = ' + json.dumps({'P': P, 'CUES': CUES}, ensure_ascii=False) + ';\n')
json.dump(segs, open('story16/segments.json', 'w'), ensure_ascii=False, indent=1)
