#!/usr/bin/env bash
# usage: film/film17/fetch_takes.sh <out_root> [take ...]
# Fetches the approved render takes of film 17 into <out_root>/sNN/{meta.json,take.mkv}
# (meta.json + take.mkv[.part*] only; parts are cat-joined in sorted order into take.mkv).
# Rows with TODO are skipped with a warning; fill them in when a take is approved (see gate/STATUS.md).
# Env: REPO=<git checkout> (default: the repo this script lives in)
set -euo pipefail
OUT=${1:?usage: fetch_takes.sh <out_root> [take ...]}; shift || true
REPO=${REPO:-$(cd "$(dirname "$0")/../.." && pwd)}

# take  branch  commit    (source: gate/STATUS.md "USE THIS" + RENDER_TEAMS.md)
TABLE='
s01 render17/team1  d6ecda5
s02 render17/team2  c2c810e
s03 render17/team3  3fcb09e
s04 render17/team4  TODO     # FAIL R2 (last b3326ff), fill when approved
s05 render17/team2  e553276  # moved from team5 to team2
s06 render17/team5  6fe61b4
s07 render17/team1  TODO     # reassigned to team1, fill when approved (last 34bb2c8 = FAIL R3)
s08 render17/team7  5866892
s09 render17/team8  084ef5b
s10 render17/team9  669e44b  # PASS R5
s11 render17/team10 55446ee  # PASS R3
s12 render17/team11 3c91397
s13 render17/team12 ba82a63  # not ca5cc1a (unreviewed variant)
'
WANT=" $* "
cd "$REPO"; mkdir -p "$OUT"; fetched=(); skipped=()
while read -r take branch commit _; do
  [[ -z "${take:-}" || "$take" == \#* ]] && continue
  if [[ "$WANT" != "  " && "$WANT" != *" $take "* ]]; then continue; fi
  if [[ "$commit" == TODO* ]]; then echo "SKIP $take (TODO)"; skipped+=("$take"); continue; fi
  echo "== $take  $branch @ $commit"
  git fetch -q origin "$branch"
  git cat-file -e "$commit^{commit}"
  d="$OUT/$take"; rm -rf "$d"; mkdir -p "$d"
  git archive "$commit" "film/v3/film17/$take/meta.json" "film/v3/film17/$take/take.mkv*" | tar -x -C "$d" --strip-components=4
  if [[ ! -f "$d/take.mkv" ]]; then
    shopt -s nullglob; parts=("$d"/take.mkv.part*); shopt -u nullglob   # glob expands sorted: partaa.. / part00..
    [[ ${#parts[@]} -gt 0 ]] || { echo "ERROR $take: no take.mkv or parts in $commit" >&2; exit 1; }
    cat "${parts[@]}" > "$d/take.mkv"; rm -f "${parts[@]}"
  fi
  [[ -s "$d/take.mkv" && -f "$d/meta.json" ]] || { echo "ERROR $take: incomplete" >&2; exit 1; }
  fetched+=("$take")
done <<< "$TABLE"
echo "fetched: ${fetched[*]:-none}"; echo "skipped (TODO): ${skipped[*]:-none}"
