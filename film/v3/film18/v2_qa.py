#!/usr/bin/env python3
"""v2_qa.py -- append the v2 section to QA.md of a take (run in the take folder): python3 ../v2_qa.py "<notes>" """
import json, sys
m = json.load(open('meta.json')); fd = m['framediff']
g = open('GROUND.md').read().splitlines(); ground = [l for l in g if 'result' in l or 'FAIL rows' in l][:2]
j = open('JITTER.txt').read().strip()
txt = "\n\n## V2 (client fixes: no camera shake / nothing floats)\n%s\n- take.mkv crf 21, first_g %d, %d frames; transition in: %s.\n- frame diff (90x160 grey, in-shot): median %s / p90 %s (rule: median >= 4).\n- ground_check (film/v3/tools/ground_check.py through film18/gc_run.py, every 6th frame): %s  (full table in GROUND.md; cards are checked by bounding box, so only a floating card base can fail; shadows are the cards' contact quads).\n- qa_jitter output:\n```\n%s\n```\n" % (
    sys.argv[1] if len(sys.argv) > 1 else '', m['first_g'], m['n_frames'], m['transition_in'], fd['median'], fd['p90'], ' / '.join(ground), j)
open('QA.md', 'a').write(txt)
