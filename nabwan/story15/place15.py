# "8 ซอง ที่อาม่าไม่เคยแกะ": "ถ้า..." hook (take H), Puck narration at 1.2x, and อาม่า's own line (take T, a female
# voice at 1.1x). Each take is kept whole; scene keys are anchored to Whisper word timestamps (Whisper hears อั่งเปา /
# ซอง / ลื้อ wrongly, so anchors use its spelling; the words themselves were checked with a second recogniser), then
# snapped to the real speech onset. Writes story15/vo.js + segments.json.
import json
import numpy as np
import soundfile as sf
W = json.load(open('story15/vo/words.json'))
BND = json.load(open('story15/vo/bounds.json'))
KEYS = 'HABCDEGTFL'
DB = {}
for k in KEYS:
    b, sr = sf.read(f'story15/vo/{k}44.wav'); f = int(sr * 0.01); n = len(b) // f
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
 'H': [('H0', 'ถ้าคุณ', None), ('H1', 'ทุกตรุษ', 'H0'), ('H2', 'ถ้าเขา', 'H1'), ('H3', 'เลยสัก', 'H2'), ('H4', 'คุณคิด', 'H3')],
 'A': [('A0', 'ตอนเด็ก', None), ('A1', 'อาม่าให้', 'A0'), ('A2', '2 ละ', 'A1')],
 'B': [('B0', 'พอได้', None), ('B1', 'เราให้', 'B0'), ('B2', 'รับสองมือ', 'B1'), ('B3', 'แล้วเก็บ', 'B2')],
 'C': [('C0', 'ปีต่อ', None), ('C1', 'ซองหนา', 'C0'), ('C2', 'ครบ', 'C1'), ('C3', '8 ซอง', 'C2')],
 'D': [('D0', 'แต่ปีนี้', None), ('D1', 'บริษัท', 'D0'), ('D2', 'แล้วตก', 'D1')],
 'E': [('E0', 'อาม่าทัก', None), ('E1', 'ปีนี้กลับ', 'E0'), ('E2', 'เราเกือบ', 'E1'), ('E3', 'เพราะ', 'E2')],
 'G': [('G0', 'สุดท้าย', None), ('G1', 'มีแค่', 'G0'), ('G2', 'อาม่าเปิด', 'G1'), ('G3', 'แปดซอง', 'G2'), ('G4', 'ไม่เคย', 'G3')],
 'T': [('T0', 'หรือ', None), ('T1', 'อัมมา', 'T0')],
 'F': [('F0', 'อามา', None), ('F1', 'พร้อม', 'F0'), ('F2', 'เหมือน', 'F1')],
 'L': [('L0', 'ตรุษจีน', None), ('L1', 'ไม่มี', 'L0'), ('L2', 'ก็กลับ', 'L1')],
}
GAP = {'H': 0.55, 'A': 0.4, 'B': 0.4, 'C': 0.55, 'D': 0.35, 'E': 0.4, 'G': 0.7, 'T': 0.75, 'F': 0.45}   # C → title; G, T hold for the moment
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
    segs.append({'file': f'story15/vo/{k}44.wav', 'src': [round(max(0, first - 0.05), 3), round(last + 0.12, 3)], 'on': round(t - 0.05, 3), 'name': k})
    t = last + off + GAP.get(k, 0.5)
    if k == 'C': P['title'] = round(last + off + GAP['C'], 3)
P['end'] = round(P['Lend'] + 1.0, 3)
P['DUR'] = round(P['end'] + END, 2)
for n in sorted(P, key=P.get): print(f'{n:5s} {P[n]:6.2f}')


def part(t_, s, a, b): return {'t': t_, 's': s, 'at': P[a], 'd': round(P[b] - P[a], 3)}


cues = [
 [part('ถ้าคุณให้อั่งเปาอาม่า', 'w', 'H0', 'H1'), part(' ทุกตรุษจีน', 'y', 'H1', 'H2')],
 [part('ถ้าเขาไม่เคยแกะ', 'w', 'H2', 'H3'), part(' เลยสักซอง', 'y', 'H3', 'H4')],
 [part('คุณคิดว่าเขาเก็บไว้ทำไม', 'r', 'H4', 'Hend')],
 [part('ตอนเด็ก', 'y', 'A0', 'A1'), part(' อาม่าให้อั่งเปาเราทุกปี', 'w', 'A1', 'A2')],
 [part('ซองละ 20 บาท', 'y', 'A2', 'Aend')],
 [part('พอได้เงินเดือนแรก', 'y', 'B0', 'B1'), part(' เราให้อาม่าคืนบ้าง', 'w', 'B1', 'B2')],
 [part('อาม่ารับสองมือ', 'w', 'B2', 'B3'), part(' แล้วเก็บใส่กล่องคุกกี้ใบเก่า', 'y', 'B3', 'Bend')],
 [part('ปีต่อๆ มา', 'w', 'C0', 'C1'), part(' ซองหนาขึ้นเรื่อยๆ', 'y', 'C1', 'C2')],
 [part('ครบ 8 ปี', 'w', 'C2', 'C3'), part(' 8 ซอง', 'r', 'C3', 'Cend')],
 [part('แต่ปีนี้', 'w', 'D0', 'D1'), part(' บริษัทปิด', 'w', 'D1', 'D2'), part(' เราตกงาน', 'r', 'D2', 'Dend')],
 [part('อาม่าทักไลน์มาว่า', 'w', 'E0', 'E1'), part(' "ปีนี้กลับไหม"', 'p', 'E1', 'E2')],
 [part('เราเกือบไม่กลับ', 'w', 'E2', 'E3'), part(' เพราะไม่มีซองจะให้', 'y', 'E3', 'Eend')],
 [part('สุดท้ายเรากลับบ้าน', 'w', 'G0', 'G1'), part(' มีแค่ส้มถุงเดียว', 'y', 'G1', 'G2')],
 [part('อาม่าเปิดกล่องคุกกี้ออกมา', 'w', 'G2', 'G3')],
 [part('8 ซอง', 'y', 'G3', 'G4'), part(' ไม่เคยถูกแกะเลยสักซอง', 'r', 'G4', 'Gend')],
 [part('"ลื้อกลับมา', 'p', 'T0', 'T1'), part(' อาม่าก็ได้อั่งเปาแล้ว"', 'p', 'T1', 'Tend')],
 [part('อาม่ายื่นกล่องคืนมา', 'w', 'F0', 'F1'), part(' พร้อมซอง 20 บาท', 'y', 'F1', 'F2')],
 [part('เหมือนตอนเด็ก', 'y', 'F2', 'Fend')],
 [part('ตรุษจีนนี้', 'w', 'L0', 'L1'), part(' ไม่มีซอง', 'y', 'L1', 'L2'), part(' ก็กลับบ้านได้', 'r', 'L2', 'Lend')],
]
CUES = []
for j, parts in enumerate(cues):
    a = parts[0]['at']; last_end = max(p['at'] + p['d'] for p in parts)
    nxt = cues[j + 1][0]['at'] if j + 1 < len(cues) else 99
    CUES.append({'a': round(a, 3), 'b': round(min(nxt - 0.04, last_end + 0.5), 3), 'parts': parts})
CUES[-1]['b'] = round(P['end'] - 0.05, 3)
open('story15/vo.js', 'w').write('// generated by story15/place15.py\nconst VO = ' + json.dumps({'P': P, 'CUES': CUES}, ensure_ascii=False) + ';\n')
json.dump(segs, open('story15/segments.json', 'w'), ensure_ascii=False, indent=1)
