"""List every actors: [...] group in the film's parts with each actor's x, y, scale, and flag kid/adult pairs at about the same depth
whose scale ratio is off (ทะเลลด used kid ≈ 0.77 × teen/adult at the same depth)."""
import re, sys
KID = {"pu", "puCam", "puNoCam"}
TEEN = {"fon", "fonPhone"}
ADULT = {"yaiBua", "yaiBuaCry", "taTian", "taTianCry"}
pat = re.compile(r'P\("(\w+)",\s*([-\d.]+|PULL\.[a-z]\[0\][^,]*),\s*([-\d.]+),\s*([\d.]+)')
for path in sys.argv[1:]:
    s = open(path).read()
    for m in re.finditer(r"actors:\s*(\[|\(\(\))", s):
        i = m.end(); depth = 1; j = i
        while j < len(s) and depth:
            depth += {"[": 1, "]": -1}.get(s[j], 0); j += 1
        block = s[i:j]
        acts = [(a, x, float(y), float(sc)) for a, x, y, sc in pat.findall(block)]
        if len(acts) < 2: continue
        line = s.count("\n", 0, m.start()) + 1
        kids = [a for a in acts if a[0] in KID]; big = [a for a in acts if a[0] in ADULT | TEEN]
        for k in kids:
            for b in big:
                if abs(k[2] - b[2]) <= 160:
                    r = k[3] / b[3]
                    flag = "  <-- off" if not (0.70 <= r <= 0.84) else ""
                    print(f"{path.split('/')[-1]}:{line}  {k[0]} s{k[3]} y{int(k[2])}  vs  {b[0]} s{b[3]} y{int(b[2])}  ratio {r:.2f}{flag}")
