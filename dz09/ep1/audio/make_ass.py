"""make_ass.py -- captions_ep1.ass (whole episode: the hook's lines and title copied verbatim from v10/film/captions_ohm.ass,
then s17-s101 from narr_ep1_timing.json) and captions_ep1_new.ass (s17-s101 only, same clock, for a conform over a hook
mezzanine that already has its captions burnt in).  Style and emphasis exactly as v10/film/finish.py ass_path() / emph()."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
AMBER_ASS, RED_ASS = "&H03B7FF&", "&H4F45F5&"                      # finish.py
COL = {"amber": AMBER_ASS, "red": RED_ASS}
def emph(text, part, col):
    if part and part in text:
        a, b = text.split(part, 1)
        return "{\\fscx112\\fscy112\\t(0,125,\\fscx100\\fscy100)}%s{\\c%s}%s{\\c&HFFFFFF&}%s" % (a, col, part, b)
    return text
ts = lambda t: "%d:%02d:%05.2f" % (t // 3600, (t % 3600) // 60, t % 60)
def main():
    src = open(os.path.join(PROJ, "v10", "film", "captions_ohm.ass"), encoding="utf-8").read().split("\n")
    head = [l for l in src if l.strip() and not l.startswith("Dialogue:")]; hook = [l for l in src if l.startswith("Dialogue:")]
    T = json.load(open(os.path.join(HERE, "narr_ep1_timing.json"), encoding="utf8"))
    lines = ["Dialogue: 0,%s,%s,Cap,,0,0,0,,{\\pos(360,900)}%s" % (ts(c["t0"]), ts(c["t1"]), emph(c["text"], c.get("emph"), COL.get(c.get("colour"), AMBER_ASS))) for c in T["captions"]]
    open(os.path.join(HERE, "captions_ep1.ass"), "w", encoding="utf-8").write("\n".join(head + hook + lines) + "\n")
    open(os.path.join(HERE, "captions_ep1_new.ass"), "w", encoding="utf-8").write("\n".join(head + lines) + "\n")
    print(len(hook), "hook lines,", len(lines), "new lines,", sum(1 for c in T["captions"] if c.get("emph")), "with a coloured word")
if __name__ == "__main__":
    main()
