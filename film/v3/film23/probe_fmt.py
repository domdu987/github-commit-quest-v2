import sys,json
for l in sys.stdin:
    if not l.startswith('{'): print(l.strip()); continue
    d=json.loads(l); h=d['heads']
    print(d['g'], d.get('lens',''), ' '.join('%s(%d,%d,%d)'%(k,v['x'],v['y'],v['w']) for k,v in h.items() if k.startswith('cy')), ' lift:', ' '.join('(%d,%d,%d)'%(v['x'],v['y'],v['w']) for k,v in h.items() if k.startswith('lf')))
