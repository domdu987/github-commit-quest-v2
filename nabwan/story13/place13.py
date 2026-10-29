# "15 ปีใหม่ ที่แม่อยู่บนรถทัวร์": "ถ้า..." hook (take H), Puck narration at 1.2x, and แม่'s midnight announcement (take M,
# a female voice at 1.1x, put through a PA filter in audio.py). Each take is kept whole; scene keys are anchored to Whisper
# word timestamps, then snapped to the real speech onset. Writes story13/vo.js + segments.json.
import json
import numpy as np
import soundfile as sf
W = json.load(open('story13/vo/words.json'))
BND = json.load(open('story13/vo/bounds.json'))
KEYS = 'HABCDMFE'
DB = {}
for k in KEYS:
    b, sr = sf.read(f'story13/vo/{k}44.wav'); f = int(sr * 0.01); n = len(b) // f
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
 'H': [('H0', 'ถ้าคุณ', None), ('H1', 'กลับบ้าน', 'H0'), ('H2', 'ถ้าคน', 'H1'), ('H3', 'ไม่เคย', 'H2'), ('H4', 'ตอนปี', 'H3'), ('H5', 'คุณเคยสัง', 'H4')],
 'A': [('A0', 'แม่เรา', None), ('A1', '15', 'A0'), ('A2', 'ที่ทุก', 'A1'), ('A3', 'แม่อยู่', 'A2')],
 'B': [('B0', 'ทุกปี', None), ('B1', 'กับยาย', 'B0'), ('B2', 'พอเที่ยง', 'B1'), ('B3', 'แม่จะส่ง', 'B2'), ('B4', 'สวัสดี', 'B3'), ('B5', 'แม่แจก', 'B4')],
 'C': [('C0', 'ปีนี้', None), ('C1', 'แอบจอง', 'C0'), ('C2', 'รถเที่ยว', 'C1'), ('C3', 'พอแม่', 'C2'), ('C4', 'ถึงที่นั่ง', 'C3'), ('C5', 'แม่ก็ยืน', 'C4')],
 'D': [('D0', 'เที่ยง', None), ('D1', 'แม่หยิบ', 'D0'), ('D2', 'เหมือน', 'D1')],
 'M': [('M0', 'สวัสดี', None), ('M1', 'ผู้โดย', 'M0'), ('M2', 'ปีนี้', 'M1'), ('M3', 'ก็นั่ง', 'M2')],
 'F': [('F0', '15', None), ('F1', 'นี่เป็น', 'F0'), ('F2', 'ที่เรา', 'F1')],
 'E': [('E0', 'บางคน', None), ('E1', 'เพราะ', 'E0'), ('E2', 'พาคน', 'E1')],
}
GAP = {'H': 0.6, 'A': 0.5, 'B': 0.6, 'C': 0.6, 'D': 0.45, 'M': 1.9, 'F': 1.0}   # C → title; M → F holds for the cheer
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
    segs.append({'file': f'story13/vo/{k}44.wav', 'src': [round(max(0, first - 0.05), 3), round(last + 0.12, 3)], 'on': round(t - 0.05, 3), 'name': k})
    t = last + off + GAP.get(k, 0.5)
    if k == 'C': P['title'] = round(last + off + GAP['C'], 3)
P['end'] = round(P['Eend'] + 1.0, 3)
P['DUR'] = round(P['end'] + END, 2)
for n in sorted(P, key=P.get): print(f'{n:5s} {P[n]:6.2f}')


def part(t_, s, a, b): return {'t': t_, 's': s, 'at': P[a], 'd': round(P[b] - P[a], 3)}


cues = [
 [part('ถ้าคุณเคยนั่งรถทัวร์', 'w', 'H0', 'H1'), part(' กลับบ้านช่วงปีใหม่', 'y', 'H1', 'H2')],
 [part('ถ้าคนที่ยื่นน้ำให้คุณบนรถ', 'w', 'H2', 'H3')],
 [part('ไม่เคยได้อยู่บ้าน', 'w', 'H3', 'H4'), part(' ตอนปีใหม่เลย', 'y', 'H4', 'H5')],
 [part('คุณเคยสังเกตเขาไหม', 'r', 'H5', 'Hend')],
 [part('แม่เราเป็นพนักงานต้อนรับบนรถทัวร์', 'w', 'A0', 'A1')],
 [part('15 ปีแล้ว', 'y', 'A1', 'A2'), part(' ที่ทุกคืนสิ้นปี', 'w', 'A2', 'A3')],
 [part('แม่อยู่บนถนน', 'r', 'A3', 'Aend')],
 [part('ทุกปี เรานับถอยหลัง', 'w', 'B0', 'B1'), part(' กับยายที่บ้าน', 'w', 'B1', 'B2')],
 [part('พอเที่ยงคืน', 'y', 'B2', 'B3'), part(' แม่จะส่งไลน์มาว่า', 'w', 'B3', 'B4')],
 [part('"สวัสดีปีใหม่ลูก', 'y', 'B4', 'B5'), part(' แม่แจกน้ำอยู่นะ"', 'y', 'B5', 'Bend')],
 [part('ปีนี้ เราเลย', 'w', 'C0', 'C1'), part('แอบจองที่นั่ง', 'y', 'C1', 'C2')],
 [part('รถเที่ยวที่แม่ทำงาน', 'w', 'C2', 'C3')],
 [part('พอแม่เดินมาแจกน้ำ', 'w', 'C3', 'C4'), part(' ถึงที่นั่งเรา', 'w', 'C4', 'C5')],
 [part('แม่ก็ยืนนิ่งไปเลย', 'r', 'C5', 'Cend')],
 [part('เที่ยงคืนตรง', 'y', 'D0', 'D1')],
 [part('แม่หยิบไมค์ขึ้นมา', 'w', 'D1', 'D2'), part(' เหมือนทุกปี', 'w', 'D2', 'Dend')],
 [part('"สวัสดีปีใหม่ค่ะ', 'p', 'M0', 'M1'), part(' ผู้โดยสารทุกท่าน', 'p', 'M1', 'M2')],
 [part('ปีนี้ ลูกสาวของดิฉัน', 'p', 'M2', 'M3')],
 [part('ก็นั่งอยู่บนรถคันนี้ด้วยนะคะ"', 'r', 'M3', 'Mend')],
 [part('15 ปี', 'y', 'F0', 'F1'), part(' นี่เป็นปีแรก', 'w', 'F1', 'F2')],
 [part('ที่เราได้นับถอยหลังกับแม่', 'y', 'F2', 'Fend')],
 [part('บางคนไม่ได้กลับบ้านช่วงปีใหม่', 'w', 'E0', 'E1')],
 [part('เพราะเขาต้อง', 'w', 'E1', 'E2'), part('พาคนอื่นกลับบ้าน', 'r', 'E2', 'Eend')],
]
CUES = []
for j, parts in enumerate(cues):
    a = parts[0]['at']; last_end = max(p['at'] + p['d'] for p in parts)
    nxt = cues[j + 1][0]['at'] if j + 1 < len(cues) else 99
    CUES.append({'a': round(a, 3), 'b': round(min(nxt - 0.04, last_end + 0.5), 3), 'parts': parts})
CUES[-1]['b'] = round(P['end'] - 0.05, 3)
open('story13/vo.js', 'w').write('// generated by story13/place13.py\nconst VO = ' + json.dumps({'P': P, 'CUES': CUES}, ensure_ascii=False) + ';\n')
json.dump(segs, open('story13/segments.json', 'w'), ensure_ascii=False, indent=1)
