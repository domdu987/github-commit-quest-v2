#!/usr/bin/env python3
"""List the takes a sweeper has to finish. Read-only: it changes nothing.

usage: python3 sweep_takes.py <project dir> <journal.jsonl> [<journal.jsonl> ...]

For every take a workflow worker returned with complete=false (read from the journals, not from the summary
line), and for every take folder under <project>/v3/film/ that lacks one of the finished-take files, it prints:
  - frames on disk against the range in meta.json (or g0/g1 from the worker's result),
  - which of meta.json, cues.json, contact.jpg, QA.md exist,
  - whether a render process still runs in that folder (ps plus /proc/PID/cwd),
  - CLAIMED.txt if another lane owns the folder,
  - the first 200 characters of the worker's note.
Then finish each take by hand: wait for its render, run the take's own post, grade, contact, qa and QA.md
commands (they are in its shot.py, runner or work/*.sh), and look at the contact sheet.
"""
import json, os, re, subprocess, sys

def renders_by_folder():
    out = {}
    try:
        ps = subprocess.run(['ps', '-eo', 'pid,args'], capture_output=True, text=True).stdout.splitlines()[1:]
    except Exception:
        return out
    for line in ps:
        pid, _, cmd = line.strip().partition(' ')
        if not re.search(r'(shot|otake|bshot|kshot|mc|render)\w*\.py|blender', cmd):
            continue
        try:
            cwd = os.readlink('/proc/%s/cwd' % pid)
        except OSError:
            continue
        out.setdefault(cwd, []).append('%s %s' % (pid, cmd[:80]))
    return out

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    film = os.path.join(os.path.abspath(sys.argv[1]), 'v3', 'film')
    results, labels = {}, {}
    for j in sys.argv[2:]:
        for line in open(j, encoding='utf8'):
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            if ev.get('type') == 'started':
                labels[ev.get('agentId')] = ev.get('label', '')
            if ev.get('type') != 'result' or not isinstance(ev.get('result'), dict):
                continue
            for t in ev['result'].get('takes', []) or []:
                name = os.path.basename(str(t.get('take', '')).rstrip('/'))
                if name:
                    results[name] = (t, labels.get(ev.get('agentId'), ''))
    procs = renders_by_folder()
    names = sorted(set(results) | {d for d in os.listdir(film) if re.fullmatch(r's\d\d', d)})
    for name in names:
        d = os.path.join(film, name)
        t, label = results.get(name, ({}, ''))
        files = {f: os.path.exists(os.path.join(d, f)) for f in ('meta.json', 'cues.json', 'contact.jpg', 'QA.md')}
        nfr = len([f for f in os.listdir(os.path.join(d, 'frames'))]) if os.path.isdir(os.path.join(d, 'frames')) else 0
        want = None
        if files['meta.json']:
            m = json.load(open(os.path.join(d, 'meta.json')))
            want = m['g1'] - m['g0'] + m.get('handle_in', 0) + m.get('handle_out', 0)
        elif 'g0' in t and 'g1' in t:
            want = '>= %d' % (t['g1'] - t['g0'])
        running = [v for k, v in procs.items() if k == d or k.startswith(d + os.sep)]
        claimed = open(os.path.join(d, 'CLAIMED.txt')).read().strip()[:80] if os.path.exists(os.path.join(d, 'CLAIMED.txt')) else ''
        done = t.get('complete', True) is not False and all(files.values()) and (want is None or nfr == want)
        if done and not running:
            continue
        missing = [k for k, v in files.items() if not v]
        disk_ok = not missing and (want is None or nfr == want) and not running
        print('%s  frames %s / %s  %s  %s' % (name, nfr, want, ('missing: ' + ' '.join(missing)) if missing else 'files ok',
              ('complete=false' if t.get('complete') is False else '') +
              ('  (complete on disk: look at contact.jpg, then count it as swept)' if disk_ok else '')))
        for r in running:
            print('    RENDER RUNNING: %s' % '; '.join(r))
        if claimed:
            print('    CLAIMED: %s' % claimed)
        if t.get('notes'):
            print('    note (%s): %s' % (label, t['notes'][:200].replace('\n', ' ')))

if __name__ == '__main__':
    main()
