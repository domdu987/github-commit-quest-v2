#!/bin/bash
# หนวดใส คลิปยาว 16:9: re-lay the vertical builds (hf/ep1c ep2c brc ep3c) as hf/L1 L2 Lbr L3 with landscape.js, then the blurred
# side-fill behind every fitted card (fitbg.cjs; needs the L servers on 8981 8982 8988 8987)
set -euo pipefail
J="$(cd "$(dirname "$0")/.." && pwd)"; cd "$J/hf"
python3 "$J/land/toland.py" ep1c L1 "$J/land/fix1.json" && python3 "$J/land/patchL1.py" L1/index.html
python3 "$J/land/toland.py" ep2c L2 "$J/land/fix2.json"
python3 "$J/land/toland.py" brc Lbr "$J/land/fixbr.json"
python3 "$J/land/toland.py" fbc Lfb "$J/land/fixfb.json"
python3 "$J/land/toland.py" endc Lend
python3 "$J/land/toland.py" ep3c L3 "$J/land/fix3.json"
for x in "8981 L1 ep1c 1" "8982 L2 ep2c 2" "8988 Lbr brc br" "8987 L3 ep3c 3" "8990 Lfb fbc fb"; do set -- $x; S=""; [ -f "$J/land/src$4.json" ] && S="$J/land/src$4.json"; node "$J/land/fitbg.cjs" $1 "$J/hf/$2" "$J/$3/schedule.json" $S; done
echo ok
