"""IconFX board sounds per material (owner 1 Nov: sounds must fit the theme). ElevenLabs Sound Effects v2 via fal ($0.002/s).
usage: python3 -I gen_sfx.py [name ...]   → <name>.mp3 next to this file (skips files that exist)."""
import json, os, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
END = "https://fal.run/fal-ai/elevenlabs/sound-effects/v2"
SFX = {
    "clip_snap": ("metal clipboard spring clip snapping shut, sharp aluminium click, close up, dry", 0.8),
    "marker_write": ("felt tip marker pen writing a quick stroke on paper, squeaky marker scribble, close up", 1.0),
    "paper_flutter": ("single sheet of paper fluttering in a breeze on a clipboard, light rustle", 1.0),
    "board_knock": ("wooden board knocking against a nail on a wall, hollow wood thud, classroom", 0.8),
    "chalk_tap": ("chalk tapping and scraping on a blackboard, short underline stroke", 1.0),
    "eraser_rub": ("felt blackboard eraser wiping a chalkboard, soft brushing", 1.0),
    "chain_rattle": ("heavy steel truck tailgate chains rattling, short metallic chain clatter", 1.0),
    "steel_slam": ("heavy steel truck tailgate slamming shut, deep metallic clang with ring", 1.0),
    "spray_short": ("short burst of aerosol spray paint can, hiss psst", 0.7),
    "sign_bong": ("enamel steel road sign swinging on a bolt and hitting a post, metallic bong, outdoors", 1.0),
    "water_drip": ("water droplets dripping into a canal, three small drips, plink", 1.0),
    "brush_swipe": ("wet paint brush swiping across a metal sign, one quick stroke", 0.8),
    "canvas_slap": ("canvas field notebook slapped down on dirt ground, dull thump with dust", 0.7),
    "pencil_scratch": ("pencil scratching on paper, quick circle being drawn", 1.0),
    "buckle_clink": ("leather strap metal buckle clinking, small metal clink", 0.6),
    "cloth_flap": ("cloth banner unfurling and flapping once, fabric whoosh", 0.9),
    "temple_bell": ("small Thai temple bell and soft gong, gentle ring with long tail, eerie", 1.6),
    "candle_whoosh": ("candle flame flickering in a draft, soft whoosh", 0.8),
    "seat_card": ("laminated plastic card sliding out of an airplane seat back pocket, smooth slide and rustle", 1.0),
    "pen_line": ("ballpoint pen drawing a quick line under text on glossy card, scratch", 0.7),
}
names = sys.argv[1:] or list(SFX)
for n in names:
    out = os.path.join(HERE, f"{n}.mp3")
    if os.path.exists(out): continue
    text, dur = SFX[n]
    body = json.dumps({"text": text, "duration_seconds": dur, "prompt_influence": 0.6}).encode()
    for a in range(4):
        try:
            res = json.load(urllib.request.urlopen(urllib.request.Request(END, data=body, headers={"Content-Type": "application/json", "Authorization": "Key proxy"}), timeout=120))
            url = res.get("audio", {}).get("url") or res.get("audio_file", {}).get("url")
            urllib.request.urlretrieve(url, out); print("ok", n, dur); break
        except Exception as e:
            print("retry", n, e, file=sys.stderr); time.sleep(4 * (a + 1))
print("total seconds", sum(SFX[n][1] for n in names))
