"""ep2d.py -- base of the class C1 shots: full frames DRAWN by code (PIL / numpy / cv2), no Cycles, no bpy.

A C1 module has
    CLASS = "C1"
    def draw(ctx) -> PIL.Image (RGB, ctx.W x ctx.H) or a uint8 numpy array H x W x 3
ctx: W, H (the asked output size), k (frame in the shot), n (frames in the shot), u (0..1), g, t (stage clock),
     scene (epcommon.Scene: .word(), .cue(), .mouth()), tier, ss (supersampling the helpers use: 2 at the final tier),
     frame_path(shot_id, k) -> path of another shot's rendered frame at this tier and size (for re-used frames).
Draw at ctx.W x ctx.H whatever the size is: lay out in fractions of the frame (ctx.px(0.5) = half the width).
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import epcommon as E

INK = (22, 20, 24)


class Ctx:
    def __init__(self, scene, shot, k, W, H, tier, out_base):
        self.scene, self.shot, self.k, self.W, self.H, self.tier = scene, shot, k, W, H, tier
        self.n = shot["f1"] - shot["f0"]
        self.u = k / float(max(self.n - 1, 1))
        self.g = scene.g_base + shot["f0"] + k
        self.t = self.g / float(E.FPS)
        self.ss = 2 if tier in E.FINAL_TIERS else 1
        self._base = out_base

    def px(self, frac):
        return frac * self.W

    def frame_path(self, sid, k):
        return os.path.join(self._base, E.norm_id(sid), E.frame_name(k) + ".png")

    def canvas(self, colour=(8, 10, 16)):
        """an RGB canvas at ss x the output size and its ImageDraw; finish with ctx.done(im)."""
        im = Image.new("RGB", (self.W * self.ss, self.H * self.ss), colour)
        return im, ImageDraw.Draw(im)

    def done(self, im):
        return im.resize((self.W, self.H), Image.LANCZOS) if im.size != (self.W, self.H) else im


def font(size, path=None):
    return ImageFont.truetype(path or E.KANIT, int(size), layout_engine=ImageFont.Layout.RAQM)


def rain(im, k, amount=0.2, seed=7):
    """a few light rain streaks over a drawn frame (the standing light-rain level), deterministic per frame."""
    W, H = im.size
    d = ImageDraw.Draw(im, "RGBA")
    rng = np.random.default_rng(seed * 1000 + k)
    for _ in range(int(90 * amount)):
        x = rng.uniform(0, W); y = rng.uniform(-0.1 * H, H); L = rng.uniform(0.03, 0.07) * H
        d.line([(x, y), (x - 0.12 * L, y + L)], fill=(200, 215, 235, int(rng.uniform(40, 110))), width=max(1, W // 360))
    return im


def vignette(im, strength=0.45):
    a = np.asarray(im).astype(np.float32)
    H, W = a.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    a *= (1 - strength * np.clip(r - 0.35, 0, 1) ** 1.5)[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
