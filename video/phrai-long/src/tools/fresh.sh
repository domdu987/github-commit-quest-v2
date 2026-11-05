#!/bin/bash
# มือพราย long version: fresh working copies from the repo (no patches yet).
#   phrailong/epN    ← video/phrai-epN/production (parts, lines, timing, make, mix, vo)
#   phrailong/hf/libN ← video/phrai-epN/lib (the libraries each episode was delivered with)
#   phrailong/hf/rig  ← package.json, hyperframes.json, meta.json and fonts from the delivered EP.1 composition
set -euo pipefail
W="$(cd "$(dirname "$0")/.." && pwd)"; R="$(git -C /home/user/github-commit-quest-v2 rev-parse --show-toplevel)"; V="$R/video"
rm -rf "$W/hf/rig"; mkdir -p "$W/hf/rig/assets"
cp "$V"/phrai-ep1/composition/{package.json,hyperframes.json,meta.json} "$W/hf/rig/"; cp -r "$V"/phrai-ep1/composition/assets/fonts "$W/hf/rig/assets/"
for e in 1 2 3; do
  rm -rf "$W/ep$e" "$W/hf/lib$e"; mkdir -p "$W/ep$e" "$W/hf/lib$e"
  cp -r "$V"/phrai-ep$e/production/. "$W/ep$e/"
  cp "$V"/phrai-ep$e/lib/*.js "$W/hf/lib$e/"
  sed -i -E "s#^LIB = os.path.join\(HERE, \"..\", \"hf\", \"lib\"\)#LIB = os.path.join(HERE, \"..\", \"hf\", \"lib$e\")#" "$W/ep$e/make.py"
  sed -i -E "s#^PROJ = os.path.join\(HERE, \"..\", \"hf\", \"phrai$e\"\)#PROJ = os.environ.get(\"PROJ\") or os.path.join(HERE, \"..\", \"build\", \"ep$e\")#" "$W/ep$e/make.py"
  grep -q "hf\", \"lib$e\")" "$W/ep$e/make.py" && grep -q 'os.environ.get("PROJ")' "$W/ep$e/make.py"
done
echo "fresh copies: $(ls -d $W/ep? | tr '\n' ' ')"
