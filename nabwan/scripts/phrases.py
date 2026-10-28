# Phrase table for chosen takes: fal char timestamps grouped at '...' and refined with an RMS gate.
import json, sys
import numpy as np, soundfile as sf
out = {}
for name in sys.argv[1:]:
    res = json.load(open(f'vo4/res_{name}.json'))
    y, sr = sf.read(f'vo4/{name}44.wav')
    hop = 220
    rms = np.sqrt(np.convolve(y ** 2, np.ones(hop * 2) / (hop * 2), mode='same'))[::hop]
    db = 20 * np.log10(rms + 1e-9)
    gate = db.max() - 38
    chars = [(c, a, b) for blk in res['timestamps'] for c, a, b in zip(blk['characters'], blk['character_start_times_seconds'], blk['character_end_times_seconds'])]
    phrases, cur, inTag = [], None, False
    for c, a, b in chars:
        if c == '[': inTag = True
        if inTag:
            if c == ']': inTag = False
            continue
        if c in '. ':
            if cur and cur['t'].strip(): phrases.append(cur)
            cur = None
            continue
        if cur is None: cur = {'t': '', 'a': a, 'b': b}
        cur['t'] += c; cur['b'] = b
    if cur and cur['t'].strip(): phrases.append(cur)
    # refine: first frame above gate within [a-0.25, a+0.25], last above gate within [b-0.3, b+0.35]
    for p in phrases:
        i0, i1 = int((p['a'] - 0.25) * sr / hop), int((p['a'] + 0.25) * sr / hop)
        idx = np.where(db[max(0, i0):i1] > gate)[0]
        p['on'] = round((max(0, i0) + idx[0]) * hop / sr, 3) if len(idx) else p['a']
        j0, j1 = int((p['b'] - 0.3) * sr / hop), int((p['b'] + 0.35) * sr / hop)
        idx = np.where(db[j0:min(len(db), j1)] > gate)[0]
        p['off'] = round((j0 + idx[-1]) * hop / sr, 3) if len(idx) else p['b']
    out[name] = {'dur': round(len(y) / sr, 3), 'phrases': phrases}
    print(name, out[name]['dur'])
    for p in phrases: print(f"   {p['on']:6.2f} {p['off']:6.2f}  (fal {p['a']:.2f}-{p['b']:.2f})  {p['t']}")
json.dump(out, open('vo4/phrases.json', 'w'), ensure_ascii=False, indent=1)
