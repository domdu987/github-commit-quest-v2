#!/usr/bin/env python3
"""Rasterise the printed wall map at 2000 px per D (6000 x 4320) with the set's own drawing code (textures.wall_map), for the
close lens positions (shots 9c, 19, 20, 22). Output: tex/map_6000.png (+ map_6000.json with the svg hash). No bpy."""
import os, sys, json, hashlib, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d'))
import textures as T

def ensure(ppd=2000, force=False):
    T.JOBS.clear(); T.wall_map(ppd=ppd); j = T.JOBS['map']
    out = os.path.join(HERE, 'tex', 'map_%d.png' % (j['w'])); meta = out[:-4] + '.json'
    h = hashlib.sha1(j['svg'].encode()).hexdigest()
    if not force and os.path.exists(out) and os.path.exists(meta) and json.load(open(meta)).get('sha1') == h: return out
    os.makedirs(os.path.join(HERE, 'tmp'), exist_ok=True); sp = os.path.join(HERE, 'tmp', 'map_hi.svg'); open(sp, 'w').write(j['svg'])
    jp = os.path.join(HERE, 'tmp', 'map_hi_job.json'); json.dump([dict(src=sp, out=out, w=j['w'], h=j['h'], transparent=False)], open(jp, 'w'))
    r = subprocess.run(['node', os.path.join(PROJ, 'v3', 'set3d', 'raster.js'), jp], capture_output=True, text=True,
                       env=dict(os.environ, NODE_PATH=os.environ.get('NODE_PATH', '/opt/node22/lib/node_modules')))
    if r.returncode != 0: raise RuntimeError(r.stderr[-1500:])
    json.dump(dict(sha1=h, ppd=ppd, w=j['w'], h=j['h']), open(meta, 'w'))
    return out

if __name__ == '__main__':
    print(ensure(int(sys.argv[1]) if len(sys.argv) > 1 else 2000))
