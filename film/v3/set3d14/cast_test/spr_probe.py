import sys, os
V3="/home/user/github-commit-quest-v2/film/v3"
sys.path.insert(0, V3+"/cast14"); sys.path.insert(0, V3+"/stage")
import cast14, sprites
print(cast14.CANVAS14["matriarch"], cast14.CANVAS14["calf"], cast14.CANVAS14_FRONT.get("matriarch"))
cast,pose=cast14.STORY14["matriarch_walk_to_fence"]; print(cast,pose)
r=sprites.render_sprites([{"cast":cast,"pose":pose,"px_per_D":96,"out":os.path.abspath("sprites/probe.png"),"canvas":cast14.CANVAS14[cast]}])
print({k:v for k,v in r[0].items() if k!="anchors"}); print(r[0]["anchors"].get("feet"),r[0]["anchors"].get("head"))
