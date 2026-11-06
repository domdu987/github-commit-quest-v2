"""Long-cut-only changes to the 16:9 EP.1 build (hf/L1/index.html): the hook title reads ตอน 1 (the long has its own title card) and sits above the caption band."""
import sys
p = sys.argv[1]; s = open(p).read()
for a, b, n in [                                ('paint-order="stroke">EP.1</text>', 'paint-order="stroke">ตอน 1</text>', 1),
                                                ]:   # the badge is set to "หนวดใส" by toland.py
    assert s.count(a) == n, (a, s.count(a)); s = s.replace(a, b)
open(p, "w").write(s); print("patched", p)
