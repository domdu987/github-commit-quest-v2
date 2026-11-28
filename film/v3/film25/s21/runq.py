#!/usr/bin/env python3
"""runq.py -- tiny job queue: at most 2 render processes at once.  Jobs = lines of queue.txt ("<dir> <args...>" runs `python3 <dir>/shot.py final <args>` with SETPROJ);
a line is taken once (renamed to done.txt).  Run: nohup python3 runq.py &"""
import os, subprocess, time, sys
HERE = os.path.dirname(os.path.abspath(__file__))
Q = os.path.join(HERE, "queue.txt"); DONE = os.path.join(HERE, "done.txt")
ENV = dict(os.environ, SETPROJ="/tmp/claude-0/-home-user-github-commit-quest-v2/e18b3327-71fd-5528-a102-9641336ac590/scratchpad/snap")
procs = []
while True:
    procs = [p for p in procs if p.poll() is None]
    if len(procs) < 2 and os.path.exists(Q):
        lines = [l for l in open(Q).read().splitlines() if l.strip()]
        if lines:
            job = lines[0]; open(Q, "w").write("\n".join(lines[1:]) + ("\n" if len(lines) > 1 else ""))
            open(DONE, "a").write(job + "\n")
            d, *a = job.split()
            td = os.path.join(HERE, "..", d)
            log = open(os.path.join(td, "log_%s.txt" % a[0].replace(":", "_").replace(",", "_")), "a")
            procs.append(subprocess.Popen(["python3", os.path.join(td, "shot.py"), "final"] + a, cwd=td, env=ENV, stdout=log, stderr=subprocess.STDOUT))
            continue
    time.sleep(5)
