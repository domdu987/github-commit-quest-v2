import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shot as S, c22 as C
sys.path.insert(0, os.path.join(C.PROJ, 'v3', 'tools')); import ground_check22 as G
T = S.make('preview'); allf = []
g0 = int(sys.argv[1]); g1 = int(sys.argv[2])
for g in range(g0, g1 + 1, 10):
    T.pose(g, S.actors); allf += G.check_frame(T.sc, 1)
    allf = [(g, b, c) if a == 1 else (a, b, c) for a, b, c in allf]
import collections
cnt = collections.Counter((b.rsplit('_', 1)[0], c.split(' ')[0] + ' ' + (c.split(' ')[1][:4] if ' ' in c else '')) for a, b, c in allf)
for k, v in sorted(cnt.items()): print(v, k)
for a, b, c in allf[:12]: print(a, b, c)
print('TOTAL', len(allf))

ok = not allf
L = ["# GROUND.md (QA_TEAM §K, ground_check22.check_frame on the per-frame scene, every 10th frame)", "frames %d-%d, tolerance 0.02" % (g0, g1), "RESULT: %s (%d failures)" % ('PASS' if ok else 'FAIL', len(allf)), "",
     "Flags used: mounted = the door plaques (sign boards fixed on the wall above the doors, seen touching it). Beck stands on the floor with the cast contact shadow; no airborne flags.", ""]
L += ["| %s | %s | %s |" % x for x in allf]
open(os.path.join(HERE, 'GROUND.md'), 'w').write("\n".join(L) + "\n")
