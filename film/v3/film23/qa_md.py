#!/usr/bin/env python3
"""qa_md.py <sNN> -- write sNN/QA.md from numbers.json + QA_AUTO.md + QA_JITTER.txt + GROUND.md + the per-take notes below."""
import os, sys, json, re
HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = json.load(open(os.path.join(HERE, 'qa_notes.json')))
def main(name):
    D = os.path.join(HERE, name); n = json.load(open(os.path.join(D, 'numbers.json'))); m = json.load(open(os.path.join(D, 'meta.json'))); nt = NOTES[name]
    qa = open(os.path.join(D, 'QA_AUTO.md')).read().splitlines()[0]
    gr = open(os.path.join(D, 'GROUND.md')).read().splitlines(); gl = [l for l in gr if 'result' in l][:1]
    jit = open(os.path.join(D, 'QA_JITTER.txt')).read().strip()
    L = ['# %s QA: film 23, shot %s (%s %s)' % (name, m['shots'][0], m['location'], m['light']), '',
         '## Delivered', nt['delivered'].format(**dict({k: v for k, v in n.items() if not isinstance(v, (dict, list))}, **{k: v for k, v in m.items() if not isinstance(v, (dict, list))})), '',
         '## Clock (ESTIMATED timing: timing_EST.json + plan table)',
         '- g0 %d, g1 %d (planned, round(t*30)), g1_render %d (planned + 25 %% tail: the move and the action continue, eased), first_g %d (in-handle %d), n_frames %d.' % (m['g0'], m['g1'], m['g1_render'], m['first_g'], m['handle_in'], m['n_frames']),
         '- transition_in: %s %d frames (plan).' % (m['transition_in']['type'], m['transition_in']['frames']), '',
         '## Automatic QA', '- `qa_auto.py`: %s' % qa.replace('# ', ''), '- `qa_jitter.py` (every second must be <= 2.0 px; no line = clean): ```%s```' % jit.replace('\n', ' / '),
         '- ground_check (`--every 10` equivalent on the built scene, GROUND.md): %s' % (gl[0].replace('- ', '') if gl else 'see GROUND.md'),
         '- frame-diff (90x160 grey, body frames): median %.2f, p90 %.2f, min %.2f (rhythm target median >= 4, p90 >= 12)%s' % (n['diff_median'], n['diff_p90'], n['diff_min'], nt.get('diff_note', '')),
         '- luma (mean of RGB, every 5th frame): %.1f .. %.1f (mean %.1f)%s' % (n['luma_min'], n['luma_max'], n['luma_mean'], nt.get('luma_note', '')),
         '- shade hue (target 240-260; first / mid / last): ' + ', '.join('g%s %.1f' % (g, v['shade_hue']) for g, v in n['shade_hue'].items()) + nt.get('hue_note', ''),
         '- heads: max head-centre y %.1f px over the whole take (caption band starts y 880; head radius at most ~%s px): %s' % (n['max_head_centre_y'], nt.get('head_r', '30'), ', '.join('%s %.0f' % (k, v) for k, v in n['head_y_by_card'].items())),
         ] + (['- water share of the frame (far water line): %.1f %% .. %.1f %%' % (100 * n['water_frac_range'][0], 100 * n['water_frac_range'][1])] if n.get('water_frac_range') else []) + [
         '- render: 720x1280, 12 samples, OIDN, %s s/frame wall (%s s CPU), 2 threads while a second render ran.' % (n['s_per_frame_wall'], n['s_per_frame_cpu']), '',
         '## Look checks (contact.jpg at 6 fps, phone_sheet.jpg)'] + ['- ' + x for x in nt['look']] + ['', '## Rules'] + ['- ' + x for x in nt['rules']] + ['', '## Deviations from the plan / set'] + ['- ' + x for x in nt['dev']]
    open(os.path.join(D, 'QA.md'), 'w').write('\n'.join(L) + '\n')
if __name__ == '__main__': main(sys.argv[1])
