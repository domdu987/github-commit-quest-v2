import sys; sys.argv=['x']; 
import shot as S, c22 as C, beck
T = S.make('preview'); T.pose(S.G0+130, S.actors)
for o in T.ob:
    if 'head' in o.get('anc',{}): print(o.name, [round(x,2) for x in beck.card_anchor(o,'head')], 'loc', [round(x,2) for x in o.location])
