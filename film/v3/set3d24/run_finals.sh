#!/bin/bash
# one render process at a time (2 threads): 18 presets + 12 states -> joseon_work/final/
cd "$(dirname "$0")"
python3 joseon.py final roof_low bow yard_wide roof_top macro_spikes macro_dragon fleet_wide flag_deck flag_deck_b flag_deck_crew hansan_high flag_bow chase board reveal_top aftermath shore macro_oar \
  macro_oar:special=solo,os0.12 macro_oar:special=solo,os0.8 \
  roof_top:sp0 roof_top:sp1 roof_top:sp2 roof_top:sp3 roof_low:sp3,pt1 hansan_high:k0 hansan_high:k1 reveal_top:k1,cs1 fleet_wide:dm1 bow:sp3,ds1.5 2>&1 | grep -E "^final|Error|Trace|line " | tee joseon_work/final_log.txt
