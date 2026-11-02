"""ต้นตะเคียนกลางนา EP.2 อย่ากลัวจับตัวเขา — shot timing from the recorded voice (writes schedule.json)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "lib"))
import timing_core as T
SHOTS = [
    ("hook", ["n01"], 0.15, 0.1, 2.21),      # from EP.1's last frame: ลุง still beside the smoking tree, the family frozen
    ("cmd", ["n02"], 0.0, 0.25, 1.7),       # พลอย's hand hovers over him
    ("fear", ["p01"], 0.05, 0.2, 2.04),      # พลอย, close, shaking
    ("safe", ["n03"], 0.1, 0.25, 3.4),       # ต้น's small hand lands on ลุง's arm: nothing happens
    ("rap", ["t01"], 0.3, 0.25, 3.74),       # ต้น kneels at him rapping rule 2; the bamboo rules drop in (rule 1 ticked, rule 2 lit)
    ("call", ["p02"], 0.05, 0.2, 1.7),      # พลอย taps his shoulders, shouts
    ("still", ["n05"], 0.1, 0.25, 2.72),      # his face, his chest not moving, rain on him
    ("phone", ["p03"], 0.05, 0.2, 3.23),     # พลอย on the phone, kneeling
    ("speak", ["n06"], 0.1, 0.2, 2.72),      # top-down: the phone on the grass on speaker, her hands go to his chest
    ("hands", ["n07"], 0.1, 0.25, 4.25),      # top-down: hands stacked lower half of the breastbone, arms straight
    ("rate", ["n08"], 0.1, 0.25, 3.91),       # side view: she pumps
    ("count", ["t02"], 0.05, 0.2, 2.38),     # ต้น counts beside her
    ("drag", ["y01"], 0.05, 0.2, 2.89),      # ยาย takes his ankles to drag him to the tree
    ("no", ["p04"], 0.05, 0.25, 2.21),        # พลอย: no! points at the burnt tree
    ("only", ["n10"], 0.1, 0.25, 4.08),       # side view: keep pumping, hands never lift
    ("tired", ["p05"], 0.05, 0.2, 1.53),     # พลอย spent
    ("swap", ["t03"], 0.05, 0.25, 1.7),     # ต้น takes over
    ("gasp", ["n11"], 0.1, 0.25, 2.55),       # ลุง jolts and draws a breath
    ("joke", ["l01"], 0.05, 0.25, 2.21),      # ลุง, groggy
    ("clear", ["n12"], 0.3, 0.25, 3.91),      # the ambulance on the dirt road, the rain stops, a rainbow
    ("buff", ["t04"], 0.05, 0.2, 1.7),      # ต้น runs off toward the tree for the buffalo
    ("far", ["n13"], 0.1, 0.25, 2.55),        # far horizon: the black cloud flickers in silence
    ("watch", ["y02"], 0.05, 0.25, 3.06),    # ยาย grabs ต้น's toy stopwatch: 12:04 since the last thunder
    ("rule3", ["p06"], 0.3, 0.25, 4.59),      # rule 3 on the bamboo; พลอย shouting it
    ("again", [("n14", 1.2)], 0.0, 0.25, 4.08),  # the bolt from the blue hits the tree again; ต้น stops mid-bund and sits down hard
    ("alive", ["t05"], 0.2, 0.25, 1.7),      # ต้น in the mud, shaking
    ("scars", ["n15"], 0.1, 0.25, 3.4),      # the smoke clears: old burn scars down the trunk
    ("photo", ["p07"], 0.1, 0.2, 2.21),      # the shrine photo
    ("grand", ["y03"], 0.1, 0.25, 3.4),      # ยาย, quiet
    ("truth", ["y04"], 0.2, 0.25, 2.89),      # the family, the tree behind them
    ("end", ["n16"], 0.3, 1.4, 4.42),        # all three rules ticked
]
if __name__ == "__main__":
    T.setup(HERE, SHOTS); T.SHOTS = SHOTS
    T.main()
