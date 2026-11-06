"""hookcheck on a long-form schedule: hooklong.py <schedule.json> <out dir> — writes a schedule/lines pair hookcheck.py can read
(each line's text = its caption without the box marks; narrator lines = ids n.., c01, x02) and runs it."""
import json, os, re, subprocess, sys
sc, out = json.load(open(sys.argv[1])), sys.argv[2]; os.makedirs(out, exist_ok=True)
lines, shots = {}, []
for s in sc["shots"]:
    vo = []
    for v in s["vo"]:
        uid = f'{s["key"]}:{v["id"]}'; base = v["id"].split("/")[-1]
        lines[uid] = {"id": uid, "text": re.sub(r"[\[\]{}]", "", v.get("cap", "")).replace(" / ", " "), "voice": "Puck" if re.match(r"(n\d|c01|x02)", base) else "char"}
        vo.append({**v, "id": uid})
    shots.append({**s, "vo": vo})
json.dump({"shots": shots}, open(os.path.join(out, "schedule.json"), "w"), ensure_ascii=False)
json.dump(list(lines.values()), open(os.path.join(out, "lines.json"), "w"), ensure_ascii=False)
subprocess.run([sys.executable, "/home/user/github-commit-quest-v2/.claude/skills/rodmai-club-video/scripts/hookcheck.py", out])
