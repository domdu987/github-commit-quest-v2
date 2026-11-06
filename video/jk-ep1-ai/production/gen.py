"""AI art jobs for the clip: python3 gen.py jobs.json  → ai/<name>.jpg|png (+ .json log).  op: edit (nano-banana/edit, refs = image paths) | cut (birefnet v2 cut-out of src)."""
import base64, json, mimetypes, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "ai"); os.makedirs(OUT, exist_ok=True)
def uri(p):
    mt = mimetypes.guess_type(p)[0] or "image/jpeg"
    return f"data:{mt};base64," + base64.b64encode(open(p, "rb").read()).decode()
def call(endpoint, payload, name):
    pj = os.path.join(OUT, f"{name}.req.json"); json.dump(payload, open(pj, "w"))
    oj = os.path.join(OUT, f"{name}.out.json")
    r = subprocess.run(["curl", "-sS", "--max-time", "420", "-X", "POST", f"https://fal.run/{endpoint}", "-H", "Content-Type: application/json", "--data-binary", f"@{pj}", "-o", oj], capture_output=True, text=True)
    os.remove(pj)
    try: return json.load(open(oj))
    except Exception as e: return {"error": f"{e} {r.stderr[:200]}"}
def fetch(url, path):
    subprocess.run(["curl", "-sS", "--max-time", "120", "-o", path, url], check=True)
def job(j):
    name, t0 = j["name"], time.time()
    if j["op"] == "edit":
        res = call("fal-ai/nano-banana/edit", {"prompt": j["prompt"], "image_urls": [uri(p) for p in j["refs"]], "num_images": 1, "output_format": "jpeg", "aspect_ratio": j.get("ar", "9:16")}, name)
        if "images" not in res: return f"FAIL {name}: {str(res)[:200]}"
        fetch(res["images"][0]["url"], os.path.join(OUT, f"{name}.jpg"))
    elif j["op"] == "cut":
        res = call("fal-ai/birefnet/v2", {"image_url": uri(j["src"]), "output_format": "png"}, name)
        if "image" not in res: return f"FAIL {name}: {str(res)[:200]}"
        fetch(res["image"]["url"], os.path.join(OUT, f"{name}.png"))
    return f"ok {name} {time.time() - t0:.0f}s"
jobs = json.load(open(sys.argv[1]))
if len(sys.argv) > 2: jobs = [j for j in jobs if j["name"] in sys.argv[2:]]
with ThreadPoolExecutor(max_workers=6) as ex:
    for r in ex.map(job, jobs): print(r, flush=True)
