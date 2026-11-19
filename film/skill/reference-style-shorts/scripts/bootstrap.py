#!/usr/bin/env python3
"""Unpack the bundled pipeline into a working project folder and point every path at it.

usage: python3 bootstrap.py <project_dir> [--uploads <dir with the reference clips>] [--scratch <scratch dir>]

The bundled files carry three placeholders instead of machine paths:
  __PROJ__     the project root (code, specs, audio, renders live under it)
  __SCRATCH__  the parent scratch folder (defaults to the parent of the project root)
  __UPLOADS__  the folder that holds the reference clips the user uploaded
This script copies pipeline/ to <project_dir> and replaces the placeholders in every text file.
It never overwrites an existing file unless --force is given, so it is safe to run again after an update.
"""
import os, sys, shutil, argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("--uploads", default="")
    ap.add_argument("--scratch", default="")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    proj = os.path.abspath(a.project_dir)
    scratch = os.path.abspath(a.scratch) if a.scratch else os.path.dirname(proj)
    uploads = os.path.abspath(a.uploads) if a.uploads else os.path.join(proj, "uploads")
    src = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pipeline")
    n = skipped = 0
    for root, _, files in os.walk(src):
        for f in files:
            s = os.path.join(root, f)
            d = os.path.join(proj, os.path.relpath(s, src))
            os.makedirs(os.path.dirname(d), exist_ok=True)
            if os.path.exists(d) and not a.force:
                skipped += 1
                continue
            if f.lower().endswith((".ttf", ".otf", ".png", ".jpg", ".wav", ".mp3")):
                shutil.copy(s, d)
            else:
                t = open(s, encoding="utf8", errors="replace").read()
                t = t.replace("__PROJ__", proj).replace("__SCRATCH__", scratch).replace("__UPLOADS__", uploads)
                open(d, "w", encoding="utf8").write(t)
            n += 1
    for sub in ("ref/a", "ref/b", "audio", "deliver", "plan"):
        os.makedirs(os.path.join(proj, sub), exist_ok=True)
    print(f"project ready at {proj}: {n} files written, {skipped} kept as they were")
    print("next: check the environment with scripts/check_env.sh, then follow SKILL.md")

if __name__ == "__main__":
    main()
