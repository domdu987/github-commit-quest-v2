cd /home/user/github-commit-quest-v2/film/v3/film17v2/T4
for g in "$@"; do T4_NOBEAM=1 python3 dbg.py $g /tmp/claude-0/s/f_$g.png 2>&1 | grep -v "WARNING\|ERROR\|tripod\|coat" | tail -2; done
