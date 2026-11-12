#!/usr/bin/env python3
"""score.py - likeness scorecard against the two reference clips.

Usage:
    python3 score.py INPUT --out DIR [--label NAME] [--frames A:B] [--no-captions]
    python3 score.py --metrics-md          # print the metric table (definitions, ranges, sources)

INPUT is an MP4, a folder of frames (f_0001.png ... at 30 fps) or a single still.
--frames A:B   score only frames A to B (0-based, inclusive) of a video or frame folder.
--no-captions  the input is a render without burned-in captions: leave the captions group out
               (without this flag a clip without captions scores 0 on captions).
Writes DIR/scorecard.json, DIR/scorecard.md and DIR/report.jpg.

The index only covers measurable properties (colour statistics, line widths, camera motion,
caption geometry ...).  It is not a perceptual similarity score.
"""
import argparse
import colorsys
import glob
import json
import math
import os
import re
import sys
import time

import numpy as np
import cv2

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import heads as HD  # noqa: E402

cv2.setNumThreads(2)

W, H = 720, 1280
FPS = 30.0
CAP_Y0, CAP_Y1 = 850, 960            # caption band masked for every picture statistic
LW, LH = 360, 640                    # low-res size used for global motion (as camera-motion/gmotion.py)
TW, TH = 90, 160                     # tiny size used for the cut / dissolve scan
HERE = os.path.dirname(os.path.abspath(__file__))

GROUPS = [
    ('characters', 'Characters', 0.30),
    ('colour', 'Colour and tone', 0.15),
    ('density', 'Density and light structure', 0.15),
    ('camera', 'Camera and edit', 0.20),
    ('animation', 'Animation life', 0.10),
    ('captions', 'Captions', 0.10),
]

LS = 'LOOK_SPEC'
VM = 'verify_measurements'


def M(key, group, label, lo, hi, tol, fmt, src, definition, circ=False):
    return dict(key=key, group=group, label=label, lo=lo, hi=hi, tol=tol, fmt=fmt, src=src,
                definition=definition, circ=circ)


# Reference ranges.  "lo..hi" scores 1; the score falls linearly to 0 at "tol" outside the range.
# Sources name the spec section; where a bound was widened so that it spans what this tool measures
# on both reference clips, the source text says so.
METRICS = [
    # ---- 1. colour and tone (median over sampled frames, caption band masked) ----
    M('c_sat_mean', 'colour', 'Saturation mean (HSV S)', 0.40, 0.60, 0.15, '%.3f',
      LS + ' 4.1 row 1 (target 0.40-0.60; clip medians A 0.483, B 0.405; v1 0.293); ' + VM + ' row 13',
      'mean HSV saturation of the frame'),
    M('c_luma_p50', 'colour', 'Luma p50', 0.22, 0.47, 0.20, '%.3f',
      LS + ' 4.1 row 5 (target 0.22-0.45, interiors 0.147-0.423; v1 0.654); upper bound widened to this tool\'s clip A median',
      'median Rec.709 luma (0..1) of the encoded values'),
    M('c_black', 'colour', 'Black point (luma p1)', 0.08, 0.12, 0.06, '%.3f',
      LS + ' 4.1 row 12 (target 0.08-0.12; A 0.104, B 0.095; v1 0.153); ' + VM + ' row 14',
      '1st percentile of luma'),
    M('c_contrast', 'colour', 'Contrast (luma p95 - p5)', 0.60, 0.75, 0.25, '%.3f',
      LS + ' 4.1 row 7 (target 0.60-0.75; clip median 0.61, mid-interval frames 0.60; v1 0.678 already passes)',
      'luma p95 minus luma p5'),
    M('c_colourful', 'colour', 'Colourfulness (Hasler-Suesstrunk)', 55.0, 100.0, 25.0, '%.1f',
      LS + ' 4.1 row 8 (target 55-100; A 82, B 56; v1 49.7); ' + VM + ' row 13',
      'sqrt(std(R-G)^2 + std(0.5(R+G)-B)^2) + 0.3 sqrt(mean(R-G)^2 + mean(0.5(R+G)-B)^2), 8-bit scale'),
    M('c_share_s50', 'colour', 'Share of pixels with S > 0.5', 0.25, 0.90, 0.20, '%.3f',
      LS + ' 4.1 row 9 (target at least 0.25; interiors 0.230-0.875; v1 0.063)',
      'share of pixels whose HSV saturation exceeds 0.5'),
    M('c_dark_hue', 'colour', 'Hue of the darkest tenth (deg)', 250.0, 345.0, 45.0, '%.0f',
      LS + ' 4.1 row 13 (target hue 250-345; A #3d1c32 hue 319, B #392433 hue 318; v1 hue 26); ' + VM + ' row 14',
      'hue of the mean colour of the darkest 10 percent of pixels (mean taken over all sampled frames)', circ=True),
    M('c_share_v95', 'colour', 'Share of pixels with V > 0.95', 0.02, 0.09, 0.08, '%.3f',
      LS + ' 4.1 row 11 (target 0.02-0.09; A 0.035, B 0.045; v1 0.066 passes); ' + VM + ' row 13',
      'share of pixels whose HSV value exceeds 0.95'),
    M('c_dark_sat', 'colour', 'Saturation of the darkest tenth', 0.30, 1.0, 0.25, '%.2f',
      LS + ' 4.1 row 13 (target S at least 0.35; A #3d1c32 S 0.53, B #392433 S 0.37; v1 #4a3a2d S 0.39 passes, it fails on the hue); added in validation so that a grey shadow cannot pass the hue test; lower bound widened to 0.30 because this tool reads 0.33 on clip B (0.45 on clip A)',
      'HSV saturation of the mean colour of the darkest 10 percent of pixels (same colour as the hue metric)'),
    # ---- 2. density and light structure ----
    M('d_edge', 'density', 'Canny edge density (60/140)', 0.050, 0.110, 0.035, '%.3f',
      LS + ' 3.5 (pass at least 0.05; A 0.060, B 0.067; v1 0.016); upper bound = p90 of reference frames (environment_materials 2.1: 0.091 A, 0.107 B)',
      'share of pixels on a Canny edge (thresholds 60 / 140) of the grey frame'),
    M('d_featureless', 'density', 'Featureless 40 px blocks', 0.0, 0.33, 0.30, '%.3f',
      LS + ' 3.5 (pass at most 0.30; A 0.30, B 0.27; v1 0.64); filter = sigma-4 high-pass, std under 3 (' + VM + ' "other things": 0.32 / 0.29 with this filter)',
      'share of 40 x 40 px blocks whose high-pass (grey minus Gaussian sigma 4) standard deviation is under 3 levels'),
    M('d_luma_top', 'density', 'Mean luma, top third (0-255)', 85.0, 135.0, 60.0, '%.0f',
      'environment_materials 2.2 (top row A 119, B 108; v1 213) and ' + LS + ' 3.5 (top eighth 40-90 interiors; v1 212); thirds calibrated on clips A and B with this tool',
      'mean luma of rows 0-426'),
    M('d_luma_mid', 'density', 'Mean luma, middle third (0-255)', 105.0, 150.0, 50.0, '%.0f',
      'environment_materials 2.2 (middle rows A 120, B 125; v1 154) and ' + LS + ' 3.5 (brightest middle rows 105-150; v1 206)',
      'mean luma of rows 427-849'),
    M('d_luma_bot', 'density', 'Mean luma, bottom third (0-255)', 60.0, 105.0, 50.0, '%.0f',
      'environment_materials 2.2 (bottom row A 93, B 79; v1 160) and ' + LS + ' 3.5 (bottom eighth 30-70 interiors; v1 163)',
      'mean luma of rows 960-1279 (the caption band 850-959 is left out)'),
    M('d_thin_lines', 'density', 'Thin dark line share', 0.030, 0.200, 0.030, '%.3f',
      'environment_materials 2.3 (black-hat over 28: B patches 0.11-0.36, A patches 0.001-0.017, v1 wall and floor 0.000); whole-frame range calibrated on clips A and B with this tool',
      'share of pixels where the 11 px black-hat of the grey frame exceeds 28 levels'),
    # ---- 3. characters ----
    M('h_fill_v', 'characters', 'Head fill value (HSV V)', 0.96, 0.995, 0.02, '%.3f',
      LS + ' 4.1 row 16 (V 0.97-0.995; v1 #ffffff clipped); ' + VM + ' row 7 (fill #fdf8f7); lower bound widened to clip B, whose lamp-lit shots tint the figure',
      'HSV value of the median fill colour, median over detected heads'),
    M('h_fill_s', 'characters', 'Head fill saturation (HSV S)', 0.0, 0.055, 0.15, '%.3f',
      LS + ' 4.1 row 16 (S at most 0.04) widened to this tool\'s clip B median 0.049 (lamp-lit shots tint the whole figure); score 0 at 0.205, just above the strongest per-shot tint of ' + LS + ' 2.4 (S 0.18)',
      'HSV saturation of the median fill colour, median over detected heads'),
    M('h_flat', 'characters', 'Head flatness (luma spread)', 0.0, 0.11, 0.12, '%.3f',
      LS + ' 4.1 row 17 (flat fill, V difference at most 0.07 on the crescent side only; v1 1.00 against 0.62); 2.4 fill #fef7f6 against crescent #e9dceb',
      'luma p95 minus p5 (0..1) over the fill pixels inside 0.9 of the fill radius, ink excluded; median over heads'),
    M('h_ink_de', 'characters', 'Ink colour distance to #3a2832 (dE76)', 0.0, 8.0, 6.0, '%.1f',
      LS + ' 2.4 (ink #3a2832; night shots shift it towards #1e142e); ' + VM + ' row 6 (stroke centre #3d2835, darkest fifth #3a2731); 4.1 row 23 (v1 #272727); upper bound widened to this tool\'s clip B value',
      'CIE76 distance between the median stroke-centre colour of the head outline and #3a2832'),
    M('h_ink_c', 'characters', 'Ink colour strength (Lab chroma)', 6.0, 25.0, 6.0, '%.1f',
      LS + ' 2.4 (ink #3a2832 is a plum, chroma 10.9; night ink #1e142e 19.7) against 4.1 row 23 (v1 #272727, neutral, chroma 0); added in validation because single scenes of clip B carry inks 13 to 18 dE away from #3a2832 (brown-black in lamp light, purple-black at night), as far as the neutral v1 ink, while every reference scene keeps a chroma of 6 to 22',
      'CIE Lab chroma, sqrt(a^2 + b^2), of the median stroke-centre colour of the head outline'),
    M('h_thin', 'characters', 'Head outline, thin side / D', 0.018, 0.035, 0.020, '%.3f',
      VM + ' row 4 (thin side 0.018-0.035 over all heads); ' + LS + ' 2.2 (0.020 left)',
      '10th percentile of the ink width along rays through the outline, as a fraction of the outer head diameter; heads of 110 px or more'),
    M('h_thick', 'characters', 'Head outline, thick side / D', 0.065, 0.083, 0.030, '%.3f',
      VM + ' row 4 (thick side 0.065-0.083; v1 0.018 uniform per ' + LS + ' 4.1 row 23)',
      '90th percentile of the ink width along rays through the outline, as a fraction of D; heads of 110 px or more'),
    M('h_ratio', 'characters', 'Head outline, thick / thin ratio', 1.8, 4.2, 0.9, '%.2f',
      VM + ' row 4 (thin 0.018-0.035 against thick 0.065-0.083; 0.074 / 0.020 for a key from the upper left); ' + LS + ' 2.2 quick head (0.062 / 0.022); 4.1 row 23 (v1 uniform, ratio 1)',
      'thick-side width divided by thin-side width of the same head, median over heads of 110 px or more'),
    M('h_diam', 'characters', 'Main head diameter, median (px)', 115.0, 265.0, 90.0, '%.0f',
      VM + ' row 15 (classes: wide 110-136, medium 155-215, medium-close 230-265, close 300-385; D is a continuum 119-382); range = wide to medium-close, which holds both clip medians',
      'outer diameter D of the largest head in each sampled frame, median over frames; the table also lists the share per shot class'),
    M('h_cy', 'characters', 'Main head centre height (y / H)', 0.23, 0.59, 0.15, '%.3f',
      VM + ' row 15 (head centre y 0.23-0.59 H, corrects ' + LS + ' 5.2 rule 1: 0.35-0.59 H)',
      'y of the centre of the largest head divided by 1280, median over sampled frames'),
    M('h_above', 'characters', 'Heads entirely above y = 880', 0.85, 1.0, 0.40, '%.2f',
      'camera_motion 1.6 (91 percent of heads entirely above the caption top, every centre above it); ' + LS + ' 5.2 rule 1; ' + VM + ' row 15 (clip B balcony shots sit lower)',
      'share of detected heads whose lowest point (centre y + D / 2) is above y = 880'),
    M('h_edge', 'characters', 'Head ink edge softness (px)', 1.0, 3.2, 3.0, '%.2f',
      'added in validation (a blurred picture kept its characters score): no spec number; ' + LS + ' 4.1 row 22 (no grain, no sharpening) and the prototype builder\'s edge check (reference ink edges 1.5 to 1.9 px); range calibrated on clips A and B with this tool (single reference heads read 1.6 to 2.7 px)',
      'distance between the 10 and 90 percent points of the luma fall from head fill to outline ink, along the rays whose ink line is 3 px or wider; median over rays, then over heads of 110 px or more'),
    M('h_limb', 'characters', 'Limb stroke width / D', 0.05, 0.08, 0.030, '%.3f',
      VM + ' row 10 (arms 0.053-0.064, legs 0.051-0.080); ' + LS + ' 2.2 (0.062, allowed 0.055-0.075)',
      'best effort: peak of the stroke-width histogram of dark strokes under the head (0.045-0.105 D), median over heads where it could be measured'),
    # ---- 4. camera and edit ----
    M('m_static', 'camera', 'Static frames, share of in-shot frames', 0.0, 0.08, 0.25, '%.3f',
      LS + ' 5.3 (fully static frames are 4 to 6 percent); camera_motion 1.1 (A 3.8, B 5.5 percent)',
      'share of in-shot frames with zoom rate under 1.5 percent/s and pan under 8 px/s'),
    M('m_hold', 'camera', 'Longest static hold (frames)', 0.0, 15.0, 30.0, '%.0f',
      LS + ' 5.3 (hold 6 to 14 frames); camera_motion 1.1 (longest 0.47 s = 14 frames)',
      'longest run of consecutive static frames'),
    M('m_zoom', 'camera', 'Zoom rate, median |percent/s|', 7.0, 22.0, 7.0, '%.1f',
      'camera_motion 2.1 (all in-shot frames p50: A 20.8, B 9.7 percent/s; drift median 7.6-7.8); ' + LS + ' 5.3 (drift 6 to 10 percent/s)',
      'median absolute zoom rate over in-shot frames, from the frame-to-frame similarity fit of tracked background features'),
    M('m_pan', 'camera', 'Pan, median px/s', 40.0, 150.0, 40.0, '%.0f',
      'camera_motion 2.1 (all in-shot frames p50: A 133, B 57 px/s; drift pan 30-33 px/s); ' + LS + ' 5.3 (drift slide 20 to 60 px/s); upper bound widened to this tool\'s clip A value',
      'median translation of the frame centre over in-shot frames'),
    M('m_interval', 'camera', 'Interval between framing changes (s)', 1.2, 1.7, 2.0, '%.2f',
      LS + ' 5.3 (framing changes every 1.2 to 1.5 s); camera_motion 2.1 (median 1.19 / 1.26 s, mean 1.25 / 1.54 s); upper bound widened to this tool\'s clip B value (hidden cuts and whip pans are not detected)',
      'clip length divided by (transitions + in-shot snap reframings + 1)'),
    M('m_shot_len', 'camera', 'Mean shot length (s)', 2.0, 4.8, 3.0, '%.2f',
      'camera_motion 1.4 (A 16 shots, mean 3.75 s; B 22 shots, mean 2.62 s); ' + LS + ' 5.3 (about 22 shots of 2 to 3.5 s); upper bound widened to this tool\'s clip A value (it finds 14 of the 16 shots: hidden cuts are not detected)',
      'clip length divided by the number of shots (transitions + 1)'),
    M('m_diss_share', 'camera', 'Dissolves, share of transitions', 0.7, 1.0, 0.50, '%.2f',
      LS + ' 5.4 (four of five transitions are cross-dissolves); camera_motion 1.4 (A 11 of 15, B 18 of 21); upper bound widened because wipes, whip pans and hidden cuts are not detected as transitions',
      'detected dissolves divided by all detected transitions'),
    M('m_diss_len', 'camera', 'Dissolve length, median (frames)', 9.0, 16.0, 8.0, '%.1f',
      LS + ' 5.4 (11 frames; 9 quick, 13 to 16 for a change of place); camera_motion 1.4 (A median 13, B 10.5)',
      'length N of the mix, from the 25 and 75 percent crossings of the blend factor: N = (t75 - t25) / 0.275 - 1; median over dissolves'),
    M('m_ease', 'camera', 'Snap easing, peak / mean speed', 1.5, 2.1, 0.5, '%.2f',
      LS + ' 5.3 (sine in-out 1.57; measured 1.56 to 2.09); camera_motion 1.3 (median 1.71; linear = 1.00)',
      'peak corner speed of a snap move divided by its mean, median over snaps'),
    # ---- 5. animation life ----
    M('a_blink', 'animation', 'Blinks per second per head', 0.2, 1.4, 0.2, '%.2f',
      LS + ' 5.5 item 3 (every 0.7 to 1.2 s in close-ups, about every 2 s otherwise); camera_motion 1.7 (A 1.4-1.8 per s, B 0.4 per s); lower bound widened to this tool\'s clip A reading 0.31: the detector finds 3 of 7 known blinks and 5 of its 8 events in clip A are not blinks (VALIDATION.md check 2), so this is a count of blink-like eye events, not the blink rate',
      'dips of the eye ink (at least 25 percent, back after 1 to 5 frames) per second of tracked head (heads of 80 px or more); needs 15 s of tracked heads'),
    M('a_face', 'animation', 'Face-drawing changes per second per head', 1.3, 9.8, 1.3, '%.2f',
      LS + ' 5.5 items 4 and 5 (1 to 3 swaps per second in a reaction; mouth about 7 per second, measured 4.9 to 9.8); camera_motion 1.7',
      'frames in which the eye ink or the mouth ink changes by more than 25 percent, per second of tracked head'),
    M('a_char', 'animation', 'Character moves on its own while camera is steady', 0.30, 1.0, 0.30, '%.2f',
      LS + ' 5.5 items 1 and 2 (bodies move on ones; the speaker moves, the listener freezes); camera_motion 1.7 (0 of 60 frame pairs is a hold). Redefined in validation: the builder\'s version read 1.00 on a still picture under a 2D zoom. Lower bound calibrated on clips A and B with this tool (0.39 and 0.68)',
      'share of steady-camera frames (zoom under 10 percent/s, pan under 60 px/s) in which the picture change inside the character box, after removing the fitted camera move and dividing by the local contrast, is over 1.3 times that of the background (and over 0.8 grey levels); a rigid picture under any 2D camera move reads 0'),
    # ---- 6. captions ----
    M('t_cx', 'captions', 'Caption centre x (px)', 357.0, 362.0, 20.0, '%.1f',
      'captions.md (x = 359-360); ' + VM + ' "other things" (centre x 359.5)',
      'centre of the white text box, median over captions'),
    M('t_cover', 'captions', 'Frames with a caption', 0.90, 1.0, 0.60, '%.2f',
      'captions.md (a caption is on screen throughout; one short phrase at a time); added in validation (covering the captions used to raise the index): this tool finds a caption in 100 percent of clip A frames and 96.5 percent of clip B frames, lowest 5 s window 55 percent',
      'share of frames in which a caption (white text with a black stroke in rows 836 to 976) is found'),
    M('t_cy', 'captions', 'Caption centre y (px)', 899.5, 905.5, 15.0, '%.1f',
      VM + ' "other things" (white-fill centre y 903 median, 899.5 to 905.5); captions.md (text line centred at y = 900; v1 915)',
      'centre of the white text box, median over captions'),
    M('t_fill', 'captions', 'Caption fill, distance from white (levels)', 0.0, 6.0, 40.0, '%.1f',
      'captions.md (fill pure white #FFFFFF)',
      '255 minus the lowest channel of the median fill colour'),
    M('t_stroke', 'captions', 'Caption stroke width (px)', 3.6, 4.4, 1.0, '%.1f',
      'captions.md (black, 4 px each side; v1 5 px); ' + VM + ' "other things" (4 px, mode of 4574 runs). Repaired in validation: the builder counted pixels under luma 80, which takes in the soft halo, read 4.8 on the reference and 5.0 on a hard 5 px outline (no separation) and jumped between 4.2 and 4.8 on parts of one clip; with luma under 40 (solid black) the reference reads 4.0, a hard 5 px outline 4.9',
      'modal length of the solid black runs (luma under 40) that flank the white fill along rows, averaged over the mode and its two neighbours'),
    M('t_cap_h', 'captions', 'Caption text height (px)', 33.0, 40.0, 10.0, '%.1f',
      'captions.md (ascender-height word = 36 px fill, font size 50); ' + VM + ' "other things" (fill height 36 px median in clip A)',
      'height of the white text box, median over captions'),
    M('t_words', 'captions', 'Words per caption (mean)', 1.0, 3.0, 2.0, '%.2f',
      'captions.md (1 to 3 words, one short phrase at a time)',
      'no OCR: number of word-sized gaps in the column profile of the white text mask plus one; mean over captions'),
    M('t_dur', 'captions', 'Caption duration, median (frames)', 6.0, 18.0, 12.0, '%.1f',
      'captions.md (about 0.2 to 0.6 s per phrase, 6 to 18 frames)',
      'frames between two changes of the caption text'),
    M('t_swap', 'captions', 'Captions at full size on their first frame', 0.90, 1.0, 0.50, '%.2f',
      'captions.md (animation: none, hard swap, width constant across every frame of a phrase; v1 used a pop-in scale)',
      'share of captions whose first-frame box is within 4 percent of the settled width and height'),
]
METRIC_BY_KEY = {m['key']: m for m in METRICS}


# ------------------------------------------------------------------------------------------------
# input
# ------------------------------------------------------------------------------------------------
IMG_EXT = ('.png', '.jpg', '.jpeg', '.webp', '.bmp')


class Source:
    def __init__(self, path, first=0, last=None):
        self.path = path
        self.files = None
        self.cap = None
        self.first = max(0, int(first)); self.last = last
        if os.path.isdir(path):
            names = sorted(os.listdir(path))
            fr = [n for n in names if re.match(r'^f_?\d+\.(png|jpe?g)$', n, re.I)]
            if not fr:
                fr = [n for n in names if n.lower().endswith(IMG_EXT)]
            if not fr:
                raise SystemExit('no frames found in ' + path)
            self.files = [os.path.join(path, n) for n in fr]
            self.files = self.files[self.first:(None if self.last is None else self.last + 1)]
            if not self.files:
                raise SystemExit('no frames in the range given by --frames')
            self.kind = 'frames' if len(self.files) > 1 else 'still'
            self.n_est = len(self.files)
        elif path.lower().endswith(IMG_EXT):
            self.files = [path]
            self.kind = 'still'
            self.n_est = 1
        else:
            try:
                self.cap = cv2.VideoCapture(path, cv2.CAP_FFMPEG, [cv2.CAP_PROP_N_THREADS, 2])
            except Exception:
                self.cap = cv2.VideoCapture(path)
            if not self.cap.isOpened():
                raise SystemExit('cannot open ' + path)
            self.kind = 'video'
            self.n_est = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if self.last is not None:
                self.n_est = min(self.n_est, self.last + 1)
            self.n_est = max(1, self.n_est - self.first)
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.fps_in = float(fps) if fps and fps > 0 else FPS

    def __iter__(self):
        if self.files is not None:
            for f in self.files:
                im = cv2.imread(f, cv2.IMREAD_COLOR)
                if im is None:
                    continue
                yield fit_frame(im)
        else:
            k = 0                                   # frames are decoded in order (no seeking): exact frame numbers
            while True:
                if self.last is not None and k > self.last:
                    break
                if k < self.first:
                    if not self.cap.grab():
                        break
                    k += 1
                    continue
                ok, im = self.cap.read()
                if not ok:
                    break
                k += 1
                yield fit_frame(im)


def fit_frame(im):
    if im.shape[0] != H or im.shape[1] != W:
        im = cv2.resize(im, (W, H), interpolation=cv2.INTER_AREA)
    return im


# ------------------------------------------------------------------------------------------------
# picture statistics (groups 1 and 2)
# ------------------------------------------------------------------------------------------------
def picture_stats(bgr, gray):
    keep = np.r_[0:CAP_Y0, CAP_Y1:H]
    f = bgr[keep].astype(np.float32) / 255.0
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    S = hsv[..., 1].ravel(); V = hsv[..., 2].ravel()
    B = f[..., 0].ravel(); G = f[..., 1].ravel(); R = f[..., 2].ravel()
    Y = 0.2126 * R + 0.7152 * G + 0.0722 * B
    p1, p5, p10, p50, p95 = np.percentile(Y, [1, 5, 10, 50, 95])
    rg = (R - G) * 255.0; yb = (0.5 * (R + G) - B) * 255.0
    cf = float(math.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * math.sqrt(rg.mean() ** 2 + yb.mean() ** 2))
    dk = Y <= p10
    out = dict(
        c_sat_mean=float(S.mean()), c_luma_p50=float(p50), c_black=float(p1), c_contrast=float(p95 - p5),
        c_colourful=cf, c_share_s50=float((S > 0.5).mean()), c_share_v95=float((V > 0.95).mean()),
        dark_rgb=[float(R[dk].mean()), float(G[dk].mean()), float(B[dk].mean())],
    )
    # density and light structure
    ed = cv2.Canny(gray, 60, 140)
    out['d_edge'] = float((ed[keep] > 0).mean())
    g = gray.astype(np.float32)
    hp = g - cv2.GaussianBlur(g, (0, 0), 4)
    m1 = cv2.blur(hp, (40, 40)); m2 = cv2.blur(hp * hp, (40, 40))
    sd = np.sqrt(np.maximum(m2 - m1 * m1, 0))[20::40, 20::40]            # one value per 40 px block
    rows = np.arange(20, H, 40)
    okrow = (rows + 20 <= CAP_Y0) | (rows - 20 >= CAP_Y1)
    out['d_featureless'] = float((sd[okrow] < 3.0).mean())
    Yf = HD.luma_of(bgr)
    out['d_luma_top'] = float(Yf[0:427].mean())
    out['d_luma_mid'] = float(Yf[427:CAP_Y0].mean())
    out['d_luma_bot'] = float(Yf[CAP_Y1:H].mean())
    bh = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))
    out['d_thin_lines'] = float((bh[keep] > 28).mean())
    # colour variety (plausibility guard, not a metric): entropy of the colour histogram at 4 bits per channel.
    # Reference frames: median 7.2 to 7.4 bits, 5th percentile 5.7, lowest single frame 3.7; a card of 8 flat colours: at most 3.
    q = (bgr[keep] >> 4).astype(np.int32)
    hc = np.bincount(((q[..., 0] << 8) | (q[..., 1] << 4) | q[..., 2]).ravel(), minlength=4096).astype(np.float64)
    pc = hc[hc > 0] / hc.sum()
    out['colour_entropy'] = float(-(pc * np.log2(pc)).sum())
    return out, Yf


# ------------------------------------------------------------------------------------------------
# captions (group 6)
# ------------------------------------------------------------------------------------------------
CB0, CB1 = 836, 976          # rows analysed for the caption (band plus a margin)
SIG_W, SIG_H = 48, 12
STROKE_LUMA = 40             # a stroke pixel is solid black (the soft halo around the stroke is lighter than this)
TEXT_FILL_MIN, TEXT_FILL_MAX = 0.12, 0.85    # share of the caption box that is white fill; lettering sits between


def caption_measure(bgr, detail=False):
    """White, black-stroked text in the caption band.  Returns None or a dict with the box of the
    white fill (frame coordinates), a scale-free signature of the text, the word estimate and,
    with detail=True, fill colour and stroke runs."""
    band = bgr[CB0:CB1]
    b, g, r = cv2.split(band)
    mn = cv2.min(cv2.min(b, g), r); mx = cv2.max(cv2.max(b, g), r)
    white = cv2.compare(mn, 224, cv2.CMP_GT)
    if cv2.countNonZero(white) < 40:
        return None
    dark = cv2.compare(mx, 95, cv2.CMP_LT)
    n, lab, st, _ = cv2.connectedComponentsWithStats(white, 8)
    if n <= 1 or n > 400:
        return None
    # ring two pixels outside each white component: text is surrounded by its black stroke
    k5 = np.ones((5, 5), np.uint8); k3 = np.ones((3, 3), np.uint8)
    labf = lab.astype(np.float32)
    near = cv2.dilate(labf, k5).astype(np.int32)
    ring = (cv2.dilate(white, k5) > 0) & (cv2.dilate(white, k3) == 0)
    tot = np.bincount(near[ring], minlength=n).astype(np.float64)
    drk = np.bincount(near[ring & (dark > 0)], minlength=n).astype(np.float64)
    ok = np.zeros(n, bool)
    hb = band.shape[0]
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if a < 10 or h < 6 or h > 70 or w > 120:
            continue
        if y <= 1 or y + h >= hb - 1:
            continue
        if tot[i] < 8 or drk[i] / tot[i] < 0.72:
            continue
        ok[i] = True
    if not ok.any():
        return None
    idx = np.nonzero(ok)[0]
    # keep the components on the main text line (the median row of the candidates)
    cyc = st[idx, 1] + st[idx, 3] / 2.0
    med = float(np.median(cyc))
    idx = idx[np.abs(cyc - med) < 34]
    # one phrase: split at horizontal gaps over two text heights and keep the group with the most fill
    order = idx[np.argsort(st[idx, 0])]
    groups = [[order[0]]]
    right = st[order[0], 0] + st[order[0], 2]
    gap_split = max(60.0, 2.0 * float(np.median(st[idx, 3])))
    for i in order[1:]:
        if st[i, 0] - right > gap_split:
            groups.append([i])
        else:
            groups[-1].append(i)
        right = max(right, st[i, 0] + st[i, 2])
    if len(groups) > 1:
        idx = np.array(max(groups, key=lambda gq: sum(int(st[i, 4]) for i in gq)))
    tm = np.isin(lab, idx)
    ys, xs = np.nonzero(tm)
    if len(xs) < 40:
        return None
    x0, x1, y0, y1 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
    bw, bhh = x1 - x0 + 1, y1 - y0 + 1
    if bhh < 12 or bw < 8:
        return None
    crop = tm[y0:y1 + 1, x0:x1 + 1].astype(np.uint8)
    fillr = float(crop.mean())
    if fillr > TEXT_FILL_MAX or fillr < TEXT_FILL_MIN:
        return None                     # a solid white bar or a few specks: not lettering
    sig = cv2.resize(crop * 255, (SIG_W, SIG_H), interpolation=cv2.INTER_AREA).astype(np.float32).ravel() / 255.0
    # words: gaps in the column profile wider than about a third of the lower-case height
    col = crop.max(axis=0)
    gaps = []
    run = 0
    for v in col:
        if v:
            if run:
                gaps.append(run)
            run = 0
        else:
            run += 1
    gap_thr = max(8.0, 0.30 * min(bhh, 40))
    words = 1 + sum(1 for gp in gaps if gp >= gap_thr)
    # share of the marks that are plain filled rectangles (a letter l or i is one; a caption made only of such bars is not text)
    big = [i for i in idx if st[i, 4] >= 20]
    bars = float(np.mean([st[i, 4] >= 0.92 * st[i, 2] * st[i, 3] for i in big])) if big else 0.0
    out = dict(x0=x0, x1=x1, y0=y0 + CB0, y1=y1 + CB0, w=bw, h=bhh, sig=sig, words=words, ncomp=int(len(idx)), fillr=fillr, bars=bars,
               nbig=len(big))
    if detail:
        core = cv2.erode(tm.astype(np.uint8), k3) > 0
        if core.sum() >= 10:
            out['fill_bgr'] = [float(v) for v in np.median(band[core].astype(np.float32), axis=0)]
        # stroke runs: solid black run directly left or right of a white text run, closed by a lighter pixel
        Yb = HD.luma_of(band)
        dk = Yb < STROKE_LUMA
        runs = []
        for yy in range(y0, y1 + 1, 2):
            trow = tm[yy]; drow = dk[yy]
            edges = np.nonzero(trow[1:] != trow[:-1])[0]
            for e in edges:
                if trow[e]:                 # text ends at e: stroke to the right
                    j = e + 1; step = 1
                else:                       # text starts at e + 1: stroke to the left
                    j = e; step = -1
                skip = 0                    # antialiased pixels between fill and stroke
                while 0 <= j < W and not drow[j] and skip < 3:
                    j += step; skip += 1
                ln = 0
                while 0 <= j < W and drow[j] and ln < 14:
                    j += step; ln += 1
                if 0 <= j < W and 1 <= ln <= 12 and not trow[j]:
                    runs.append(ln)
        out['runs'] = runs
    return out


# ------------------------------------------------------------------------------------------------
# camera and edit (group 4)
# ------------------------------------------------------------------------------------------------
_GM_MASK = np.full((LH, LW), 255, np.uint8)
_GM_MASK[int(LH * 0.655):int(LH * 0.76)] = 0


def global_motion(prev, cur):
    """Similarity transform prev -> cur at 360x640 (same procedure as camera-motion/gmotion.py).
    Returns (scale, centre tx, centre ty, 2x3 matrix) or None."""
    p0 = cv2.goodFeaturesToTrack(prev, 600, 0.01, 7, mask=_GM_MASK)
    if p0 is None or len(p0) < 12:
        return None
    p1, st, _ = cv2.calcOpticalFlowPyrLK(prev, cur, p0, None, winSize=(21, 21), maxLevel=3)
    p0b, st2, _ = cv2.calcOpticalFlowPyrLK(cur, prev, p1, None, winSize=(21, 21), maxLevel=3)
    fb = np.linalg.norm((p0 - p0b).reshape(-1, 2), axis=1)
    good = (st.ravel() == 1) & (st2.ravel() == 1) & (fb < 1.0)
    a = p0.reshape(-1, 2)[good]; b = p1.reshape(-1, 2)[good]
    if len(a) < 12:
        return None
    Mx, inl = cv2.estimateAffinePartial2D(a, b, method=cv2.RANSAC, ransacReprojThreshold=1.5, maxIters=2000, confidence=0.995)
    if Mx is None:
        return None
    s = float(math.hypot(Mx[0, 0], Mx[1, 0]))
    c = np.array([LW / 2, LH / 2, 1.0])
    tc = Mx @ c - c[:2]
    return s, float(tc[0]), float(tc[1]), Mx


_SS_MASK = np.full((320, 180), 255, np.uint8)
_SS_MASK[int(320 * 0.655):int(320 * 0.76)] = 0
KQ = 0.275          # (t75 - t25) / (N + 1) of the reference mix curve, calibrated on both clips
TRACK_SHARE_MAX = 0.10   # a dissolve candidate is dropped when more than this share of features tracks across it ...
TRACK_CHANCE_MAX = 20    # ... and more than this many (chance matches between two feature-poor pictures)


def tracked_share(X, Y):
    """Can the picture X (180x320 grey) be followed into Y?  Returns (features in X, features in
    Y, features tracked forward and back within 1 px).  Two frames of the same shot share most
    features; the two sides of a cut or dissolve share almost none."""
    p0 = cv2.goodFeaturesToTrack(X, 400, 0.01, 5, mask=_SS_MASK)
    q0 = cv2.goodFeaturesToTrack(Y, 400, 0.01, 5, mask=_SS_MASK)
    n0 = 0 if p0 is None else len(p0); n1 = 0 if q0 is None else len(q0)
    if n0 < 25 or n1 < 25:
        return n0, n1, -1
    p1, st, _ = cv2.calcOpticalFlowPyrLK(X, Y, p0, None, winSize=(21, 21), maxLevel=3)
    p0b, st2, _ = cv2.calcOpticalFlowPyrLK(Y, X, p1, None, winSize=(21, 21), maxLevel=3)
    fb = np.linalg.norm((p0 - p0b).reshape(-1, 2), axis=1)
    good = (st.ravel() == 1) & (st2.ravel() == 1) & (fb < 1.0)
    return n0, n1, int(good.sum())


def _blend_residual(Tf, lo, hi):
    X = Tf[lo]; Y = Tf[hi]; d = Y - X
    dd = float(d @ d)
    if dd <= 0:
        return 9.0
    F = Tf[lo + 1:hi]
    if len(F) == 0:
        return 0.0
    al = ((F - X) @ d) / dd
    return float((np.abs(F - (X[None, :] + al[:, None] * d[None, :])).mean(axis=1) / max(1e-3, float(np.abs(d).mean()))).max())


def _alpha(C, f, lo, hi):
    d = C[hi] - C[lo]
    dd = float(d @ d)
    return float((C[f] - C[lo]) @ d) / dd if dd > 0 else 0.0


def _crossing(al, level, start=1):
    for i in range(max(1, start), len(al)):
        if al[i] >= level:
            a0, a1 = al[i - 1], al[i]
            return i - 1 + (level - a0) / (a1 - a0) if a1 > a0 else float(i)
    return None


def find_transitions(T180, mad, v):
    """Hard cuts and dissolves.

    T180: frames at 180x320 grey with the caption band blanked; mad[i]: mean absolute difference
    between frame i-1 and i at 360x640; v: corner speed of the fitted camera motion (px/s).
    1. Candidates: windows of 9 and 15 frames whose inner frames are linear blends of the two end
       frames (residual under 0.5 of the end-to-end difference, blend factor monotone).
    2. Each candidate window is grown frame by frame while the next frame still adds blend and
       the window stays blend-like; the length is read from the 25 and 75 percent crossings of
       the blend factor on a 9x16 block-mean picture (N = (t75 - t25) / 0.275 - 1), which is
       insensitive to the slow drift of both shots.
    3. A candidate is kept only if the picture before it cannot be tracked into the picture after
       it (under 10 percent of the features), and it does not sit inside a fast camera move.
    4. A spike of the frame difference (over 18 and over 3 x the neighbours + 4) is a hard cut.
    Returns dicts {a, b, kind, length}; for a cut a = b = first frame of the new shot."""
    n = len(T180)
    if n < 12:
        return []
    Tf = np.stack([cv2.resize(t, (TW, TH), interpolation=cv2.INTER_AREA) for t in T180]).reshape(n, -1).astype(np.float32)
    C = np.stack([cv2.resize(t, (9, 16), interpolation=cv2.INTER_AREA) for t in T180]).reshape(n, -1).astype(np.float32)
    wins = []
    for half in (4, 7):
        if n < 2 * half + 2:
            continue
        base_all = np.abs(Tf[2 * half:] - Tf[:-2 * half]).mean(axis=1)
        for c in np.nonzero(base_all > 20.0)[0] + half:
            X = Tf[c - half]; Y = Tf[c + half]
            d = Y - X
            dd = float(d @ d)
            if dd <= 0:
                continue
            F = Tf[c - half + 1:c + half]
            a = ((F - X) @ d) / dd
            res = float((np.abs(F - (X[None, :] + a[:, None] * d[None, :])).mean(axis=1) / base_all[c - half]).max())
            if res < 0.50 and np.all(np.diff(np.r_[0.0, a, 1.0]) > -0.04):
                wins.append((float(base_all[c - half]) * (0.6 - res), int(c), half, res))
    wins.sort(reverse=True)
    used = np.zeros(n, bool)
    out = []
    for sc, c0, half, res in wins:
        if used[c0 - half:c0 + half + 1].any():
            continue
        lo, hi = c0 - half, c0 + half
        lim = max(0.45, res + 0.10)
        ch = True
        while ch and hi - lo < 44:
            ch = False
            if lo - 1 >= 0 and _alpha(C, lo, lo - 1, hi) >= 0.02 and _blend_residual(Tf, lo - 1, hi) <= lim:
                lo -= 1; ch = True
            if hi + 1 <= n - 1 and 1.0 - _alpha(C, hi, lo, hi + 1) >= 0.02 and _blend_residual(Tf, lo, hi + 1) <= lim:
                hi += 1; ch = True
        used[max(0, lo - 6):hi + 7] = True
        d = C[hi] - C[lo]
        dd = float(d @ d)
        if dd <= 0:
            continue
        al = ((C[lo:hi + 1] - C[lo]) @ d) / dd
        t25 = _crossing(al, 0.25)
        t75 = _crossing(al, 0.75, int(math.floor(t25))) if t25 is not None else None
        if t75 is None:
            continue
        mid = lo + (t25 + t75) / 2.0
        N = max(0.0, (t75 - t25) / KQ - 1.0)
        n0, n1, good = tracked_share(T180[max(0, lo - 1)], T180[min(n - 1, hi + 1)])
        # the two sides of a real transition share almost no trackable features (0 to 3 of 400 on the reference
        # dissolves); two smooth pictures with few features give up to 18 chance matches of 140; the same shot gives
        # 30 to 97 percent, and 17 percent (38 of 220) inside the rotating shot of clip B, which must not pass
        if not (good >= 0 and good < max(TRACK_CHANCE_MAX, TRACK_SHARE_MAX * n0)):
            continue
        vin = float(np.median(v[lo:hi + 1]))
        vb = float(np.median(v[max(0, lo - 4):lo])) if lo > 0 else 0.0
        va = float(np.median(v[hi + 1:hi + 5])) if hi + 1 < n else 0.0
        if vin > 450 and min(vb, va) > 300:
            continue                    # inside a fast camera move: not a transition
        if N < 2.5 or hi - lo - 1 <= 1:
            f = int(math.ceil(mid))
            out.append(dict(a=f, b=f, kind='cut', length=0.0))
        else:
            out.append(dict(a=lo + 1, b=hi - 1, kind='dissolve', length=float(N)))
    for i in range(1, n):
        lo = max(1, i - 8); hi = min(n, i + 9)
        nb = np.r_[mad[lo:i], mad[i + 1:hi]]
        if len(nb) == 0:
            continue
        if mad[i] > 18 and mad[i] > 3.0 * float(np.median(nb)) + 4 and not any(t['a'] - 3 <= i <= t['b'] + 3 for t in out):
            n0, n1, good = tracked_share(T180[max(0, i - 2)], T180[min(n - 1, i + 1)])
            if not (good >= 0 and good > 0.5 * n0):
                out.append(dict(a=i, b=i, kind='cut', length=0.0))
    out.sort(key=lambda t: t['a'])
    return out


def smooth3(x):
    return np.convolve(x, np.ones(3) / 3.0, mode='same')


def motion_series(gm):
    """zoom rate (percent/s), pan (px/s), corner speed (px/s) and validity from the per-frame fits."""
    S = gm[:, 0].copy(); TX = gm[:, 1] * 2.0; TY = gm[:, 2] * 2.0
    valid = np.isfinite(S)
    Sz = np.where(valid, S, 1.0)
    zr = (Sz - 1.0) * FPS * 100.0                      # percent per second
    tv = np.where(valid, np.hypot(TX, TY), 0.0) * FPS  # px per second
    v = smooth3(np.abs(zr) / 100.0 * 734.0 + tv)       # corner speed, px/s
    return zr, tv, v, valid


def camera_analysis(gm, trans, n):
    """gm: array (n, 3) of scale, tx, ty at low-res per frame (nan when the fit failed; row 0 nan).
    Returns per-frame series and the events (snaps, holds)."""
    zr, tv, v, valid = motion_series(gm)
    intr = np.zeros(n, bool)                           # frames inside a transition
    for t in trans:
        intr[max(0, t['a'] - 1):min(n, t['b'] + 2)] = True
    inshot = valid & ~intr
    inshot[0] = False
    # snap moves: corner speed above 450 px/s for 3 frames or more (camera-motion/beats.py)
    snap = (v > 450) & ~intr
    runs = []
    f = 0
    while f < n:
        if snap[f]:
            g = f
            while g + 1 < n and (snap[g + 1] or (g + 2 < n and snap[g + 2])):
                g += 1
            if g - f + 1 >= 3:
                runs.append((f, g))
            f = g + 1
        else:
            f += 1
    insnap = np.zeros(n, bool)
    for a, b in runs:
        insnap[a:b + 1] = True
    # static frames and holds
    static = inshot & (np.abs(zr) < 1.5) & (tv < 8.0)
    holds = []
    f = 0
    while f < n:
        if static[f]:
            g = f
            while g + 1 < n and static[g + 1]:
                g += 1
            holds.append((f, g))
            f = g + 1
        else:
            f += 1
    # easing of snap moves (camera-motion/easing.py)
    ratios = []
    for a0, b0 in runs:
        p = a0 + int(np.argmax(v[a0:b0 + 1]))
        a = p
        while a > 0 and v[a - 1] > 0.12 * v[p] and not intr[a - 1] and v[a - 1] <= v[a] * 1.25:
            a -= 1
        b = p
        while b < n - 1 and v[b + 1] > 0.12 * v[p] and not intr[b + 1] and v[b + 1] <= v[b] * 1.25:
            b += 1
        if b - a < 4:
            continue
        seg = v[a:b + 1]
        ratios.append(float(seg.max() / seg.mean()))
    return dict(zr=zr, tv=tv, v=v, intr=intr, inshot=inshot, snaps=runs, insnap=insnap, static=static,
                holds=holds, ease=ratios, valid=valid)


# ------------------------------------------------------------------------------------------------
# animation life (group 5)
# ------------------------------------------------------------------------------------------------
FC = 48                                    # face crop size
CTX = 96                                   # context crop: square of half-size 1.5 r around the head
_yy, _xx = np.mgrid[0:FC, 0:FC]
_FACE_IN = (((_xx - FC / 2 + 0.5) / (0.40 * FC)) ** 2 + ((_yy - FC / 2 + 0.5) / (0.40 * FC)) ** 2) < 1.0
_EYE = _FACE_IN & (_yy >= int(0.22 * FC)) & (_yy < int(0.64 * FC))
_EYE_ROWS = (int(0.22 * FC), int(0.64 * FC))


def context_crop(Yf, hd):
    """96x96 crop of the square of half-size 1.5 r around the head (kept per frame so that the
    face can be re-cropped later with a geometry smoothed along the track)."""
    r = hd['r_fill']
    s = CTX / (3.0 * r)
    Mx = np.float32([[s, 0, -(hd['cx'] - 1.5 * r) * s], [0, s, -(hd['cy'] - 1.5 * r) * s]])
    return cv2.warpAffine(Yf, Mx, (CTX, CTX), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_REPLICATE).astype(np.uint8)


def face_from_context(ctx, raw, sm):
    """48x48 face crop (square of half-size r around the centre) for the smoothed geometry sm =
    (cx, cy, r), cut out of the context crop that was taken with the raw geometry."""
    cxr, cyr, rr = raw
    cxs, cys, rs = sm
    k = (CTX / 3.0) / rr                       # context pixels per frame pixel
    a = (2.0 * rs / FC) * k
    bx = (cxs - rs - cxr + 1.5 * rr) * k
    by = (cys - rs - cyr + 1.5 * rr) * k
    Mx = np.float32([[a, 0, bx], [0, a, by]])
    return cv2.warpAffine(ctx, Mx, (FC, FC), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE)


def _runmed(x, k):
    n = len(x)
    out = np.empty(n)
    h = k // 2
    for i in range(n):
        out[i] = np.median(x[max(0, i - h):min(n, i + h + 1)])
    return out


def build_tracks(per_frame_heads):
    """Greedy nearest-neighbour linking of head detections through consecutive frames."""
    tracks = []
    active = []
    for fi, hs in enumerate(per_frame_heads):
        used = set()
        nxt = []
        for tr in active:
            last = tr['items'][-1]
            lf, lh = last
            if fi - lf > 2:
                continue
            best = None; bd = 1e9
            for k, h in enumerate(hs):
                if k in used:
                    continue
                d = math.hypot(h['cx'] - lh['cx'], h['cy'] - lh['cy'])
                ratio = h['r_fill'] / lh['r_fill']
                if d < 0.6 * lh['D'] and 0.70 < ratio < 1.43 and d < bd:
                    best = k; bd = d
            if best is not None:
                used.add(best)
                tr['items'].append((fi, hs[best]))
                nxt.append(tr)
            elif fi - lf < 2:
                nxt.append(tr)
        for k, h in enumerate(hs):
            if k not in used:
                tr = dict(items=[(fi, h)])
                tracks.append(tr); nxt.append(tr)
        active = nxt
    return tracks


def _fill_masks(C):
    """Face masks for one run of crops: the pixels that are head fill most of the time, with the
    small ink features inside it (eyes, brows, mouth) filled in and the hat, hair and outline left
    out.  Returns (whole face, eye band) for the inner FC-4 window, or None."""
    medimg = np.median(C, axis=0)
    lf = float(np.percentile(medimg[_FACE_IN], 80))
    bright = (medimg > 0.72 * lf).astype(np.uint8)
    closed = cv2.morphologyEx(bright, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13)))
    # the closing must not bridge into the hat: keep only what is within 6 px of real fill
    near = cv2.dilate(bright, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13)))
    face = (closed > 0) & (near > 0) & _FACE_IN
    face = cv2.erode(face.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    face = face[2:FC - 2, 2:FC - 2]
    if face.sum() < 150:
        return None
    eye = face.copy()
    eye[_EYE_ROWS[1] - 2:] = False
    if eye.sum() < 80:
        return None
    return face, eye


def animation_analysis(tracks):
    """Blinks and face-drawing changes on tracked heads of 80 px or more.

    The face crops are cut with a head geometry smoothed along the track (running median), and
    only the head fill is looked at (hat, hair and outline are masked out per run).  Per frame
    the amount of ink (pixels darker than half the fill luma) is counted in the eye band and in
    the mouth band of the 48 px crop; ink counts do not depend on small shifts of the crop.
    Blink: the eye ink falls by at least 25 percent (and 2.5 x the frame-to-frame noise) below
    the median of the five frames before, and is back within 12 percent after 1 to 5 frames.
    Face-drawing change: the eye ink or the mouth ink changes by more than 25 percent (at least
    6 px and 3 x noise) from one frame to the next."""
    blinks = []; changes = []; seconds = 0.0
    for tr in tracks:
        items = [(f, h) for f, h in tr['items'] if h.get('ctx') is not None and h['D'] >= 80]
        if len(items) < 12:
            continue
        runs = []; cur = [items[0]]
        for it in items[1:]:
            if it[0] == cur[-1][0] + 1:
                cur.append(it)
            else:
                runs.append(cur); cur = [it]
        runs.append(cur)
        for run in runs:
            if len(run) < 12:
                continue
            fr = np.array([f for f, _ in run])
            cx = np.array([h['cx'] for _, h in run]); cy = np.array([h['cy'] for _, h in run]); rr = np.array([h['r_fill'] for _, h in run])
            rs = _runmed(rr, 9)
            # where the radius is an outlier the centre is one too: take the centre from the neighbours
            bad = np.abs(rr - rs) > 0.04 * rs
            cxs = cx.copy(); cys = cy.copy()
            good_idx = np.nonzero(~bad)[0]
            if len(good_idx) >= 2:
                cxs = np.interp(np.arange(len(cx)), good_idx, cx[good_idx])
                cys = np.interp(np.arange(len(cy)), good_idx, cy[good_idx])
            cxs = _runmed(cxs, 3); cys = _runmed(cys, 3)
            C = np.stack([face_from_context(h['ctx'], (cx[i], cy[i], rr[i]), (cxs[i], cys[i], rs[i])) for i, (_, h) in enumerate(run)]).astype(np.float32)
            m = len(run)
            masks = _fill_masks(C)
            if masks is None:
                continue
            mface, meye = masks
            mmouth = mface & ~meye
            lf = float(np.percentile(np.median(C, axis=0)[_FACE_IN], 80))
            dark = C[:, 2:FC - 2, 2:FC - 2] < 0.5 * lf
            eye = dark[:, meye].sum(axis=1).astype(np.float64)
            mouth = dark[:, mmouth].sum(axis=1).astype(np.float64) if mmouth.sum() >= 40 else np.zeros(m)
            seconds += m / FPS
            se = float(np.median(np.abs(np.diff(eye)))); sm_ = float(np.median(np.abs(np.diff(mouth))))
            for i in range(1, m):
                ce = abs(eye[i] - eye[i - 1]) > max(0.25 * max(eye[i], eye[i - 1]), 6.0, 3.0 * se)
                cm = abs(mouth[i] - mouth[i - 1]) > max(0.25 * max(mouth[i], mouth[i - 1]), 6.0, 3.0 * sm_)
                if ce or cm:
                    changes.append(int(fr[i]))
            i = 3
            while i < m - 1:
                prev = eye[max(0, i - 5):i]
                bl = float(np.median(prev))
                if bl >= 8 and (prev.max() - prev.min()) <= 0.35 * bl and eye[i] < bl - max(0.25 * bl, 2.5 * se):
                    found = None
                    for L in range(1, 6):
                        if i + L >= m:
                            break
                        if eye[i + L] >= 0.88 * bl:
                            found = L
                            break
                    if found is not None:
                        blinks.append(int(fr[i]))
                        i += found + 1
                        continue
                i += 1
    return dict(blinks=blinks, changes=changes, seconds=seconds)


# ------------------------------------------------------------------------------------------------
# scoring
# ------------------------------------------------------------------------------------------------
_REF_WIN = None


def piece_ranges(kind, seconds):
    """Ranges for short inputs.  The ranges of the metric table hold for a whole film; one scene can sit outside them
    without being wrong (a lamp-lit scene tints the figures, a close-up scene has large heads, one shot can be a fast
    move).  ref_windows.json holds, per metric, the 10th and 90th percentile over the non-overlapping 5, 10 and 20 s
    pieces of the two reference clips; for an input of that length the range of a characters, camera, animation or
    captions metric is widened to include them.  Colour and density keep their ranges: LOOK_SPEC 4.1 and 3.5 state
    them as targets for single interior frames, and widening them to the reference's sky and desert scenes let the
    pale v1 stills pass (tried in validation: v1 still 0.52 became 0.76).
    Returns (dict key -> (p10, p90), text) or ({}, None)."""
    global _REF_WIN
    if _REF_WIN is None:
        p = os.path.join(HERE, 'ref_windows.json')
        try:
            _REF_WIN = json.load(open(p)) if os.path.exists(p) else {}
        except Exception:
            _REF_WIN = {}
    if kind == 'still':
        return _REF_WIN.get('5', {}), '5 s pieces of the reference'
    if seconds < 7.5:
        return _REF_WIN.get('5', {}), '5 s pieces of the reference'
    if seconds < 15.0:
        return _REF_WIN.get('10', {}), '10 s pieces of the reference'
    if seconds < 30.0:
        return _REF_WIN.get('20', {}), '20 s pieces of the reference'
    return {}, None


def score_value(m, v):
    if v is None or not np.isfinite(v):
        return None
    lo, hi, tol = m['lo'], m['hi'], m['tol']
    if m['circ']:
        v = v % 360.0
        if lo <= v <= hi:
            return 1.0
        d = min((lo - v) % 360.0, (v - hi) % 360.0)
    else:
        if lo <= v <= hi:
            return 1.0
        d = lo - v if v < lo else v - hi
    return float(max(0.0, 1.0 - d / tol))


def verdict(s):
    if s is None:
        return 'not measured'
    if s >= 0.999:
        return 'in range'
    if s >= 0.5:
        return 'near'
    if s > 0:
        return 'off'
    return 'far off'


def hexrgb(bgr):
    return '#%02x%02x%02x' % (int(round(bgr[2])), int(round(bgr[1])), int(round(bgr[0])))


def lab_of_bgr(bgr):
    a = np.array([[bgr]], np.float32) / 255.0
    return cv2.cvtColor(a, cv2.COLOR_BGR2Lab)[0, 0]


INK_REF_BGR = (0x32, 0x28, 0x3a)       # #3a2832


def med(x):
    x = [v for v in x if v is not None and np.isfinite(v)]
    return float(np.median(x)) if x else None


# ------------------------------------------------------------------------------------------------
# main analysis
# ------------------------------------------------------------------------------------------------
# Minimum amounts of material below which a metric is reported as "not measured" instead of scored
# (VALIDATION.md check 6: what pieces of the reference clips themselves score at 5, 10 and 20 s).
MIN_S_INTERVAL = 8.0         # s of video for the interval between framing changes
MIN_S_SHOT_LEN = 15.0        # s of video for the mean shot length
MIN_TRANSITIONS = 4          # transitions for the dissolve share
MIN_DISSOLVES = 2            # dissolves for the dissolve length
MIN_SNAPS = 3                # snap moves for the easing ratio
MIN_INSHOT = 30              # in-shot frames for static share, hold, zoom and pan
MIN_S_BLINK = 15.0           # s of tracked heads for the blink-like event rate
MIN_S_FACE = 3.0             # s of tracked heads for the face-change rate
MIN_STEADY = 30              # steady-camera frames with a character for a_char
MIN_CAPTIONS = 5             # captions for duration and hard-swap
MIN_STROKE_RUNS = 200        # stroke runs for the caption stroke width
MIN_HEAD_FRAMES = 3          # sampled frames with a head (video) before the characters group is scored
MIN_OUTLINE_HEADS = 2        # heads with a measurable outline (video) for the outline metrics
FLAT_CARD_BITS = 3.5         # colour entropy below which the input is treated as a flat colour card
CHAR_RATIO = 1.3             # a_char: contrast-normalised change in the character box against the background
CHAR_FLOOR = 0.8             # a_char: and at least this many grey levels of mean change
CHAR_EPS = 0.15              # a_char: background change added before dividing (codec noise of a locked-off picture)


def analyse(path, label, log=print, first=0, last=None, no_captions=False):
    t0 = time.time()
    src = Source(path, first, last)
    kind = src.kind
    n_est = src.n_est
    if kind == 'still':
        step, off = 1, 0
    elif n_est > 300:
        step, off = 15, 6            # the half-second stills are frames 30 x SS.S + 6
    else:
        step, off = 5, 2
    n_samp_est = max(1, (n_est - off + step - 1) // step)
    rep_every = max(1, int(math.ceil(n_samp_est / 16.0)))

    pstats = []                 # picture statistics of sampled frames
    sample_idx = []
    heads_pf = []               # heads per frame (video / frames) or per sampled frame (still)
    sampled_heads = []          # (frame, head) of sampled frames, with limb measurement
    thumbs = []                 # (frame, thumbnail with overlays)
    head_crops = []             # (frame, D, tile)
    cap_pf = []                 # per frame caption record or None
    cap_thumbs = []
    cap_runs = []; cap_fill = []
    gm_rows = []; mad = []; tiny = []
    chardiff = []               # (per head (head, change, contrast), background change, background contrast) or None
    prev_low = None; prev_sig = None; prev_lowb = None
    video = kind != 'still'
    n = 0
    for bgr in src:
        i = n
        n += 1
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        sampled = (i % step == off % step) if video else True
        Yf = None
        if sampled:
            ps, Yf = picture_stats(bgr, gray)
            pstats.append(ps); sample_idx.append(i)
        if Yf is None:
            Yf = HD.luma_of(bgr)
        hs = HD.detect_heads(bgr, Y=Yf, want_limbs=sampled)     # fixed seed per frame: identical frames give identical fits
        if video:
            for h in hs:
                h['ctx'] = context_crop(Yf, h) if h['D'] >= 80 else None
        # captions
        cm = caption_measure(bgr, detail=(i % 3 == 0) or not video)
        if cm is not None:
            same = False
            if prev_sig is not None:
                a = cm['sig'] - cm['sig'].mean(); b = prev_sig - prev_sig.mean()
                den = float(np.linalg.norm(a) * np.linalg.norm(b))
                same = den > 0 and float(a @ b) / den > 0.60
            cm['same'] = same
            prev_sig = cm['sig']
            if 'runs' in cm:
                cap_runs.extend(cm.pop('runs'))
            if 'fill_bgr' in cm:
                cap_fill.append(cm['fill_bgr'])
            if (not same) and len(cap_thumbs) < 400:
                x0 = max(0, cm['x0'] - 30); x1 = min(W, cm['x1'] + 30)
                tile = bgr[CB0 + 4:CB1 - 4, :].copy()
                cv2.rectangle(tile, (cm['x0'], cm['y0'] - CB0 - 4), (cm['x1'], cm['y1'] - CB0 - 4), (255, 0, 255), 1)
                cap_thumbs.append((i, cm['words'], cv2.resize(tile, (360, 66), interpolation=cv2.INTER_AREA)))
        else:
            prev_sig = None
        cap_pf.append(None if cm is None else dict(x0=cm['x0'], x1=cm['x1'], y0=cm['y0'], y1=cm['y1'], w=cm['w'], h=cm['h'],
                                                    words=cm['words'], same=cm['same'], fillr=cm['fillr'], bars=cm['bars'], nbig=cm['nbig']))
        # camera
        if video:
            low = cv2.resize(gray, (LW, LH), interpolation=cv2.INTER_AREA)
            lowb = cv2.GaussianBlur(low.astype(np.float32), (0, 0), 1.0)
            lowm = low.copy(); lowm[int(LH * 0.655):int(LH * 0.76)] = 0
            tiny.append(cv2.resize(lowm, (180, 320), interpolation=cv2.INTER_AREA))
            if prev_low is None:
                gm_rows.append((np.nan, np.nan, np.nan)); mad.append(0.0); chardiff.append(None)
            else:
                mad.append(float(cv2.absdiff(lowm, prev_lowm).mean()))
                res = global_motion(prev_low, low)
                if res is None:
                    gm_rows.append((np.nan, np.nan, np.nan)); chardiff.append(None)
                else:
                    s, tx, ty, Mx = res
                    gm_rows.append((s, tx, ty))
                    cd = None
                    if hs:
                        # change left after the fitted camera move, and the local contrast it has to be judged against:
                        # a rigid picture under a 2D move leaves a change proportional to contrast everywhere
                        wp = cv2.warpAffine(prev_lowb, Mx, (LW, LH), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
                        R = cv2.absdiff(lowb, wp)
                        Gc = (np.abs(cv2.Sobel(lowb, cv2.CV_32F, 1, 0, ksize=3)) + np.abs(cv2.Sobel(lowb, cv2.CV_32F, 0, 1, ksize=3))) / 8.0
                        okm = np.ones((LH, LW), bool)
                        okm[:6] = False; okm[-6:] = False; okm[:, :6] = False; okm[:, -6:] = False
                        okm[int(LH * 0.655):int(LH * 0.76)] = False
                        reg = np.zeros((LH, LW), bool)
                        per = []
                        for h in hs:
                            if h['D'] < 80:
                                continue
                            xa = int(max(6, (h['cx'] - 0.9 * h['D']) / 2)); xb = int(min(LW - 6, (h['cx'] + 0.9 * h['D']) / 2))
                            ya = int(max(6, (h['cy'] - 0.75 * h['D']) / 2)); yb = int(min(LH - 6, (h['cy'] + 2.6 * h['D']) / 2))
                            if xb > xa and yb > ya:
                                mm = okm[ya:yb, xa:xb]
                                if mm.sum() > 400:
                                    per.append((h, float(R[ya:yb, xa:xb][mm].mean()), float(Gc[ya:yb, xa:xb][mm].mean())))
                                reg[ya:yb, xa:xb] = True
                        bgm = okm & ~reg
                        if per and bgm.sum() > 2000:
                            cd = (per, float(R[bgm].mean()), float(Gc[bgm].mean()))
                    chardiff.append(cd)
            prev_low = low; prev_lowm = lowm; prev_lowb = lowb
        # report material (overlays are drawn after the head tracks have been checked)
        if sampled:
            for h in hs:
                sampled_heads.append((i, h))
            si = len(sample_idx) - 1
            if si % rep_every == 0 and len(thumbs) < 20:
                thumbs.append((i, cv2.resize(bgr, (360, 640), interpolation=cv2.INTER_AREA), hs, cm))
            for h in hs:
                if len(head_crops) < 300:
                    head_crops.append((i, h, head_tile(bgr, h, 'f%d' % i)))
        for h in hs:
            h.pop('_rays', None)
        heads_pf.append(hs)
    if n == 0:
        raise SystemExit('no frames could be read from ' + path)
    if n == 1:
        kind = 'still'; video = False
    log('  read %d frames in %.1f s' % (n, time.time() - t0))

    values = {}
    info = {}
    notes = []
    gates = {}                  # metric key -> reason why the value is shown but not scored

    def gate(key, ok, reason):
        if key in values and values[key] is not None and not ok:
            gates[key] = reason
    if src.cap is not None and abs(getattr(src, 'fps_in', FPS) - FPS) > 0.5:
        notes.append('The file reports %.2f frames per second; every time value here assumes 30.' % src.fps_in)
    # ---------------- which pale round blobs are heads ----------------
    # A blob counts as a head when it shows a pair of eyes.  In a video the test is made per track:
    # the track is kept when the eyes are seen in at least a quarter of its frames (and twice), so
    # a head stays a head while it blinks, and a wall clock never becomes one.
    raw_detections = int(sum(len(hs) for hs in heads_pf))
    tracks = []
    if video:
        tracks = build_tracks(heads_pf)
        for tr in tracks:
            ne = sum(1 for _, h in tr['items'] if h.get('eyes'))
            ok = ne >= max(2, int(math.ceil(0.25 * len(tr['items'])))) if len(tr['items']) > 1 else ne >= 1
            for _, h in tr['items']:
                h['ok'] = ok
        tracks = [tr for tr in tracks if tr['items'][0][1]['ok']]
    else:
        for hs in heads_pf:
            for h in hs:
                h['ok'] = bool(h.get('eyes'))
    heads_pf = [[h for h in hs if h.get('ok')] for hs in heads_pf]
    sampled_heads = [(fi, h) for fi, h in sampled_heads if h.get('ok')]
    info['round_pale_blobs_rejected_as_not_heads'] = raw_detections - int(sum(len(hs) for hs in heads_pf))
    # ---------------- groups 1 and 2 ----------------
    for k in ('c_sat_mean', 'c_luma_p50', 'c_black', 'c_contrast', 'c_colourful', 'c_share_s50', 'c_share_v95',
              'd_edge', 'd_featureless', 'd_luma_top', 'd_luma_mid', 'd_luma_bot', 'd_thin_lines'):
        values[k] = med([p[k] for p in pstats])
    spread = {}
    if len(pstats) >= 5:
        for k in ('c_sat_mean', 'c_luma_p50', 'c_black', 'c_contrast', 'c_colourful', 'c_share_s50', 'c_share_v95',
                  'd_edge', 'd_featureless', 'd_luma_top', 'd_luma_mid', 'd_luma_bot', 'd_thin_lines'):
            vals = np.array([p[k] for p in pstats])
            spread[k] = [float(np.percentile(vals, 10)), float(np.percentile(vals, 90))]
    dr = np.mean(np.array([p['dark_rgb'] for p in pstats]), axis=0)
    hh_, ss_, vv_ = colorsys.rgb_to_hsv(*[float(x) for x in dr])
    values['c_dark_hue'] = hh_ * 360.0
    values['c_dark_sat'] = float(ss_)
    info['dark_tenth_hex'] = '#%02x%02x%02x' % tuple(int(round(x * 255)) for x in dr)
    info['colour_entropy_bits_median'] = med([p['colour_entropy'] for p in pstats])
    flat_card = info['colour_entropy_bits_median'] is not None and info['colour_entropy_bits_median'] < FLAT_CARD_BITS
    info['sampled_frames'] = len(pstats)

    # ---------------- group 3: characters ----------------
    all_heads = [(fi, h) for fi, hs in enumerate(heads_pf) for h in hs]
    info['heads_found_all_frames'] = len(all_heads)
    info['frames_with_heads'] = int(sum(1 for hs in heads_pf if hs))
    info['heads_in_sampled_frames'] = len(sampled_heads)
    meas = [h for _, h in sampled_heads]
    outl = [h for h in meas if h['outline_ok'] and h['D'] >= 110]
    info['heads_with_outline'] = len(outl)
    info['sampled_frames_with_heads'] = len(set(fi for fi, _ in sampled_heads))
    if meas:
        fill = np.median(np.array([h['fill_bgr'] for h in meas]), axis=0)
        info['head_fill_hex'] = hexrgb(fill)
        values['h_fill_v'] = float(fill.max() / 255.0)
        values['h_fill_s'] = float((fill.max() - fill.min()) / max(1.0, fill.max()))
        values['h_flat'] = med([h['flat'] for h in meas])
        main = {}
        for fi, h in sampled_heads:
            if fi not in main or h['D'] > main[fi]['D']:
                main[fi] = h
        ds = [h['D'] for h in main.values()]
        values['h_diam'] = med(ds)
        values['h_cy'] = med([h['cy'] / H for h in main.values()])
        values['h_above'] = float(np.mean([(h['cy'] + h['D'] / 2.0) < 880 for h in meas]))
        cls = dict(establishing=0, wide=0, medium=0, medium_close=0, close=0, extreme_close=0, between=0)
        for d in ds:
            if d < 95:
                cls['establishing'] += 1
            elif d <= 136:
                cls['wide'] += 1
            elif 155 <= d <= 215:
                cls['medium'] += 1
            elif 230 <= d <= 265:
                cls['medium_close'] += 1
            elif 300 <= d <= 385:
                cls['close'] += 1
            elif d > 385:
                cls['extreme_close'] += 1
            else:
                cls['between'] += 1
        info['head_diameter_classes'] = {k: round(v / max(1, len(ds)), 3) for k, v in cls.items()}
        info['head_diameter_p10_p90'] = [float(np.percentile(ds, 10)), float(np.percentile(ds, 90))]
        lim = [h['limb'] for h in meas if np.isfinite(h.get('limb', float('nan')))]
        info['limb_measurements'] = len(lim)
        if len(lim) >= 3 or (not video and len(lim) >= 1):
            values['h_limb'] = med(lim)
    if outl:
        values['h_thin'] = med([h['thin'] for h in outl])
        values['h_thick'] = med([h['thick'] for h in outl])
        values['h_ratio'] = med([h['thick'] / h['thin'] for h in outl if h['thin'] > 0])
        values['h_edge'] = med([h.get('edge_px') for h in outl])
        few = 'needs %d heads with a measurable outline (found %d)' % (MIN_OUTLINE_HEADS, len(outl))
        for k in ('h_thin', 'h_thick', 'h_ratio', 'h_edge', 'h_ink_de'):
            gate(k, (not video) or len(outl) >= MIN_OUTLINE_HEADS, few)
        inks = [h['ink_bgr'] for h in outl if h['ink_bgr'] is not None]
        if inks:
            ink = np.median(np.array(inks), axis=0)
            info['ink_hex'] = hexrgb(ink)
            values['h_ink_de'] = float(np.linalg.norm(lab_of_bgr(ink) - lab_of_bgr(INK_REF_BGR)))
            lab_ink = lab_of_bgr(ink)
            values['h_ink_c'] = float(math.hypot(float(lab_ink[1]), float(lab_ink[2])))
            gate('h_ink_de', (not video) or len(outl) >= MIN_OUTLINE_HEADS, few)
            gate('h_ink_c', (not video) or len(outl) >= MIN_OUTLINE_HEADS, few)
        info['thick_side_angle_median'] = med([h['thick_angle'] for h in outl])

    # ---------------- group 6: captions ----------------
    segs = []
    cur = None
    for i, c in enumerate(cap_pf):
        if c is None:
            cur = None
            continue
        if cur is not None and c['same'] and cur['frames'][-1] == i - 1:
            cur['frames'].append(i); cur['recs'].append(c)
        else:
            cur = dict(frames=[i], recs=[c])
            segs.append(cur)
    # drop one-frame flickers that are not real captions (need 2 frames in a video)
    if video:
        segs = [s for s in segs if len(s['frames']) >= 2]
    info['captions_found'] = len(segs)
    info['frames_with_caption'] = int(sum(len(s['frames']) for s in segs))
    values['t_cover'] = info['frames_with_caption'] / float(n)
    bar_caps = False
    if segs:
        # plausibility: captions whose marks are all plain bars (3 or more of them) are not lettering
        allbars = [float(np.median([q['bars'] for q in s['recs']])) >= 0.999 and float(np.median([q['nbig'] for q in s['recs']])) >= 3 for s in segs]
        info['captions_made_of_plain_bars'] = float(np.mean(allbars))
        bar_caps = info['captions_made_of_plain_bars'] > 0.5
        info['caption_fill_share_p5_p95'] = [float(np.percentile([q['fillr'] for s in segs for q in s['recs']], 5)),
                                             float(np.percentile([q['fillr'] for s in segs for q in s['recs']], 95))]
        cxs = []; cys = []; hts = []; wds = []; durs = []; swaps = []; widths = []
        for k, s in enumerate(segs):
            r = s['recs']
            late = r[min(3, len(r) - 1):] if len(r) > 3 else r
            wmed = float(np.median([q['w'] for q in late])); hmed = float(np.median([q['h'] for q in late]))
            cxs.append(float(np.median([(q['x0'] + q['x1']) / 2.0 for q in late])))
            cys.append(float(np.median([(q['y0'] + q['y1']) / 2.0 for q in late])))
            hts.append(hmed); widths.append(wmed)
            wds.append(float(np.median([q['words'] for q in late])))
            inner = s['frames'][0] > 0 and s['frames'][-1] < n - 1
            if video and inner:
                durs.append(len(s['frames']))
            if video and len(r) >= 4:
                swaps.append(abs(r[0]['w'] / wmed - 1.0) <= 0.04 and abs(r[0]['h'] / hmed - 1.0) <= 0.04)
        values['t_cx'] = med(cxs); values['t_cy'] = med(cys); values['t_cap_h'] = med(hts)
        values['t_words'] = float(np.mean(wds))
        info['caption_width_median_px'] = med(widths)
        info['caption_words_max'] = float(max(wds))
        if cap_fill:
            fb = np.median(np.array(cap_fill), axis=0)
            info['caption_fill_hex'] = hexrgb(fb)
            values['t_fill'] = float(255.0 - fb.min())
        if len(cap_runs) >= 30:
            hist = np.bincount(np.array(cap_runs, int), minlength=14)[:14].astype(float)
            pk = int(np.argmax(hist[1:])) + 1
            lo_, hi_ = max(1, pk - 1), min(13, pk + 1)
            values['t_stroke'] = float(sum(k * hist[k] for k in range(lo_, hi_ + 1)) / hist[lo_:hi_ + 1].sum())
        if video and len(durs) >= 2:
            values['t_dur'] = med(durs)
        if video and len(swaps) >= 2:
            values['t_swap'] = float(np.mean(swaps))
        gate('t_dur', len(durs) >= MIN_CAPTIONS, 'needs %d captions that start and end inside the clip (found %d)' % (MIN_CAPTIONS, len(durs)))
        gate('t_swap', len(swaps) >= MIN_CAPTIONS, 'needs %d captions of 4 frames or more (found %d)' % (MIN_CAPTIONS, len(swaps)))
        gate('t_stroke', len(cap_runs) >= MIN_STROKE_RUNS, 'needs %d stroke runs (found %d)' % (MIN_STROKE_RUNS, len(cap_runs)))

    # ---------------- groups 4 and 5 ----------------
    cam = None; trans = []; anim = None
    if video and n >= 20:
        gm = np.array(gm_rows, np.float64)
        madv = np.array(mad)
        trans = find_transitions(tiny, madv, motion_series(gm)[2])
        cam = camera_analysis(gm, trans, n)
        dur = n / FPS
        inshot = cam['inshot']
        info['frames'] = n
        info['duration_s'] = dur
        info['motion_fit_failed_frames'] = int((~cam['valid'][1:]).sum())
        cuts = [t for t in trans if t['kind'] == 'cut']; diss = [t for t in trans if t['kind'] == 'dissolve']
        info['shots'] = len(trans) + 1
        info['hard_cuts'] = len(cuts); info['dissolves'] = len(diss)
        info['snap_reframings'] = len(cam['snaps'])
        info['snap_duration_median_frames'] = med([b - a + 1 for a, b in cam['snaps']])
        if inshot.sum() >= MIN_INSHOT:
            values['m_static'] = float(cam['static'].sum() / inshot.sum())
            values['m_hold'] = float(max([b - a + 1 for a, b in cam['holds']], default=0))
            values['m_zoom'] = float(np.median(np.abs(cam['zr'][inshot])))
            values['m_pan'] = float(np.median(cam['tv'][inshot]))
            info['zoom_rate_p90'] = float(np.percentile(np.abs(cam['zr'][inshot]), 90))
            info['pan_p90'] = float(np.percentile(cam['tv'][inshot], 90))
            info['static_holds_6plus'] = [(int(a), int(b)) for a, b in cam['holds'] if b - a + 1 >= 6]
        nchg = len(trans) + len(cam['snaps'])
        values['m_interval'] = dur / (nchg + 1)
        values['m_shot_len'] = dur / (len(trans) + 1)
        if len(trans) >= 1:
            values['m_diss_share'] = len(diss) / float(len(trans))
        if diss:
            values['m_diss_len'] = med([t['length'] for t in diss])
        if cam['ease']:
            values['m_ease'] = med(cam['ease'])
        if nchg == 0:
            notes.append('No transition and no snap reframing was found: the interval between framing changes and the shot length are the clip length (%.1f s), a lower bound.' % dur)
        gate('m_interval', dur >= MIN_S_INTERVAL, 'needs %.0f s of video (clip is %.1f s)' % (MIN_S_INTERVAL, dur))
        gate('m_shot_len', dur >= MIN_S_SHOT_LEN, 'needs %.0f s of video (clip is %.1f s)' % (MIN_S_SHOT_LEN, dur))
        gate('m_diss_share', len(trans) >= MIN_TRANSITIONS, 'needs %d transitions (found %d)' % (MIN_TRANSITIONS, len(trans)))
        gate('m_diss_len', len(diss) >= MIN_DISSOLVES, 'needs %d dissolves (found %d)' % (MIN_DISSOLVES, len(diss)))
        gate('m_ease', len(cam['ease']) >= MIN_SNAPS, 'needs %d snap moves (found %d)' % (MIN_SNAPS, len(cam['ease'])))
        # animation
        anim = animation_analysis(tracks)
        info['tracked_head_seconds'] = anim['seconds']
        info['blinks'] = len(anim['blinks']); info['face_changes'] = len(anim['changes'])
        if anim['seconds'] >= 1.0:
            values['a_blink'] = len(anim['blinks']) / anim['seconds']
            values['a_face'] = len(anim['changes']) / anim['seconds']
        gate('a_blink', anim['seconds'] >= MIN_S_BLINK, 'needs %.0f s of tracked heads (found %.1f s)' % (MIN_S_BLINK, anim['seconds']))
        gate('a_face', anim['seconds'] >= MIN_S_FACE, 'needs %.0f s of tracked heads (found %.1f s)' % (MIN_S_FACE, anim['seconds']))
        # character moving on its own: the change in the character box, after the fitted camera move has been taken
        # out, is compared with the change in the background, each divided by its local contrast.  A rigid picture
        # under a 2D move gives a ratio of 1 (measured 0.8 to 1.05 on a synthetic zoom and pan), a frozen picture gives
        # no change at all, a character that moves or changes its drawing gives a ratio well above 1.
        steady = inshot & (np.abs(cam['zr']) < 10.0) & (cam['tv'] < 60.0)
        cds = []; cq = []
        for i in range(n):
            if steady[i] and chardiff[i] is not None:
                per, bg_r, bg_g = chardiff[i]
                own = None; qbest = None
                for h, r_, g_ in per:
                    if not h.get('ok'):
                        continue
                    q_ = (r_ / max(g_, 1e-3)) / ((bg_r + CHAR_EPS) / max(bg_g, 1e-3))
                    o_ = (r_ > CHAR_FLOOR) and (q_ > CHAR_RATIO)
                    own = o_ if own is None else (own or o_)
                    qbest = q_ if qbest is None else max(qbest, q_)
                if own is not None:
                    cds.append(own); cq.append((i, qbest))
        info['steady_frames_with_character'] = len(cds)
        if len(cds) >= 10:
            values['a_char'] = float(np.mean(cds))
            info['character_change_ratio_p10_p50_p90'] = [float(v) for v in np.percentile([q for _, q in cq], [10, 50, 90])]
        gate('a_char', len(cds) >= MIN_STEADY, 'needs %d steady-camera frames with a tracked head (found %d)' % (MIN_STEADY, len(cds)))

    # ---------------- scores ----------------
    if no_captions:
        for k in [m['key'] for m in METRICS if m['group'] == 'captions']:
            if values.get(k) is not None:
                gates[k] = 'captions left out on request (--no-captions)'
    rows = []
    pr, pr_text = piece_ranges(kind, n / FPS)
    n_wide = 0
    for m in METRICS:
        v = values.get(m['key'])
        lo, hi = m['lo'], m['hi']
        wide = False
        if m['key'] in pr and not m['circ'] and m['group'] not in ('colour', 'density'):
            a_, b_ = pr[m['key']]
            if a_ < lo:
                lo = float(a_); wide = True
            if b_ > hi:
                hi = float(b_); wide = True
        s = score_value(dict(m, lo=lo, hi=hi), v) if v is not None else None
        why_m = gates.get(m['key'])
        if why_m is not None:
            s = None
        n_wide += int(wide)
        rows.append(dict(key=m['key'], group=m['group'], label=m['label'], value=v, lo=lo, hi=hi, tol=m['tol'],
                         film_lo=m['lo'], film_hi=m['hi'], piece_range=wide,
                         score=s, verdict=verdict(s), why=why_m, source=m['src'], fmt=m['fmt'], circ=m['circ']))
    if n_wide:
        notes.append('Short input: %d ranges of the characters, camera, animation and captions groups were widened from the whole-film range to the 10th to 90th percentile of %s (marked "piece range" in the tables). Colour and density keep the spec targets, which are meant for interior frames: an exterior or night scene can score low there without being wrong (5 s pieces of the reference score 0.67 to 1.00 on colour and 0.50 to 1.00 on density).' % (n_wide, pr_text))
    if video and n / FPS < 30.0:
        notes.append('Scores of short clips scatter. With whole-film ranges, pieces of the reference clips themselves scored: 5 s pieces index 0.81 to 0.96 (median 0.91), 10 s pieces 0.91 to 0.98 (0.95), 20 s pieces 0.93 to 1.00 (0.97); see VALIDATION.md check 6. Differences smaller than that between two short clips mean nothing.')
    nheads = len(meas)
    head_frames = info.get('sampled_frames_with_heads', 0)
    too_few_heads = video and 0 < head_frames < MIN_HEAD_FRAMES
    groups = {}
    for gk, gl, gw in GROUPS:
        sc = [r['score'] for r in rows if r['group'] == gk and r['score'] is not None]
        why = None; applicable = True; forced = None
        if gk == 'characters' and nheads == 0:
            sc = []; why = 'no head was detected'
        if gk == 'characters' and too_few_heads:
            sc = []; why = 'a head was found in only %d sampled frame%s (%d needed)' % (head_frames, '' if head_frames == 1 else 's', MIN_HEAD_FRAMES)
        if gk in ('camera', 'animation') and not video:
            sc = []; why = 'needs a video or a frame folder'; applicable = False
        if gk == 'animation' and video and not sc:
            why = 'not enough tracked head time or steady-camera frames'
        if gk == 'captions' and no_captions:
            sc = []; why = 'left out on request (--no-captions)'; applicable = False
        elif gk == 'captions' and values.get('t_cover', 0) == 0:
            why = 'no caption was found in the band y 850-960: scored 0 (the reference shows a caption in 96 to 100 percent of its frames)'
        elif gk == 'captions' and bar_caps:
            forced = 0.0
            why = 'implausible input: %.0f percent of the captions consist only of plain filled bars, not lettering: scored 0' % (100 * info['captions_made_of_plain_bars'])
        if gk == 'camera' and video and not sc:
            why = 'clip too short'
        if gk in ('colour', 'density') and flat_card:
            forced = 0.0
            why = 'implausible input: a flat colour card (colour entropy %.1f bits; reference frames 5.7 to 7.4): scored 0' % info['colour_entropy_bits_median']
        score_g = forced if forced is not None else (float(np.mean(sc)) if sc else None)
        groups[gk] = dict(label=gl, weight=gw, score=score_g, n_metrics=len(sc), why=why, applicable=applicable)
    if nheads == 0 or too_few_heads:
        for r in rows:
            if r['group'] == 'characters':
                r['score'] = None; r['verdict'] = 'not measured'
    measured = [g for g in groups.values() if g['score'] is not None]
    wsum = sum(g['weight'] for g in measured)
    index = float(sum(g['weight'] * g['score'] for g in measured) / wsum) if wsum > 0 else None
    wapp = sum(g['weight'] for g in groups.values() if g['applicable'])
    coverage = float(wsum / sum(gw for _, _, gw in GROUPS))
    index_strict = float(sum(g['weight'] * g['score'] for g in measured) / wapp) if wapp > 0 else None
    missing = [g['label'] for g in groups.values() if g['applicable'] and g['score'] is None]
    if missing:
        notes.append('Not measured although the input kind allows it: %s. The index leaves these out (it covers %.0f percent of the weight); the strict index counts them as 0.' % (', '.join(missing), 100 * coverage))
    if flat_card:
        notes.append('The sampled frames hold almost no colour variety (entropy %.1f bits): treated as a flat colour card, colour and density scored 0.' % info['colour_entropy_bits_median'])
    result = dict(label=label, input=os.path.abspath(path), kind=kind, frames=n, seconds=n / FPS if video else 0.0,
                  index=index, index_strict=index_strict, coverage=coverage,
                  groups=groups, metrics=rows, info=info, notes=notes, frame_spread=spread,
                  not_measured_groups=[g['label'] for g in groups.values() if g['score'] is None],
                  transitions=[dict(a=int(t['a']), b=int(t['b']), kind=t['kind'], length=round(float(t['length']), 1)) for t in trans],
                  snaps=[(int(a), int(b)) for a, b in cam['snaps']] if cam else [],
                  elapsed_s=time.time() - t0)
    thumbs_final = []
    for fi, small, hs_all, cm in thumbs:
        vis = small.copy()
        for h in hs_all:
            okh = bool(h.get('ok'))
            c = (int(round(h['cx'] / 2)), int(round(h['cy'] / 2)))
            cv2.circle(vis, c, int(round(h['r_fill'] / 2)), (60, 220, 60) if okh else (60, 60, 255), 2, cv2.LINE_AA)
            if okh:
                cv2.putText(vis, 'D%.0f' % h['D'], (int((h['cx'] - h['r_fill']) / 2), int(min(H - 10, h['cy'] + h['r_fill'] + 44) / 2)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
            else:
                cv2.line(vis, (c[0] - 8, c[1] - 8), (c[0] + 8, c[1] + 8), (60, 60, 255), 2)
                cv2.line(vis, (c[0] - 8, c[1] + 8), (c[0] + 8, c[1] - 8), (60, 60, 255), 2)
        if cm is not None:
            cv2.rectangle(vis, (cm['x0'] // 2, cm['y0'] // 2), (cm['x1'] // 2, cm['y1'] // 2), (255, 0, 255), 2)
        cv2.line(vis, (0, 440), (360, 440), (255, 255, 0), 1)
        th = cv2.resize(vis, (180, 320), interpolation=cv2.INTER_AREA)
        cv2.putText(th, 'f%d' % fi, (4, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1, cv2.LINE_AA)
        thumbs_final.append((fi, th))
    thumbs = thumbs_final
    head_crops = [(fi, h['D'], t) for fi, h, t in head_crops if h.get('ok')]
    extras = dict(thumbs=thumbs, head_crops=head_crops, cap_thumbs=cap_thumbs, cam=cam, trans=trans, anim=anim,
                  cap_pf=cap_pf, heads_pf=heads_pf, n=n, video=video, segs=segs, pstats=pstats, sample_idx=sample_idx,
                  chardiff=[None if c is None else ([(h.get('ok'), r_, g_) for h, r_, g_ in c[0]], c[1], c[2]) for c in chardiff])
    return result, extras


def head_tile(bgr, h, label, size=150):
    R = 0.80 * h['D']
    cx, cy = h['cx'], h['cy']
    s = size / (2 * R)
    Mx = np.float32([[s, 0, -(cx - R) * s], [0, s, -(cy - R) * s]])
    t = cv2.warpAffine(bgr, Mx, (size, size), flags=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC, borderValue=(40, 40, 40))
    HD.draw_head(t, h, scale=s, ox=cx - R, oy=cy - R)
    cv2.putText(t, label, (3, 11), cv2.FONT_HERSHEY_SIMPLEX, 0.36, (0, 255, 255), 1, cv2.LINE_AA)
    txt = 'D%.0f' % h['D'] + (' %.3f/%.3f' % (h['thin'], h['thick']) if h['outline_ok'] else ' no outline')
    cv2.putText(t, txt, (3, size - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.36, (0, 255, 255), 1, cv2.LINE_AA)
    return t


# ------------------------------------------------------------------------------------------------
# outputs
# ------------------------------------------------------------------------------------------------
def load_ref():
    p = os.path.join(HERE, 'ref_clips.json')
    if os.path.exists(p):
        try:
            return json.load(open(p))
        except Exception:
            return {}
    return {}


def fmt_val(r, v):
    if v is None:
        return '-'
    return r['fmt'] % v


def range_text(r):
    f = r['fmt']
    tag = ' [piece range; film ' + (f % r['film_lo']) + ' to ' + (f % r['film_hi']) + ']' if r.get('piece_range') else ''
    if r['key'] in ('h_flat', 'h_fill_s', 'h_ink_de', 'm_static', 'm_hold', 'd_featureless', 't_fill') and r['lo'] == 0:
        return 'at most ' + (f % r['hi']) + ' (0 at ' + (f % (r['hi'] + r['tol'])) + ')' + tag
    if r['hi'] == 1.0 and r['key'] in ('h_above', 'a_char', 't_swap', 'm_diss_share', 't_cover', 'c_dark_sat'):
        return 'at least ' + (f % r['lo']) + ' (0 at ' + (f % (r['lo'] - r['tol'])) + ')' + tag
    return (f % r['lo']) + ' to ' + (f % r['hi']) + ' (0 at ' + (f % r['tol']) + ' outside)' + tag


def write_md(res, path):
    ref = load_ref()
    L = []
    L.append('# Likeness scorecard: %s' % res['label'])
    L.append('')
    L.append('Input: `%s` (%s, %d frame%s%s)' % (res['input'], res['kind'], res['frames'], '' if res['frames'] == 1 else 's',
                                                 ', %.1f s' % res['seconds'] if res['seconds'] else ''))
    L.append('')
    L.append('**This index only covers measurable properties (colour statistics, edge density, line widths, camera motion, caption geometry). It is not a perceptual similarity score: a frame can score high here and still look wrong, and the other way round.**')
    L.append('')
    idx = res['index']
    L.append('## Overall index: %s' % ('%.3f' % idx if idx is not None else 'not measured'))
    L.append('')
    L.append('Weighted mean of the measured groups (weights re-normalised over the groups that were measured). The measured groups carry %.0f percent of the total weight.' % (100 * res.get('coverage', 0)))
    L.append('')
    L.append('Strict index: %s. Here a group that this kind of input allows but that could not be measured counts as 0 (for example no head found, or a picture so washed out that the detectors fail). Compare inputs on the strict index when their "not measured" groups differ.' % (
        '%.3f' % res['index_strict'] if res.get('index_strict') is not None else 'not measured'))
    L.append('')
    L.append('| Group | Weight | Score | Metrics scored | Note |')
    L.append('|---|---|---|---|---|')
    for gk, gl, gw in GROUPS:
        g = res['groups'][gk]
        L.append('| %s | %.2f | %s | %d | %s |' % (gl, gw, '%.3f' % g['score'] if g['score'] is not None else 'not measured', g['n_metrics'], g['why'] or ''))
    nm = res['not_measured_groups']
    L.append('')
    L.append('Groups not measured: %s.' % (', '.join(nm) if nm else 'none'))
    inf = res['info']
    L.append('')
    L.append('Heads found: %d in the %d sampled frames (%d with a measurable outline of 110 px or more)%s. Pale round blobs rejected by the eye test (clocks, plates, lamps): %d.' % (
        inf.get('heads_in_sampled_frames', 0), inf.get('sampled_frames', 0), inf.get('heads_with_outline', 0),
        '; %d detections over all %d frames' % (inf.get('heads_found_all_frames', 0), res['frames']) if res['kind'] != 'still' else '',
        inf.get('round_pale_blobs_rejected_as_not_heads', 0)))
    for nt in res['notes']:
        L.append('')
        L.append('Note: ' + nt)
    for gk, gl, gw in GROUPS:
        L.append('')
        g = res['groups'][gk]
        L.append('## %s (%s)' % (gl, 'score %.3f' % g['score'] if g['score'] is not None else 'not measured' + (': ' + g['why'] if g['why'] else '')))
        L.append('')
        L.append('| Metric | Our value | Reference range | Clip A | Clip B | Score | Verdict | Source |')
        L.append('|---|---|---|---|---|---|---|---|')
        for r in res['metrics']:
            if r['group'] != gk:
                continue
            a = ref.get('A', {}).get(r['key']); b = ref.get('B', {}).get(r['key'])
            L.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % (
                r['label'], fmt_val(r, r['value']), range_text(r), fmt_val(r, a), fmt_val(r, b),
                '%.2f' % r['score'] if r['score'] is not None else '-',
                r['verdict'] + (': ' + r['why'] if r.get('why') else ''), r['source']))
    if ref.get('A_spread') and ref.get('B_spread'):
        L.append('')
        L.append('## How much single frames of the reference scatter')
        L.append('')
        L.append('The ranges above are clip medians. One frame, or a clip of one scene, can sit outside them and still be a frame the reference could contain. 10th to 90th percentile of the half-second frames of each reference clip, measured by this tool:')
        L.append('')
        L.append('| Metric | Our value | Clip A frames p10-p90 | Clip B frames p10-p90 |')
        L.append('|---|---|---|---|')
        for r in res['metrics']:
            if r['key'] in ref['A_spread']:
                f = r['fmt']
                a = ref['A_spread'][r['key']]; b = ref['B_spread'][r['key']]
                L.append('| %s | %s | %s to %s | %s to %s |' % (r['label'], fmt_val(r, r['value']), f % a[0], f % a[1], f % b[0], f % b[1]))
    L.append('')
    L.append('## Other measurements (not scored)')
    L.append('')
    L.append('| Item | Value |')
    L.append('|---|---|')
    for k in sorted(inf.keys()):
        v = inf[k]
        if isinstance(v, float):
            v = '%.3f' % v
        L.append('| %s | %s |' % (k.replace('_', ' '), v))
    if res['transitions']:
        L.append('')
        L.append('Transitions (frame numbers, 0-based): ' + ', '.join(
            ('cut f%d' % t['b']) if t['kind'] == 'cut' else ('dissolve f%d-f%d (%.1f)' % (t['a'], t['b'], t['length'])) for t in res['transitions']))
    if res['snaps']:
        L.append('')
        L.append('Snap reframings: ' + ', '.join('f%d-f%d' % (a, b) for a, b in res['snaps']))
    L.append('')
    L.append('Elapsed: %.1f s. Report sheet: `report.jpg` in the same folder.' % res['elapsed_s'])
    open(path, 'w').write('\n'.join(L) + '\n')


def put(img, txt, x, y, s=0.5, col=(230, 230, 230), th=1):
    cv2.putText(img, txt, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, s, col, th, cv2.LINE_AA)


def score_colour(s):
    if s is None:
        return (120, 120, 120)
    if s >= 0.8:
        return (80, 190, 80)
    if s >= 0.5:
        return (60, 190, 230)
    return (70, 70, 230)


def write_report(res, ex, path):
    RW = 1600
    blocks = []
    # ---- header with group bars ----
    hd = np.full((150, RW, 3), 28, np.uint8)
    idx = res['index']
    put(hd, 'Likeness scorecard: %s' % res['label'], 16, 34, 0.9, (255, 255, 255), 2)
    put(hd, '%s, %d frames' % (res['kind'], res['frames']) + (', %.1f s' % res['seconds'] if res['seconds'] else '') +
        '   index %s, strict %s, weight covered %.0f%% (measurable properties only, not a perceptual score)' % (
            '%.3f' % idx if idx is not None else 'n/a', '%.3f' % res['index_strict'] if res.get('index_strict') is not None else 'n/a',
            100 * res.get('coverage', 0)), 16, 62, 0.55)
    x = 16
    for gk, gl, gw in GROUPS:
        g = res['groups'][gk]
        put(hd, gl, x, 90, 0.45)
        cv2.rectangle(hd, (x, 100), (x + 240, 122), (70, 70, 70), -1)
        if g['score'] is not None:
            cv2.rectangle(hd, (x, 100), (x + int(240 * g['score']), 122), score_colour(g['score']), -1)
            put(hd, '%.2f' % g['score'], x + 6, 117, 0.5, (255, 255, 255), 1)
        else:
            put(hd, 'not measured', x + 6, 117, 0.45, (200, 200, 200), 1)
        x += 262
    put(hd, 'green circle = head (fitted fill circle); red crossed circle = pale round blob rejected by the eye test; cyan / orange dots = measured inner / outer ink edge; magenta box = caption fill; yellow line = y 880',
        16, 142, 0.42, (180, 180, 180))
    blocks.append(hd)
    # ---- sampled frames ----
    th = [t for _, t in ex['thumbs']][:16]
    if th:
        per = 8
        if len(th) == 1:
            big = cv2.resize(th[0], (360, 640), interpolation=cv2.INTER_LINEAR)
            row = np.full((640, RW, 3), 28, np.uint8); row[:, :360] = big
            # more room: head tiles to the right of a still
            tiles = [t for _, _, t in ex['head_crops']][:6]
            for k, t in enumerate(tiles):
                tt = cv2.resize(t, (300, 300), interpolation=cv2.INTER_CUBIC)
                xx = 380 + (k % 4) * 304; yy = 10 + (k // 4) * 310
                row[yy:yy + 300, xx:xx + 300] = tt
            blocks.append(row)
        else:
            for a in range(0, len(th), per):
                row = np.full((320, RW, 3), 28, np.uint8)
                for k, t in enumerate(th[a:a + per]):
                    row[:, k * 200:k * 200 + 180] = t
                blocks.append(row)
    # ---- head tiles ----
    hc = ex['head_crops']
    if hc and len(th) != 1:
        hc = sorted(hc, key=lambda t: t[0])
        want = 20
        sel = [hc[int(round(k))] for k in np.linspace(0, len(hc) - 1, min(want, len(hc)))]
        cap = np.full((24, RW, 3), 28, np.uint8)
        put(cap, 'Detected heads (%d shown of %d in sampled frames): D px, thin / thick ink as a fraction of D' % (len(sel), len(hc)), 16, 17, 0.5)
        blocks.append(cap)
        for a in range(0, len(sel), 10):
            row = np.full((156, RW, 3), 28, np.uint8)
            for k, (_, _, t) in enumerate(sel[a:a + 10]):
                row[3:153, k * 158:k * 158 + 150] = t
            blocks.append(row)
    elif not hc:
        cap = np.full((30, RW, 3), 28, np.uint8)
        put(cap, 'No head detected: the characters group is not measured.', 16, 20, 0.55, (80, 80, 255))
        blocks.append(cap)
    # ---- timeline ----
    cam = ex['cam']
    n = ex['n']
    if cam is not None:
        TLH = 330
        tl = np.full((TLH, RW, 3), 28, np.uint8)
        x0, x1 = 110, RW - 20
        fx = lambda f: int(x0 + (x1 - x0) * f / max(1, n - 1))
        put(tl, 'Timeline (frames 0..%d): detected cuts (red), dissolves (orange), snap reframings (blue), static holds (white), captions, heads, blinks' % (n - 1), 16, 18, 0.5)
        # rows
        def lane(y, h, name):
            cv2.rectangle(tl, (x0, y), (x1, y + h), (45, 45, 45), -1)
            put(tl, name, 8, y + h // 2 + 5, 0.4, (200, 200, 200))
        lane(30, 70, 'zoom %/s'); lane(108, 70, 'pan px/s'); lane(186, 26, 'edit'); lane(218, 20, 'static'); lane(244, 20, 'caption'); lane(270, 20, 'heads'); lane(296, 20, 'blinks')
        zr = np.clip(cam['zr'], -150, 150); tv = np.clip(cam['tv'], 0, 1500)
        cv2.line(tl, (x0, 65), (x1, 65), (90, 90, 90), 1)
        pts = np.array([[fx(f), int(65 - zr[f] / 150.0 * 33)] for f in range(n)], np.int32)
        cv2.polylines(tl, [pts], False, (120, 220, 255), 1, cv2.LINE_AA)
        pts = np.array([[fx(f), int(176 - tv[f] / 1500.0 * 66)] for f in range(n)], np.int32)
        cv2.polylines(tl, [pts], False, (160, 255, 160), 1, cv2.LINE_AA)
        put(tl, '+150', x0 - 34, 40, 0.33, (150, 150, 150)); put(tl, '-150', x0 - 34, 98, 0.33, (150, 150, 150)); put(tl, '1500', x0 - 34, 118, 0.33, (150, 150, 150))
        for a, b in cam['snaps']:
            cv2.rectangle(tl, (fx(a), 187), (max(fx(a) + 1, fx(b)), 211), (230, 140, 40), -1)
        for t in ex['trans']:
            if t['kind'] == 'cut':
                cv2.line(tl, (fx(t['b']), 30), (fx(t['b']), 212), (60, 60, 255), 2)
            else:
                cv2.rectangle(tl, (fx(t['a']), 30), (max(fx(t['a']) + 2, fx(t['b'])), 212), (40, 160, 255), 1)
                cv2.rectangle(tl, (fx(t['a']), 187), (max(fx(t['a']) + 2, fx(t['b'])), 211), (40, 160, 255), -1)
        for a, b in cam['holds']:
            if b - a + 1 >= 3:
                cv2.rectangle(tl, (fx(a), 219), (max(fx(a) + 1, fx(b)), 237), (240, 240, 240), -1)
        k = 0
        for s in ex['segs']:
            col = (255, 90, 255) if k % 2 == 0 else (160, 60, 200)
            cv2.rectangle(tl, (fx(s['frames'][0]), 245), (max(fx(s['frames'][0]) + 1, fx(s['frames'][-1])), 263), col, -1)
            k += 1
        hp = np.array([1 if hs else 0 for hs in ex['heads_pf']])
        f = 0
        while f < n:
            if hp[f]:
                g = f
                while g + 1 < n and hp[g + 1]:
                    g += 1
                cv2.rectangle(tl, (fx(f), 271), (max(fx(f) + 1, fx(g)), 289), (80, 200, 80), -1)
                f = g + 1
            else:
                f += 1
        if ex['anim'] is not None:
            for b in ex['anim']['blinks']:
                cv2.line(tl, (fx(b), 297), (fx(b), 315), (255, 255, 0), 1)
        # frame ticks
        tick = 150 if n > 600 else 30
        for f in range(0, n, tick):
            cv2.line(tl, (fx(f), 318), (fx(f), 322), (160, 160, 160), 1)
            put(tl, 'f%d' % f, fx(f) - 10, TLH - 2, 0.3, (160, 160, 160))
        blocks.append(tl)
    # ---- caption crops ----
    ct = ex['cap_thumbs']
    if ct:
        sel = [ct[int(round(k))] for k in np.linspace(0, len(ct) - 1, min(12, len(ct)))]
        cap = np.full((24, RW, 3), 28, np.uint8)
        put(cap, 'Caption boxes (%d captions found; frame number and estimated word count)' % res['info'].get('captions_found', 0), 16, 17, 0.5)
        blocks.append(cap)
        for a in range(0, len(sel), 4):
            row = np.full((72, RW, 3), 28, np.uint8)
            for k, (fi, wn, t) in enumerate(sel[a:a + 4]):
                row[3:69, k * 398:k * 398 + 360] = t
                put(row, 'f%d  %dw' % (fi, wn), k * 398 + 4, 16, 0.4, (0, 255, 255))
            blocks.append(row)
    # ---- metric list ----
    rows = res['metrics']
    cols = 3
    per_col = int(math.ceil(len(rows) / float(cols)))
    tb = np.full((per_col * 19 + 34, RW, 3), 28, np.uint8)
    put(tb, 'Metric: our value [reference range] score', 16, 18, 0.5)
    for k, r in enumerate(rows):
        cx_ = 16 + (k // per_col) * 528; cy_ = 40 + (k % per_col) * 19
        f = r['fmt']
        txt = '%s: %s [%s..%s]' % (r['label'][:38], fmt_val(r, r['value']), f % r['lo'], f % r['hi'])
        put(tb, txt, cx_, cy_, 0.4, (220, 220, 220))
        put(tb, '%.2f' % r['score'] if r['score'] is not None else 'n/m', cx_ + 478, cy_, 0.4, score_colour(r['score']))
    blocks.append(tb)
    sheet = np.vstack(blocks)
    cv2.imwrite(path, sheet, [cv2.IMWRITE_JPEG_QUALITY, 88])


def metrics_md():
    ref = load_ref()
    L = ['| Group | Metric (key) | Definition | Reference range | Score 0 at | Clip A | Clip B | Source |', '|---|---|---|---|---|---|---|---|']
    for gk, gl, gw in GROUPS:
        for m in METRICS:
            if m['group'] != gk:
                continue
            f = m['fmt']
            a = ref.get('A', {}).get(m['key']); b = ref.get('B', {}).get(m['key'])
            L.append('| %s | %s (`%s`) | %s | %s to %s | %s outside | %s | %s | %s |' % (
                gl, m['label'], m['key'], m['definition'], f % m['lo'], f % m['hi'], f % m['tol'],
                (f % a) if a is not None else '-', (f % b) if b is not None else '-', m['src']))
    return '\n'.join(L)


def jsonable(o):
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, float) and not math.isfinite(o):
        return None
    return o


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('input', nargs='?')
    ap.add_argument('--out')
    ap.add_argument('--label')
    ap.add_argument('--frames', help='A:B, score only frames A to B (0-based, inclusive)')
    ap.add_argument('--no-captions', action='store_true', help='input has no burned-in captions: leave the captions group out')
    ap.add_argument('--metrics-md', action='store_true')
    a = ap.parse_args()
    if a.metrics_md:
        print(metrics_md())
        return
    if not a.input or not a.out:
        ap.error('INPUT and --out DIR are required')
    os.makedirs(a.out, exist_ok=True)
    label = a.label or os.path.splitext(os.path.basename(a.input.rstrip('/')))[0]
    print('scoring %s' % a.input)
    first, last = 0, None
    if a.frames:
        m_ = re.match(r'^(\d*):(\d*)$', a.frames)
        if not m_:
            ap.error('--frames expects A:B')
        first = int(m_.group(1)) if m_.group(1) else 0
        last = int(m_.group(2)) if m_.group(2) else None
        if last is not None and last < first:
            ap.error('--frames: B is before A')
    res, ex = analyse(a.input, label, first=first, last=last, no_captions=a.no_captions)
    if a.frames:
        res['frame_range'] = [first, last]
    res = jsonable(res)
    json.dump(res, open(os.path.join(a.out, 'scorecard.json'), 'w'), indent=1)
    write_md(res, os.path.join(a.out, 'scorecard.md'))
    write_report(res, ex, os.path.join(a.out, 'report.jpg'))
    print('  index %s   strict index %s   weight covered %.0f%%' % ('%.3f' % res['index'] if res['index'] is not None else 'n/a',
                                                                    '%.3f' % res['index_strict'] if res['index_strict'] is not None else 'n/a', 100 * res['coverage']))
    for gk, gl, gw in GROUPS:
        g = res['groups'][gk]
        print('  %-30s %s' % (gl, '%.3f' % g['score'] if g['score'] is not None else 'not measured (%s)' % (g['why'] or '')))
    print('  wrote %s (scorecard.json, scorecard.md, report.jpg) in %.1f s' % (a.out, res['elapsed_s']))


if __name__ == '__main__':
    main()
