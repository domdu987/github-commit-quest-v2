#!/usr/bin/env python3
"""Prototype 2D SVG puppet for the reference style (spec/character_anatomy.md, recipe b).
All geometry is in head-diameter units (D = 1, origin = head centre, +y down) and scaled by D px.
Usage: python3 character_puppet_proto.py out.svg [D_px]   -> writes a two-character test sheet.
Rasterise: google-chrome --headless --no-sandbox --screenshot=out.png --window-size=W,H --default-background-color=00000000 out.svg
"""
import sys, math

INK = "#3a2832"          # sampled ink colour (clip A t44.0 / t55.0, clip B t21.0)
HEAD = "#fdf8f6"; HEAD_RIM = "#ecdeed"

def smooth_closed(pts):
    """Catmull-Rom -> cubic bezier closed path through pts."""
    n = len(pts); d = f"M{pts[0][0]:.4f},{pts[0][1]:.4f} "
    for i in range(n):
        p0, p1, p2, p3 = pts[(i-1) % n], pts[i], pts[(i+1) % n], pts[(i+2) % n]
        c1 = (p1[0] + (p2[0]-p0[0])/6, p1[1] + (p2[1]-p0[1])/6)
        c2 = (p2[0] - (p3[0]-p1[0])/6, p2[1] - (p3[1]-p1[1])/6)
        d += f"C{c1[0]:.4f},{c1[1]:.4f} {c2[0]:.4f},{c2[1]:.4f} {p2[0]:.4f},{p2[1]:.4f} "
    return d + "Z"

# half-width profile (fraction of Wt/2 , fraction of Ht), top -> bottom. Measured on clip A t16.0 (stout) / t02.0 (slim)
PROFILE_EGG  = [(0.50,0.02),(0.82,0.10),(0.93,0.25),(0.98,0.38),(1.00,0.58),(0.98,0.77),(0.93,0.84),(0.72,0.95),(0.40,0.995)]
PROFILE_PILL = [(0.60,0.02),(0.90,0.10),(0.97,0.25),(1.00,0.50),(1.00,0.70),(0.96,0.85),(0.75,0.96),(0.40,1.00)]

def torso_path(Wt, Ht, yT, profile):
    right = [(Wt/2*fx, yT + Ht*fy) for fx, fy in profile]
    left = [(-x, y) for x, y in reversed(right)]
    return smooth_closed([(0, yT)] + right + [(0, yT+Ht)] + left)

def limb(S, E, H, w, bend=1.0):
    """stroke through shoulder/hip S, elbow/knee E, hand/ankle H. bend=1 rubber hose, 0 = sharp joint."""
    C = (2*E[0] - (S[0]+H[0])/2, 2*E[1] - (S[1]+H[1])/2)       # quadratic control so curve passes through E
    C = (E[0] + (C[0]-E[0])*bend, E[1] + (C[1]-E[1])*bend)
    if bend < 0.05:
        d = f"M{S[0]:.4f},{S[1]:.4f} L{E[0]:.4f},{E[1]:.4f} L{H[0]:.4f},{H[1]:.4f}"
    else:
        d = f"M{S[0]:.4f},{S[1]:.4f} Q{C[0]:.4f},{C[1]:.4f} {H[0]:.4f},{H[1]:.4f}"
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'

def shade(hexc, k):
    r, g, b = [int(hexc[i:i+2], 16) for i in (1, 3, 5)]
    f = lambda v: max(0, min(255, int(round(v*k))))
    return "#%02x%02x%02x" % (f(r), f(g), f(b))

def character(uid, kind="hero"):
    slim = (kind == "hero")
    Wt   = 0.57 if slim else 1.00           # torso width
    Ht   = 0.99 if slim else 1.06           # torso height incl. 0.13 hidden behind the head
    yT   = 0.36                             # torso top (head bottom is at +0.49)
    yB   = yT + Ht
    band = 0.14                             # trouser band height at the torso bottom
    lw   = 0.065                            # limb stroke
    base = "#3dbda6" if slim else "#c79d2d"
    pants = "#5a4540" if slim else "#45404d"
    o = []
    o.append(f'''<defs>
  <radialGradient id="hg{uid}" cx="0.45" cy="0.40" r="0.62"><stop offset="0" stop-color="#fffaf6"/><stop offset="0.72" stop-color="{HEAD}"/><stop offset="1" stop-color="{HEAD_RIM}"/></radialGradient>
  <linearGradient id="tg{uid}" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="{shade(base,1.12)}"/><stop offset="0.35" stop-color="{base}"/><stop offset="1" stop-color="{shade(base,0.72)}"/></linearGradient>
  <clipPath id="tc{uid}"><path d="{torso_path(Wt-0.03, Ht-0.03, yT+0.015, PROFILE_PILL if slim else PROFILE_EGG)}"/></clipPath>
  <clipPath id="hc{uid}"><ellipse cx="-0.012" cy="-0.012" rx="0.458" ry="0.448"/></clipPath>
  <filter id="wob{uid}" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="{7+uid*13}" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="0.035" xChannelSelector="R" yChannelSelector="G"/></filter>
</defs>''')
    o.append(f'<g filter="url(#wob{uid})">')
    # ---- legs (behind torso): hip -> knee -> ankle, then foot stub
    hipx = 0.22 if slim else 0.14
    L = 1.10 if slim else 1.45
    for s in (-1, 1):
        hip = (s*hipx, yB-0.04); ank = (s*(hipx+0.20 if slim else hipx+0.05), yB-0.04+L); knee = ((hip[0]+ank[0])/2 + s*0.015, (hip[1]+ank[1])/2)
        o.append(limb(hip, knee, ank, lw, 0.6))
        o.append(f'<path d="M{ank[0]:.4f},{ank[1]:.4f} l{s*0.19:.4f},0.035" fill="none" stroke="{INK}" stroke-width="{lw}" stroke-linecap="round"/>')
    # ---- torso: ink silhouette (outer) + colour fill inset (0.03 line) + costume clipped inside
    prof = PROFILE_PILL if slim else PROFILE_EGG
    o.append(f'<path d="{torso_path(Wt, Ht, yT, prof)}" fill="{INK}"/>')
    o.append(f'<g clip-path="url(#tc{uid})">')
    o.append(f'<rect x="-1" y="0" width="2" height="2" fill="url(#tg{uid})"/>')
    o.append(f'<path d="M-1,{yB-band:.3f} Q0,{yB-band+0.03:.3f} 1,{yB-band:.3f} L1,2 L-1,2Z" fill="{pants}" stroke="{INK}" stroke-width="0.022"/>')
    if slim:   # engineer: bandana, two suspenders with stitches + buckles, 2 buttons, pocket outline
        for s in (-1, 1):
            o.append(f'<rect x="{s*0.12-0.022:.3f}" y="0.50" width="0.044" height="{yB-band-0.50:.3f}" fill="#483a38" stroke="{INK}" stroke-width="0.012"/>')
            o.append(f'<line x1="{s*0.12:.3f}" y1="0.52" x2="{s*0.12:.3f}" y2="{yB-band-0.02:.3f}" stroke="#b9a58c" stroke-width="0.006" stroke-dasharray="0.02 0.016"/>')
            for by in (0.60, yB-band-0.045):
                o.append(f'<rect x="{s*0.12-0.024:.3f}" y="{by:.3f}" width="0.048" height="0.04" rx="0.008" fill="#c9a23a" stroke="{INK}" stroke-width="0.012"/>')
        o.append(f'<path d="M-0.12,0.50 L0.12,0.50 L0.04,0.74 Z" fill="#af2d3d" stroke="{INK}" stroke-width="0.016" stroke-linejoin="round"/>')
        for (dx, dy) in ((-0.05,0.54),(0.0,0.56),(0.05,0.54),(-0.02,0.61),(0.03,0.62),(0.02,0.68)):
            o.append(f'<circle cx="{dx}" cy="{dy}" r="0.008" fill="#f6d9da"/>')
        for by in (0.83, 1.13):
            o.append(f'<circle cx="0" cy="{by}" r="0.022" fill="#dfeaf2" stroke="{INK}" stroke-width="0.012"/>')
        o.append(f'<rect x="-0.25" y="0.93" width="0.075" height="0.13" fill="none" stroke="{shade(base,0.55)}" stroke-width="0.012"/>')
    else:      # tycoon waistcoat: shirt V, 5 gold buttons, watch chain, 3 welt pockets
        o.append(f'<path d="M-0.10,0.46 L0.10,0.46 L0.0,0.74 Z" fill="#e7dcdb" stroke="{INK}" stroke-width="0.016" stroke-linejoin="round"/>')
        o.append(f'<line x1="0" y1="0.48" x2="0" y2="0.70" stroke="#ae9b82" stroke-width="0.006"/>')
        for (px, py, pw) in ((-0.42,0.62,0.15),(-0.44,1.00,0.16),(0.20,1.00,0.21)):
            o.append(f'<rect x="{px}" y="{py}" width="{pw}" height="0.045" fill="#8e6f2c" stroke="{INK}" stroke-width="0.014"/>')
        for i in range(5):
            o.append(f'<circle cx="0" cy="{0.80+i*0.097:.3f}" r="0.030" fill="#d7c374" stroke="{INK}" stroke-width="0.016"/>')
        n = 12
        for i in range(n+1):
            t = i/n; cx = 0.02 + 0.30*t; cy = 0.92 + 0.11*math.sin(math.pi*t) - 0.02*t
            o.append(f'<ellipse cx="{cx:.3f}" cy="{cy:.3f}" rx="0.020" ry="0.015" fill="#d8bd78" stroke="{INK}" stroke-width="0.009"/>')
        o.append(f'<circle cx="0.33" cy="0.90" r="0.030" fill="#d7c374" stroke="{INK}" stroke-width="0.016"/>')
    o.append('</g>')
    # ---- arms (in front of torso). hero: both hands on hips (clip A t02.0); boss: one on hip, one hanging (t16.0)
    sx = Wt/2 - 0.045
    if slim:
        for s in (-1, 1):
            o.append(limb((s*sx, 0.56), (s*(sx+0.21), 0.86), (s*(sx+0.02), 1.22), lw, 0.75))
            o.append(f'<circle cx="{s*(sx+0.02):.3f}" cy="1.22" r="0.062" fill="{INK}"/>')
    else:
        o.append(limb((sx-0.10, 0.42), (sx+0.20, 0.60), (sx-0.05, 0.84), lw, 0.55))
        o.append(f'<circle cx="{sx-0.05:.3f}" cy="0.84" r="0.066" fill="{INK}"/>')
        o.append(limb((-sx+0.08, 0.44), (-sx-0.06, 0.68), (-sx-0.07, 0.93), lw, 0.8))
        o.append(f'<circle cx="{-sx-0.07:.3f}" cy="0.93" r="0.066" fill="{INK}"/>')
    # ---- head: ink ellipse, fill ellipse shifted up-left => thin line upper-left (0.03), thick lower-right (0.054)
    o.append(f'<ellipse cx="0" cy="0" rx="0.50" ry="0.49" fill="{INK}"/>')
    o.append(f'<ellipse cx="-0.012" cy="-0.012" rx="0.458" ry="0.448" fill="url(#hg{uid})"/>')
    if slim:   # hair patches inside the head, from the cap edge down to just below the equator
        for s in (-1, 1):
            o.append(f'<path clip-path="url(#hc{uid})" d="M{s*0.50},-0.30 L{s*0.33},-0.30 Q{s*0.40},-0.05 {s*0.455},0.08 L{s*0.50},0.08Z" fill="#9b6d49"/>')
    # minimal face (placeholder; see face spec)
    ey = 0.05 if slim else -0.03
    for s in (-1, 1):
        o.append(f'<ellipse cx="{s*0.15}" cy="{ey+0.03}" rx="0.038" ry="0.045" fill="{INK}"/>')
        o.append(f'<path d="M{s*0.15-0.075},{ey-0.012} L{s*0.15+0.075},{ey-0.012}" stroke="{INK}" stroke-width="0.022" stroke-linecap="round"/>')
    o.append(f'<path d="M-0.05,{ey+0.20} Q0.0,{ey+0.17 if not slim else ey+0.25} 0.06,{ey+0.20}" fill="none" stroke="{INK}" stroke-width="0.024" stroke-linecap="round"/>')
    # ---- hats: drawn OVER the head, replacing its top 0.25-0.35 D (do not perch them on top)
    if slim:   # striped engineer cap: dome rx 0.425, top -0.54, band/visor bottom -0.20
        o.append(f'<g transform="rotate(-2)">')
        o.append(f'<ellipse cx="0" cy="-0.385" rx="0.44" ry="0.165" fill="{INK}"/>')
        o.append(f'<clipPath id="cc{uid}"><ellipse cx="0" cy="-0.385" rx="0.415" ry="0.140"/></clipPath>')
        o.append(f'<g clip-path="url(#cc{uid})"><rect x="-1" y="-1" width="2" height="1" fill="#44598b"/>')
        for i in range(-10, 11):                              # 21 white stripes fanning from the top button
            xb = i*0.062; xt = i*0.012
            o.append(f'<path d="M{xt-0.004:.4f},-0.53 L{xt+0.004:.4f},-0.53 L{xb+0.016:.4f},-0.22 L{xb-0.016:.4f},-0.22Z" fill="#dee9fb"/>')
        o.append('</g>')
        o.append(f'<path d="M-0.41,-0.30 Q0,-0.24 0.41,-0.30 L0.40,-0.255 Q0,-0.195 -0.40,-0.255Z" fill="#362a3b" stroke="{INK}" stroke-width="0.02" stroke-linejoin="round"/>')
        o.append(f'<path d="M-0.38,-0.262 Q0,-0.205 0.38,-0.262 Q0,-0.150 -0.38,-0.262Z" fill="#989eb6" stroke="{INK}" stroke-width="0.022" stroke-linejoin="round"/>')
        o.append(f'<ellipse cx="0" cy="-0.538" rx="0.030" ry="0.014" fill="#dee9fb" stroke="{INK}" stroke-width="0.012"/>')
        o.append('</g>')
    else:      # bowler: crown rx 0.42 x 0.31 above y=-0.37, brim rx 0.56, front dips to the brows (-0.27)
        o.append(f'<g transform="rotate(-3)">')
        o.append(f'<path d="M-0.42,-0.36 A0.42,0.31 0 0 1 0.42,-0.36 Z" fill="#463f4e" stroke="{INK}" stroke-width="0.035" stroke-linejoin="round"/>')
        o.append(f'<path d="M-0.30,-0.50 Q-0.18,-0.63 0.05,-0.635" fill="none" stroke="#cac8e2" stroke-width="0.022" stroke-linecap="round" opacity="0.8"/>')
        o.append(f'<path d="M-0.56,-0.385 Q-0.57,-0.33 -0.40,-0.31 Q0,-0.22 0.40,-0.31 Q0.57,-0.33 0.56,-0.385 Q0.30,-0.34 0,-0.345 Q-0.30,-0.34 -0.56,-0.385Z" fill="#3b2f3a" stroke="{INK}" stroke-width="0.03" stroke-linejoin="round"/>')
        o.append(f'<path d="M-0.40,-0.325 Q0,-0.27 0.36,-0.325" fill="none" stroke="#635764" stroke-width="0.014" stroke-linecap="round"/>')
        o.append('</g>')
    o.append('</g>')
    return "\n".join(o)

def sheet(D=300):
    W, H = int(3.6*D), int(3.9*D)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f'<rect width="{W}" height="{H}" fill="#e98a43"/>']
    s.append(f'<g transform="translate({0.95*D:.1f},{0.85*D:.1f}) scale({D})">{character(1,"hero")}</g>')
    s.append(f'<g transform="translate({2.55*D:.1f},{0.85*D:.1f}) scale({D})">{character(2,"boss")}</g>')
    s.append('</svg>')
    return "\n".join(s), W, H

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "puppet_proto.svg"
    D = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    svg, W, H = sheet(D)
    open(out, "w").write(svg)
    print(out, W, H)
