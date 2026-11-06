"""Long-cut-only changes to the 16:9 EP.1 build (hf/L1/index.html): the hook title reads ฉบับเต็ม and sits above the caption band."""
import sys
p = sys.argv[1]; s = open(p).read()
for a, b, n in [('cam: { keys: [{ t: 0, ...fr(600, 1450, 1.12, 540, 1060) }] }, captions: caps("c_hC")', 'cam: { keys: [{ t: 0, ...fr(600, 1500, 1.0, 540, 960) }] }, captions: caps("c_hC")', 1),
                ('stroke-linejoin="round">EP.1</text></g>`); } });', 'stroke-linejoin="round">ฉบับเต็ม</text></g>`); } });', 1),
                ('paint-order="stroke">EP.1</text>', 'paint-order="stroke">ฉบับเต็ม</text>', 1),
                ('M140,1800Q380,1772 560,1790T1000,1780V2100H140Z', 'M-660,1812Q-200,1770 140,1800Q380,1772 560,1790T1000,1780Q1400,1770 1740,1795V2800H-660Z', 1),
                ('d="M140,1800Q380,1772 560,1790T1000,1780"', 'd="M-660,1812Q-200,1770 140,1800Q380,1772 560,1790T1000,1780Q1400,1770 1740,1795"', 1),
                ('<div class="badge" id="badge">หนวดใส · EP.1</div>', '<div class="badge" id="badge">หนวดใส · ตอน 1</div>', 1)]:
    assert s.count(a) == n, (a, s.count(a)); s = s.replace(a, b)
open(p, "w").write(s); print("patched", p)
