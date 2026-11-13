#!/usr/bin/env python3
"""shot.py of this take: the engine of shots 9-12 lives in ../s09/shot.py (same cameras, quake clock, set state);
this file runs it with raw/ written into this take folder.  Usage as ../s09/shot.py."""
import os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("shot_s09", os.path.join(HERE, "..", "s09", "shot.py"))
S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
if __name__ == "__main__":
    S.main(sys.argv, take_dir=HERE)
