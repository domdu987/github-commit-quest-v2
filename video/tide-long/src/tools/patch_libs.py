"""Long version (YouTube 16:9): sets that stop short of the widened stage (x -660…1740), extended only when window.LANDSCAPE is set
(read at draw time: the libraries load before LANDSCAPE is defined). Edits the build's own copies in tidelong/hf/lib1, lib2."""
import os
W = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
def sub(path, old, new, count=1):
    s = open(path).read(); n = s.count(old)
    assert n == count, (path, old[:80], n)
    open(path, "w").write(s.replace(old, new))
# EP.1 opener (Sets.tideSand + sandDraw): the ripples, the wet sheen and the water ran x -400…1500 → seams at both sides of the frame
p = os.path.join(W, "hf", "lib1", "tide.js")
sub(p, '    const id = o.id || "ts", r = mk(o.seed || 23), title = o.title || "ทะเลลด";\n',
       '    const id = o.id || "ts", r = mk(o.seed || 23), title = o.title || "ทะเลลด";\n'
       '    const XL = window.LANDSCAPE ? -900 : -400, XR = window.LANDSCAPE ? 2000 : 1500;   // long version 16:9: the sand runs to both new edges\n')
sub(p, 'for (let x = -400; x <= 1500; x += 40) p += `${p ? "L" : "M"}${x},${f1(y0 + x * 0.12 + Math.sin(x * 0.009 + ph) * 16)}`;',
       'for (let x = XL; x <= XR; x += 40) p += `${p ? "L" : "M"}${x},${f1(y0 + x * 0.12 + Math.sin(x * 0.009 + ph) * 16)}`;')
sub(p, 's += `<path d="M-400,${f1(y)}Q540,${f1(y - 120)} 1500,${f1(y + 40)}V${f1(y + 110)}Q540,${f1(y - 20)} -400,${f1(y + 90)}Z"',
       's += `<path d="M${XL},${f1(y)}Q540,${f1(y - 120)} ${XR},${f1(y + 40)}V${f1(y + 110)}Q540,${f1(y - 20)} ${XL},${f1(y + 90)}Z"')
sub(p, '    for (let k = 0; k < 80; k++) s += `<circle cx="${f1(-100 + r() * 1300)}"',
       '    if (window.LANDSCAPE) { const r2 = mk(97); for (let k = 0; k < 220; k++) s += `<circle cx="${f1(r2() < 0.5 ? -900 + r2() * 700 : 1300 + r2() * 700)}" cy="${f1(-200 + r2() * 2400)}" r="${f1(0.8 + r2() * 1.8)}" fill="${r2() < 0.5 ? "#fff8e8" : "#7a6444"}" opacity="${f1(0.3 + r2() * 0.5)}"/>`; }\n'
       '    for (let k = 0; k < 80; k++) s += `<circle cx="${f1(-100 + r() * 1300)}"')
sub(p, '    const S = ST[id], yE = lerp(2080, -260, u);\n',
       '    const S = ST[id], yE = lerp(2080, -260, u), XL = window.LANDSCAPE ? -900 : -400, XR = window.LANDSCAPE ? 2000 : 1500;\n')
sub(p, '    const E = []; for (let x = -400; x <= 1500; x += 30) E.push([x, edge(x)]);\n    const wd = `M-400,-700H1500V${f1(edge(1500))}L${E.slice().reverse().map(P2).join("L")}Z`;',
       '    const E = []; for (let x = XL; x <= XR; x += 30) E.push([x, edge(x)]);\n    const wd = `M${XL},-700H${XR}V${f1(edge(XR))}L${E.slice().reverse().map(P2).join("L")}Z`;')
sub(p, 'el(`${id}-sheen`).setAttribute("d", `M${E.map(P2).join("L")}L1500,${f1(yE + 420)}L-400,${f1(yE + 420)}Z`);',
       'el(`${id}-sheen`).setAttribute("d", `M${E.map(P2).join("L")}L${XR},${f1(yE + 420)}L${XL},${f1(yE + 420)}Z`);')
sub(p, '    put(L.sky, `<rect x="-600" y="-600" width="2300" height="3200" fill="#cbb084"/>`);\n',
       '    put(L.sky, `<rect x="${XL - 200}" y="-600" width="${XR - XL + 400}" height="3200" fill="#cbb084"/>`);\n')
sub(p, '    s += `<rect x="-600" y="-600" width="2300" height="3200" fill="url(#${id}-sandG)"/>`;\n',
       '    s += `<rect x="${XL - 200}" y="-600" width="${XR - XL + 400}" height="3200" fill="url(#${id}-sandG)"/>`;   // (vertical: -600…1700 as before)\n')
# EP.1 cross-sections (Sets.tideSection): the sky and the floor stopped at x -600 → a dark strip down the left edge
p = os.path.join(W, "hf", "lib1", "tidemap.js")
sub(p, '    put(L.sky, `<rect x="-600" y="-600" width="2400" height="3200" fill="url(#tmSecSky)"/>',
       '    const SX = window.LANDSCAPE ? -1200 : -600, SW = window.LANDSCAPE ? 3600 : 2400;   // long version 16:9: sky and floor to both edges\n'
       '    put(L.sky, `<rect x="${SX}" y="-600" width="${SW}" height="3200" fill="url(#tmSecSky)"/>')
sub(p, '      <rect x="-600" y="1260" width="2400" height="1200" fill="url(#tmFloor)"/>`);',
       '      <rect x="${SX}" y="1260" width="${SW}" height="1200" fill="url(#tmFloor)"/>`);')
# EP.2 the second wave (Tide.waveIn / waveDraw): the wall's columns ran x -80…1160 → a strip of wave in the middle of the wide frame
p = os.path.join(W, "hf", "lib2", "tide.js")
sub(p, '    const X0 = -80, X1 = 1160, cols = [];\n',
       '    const X0 = window.LANDSCAPE ? -780 : -80, X1 = window.LANDSCAPE ? 1860 : 1160, cols = [];   // long version 16:9: the wall across the whole frame\n')
print("libs patched")
