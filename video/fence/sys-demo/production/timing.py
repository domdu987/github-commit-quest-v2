"""Schedule for the systems demo (no voice): fixed shot lengths → schedule.json in the same shape timing.py writes for an episode."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = [("title", 2.6), ("roster", 7.6), ("craft", 11.6), ("count", 13.0), ("count2", 6.8)]
t, out = 0.0, []
for k, d in SHOTS:
    out.append({"key": k, "start": round(t, 3), "dur": d, "vo": [], "voEnd": 0})
    t += d
json.dump({"total": round(t, 3), "shots": out}, open(os.path.join(HERE, "schedule.json"), "w"), ensure_ascii=False)
print("total", round(t, 3))
