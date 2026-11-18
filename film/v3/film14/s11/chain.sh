#!/bin/bash
cd "$(dirname "$0")"
while [ ! -f ../s04/work/done.txt ]; do sleep 20; done
./runjobs.sh
