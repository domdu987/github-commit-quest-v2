"""Film 20: re-time captions to the spoken phrase (FINAL gate 2 found 38/96 phrases off by > 0.15 s with proportional timing).
Input: stt_phrase_times.json = [[ass_start_film_s, text, stt_spoken_film_s, delta], ...] (96, from the gate-2 STT on the clean narration, +0.10 s film offset).
Rule: caption narration-time t = spoken film time - 0.10 (film offset) - LEAD; kept in order inside each sentence with >= MIN s on screen;
a phrase whose STT time is implausible (> 0.8 s from the old time) keeps its old time. end = next phrase start in the sentence; the sentence's last phrase keeps its end."""
import json
LEAD, MIN = 0.03, 0.22
C = json.load(open('captions_v1_proportional.json')); P = json.load(open('stt_phrase_times.json'))
assert len(C) == len(P) and all(c['text'] == p[1] for c, p in zip(C, P))
new = []
for c, p in zip(C, P):
    t = p[2] - 0.10 - LEAD
    if abs(t - c['t']) > 0.8: t = c['t']
    new.append(t)
for i in range(len(C)):                       # monotonic with a minimum duration, same sentence
    if i and C[i]['sent'] == C[i-1]['sent'] and new[i] < new[i-1] + MIN: new[i] = new[i-1] + MIN
for i, c in enumerate(C):
    c['t'] = round(new[i], 3)
for i, c in enumerate(C):
    if i + 1 < len(C) and C[i+1]['sent'] == c['sent']: c['end'] = C[i+1]['t']
    elif c.get('end') is not None: c['end'] = max(c['end'], c['t'] + MIN)
json.dump(C, open('captions.json', 'w'), ensure_ascii=False, indent=1)
d = [abs(c['t'] + 0.10 - p[2]) for c, p in zip(C, P)]
print('phrases', len(C), 'max |dev| %.3f' % max(d), 'over 0.15:', sum(x > 0.15 for x in d))
