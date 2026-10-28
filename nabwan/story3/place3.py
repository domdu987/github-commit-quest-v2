# "1,095 ข้อความของแม่" v3: "ถ้า..." hook (take H), then plain brisk Puck narration at 1.2x. Each take is kept whole;
# the old scene keys (A0..D6, same meanings as place.py) are anchored to Whisper character timestamps, first word
# clamped to the measured speech onset. Take D was synthesised in two halves (D + E). Writes story3/vo.js + segments.json.
import json
W = json.load(open('story3/vo3/words.json'))
BND = json.load(open('story3/vo3/bounds.json'))

def anchors(k, specs):
    toks = W[k]; txt = ''; idx = []
    for i, (w, a, b) in enumerate(toks):
        for _ in w: idx.append(i)
        txt += w
    out = {}
    for name, sub, after in specs:
        start = txt.find(sub, out[after][1] if after else 0)
        assert start >= 0, (k, name, sub, txt)
        while txt[start] == ' ': start += 1
        i = idx[start]; t = toks[i][1]
        if not any(c.isdigit() for c in toks[i][0]) and i + 1 < len(toks) and toks[i + 1][1] - t > 0.25: t = toks[i + 1][1] - 0.1   # first char swallowed the pause (digits are whole words)
        out[name] = (t, start)
    return {n: v[0] for n, v in out.items()}, toks[0][1], toks[-1][2]

spec = {
 'H': [('H0', 'ถ้าแม่', None), ('H1', 'ส่งรูป', 'H0'), ('H2', 'ทุกเช้า', 'H1'), ('H3', 'แล้วคุณ', 'H2'), ('H4', 'ปัดทิ้ง', 'H3'), ('H5', 'ถ้าวัน', 'H4'),
       ('H6', 'ไม่มีข้อ', 'H5'), ('H7', 'เขาจะ', 'H6')],
 'A': [('A0', 'ทุกเช้า', None), ('A1', '6', 'A0'), ('A2', 'แม่จะ', 'A1'), ('A3', 'มาทัก', 'A2'), ('A4', 'สวัสดี', 'A3'), ('A5', 'ขอให้', 'A4'),
       ('A6', '3', 'A5'), ('A6n', 'ไม่เคย', 'A6'), ('A7', 'รวมแล้ว', 'A6n'), ('A8', '1095', 'A7')],
 'B': [('B0', 'แต่ลูก', None), ('B1', 'แล้วปัด', 'B0'), ('B2', 'บางวัน', 'B1'), ('B2n', 'ปิดแจ้ง', 'B2'), ('B3', 'เพราะ', 'B2n'), ('B4', 'โดยไม่', 'B3'),
       ('B5', 'แม่ใช้', 'B4'), ('B5n', 'นิ้ว', 'B5'), ('B6', 'ค่อย', 'B5n'), ('B7', 'กว่าจะ', 'B6')],
 'C': [('C0', 'จนเช้า', None), ('C1', '6', 'C0'), ('C2', '7', 'C1'), ('C3', '8', 'C2'), ('C4', 'ไม่มีดอก', 'C3'), ('C5', 'จอเงียบ', 'C4'),
       ('C5n', 'จนใจ', 'C5'), ('C6', 'ลูกรีบ', 'C5n'), ('C7', 'เสียงแม่', 'C6'), ('C8', 'แม่แค่', 'C7'), ('C9', 'ไม่ต้อง', 'C8')],
 'D': [('D0', 'ข้อความ', None), ('D1', 'คือ', 'D0'), ('D2', 'ว่ายัง', 'D1')],
 'E': [('D3', 'วันนี้', None), ('D4', 'ตอบ', 'D3'), ('D5', 'ก่อน', 'D4'), ('D6', 'ไม่มีใคร', 'D5')],
}
GAP = {'H': 0.6, 'A': 0.45, 'B': 0.45, 'C': 0.45, 'D': 0.3}
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
    segs.append({'file': f'story3/vo3/{k}44.wav', 'src': [round(max(0, first - 0.05), 3), round(last + 0.12, 3)], 'on': round(t - 0.05, 3), 'name': k})
    t = last + off + GAP.get(k, 0.45)
    if k == 'C': P['title'] = round(last + off + 0.45, 3)
P['end'] = round(max(P['Eend'] + 0.6, P['D6'] + 1.6), 3)
P['DUR'] = round(P['end'] + END, 2)
for n in sorted(P, key=P.get): print(f'{n:5s} {P[n]:6.2f}')

def part(t_, s, a, b): return {'t': t_, 's': s, 'at': P[a], 'd': round(P[b] - P[a], 3)}
cues = [
 [part('ถ้าแม่ส่งรูปสวัสดี', 'w', 'H0', 'H2'), part('มาทุกเช้า', 'w', 'H2', 'H3')],
 [part('แล้วคุณแค่', 'w', 'H3', 'H4'), part('ปัดทิ้ง', 'r', 'H4', 'H5')],
 [part('ถ้าวันหนึ่ง', 'w', 'H5', 'H6'), part('ไม่มีข้อความมา', 'w', 'H6', 'H7')],
 [part('เขาจะเป็นยังไง', 'r', 'H7', 'Hend')],
 [part('ทุกเช้า', 'w', 'A0', 'A1'), part(' 6 โมงตรง', 'r', 'A1', 'A2')],
 [part('แม่จะส่งรูปดอกไม้', 'w', 'A2', 'A3'), part(' มาทักทาย', 'w', 'A3', 'A4')],
 [part('สวัสดีวันจันทร์', 'y', 'A4', 'A5')],
 [part('ขอให้ลูกสุขสบาย', 'w', 'A5', 'A6')],
 [part('3 ปี', 'r', 'A6', 'A6n'), part(' ไม่เคยขาด', 'w', 'A6n', 'A7')],
 [part('รวมแล้ว', 'w', 'A7', 'A8'), part(' 1,095 ข้อความ', 'r', 'A8', 'Aend')],
 [part('แต่ลูกแค่เปิดอ่าน', 'w', 'B0', 'B1'), part(' แล้วปัดผ่าน', 'w', 'B1', 'B2')],
 [part('บางวันก็', 'w', 'B2', 'B2n'), part('ปิดแจ้งเตือน', 'r', 'B2n', 'B3')],
 [part('เพราะรำคาญ', 'w', 'B3', 'B4')],
 [part('โดยไม่รู้เลยว่า', 'y', 'B4', 'B5')],
 [part('แม่ใช้', 'w', 'B5', 'B5n'), part('นิ้วเดียว', 'r', 'B5n', 'B6')],
 [part('ค่อยๆ จิ้ม', 'w', 'B6', 'B7'), part(' กว่าจะส่งได้', 'w', 'B7', 'Bend')],
 [part('จนเช้าวันหนึ่ง', 'y', 'C0', 'C1')],
 [part('6 โมง', 'w', 'C1', 'C2'), part(' 7 โมง', 'w', 'C2', 'C3'), part(' 8 โมง', 'r', 'C3', 'C4')],
 [part('ไม่มีดอกไม้', 'w', 'C4', 'C5')],
 [part('จอเงียบ', 'w', 'C5', 'C5n'), part('จนใจหาย', 'r', 'C5n', 'C6')],
 [part('ลูกรีบโทรหา', 'w', 'C6', 'C7')],
 [part('เสียงแม่แผ่วเบา', 'w', 'C7', 'C8')],
 [part('แม่แค่ไม่สบาย', 'w', 'C8', 'C9'), part(' ไม่ต้องห่วงนะลูก', 'y', 'C9', 'Cend')],
 [part('ข้อความที่เราว่าน่ารำคาญ', 'w', 'D0', 'D1')],
 [part('คือหลักฐาน', 'r', 'D1', 'D2'), part(' ว่ายังมีคนคิดถึง', 'w', 'D2', 'Dend')],
 [part('วันนี้', 'y', 'D3', 'D4'), part(' ตอบแม่สักคำ', 'y', 'D4', 'D5')],
 [part('ก่อนวันที่', 'w', 'D5', 'D6'), part(' ไม่มีใครส่งมา', 'r', 'D6', 'Eend')],
]
CUES = []
for j, parts in enumerate(cues):
    a = parts[0]['at']; last_end = max(p['at'] + p['d'] for p in parts)
    nxt = cues[j + 1][0]['at'] if j + 1 < len(cues) else 99
    CUES.append({'a': round(a, 3), 'b': round(min(nxt - 0.04, last_end + 0.5), 3), 'parts': parts})
CUES[-1]['b'] = round(P['end'] - 0.05, 3)
open('story3/vo.js', 'w').write('// generated by story3/place3.py\nconst VO = ' + json.dumps({'P': P, 'CUES': CUES}, ensure_ascii=False) + ';\n')
json.dump(segs, open('story3/segments.json', 'w'), ensure_ascii=False, indent=1)
