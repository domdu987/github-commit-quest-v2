#!/bin/bash
# ทะเลลด long version: rebuild the three working copies from the repo and apply every long-version patch (starts fresh each run).
#   tidelong/epN   ← video/tide/epN (parts, lines, timing, make, mix) + the delivered voice wavs (video/tide-epN/production/vo)
#   tidelong/hf/libN ← video/tide-epN/lib (the libraries each episode was delivered with)
set -euo pipefail
W="$(cd "$(dirname "$0")/.." && pwd)"; R="$(git -C /home/user/github-commit-quest-v2 rev-parse --show-toplevel)"; V="$R/video"
for e in 1 2 3; do
  rm -rf "$W/ep$e" "$W/hf/lib$e"; mkdir -p "$W/ep$e/vo" "$W/hf/lib$e"
  cp "$V"/tide/ep$e/*.part "$V"/tide/ep$e/*.py "$V"/tide/ep$e/*.json "$W/ep$e/"
  cp "$V"/tide-ep$e/production/vo/* "$W/ep$e/vo/"; cp "$V"/tide/ep$e/vo/*.mp3 "$W/ep$e/vo/"
  cp "$V"/tide-ep$e/lib/*.js "$W/hf/lib$e/"
  sed -i -E "s#^LIB = os.path.join\(HERE, \"..\", \"hf\", \"lib\"\)#LIB = os.path.join(HERE, \"..\", \"hf\", \"lib$e\")#" "$W/ep$e/make.py"
  sed -i -E "s#^PROJ = os.path.join\(HERE, \"..\", \"hf\", \"tide$e\"\)#PROJ = os.environ.get(\"PROJ\") or os.path.join(HERE, \"..\", \"build\", \"ep$e\")#" "$W/ep$e/make.py"
  grep -q "hf\", \"lib$e\")" "$W/ep$e/make.py" && grep -q 'os.environ.get("PROJ")' "$W/ep$e/make.py"
  cp "$W/tools/landfix.part" "$W/ep$e/landfix.part"; cp "$W/tools/land$e.part" "$W/ep$e/land.part"
done
# EP.3: the delivered build (video/tide-ep3/composition) has two fixes its working copy lacks: n03's caption in three parts, the test-tone word at x 680
python3 - "$W/ep3" <<'PY'
import json, sys
d = sys.argv[1]
L = json.load(open(d + "/lines.json"))
for l in L:
    if l["id"] == "n03":
        assert l["cap"] == "ปี 2547… / รถที่หนีคลื่น [ติดและชนกันเอง]บนถนน"; l["cap"] = "ปี 2547… / รถที่หนีคลื่น / [ติดและชนกันเอง]บนถนน"
json.dump(L, open(d + "/lines.json", "w"), ensure_ascii=False, indent=1)
s = open(d + "/body.part").read(); a = '"ปู๊ด… ทดสอบ…", 780, 520'; assert s.count(a) == 1
open(d + "/body.part", "w").write(s.replace(a, '"ปู๊ด… ทดสอบ…", 680, 520'))
PY
python3 "$W/tools/patch_timing.py"; python3 "$W/tools/patch_bridges.py"; python3 "$W/tools/patch_scale.py"; python3 "$W/tools/patch_scale2.py"; python3 "$W/tools/patch_libs.py"
[ -f "$W/tools/patch_mix.py" ] && python3 "$W/tools/patch_mix.py"
for e in 1 2 3; do (cd "$W/ep$e" && python3 timing.py > timing.log); done
echo "prepared: $(for e in 1 2 3; do tail -1 $W/ep$e/timing.log; done | tr '\n' ' ')"
