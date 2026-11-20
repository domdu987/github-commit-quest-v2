for g in $@; do T4_SAMPLES=4 python3 dbg.py $g /tmp/claude-0/s/t_$g.png 2>&1 | grep -v "WARNING\|ERROR\|Saved\|tripod" | tail -3; done
