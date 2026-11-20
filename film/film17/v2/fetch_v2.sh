#!/bin/bash
# Film 17 v2: fetch every render part (take.mkv[.partNN] + meta.json) from its render17v2/<part> branch into <parts_root>/<part>/.
# usage: bash film/film17/v2/fetch_v2.sh <parts_root>   (run from the repo root)
set -e
ROOT=${1:?parts_root}
for P in T1a T1b T2a T2b T3 T3b T4 T5a T5b T5b2 T6a T6a2 T6b T7 T8; do
  git fetch -q origin "render17v2/$P"
  mkdir -p "$ROOT/$P"
  for f in $(git ls-tree --name-only FETCH_HEAD "film/v3/film17v2/$P/" | grep -E '/(take\.mkv(\.part..)?|meta\.json)$'); do
    git show "FETCH_HEAD:$f" > "$ROOT/$P/$(basename "$f")"
  done
  echo "$P $(git rev-parse --short FETCH_HEAD) $(ls "$ROOT/$P" | tr '\n' ' ')"
done
