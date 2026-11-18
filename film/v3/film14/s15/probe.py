import c14, numpy as np
from c14 import *
c14.reg_cam('s19', (18.0, -0.6, 1.4), (9.65, 5.4, 2.0), 24)
A = c14.setup('s19', 'preview', dress=False)
PS0 = 14.0 + 10.25
for t in (0.02,0.05,0.08,0.1,0.116,0.12,0.15,0.2):
    print('t',t,'bow',float(F.wire_disp(np.array([PS0]), t, PS0)[0]))
F._clear_actors()
cl = (18,-0.6,1.4)
for nm in ('matriarch_sniff_fence','matriarch_push','matriarch_walk_to_fence'):
    c, p = story(nm); 
    r = put('probe_'+nm, c, p, (10,2,0), cl, yaw_fixed=0.0)
    w = r['world']; a = r['anchors']
    print(nm, 'feet', [round(x,2) for x in w(a['feet'])], 'chest_push', [round(x,2) for x in w(a['chest_push'])], 'head', [round(x,2) for x in w(a['head'])], 'trunk', [round(x,2) for x in w(a['trunk_tip'])], 'eye', [round(x,2) for x in w(a['eye_r'])])
for pu,le in ((0,0),(0.5,1),(1,2)):
    c,p = story('matriarch_push'); p.update(push=pu, lean=le)
    r = put('probe_p%s'%pu, c, p, (10,2,0), cl, yaw_fixed=0.0); w=r['world']; a=r['anchors']
    print('push',pu,'chest', [round(x,2) for x in w(a['chest_push'])], 'feet', [round(x,2) for x in w(a['feet'])])
