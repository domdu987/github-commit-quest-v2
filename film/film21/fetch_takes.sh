#!/usr/bin/env bash
# usage: film/film21/fetch_takes.sh <out_root> [take ...]
# Fetches the approved render takes of film 21 into <out_root>/sNN/{meta.json,take.mkv}
# (meta.json + take.mkv[.part*] only; parts are cat-joined in sorted order into take.mkv).
# Rows with TODO are skipped with a warning; fill them in when a take is approved (see gate/STATUS.md).
# Env: REPO=<git checkout> (default: the repo this script lives in)
set -euo pipefail
OUT=${1:?usage: fetch_takes.sh <out_root> [take ...]}; shift || true
REPO=${REPO:-$(cd "$(dirname "$0")/../.." && pwd)}

# take  branch  commit    (source: gate/STATUS.md "USE THIS" + RENDER_TEAMS.md)
TABLE='
sA1  render21/team1   TODO
sA2  render21/team5   TODO
sB1  render21/team7   TODO
sB2  render21/team5   TODO
sC   render21/team3   9756c30  # PASS TAKE gate v2 (QA-tech)
sD1  render21/team2   TODO
sD2  render21/team4   TODO
sE1  render21/team7   TODO
sE2  render21/team6   TODO
sF   render21/team1   TODO
sG   render21/team8   fddc54e  # PASS TAKE gate v2 (QA-tech)
sH1  render21/team9   TODO
sH2a render21/team3   408ada8  # PASS TAKE gate v2 (QA-tech + QA-art APPROVE)
sH2b render21/team10  TODO
sI   render21/team12  bc7db28  # PASS TAKE gate v2 (QA-tech)
sJ1  render21/team8   TODO
sJ2  render21/team11  TODO
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
  git archive "$commit" "film/v3/film21/$take/meta.json" "film/v3/film21/$take/take.mkv*" | tar -x -C "$d" --strip-components=4
  if [[ ! -f "$d/take.mkv" ]]; then
    shopt -s nullglob; parts=("$d"/take.mkv.part*); shopt -u nullglob   # glob expands sorted: partaa.. / part00..
    [[ ${#parts[@]} -gt 0 ]] || { echo "ERROR $take: no take.mkv or parts in $commit" >&2; exit 1; }
    cat "${parts[@]}" > "$d/take.mkv"; rm -f "${parts[@]}"
  fi
  [[ -s "$d/take.mkv" && -f "$d/meta.json" ]] || { echo "ERROR $take: incomplete" >&2; exit 1; }
  fetched+=("$take")
done <<< "$TABLE"
echo "fetched: ${fetched[*]:-none}"; echo "skipped (TODO): ${skipped[*]:-none}"
