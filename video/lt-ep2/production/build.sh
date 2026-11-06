#!/usr/bin/env bash
# build one episode page: bash build.sh ep2   (body = body_head + common + body_shots; page = head + sigcard + helpers + body + foot)
set -e; cd "$(dirname "$0")/$1"
[ -f vo/durations.json ] && python3 timing.py > /dev/null   # a landscape twin carries schedule.json from its portrait source
cat body_head.part ../common.part body_shots.part > body.part
cat helpers.part body.part > shots.part && cat head.part sigcard.part shots.part foot.part > ep.tmpl.html && python3 make.py
