#!/usr/bin/env python3
"""write_metrics.py -- out/METRICS.md = measured tables + staging / camera checks + the notes in tools/metrics_notes.md."""
import os
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(os.path.dirname(HERE), "out")
parts = [open(os.path.join(OUT, "METRICS_tables.md")).read()]
qc = os.path.join(OUT, "qa_check.txt")
if os.path.exists(qc):
    parts.append("## 4. Staging and camera (numbers from build.py, `tools/qa_check.py`)\n\n" + "\n".join("- " + l for l in open(qc).read().strip().split("\n")) + "\n")
notes = os.path.join(HERE, "metrics_notes.md")
if os.path.exists(notes):
    parts.append(open(notes).read())
open(os.path.join(OUT, "METRICS.md"), "w").write("\n".join(parts))
print("wrote", os.path.join(OUT, "METRICS.md"))
