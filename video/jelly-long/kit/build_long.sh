#!/bin/bash
# หนวดใส คลิปยาว 16:9: re-lay the five vertical builds (hf/ep1c ep2c brc ep3c) as hf/L1 L2 Lbr L3 with landscape.js
set -euo pipefail
J="$(cd "$(dirname "$0")/.." && pwd)"; cd "$J/hf"
python3 "$J/land/toland.py" ep1c L1 "$J/land/fix1.json" && python3 "$J/land/patchL1.py" L1/index.html
python3 "$J/land/toland.py" ep2c L2 && sed -i 's|<div class="badge" id="badge">หนวดใส · EP.2</div>|<div class="badge" id="badge">หนวดใส · ตอน 2</div>|' L2/index.html
python3 "$J/land/toland.py" brc Lbr
python3 "$J/land/toland.py" ep3c L3 "$J/land/fix3.json" && sed -i 's|<div class="badge" id="badge">หนวดใส · EP.3</div>|<div class="badge" id="badge">หนวดใส · ตอน 3</div>|' L3/index.html
grep -c "ตอน 2" L2/index.html >/dev/null; grep -c "ตอน 3" L3/index.html >/dev/null; echo ok
