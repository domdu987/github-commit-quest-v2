"""ต้นตะเคียนกลางนา EP.1 อย่าวิ่งไปหลบใต้ต้นตะเคียน — shot timing from the recorded voice (writes schedule.json)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "lib"))
import timing_core as T
# key, [voice ids | (id, gap) | (id, offset, "start")], pre, post, min
SHOTS = [
    ("hook", ["n01"], 0.15, 0.1, 2.21),      # the family runs the bund at the lone tree, a bolt far off, push in
    ("cmd", ["n02"], 0.0, 0.25, 1.95),        # the bolt hits the tree as they near it: white flash, silhouettes, they flinch apart
    ("stop", ["y01"], 0.05, 0.2, 1.87),      # ยายหอม grabs พลอย's wrist, everyone skids to a stop in the mud
    ("why", ["n03"], 0.1, 0.25, 3.06),       # what-if: under the tree, the side flash into the people beside the trunk (grey grade)
    ("nosafe", ["n04"], 0.1, 0.25, 2.55),     # high wide: four tiny people in the open field, the storm wall
    ("chabu", ["p01"], 0.1, 0.2, 2.38),      # two-shot พลอย / ยาย in the rain
    ("timer", ["t01"], 0.05, 0.2, 2.38),     # ต้น shows his toy stopwatch (insert) puffing his chest
    ("buff", ["l01"], 0.05, 0.25, 2.55),     # ลุงเปี๊ยก points at his buffalo tied at the foot of the tree
    ("leg1", ["n05"], 0.2, 0.2, 3.4),       # the ผ้าพระบฏ behind the shrine: tilt down the painted cloth
    ("leg2", ["n06"], 0.1, 0.25, 3.06),       # her painted arm beckons, the painted villagers under her shade
    ("joke", ["l02"], 0.05, 0.25, 2.04),      # ลุงเปี๊ยก laughs it off
    ("sci1", ["n07"], 0.1, 0.2, 2.89),       # low angle up the tree against the storm, lightning crawling in the clouds
    ("sci2", ["n08"], 0.1, 0.25, 3.23),      # what-if: strike, side flash, ground current running out
    ("rule1", ["y02"], 0.3, 0.25, 3.57),      # ยายหอม's bamboo rules drop on the hut post, rule 1 lit and ticked
    ("hut", ["t02"], 0.05, 0.25, 1.7),       # ต้น points at the เถียงนา; they run for it
    ("relief", ["p02"], 0.1, 0.2, 1.53),     # under the roof, panting
    ("nohut", ["y03"], 0.05, 0.25, 2.38),    # ยาย: open on four sides — lightning flickers through the roof
    ("shelter", ["n09"], 0.1, 0.25, 4.25),    # the pickup at the road: hard roof, windows up
    ("go", ["y04"], 0.05, 0.2, 2.21),        # ยาย points; everyone sets off at once
    ("spread", ["n10"], 0.1, 0.25, 2.89),    # top-down: the four run apart along different bunds
    ("flat", ["l04"], 0.05, 0.25, 2.04),     # ลุงเปี๊ยก throws himself flat in the mud
    ("wflat", ["n11"], 0.1, 0.25, 2.89),     # what-if: a strike near him, ground current to the man lying flat
    ("crouch", ["n12"], 0.1, 0.2, 2.72),     # what-if: crouching is no help either
    ("up", ["p04"], 0.05, 0.25, 1.36),        # พลอย hauls him up
    ("truck", ["n13"], 0.2, 0.2, 2.21),      # at the pickup: faces behind the glass; the dog under it; ลุง is not there
    ("rope", ["l05"], 0.05, 0.2, 1.7),      # ลุง jogs back toward the buffalo at the tree
    ("noo", ["t03"], 0.05, 0.25, 1.19),       # ต้น at the window, screaming
    ("strike", ["n14"], 1.9, 0.25, 3.91),  # the strike on the tree: flash, silhouette, ground cracks to his feet; he drops; 1.9 s of crack + music, then n14
    ("taken", ["t04"], 0.2, 0.25, 2.04),      # the family frozen at the field edge
    ("none", ["n15"], 0.1, 0.25, 3.06),       # พลอย's hand hovers, pulls back
    ("next", ["n16"], 0.3, 2.2, 3.91),       # the wet note slapped on the truck window
]
if __name__ == "__main__":
    T.setup(HERE, SHOTS); T.SHOTS = SHOTS
    import builtins
    T.main()
