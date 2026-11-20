# T6a2: runs T6a's render_t6a.run() UNCHANGED for g1453-1535. Resumable (skips existing frames).
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'T6a'))
import render_t6a as R
a = sys.argv[sys.argv.index('--') + 1:]
if a[0] == 'check':
    R.run([1515], os.path.join(HERE, 'check'))
else:
    R.run(range(1453, 1536), os.path.join(HERE, 'frames'))
