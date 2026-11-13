#!/usr/bin/env python3
"""deliver.py -- s23 (shots 23-24): raw/s1..s4 -> frames/, meta.json, cues.json, contact.jpg, compare.jpg, take.mkv, work/qa.txt."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s21"))
from t5deliver import deliver
S = {1: (2230, 2279, "A the kiosk front pages with her face, tracking along"), 2: (2280, 2339, "B gentleman reading the front page at the kiosk, shocked"),
     3: (2340, 2392, "C the rue: newsboy waving the front page, shouting; passers; Morris column"),
     4: (2393, 2449, "D push past a lady humming into the column poster: her smile (out-handle 2444-2449)")}
cues = [(2230, 2340, "Paris street by the kiosk: hooves, cafe chatter, rustle of newspapers", "ambience"),
        (2236, 2236, "dissolve in from the louvre hooks", "cut"), (2280, 2280, "cut to the gentleman reading", "cut"),
        (2280, 2340, "newspaper rustle / page shake, a shocked 'hmph!'", "foley"),
        (2340, 2340, "cut to the street", "cut"),
        (2340, 2393, "newsboy: 'Extra! Extra! La Joconde!' shouted (walla, not lip-synced), barrel-organ tune in the distance", "voice_walla"),
        (2340, 2393, "footsteps of passers on cobbles", "foley"),
        (2393, 2450, "the lady hums the popular Mona Lisa song (hummed melody, closed mouth)", "music"),
        (2402, 2402, "her smile on the poster: soft chime on 'จำรอยยิ้ม' (79.97 s)", "accent")]
deliver(dict(here=HERE, take="s23", shots=[23, 24], g0=2236, g1=2444, handle=6, setups=S,
             transition_in={"type": "dissolve", "frames": 10, "note": "location change louvre -> paris; in-handle g 2230-2235 rendered in 3D"},
             transition_out={"type": "dissolve", "frames": 10, "note": "next is shot 25 (attic room, dissolve in); out-handle g 2444-2449 rendered in 3D"},
             shot_ranges={"23": [2236, 2339], "24": [2340, 2443]},
             events={"cut_B_reader": 2280, "shot24_street": 2340, "newsboy_shouting": [2340, 2392], "hum_lady_walks_off": 2404, "smile_word": 2402},
             cues=cues, compare=[(2260, "a", 62), (2330, "a", 48), (2370, "a", 85), (2440, "a", 30)],
             set="v3/set3d7/louvre.py paris area (kiosk build), set_papers(24) keyed every frame (theft known: papers at full count), set_flames keyed, 4 custom cameras 22-26 mm",
             light="STREET_GOLDEN",
             cast="v3/cast7: gentleman (gentleman_read), lady_b reading (runtime colour variant), newsboy (newsboy_shout, static mouth), lady_c + gentleman_b walking, lady_d humming"))
