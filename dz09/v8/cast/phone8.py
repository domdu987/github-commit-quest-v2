"""phone8.py (copied from v4/cast_dz09/phone25.py; the avatar is drawn by draw8) -- Kong's smartphone screen: Namnuea's photo + "น้ำเหนือ — 4 สายที่ไม่ได้รับ".

Thai is set with PIL + libraqm (complex shaping: the tone marks and vowels above/below stack correctly) in
fonts/Kanit_900Black.ttf.  The text is checked glyph by glyph against the font's .notdef box (PIL mask comparison).

    screen_png(out, w=540, h=1000, missed=4, state="missed")   # "missed" | "incoming" | "off"
    data_uri(path)                                              # for prop_svg(..., {"screen_png": uri})
    verify_thai(text) -> {"missing": [...], "notdef_like": [...], "ok": bool}
    python3 phone25.py        -> out/phone_screen.png, out/phone_insert.png (phone prop at insert size), prints the check
"""
import base64, os, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
FONT = os.path.join(PROJ, "fonts", "Kanit_900Black.ttf")
CALLER = "น้ำเหนือ"
LINE = "น้ำเหนือ — 4 สายที่ไม่ได้รับ"
sys.path.insert(0, HERE)
import draw8, raster8


def _font(sz):
    return ImageFont.truetype(FONT, sz, layout_engine=ImageFont.Layout.RAQM)


def verify_thai(text, font_path=FONT):
    """every non-space character is drawn and compared with the .notdef drawing (a private-use code point);
    also the shaped line must be narrower than the sum of its glyphs (marks stacked, not placed side by side)."""
    f = ImageFont.truetype(font_path, 64, layout_engine=ImageFont.Layout.RAQM)

    def g(c):
        im = Image.new("L", (160, 160), 0)
        ImageDraw.Draw(im).text((40, 30), c, font=f, fill=255)
        return im.tobytes()
    nd = g(chr(0xE000))
    notdef = sorted("U+%04X" % ord(c) for c in set(text) if not c.isspace() and g(c) == nd)
    blank = sorted("U+%04X" % ord(c) for c in set(text) if not c.isspace() and not any(g(c)))
    line_w = f.getlength(text)
    sum_w = sum(f.getlength(c) for c in text)
    return {"chars": len(set(text) - {" "}), "notdef": notdef, "blank": blank,
            "shaped_width_px": round(line_w, 1), "sum_of_glyphs_px": round(sum_w, 1),
            "ok": not notdef and not blank}


def screen_png(out, w=540, h=1000, missed=4, state="missed"):
    im = Image.new("RGB", (w, h), (14, 18, 34))
    dr = ImageDraw.Draw(im)
    if state == "off":
        im.save(out)
        return out
    for y in range(h):                                   # night lock-screen gradient
        k = y / float(h)
        dr.line([(0, y), (w, y)], fill=(int(18 + 30 * k), int(24 + 10 * k), int(52 - 10 * k)))
    fs = _font(int(w * 0.075))
    dr.text((w // 2, int(h * 0.06)), "22:47", font=_font(int(w * 0.16)), fill=(235, 238, 245), anchor="mt")
    # avatar
    a = int(w * 0.46)
    av = _avatar(a)
    mask = Image.new("L", (a, a), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, a - 1, a - 1), fill=255)
    ax, ay = (w - a) // 2, int(h * 0.28)
    im.paste(av, (ax, ay), mask)
    dr.ellipse((ax - 4, ay - 4, ax + a + 4, ay + a + 4), outline=(240, 240, 245), width=5)
    dr.text((w // 2, ay + a + int(h * 0.03)), CALLER, font=_font(int(w * 0.12)), fill=(250, 250, 252), anchor="mt")
    if state == "missed":
        # notification card with the exact line, red badge with the count
        cy = int(h * 0.74)
        dr.rounded_rectangle((int(w * 0.05), cy, int(w * 0.95), cy + int(h * 0.12)), radius=int(w * 0.04), fill=(236, 236, 242))
        line = LINE.replace("4", str(missed))
        dr.text((int(w * 0.10), cy + int(h * 0.06)), line, font=_font(int(w * 0.058)), fill=(30, 28, 40), anchor="lm")
        r = int(w * 0.075)
        bx, by = ax + a - r // 2, ay + r // 3
        dr.ellipse((bx - r, by - r, bx + r, by + r), fill=(226, 69, 59), outline=(255, 255, 255), width=4)
        dr.text((bx, by), str(missed), font=_font(int(r * 1.3)), fill=(255, 255, 255), anchor="mm")
    else:                                               # incoming call: green / red buttons
        for x, col in ((0.25, (226, 69, 59)), (0.75, (57, 196, 90))):
            dr.ellipse((int(w * x) - 50, int(h * 0.82) - 50, int(w * x) + 50, int(h * 0.82) + 50), fill=col)
    im.save(out)
    return out


def data_uri(path):
    return "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()


def _avatar(a):
    fig = draw8.build("namnuea", {"view": "front", "expr": "smile"})
    hc = fig["anchors"]["head"]
    cv = (hc[0] - 0.85, hc[1] - 0.95, hc[0] + 0.85, hc[1] + 0.75)
    svg, W, H = draw8.doc(draw8.flat_svg(fig), cv, a / 1.7, bg="#f3c7a6")
    return Image.open(raster8.png(svg, W, H)).convert("RGB").resize((a, a))


if __name__ == "__main__":
    import json
    print(json.dumps(verify_thai(LINE)))
    p = screen_png(os.path.join(HERE, "tex", "phone_screen.png"))
    raster8.close()
