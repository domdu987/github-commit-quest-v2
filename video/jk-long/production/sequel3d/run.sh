#!/bin/bash
cd "$(dirname "$0")"
for s in "$@"; do python3 p2scene.py render $s 2>&1 | grep -E "^frame|rror" | grep -v CUEW | tail -1; done; echo P2-END
