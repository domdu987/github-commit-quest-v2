#!/bin/bash
# usage: check_handles.sh handle...   prints YT / TT / X status: free | TAKEN | ?
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
for h in "$@"; do
  yt=$(curl -s -o /dev/null -w "%{http_code}" -m 20 -A "$UA" "https://www.youtube.com/@$h")
  case $yt in 404) yt=free;; 200) yt=TAKEN;; *) yt="?$yt";; esac
  tt=$(curl -s -m 20 -A "$UA" "https://www.tiktok.com/@$h" | grep -o '"statusCode":[0-9]*' | head -1 | cut -d: -f2)
  case $tt in 10221) tt=free;; 0) tt=TAKEN;; *) tt="?$tt";; esac
  xh=${h//./_}
  x=$(curl -s -o /dev/null -w "%{http_code}" -m 20 -A "$UA" "https://x.com/$xh")
  case $x in 404) x=free;; 200) x=TAKEN;; *) x="?$x";; esac
  printf "%-18s YT:%-6s TT:%-6s X:%-6s\n" "$h" "$yt" "$tt" "$x"
done
