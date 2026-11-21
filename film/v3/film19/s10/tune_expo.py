#!/usr/bin/env python3
"""tune_expo.py -- one correction pass of the per-frame exposure table expo.json from the draft luma (work/draft): e += (102 - luma)/29 per EV.
Used to hold the mean luma near 102 through the shot (camera-independent lighting + a slow exposure curve; see shot.py EXPO_TAB)."""
import json, os, numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
tab = {int(k): v for k, v in json.load(open(os.path.join(HERE, "expo.json"))).items()}
L = np.array([float(np.asarray(Image.open(os.path.join(HERE, "work", "draft", "g_%04d.png" % g)).convert("L"), float).mean()) for g in sorted(tab)])
Ls = np.convolve(np.pad(L, 1, mode="edge"), np.ones(3) / 3, "valid")
new = {g: round(tab[g] + (102.0 - Ls[i]) / 29.0, 3) for i, g in enumerate(sorted(tab))}
json.dump(new, open(os.path.join(HERE, "expo.json"), "w"))
print("luma min/max before", round(L.min(), 1), round(L.max(), 1), "max step", round(float(np.abs(np.diff(L)).max()), 2))
