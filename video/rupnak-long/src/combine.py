"""รูพญานาค ฉบับเต็ม (YouTube 16:9): one schedule for the whole story.
EP.1 without its choice/end cards → bridge 1→2 (new lines b01–b04) → EP.2 without its hook (open, hook) and choice/end →
bridge 2→3 (b05–b07) → EP.3 without its hook. Keys get e1_/e2_/e3_ prefixes (the bodies run in blocks that add them);
voice ids get "e1/" etc. so the mix knows which episode's vo folder holds them. Writes schedule.json."""
import json, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.environ.get("EPDIR", "/home/user/github-commit-quest-v2/video/rupnak")
BR = os.path.join(HERE, "..", "bridge")
CUT = {1: {"choice", "end"}, 2: {"open", "hook", "choice", "end"}, 3: {"open", "hook"}}   # EP.2 open/hook run once, as the cold open
lines = {l["id"]: l for l in json.load(open(os.path.join(BR, "lines.json")))}
dur = json.load(open(os.path.join(BR, "vo", "durations.json")))
dur["c01"] = 2.794   # EP.2 n01 with 0.2 s of its pause after "ถ้าวันหนึ่ง…" cut (bridge/vo/c01.wav)

def frags(i):
    """caption fragment starts: letter share of the line, snapped to the nearest pause in the recording"""
    parts = lines[i]["cap"].split(" / ")
    if len(parts) == 1: return [0.0]
    out = subprocess.run(["ffmpeg", "-nostats", "-i", os.path.join(BR, "vo", f"{i}.wav"), "-af", "silencedetect=n=-35dB:d=0.08", "-f", "null", "-"], capture_output=True, text=True).stderr
    gaps = [(float(a), float(b)) for a, b in zip(re.findall(r"silence_start: ([\d.]+)", out), re.findall(r"silence_end: ([\d.]+)", out))]
    letters = [len(re.sub(r"[\s\[\]{}…!?.,]", "", p)) for p in parts]
    st, acc = [0.0], 0
    for k in range(len(parts) - 1):
        acc += letters[k]; guess = dur[i] * acc / sum(letters)
        g = min(gaps, key=lambda g: abs((g[0] + g[1]) / 2 - guess)) if gaps else None
        st.append(round(g[1] if g and abs((g[0] + g[1]) / 2 - guess) < 0.6 else guess, 2))
    return st

def bshot(key, ids, lead=0.15, gap=0.3, tail=0.4, extra=0.0):
    t, vo = lead, []
    for i in ids:
        vo.append({"id": "b/" + i, "t": round(t, 3), "dur": dur[i], "cap": lines[i]["cap"], "frags": frags(i)}); t += dur[i] + gap
    d = round(t - gap + tail + extra, 3)
    return {"key": key, "dur": d, "vo": vo, "voEnd": round(t - gap, 3)}

def ep(n):
    s = json.load(open(os.path.join(EP, f"ep{n}", "schedule.json")))["shots"]
    out = []
    for x in s:
        if x["key"] in CUT[n]: continue
        out.append({**x, "key": f"e{n}_{x['key']}", "vo": [{**v, "id": f"e{n}/{v['id']}"} for v in x["vo"]]})
    return out

B1 = [bshot("b1win", ["b01", "b02"], gap=0.45, extra=0.3), bshot("b1dust", ["b03"]), bshot("b1shake", ["b04"], tail=0.3)]
B2 = [bshot("b2call", ["b05"]), bshot("b2dawn", ["b06"], extra=0.3), bshot("b2barn", ["b07"], tail=0.35)]
def cold():
    """cold open: EP.2's open + hook (its command lands at ~2.90 s), then a 0.4 s black, then EP.1 with a time chip"""
    s = {x["key"]: x for x in json.load(open(os.path.join(EP, "ep2", "schedule.json")))["shots"]}
    o, h = s["open"], s["hook"]; v = o["vo"][0]
    o = {**o, "key": "e2_open", "dur": round(0.05 + dur["c01"], 3), "voEnd": round(0.05 + dur["c01"], 3),
         "vo": [{**v, "id": "b/c01", "t": 0.05, "dur": dur["c01"], "frags": [0.0, 0.73]}]}
    h = {**h, "key": "e2_hook", "vo": [{**x, "id": f"e2/{x['id']}"} for x in h["vo"]]}
    return [o, h, {"key": "cogap", "dur": 0.4, "vo": [], "voEnd": 0}]

E1 = ep(1); i = [x["key"] for x in E1].index("e1_close") + 1
E1 = E1[:i] + [{"key": "hg7", "dur": 1.0, "vo": [], "voEnd": 0}] + E1[i:]   # HG7: a 1 s subscribe card after EP.1's twist
seq = cold() + E1 + B1 + ep(2) + B2 + ep(3)
t = 0.0
for i, x in enumerate(seq):
    seq[i] = {**x, "start": round(t, 3)}; t += x["dur"]
keys = [x["key"] for x in seq]; assert len(keys) == len(set(keys))
start = {x["key"]: x["start"] for x in seq}
# chapters on real cuts (review M9): the three rule chapters plus seven inside them
chapters = [["บทที่ 1 · ดินแยกเป็นวง อย่าหลงเข้าใกล้", 0.0], ["นาผู้ใหญ่ทองยุบ", start["e1_morning"]], ["ใต้ดินจริงๆ คือหินปูน", start["e1_know0"]],
            ["บทที่ 2 · น้ำบ่อขุ่นแดง แจ้งแล้วถอย", start["b1win"]], ["สายด่วน 1784", start["e2_call"]], ["เครื่องสูบของใคร", start["e2_found"]],
            ["ความลับของพ่อใหญ่สิน", start["e2_valve"]], ["บทที่ 3 · รูยังกว้างได้ ไหว้ไกลร้อยเมตร", start["b2call"]],
            ["ฝนแรกของปี", start["e3_rain"]], ["ลายมือบนใบลาน", start["e3_hand"]]]
json.dump({"total": round(t, 3), "shots": seq, "chapters": chapters}, open(os.path.join(HERE, "schedule.json"), "w"), ensure_ascii=False, indent=1)
print(len(seq), "shots · total", round(t, 3), "· chapters", [(c[0][:7], round(c[1], 1)) for c in chapters])
for x in B1 + B2: print(x["key"], x["dur"], [(v["id"], v["t"], v["frags"]) for v in x["vo"]])
# render parts: 1 = cold open + EP.1 · 2 = bridge 1 + EP.2 · 3 = bridge 2 + EP.3, each re-timed to start at 0 (cut on whole frames)
bounds = [0.0, start["b1win"], start["b2call"], round(t, 3)]
for c in range(3):
    a, b = bounds[c], bounds[c + 1]
    sub = [{**x, "start": round(x["start"] - a, 4)} for x in seq if a - 1e-6 <= x["start"] < b - 1e-6]
    json.dump({"total": round(b - a, 4), "shots": sub}, open(os.path.join(HERE, f"ch{c + 1}.json"), "w"), ensure_ascii=False)
    print(f"ch{c + 1}", len(sub), "shots", round(a, 3), "→", round(b, 3), "frames", round(b * 60) - round(a * 60))
