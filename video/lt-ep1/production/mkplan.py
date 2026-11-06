"""Fill the long-cut plan with times from the landscape schedules: a part runs from the start of one shot key to the start of another (or 0 / the end).
usage: python3 mkplan.py   (reads long_plan.tmpl.json → writes long_plan.json)"""
import json, os
here = os.path.dirname(os.path.abspath(__file__))
plan = json.load(open(os.path.join(here, "long_plan.tmpl.json")))
for p in plan["parts"]:
    ep = p["video"].split("/")[0]; S = json.load(open(os.path.join(here, ep, "schedule.json"))); by = {s["key"]: s for s in S["shots"]}
    for k in ("from", "to"):
        v = p[k]
        if isinstance(v, str) and v.startswith("START:"): p[k] = round(by[v[6:]]["start"], 3)
        elif isinstance(v, str) and v == "END": p[k] = round(S["total"], 3)
json.dump(plan, open(os.path.join(here, "long_plan.json"), "w"), ensure_ascii=False, indent=1)
t = sum(p["to"] - p["from"] for p in plan["parts"]); print(json.dumps(plan["parts"], ensure_ascii=False), "\ntotal", round(t, 2))
