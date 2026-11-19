"""hook test: keys every life hook and the reveal / drawer / fan hooks and checks the values move (prints ok N bad [])."""
import sys; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bertillon as K, bpy
ok=0; bad=[]
def chk(name, cond):
    global ok
    if cond: ok+=1
    else: bad.append(name)
# measure room hooks
A=K.build(preset='measure_wide'); sc=bpy.context.scene
K.key_life(1,6)
pend=K.STATE['life']['pendulum']
chk('pend keyed', pend.animation_data is not None and pend.animation_data.action is not None)
sc.frame_set(3); a3=pend.rotation_euler.y; sc.frame_set(5); a5=pend.rotation_euler.y; chk('pend moves', abs(a3-a5)>1e-4)
sm=K.STATE['life']['smoke'][0]['puffs'][0]; sc.frame_set(2); p2=tuple(sm.location); sc.frame_set(4); p4=tuple(sm.location); chk('smoke moves', p2!=p4)
d=K.STATE['life']['dust'][0]['ob']; sc.frame_set(2); q2=tuple(d.location); sc.frame_set(5); q5=tuple(d.location); chk('dust moves', q2!=q5)
l=K.STATE['lamps'][0][0]; sc.frame_set(1); e1=l.data.energy; sc.frame_set(4); e4=l.data.energy; chk('flicker keyed', e1!=e4)
gm,gb=K.STATE['glows'][0]; sc.frame_set(1); s1=gm.node_tree.nodes['strength'].inputs[1].default_value; sc.frame_set(4); s4=gm.node_tree.nodes['strength'].inputs[1].default_value; chk('glow keyed', s1!=s4)
K.clear_keys(); chk('clear', pend.animation_data is None or pend.animation_data.action is None)
# reveal hooks
A=K.build(preset='card_hero'); sc=bpy.context.scene
K.set_drawer('big',0.0,frame=1); K.set_drawer('big',1.0,frame=11); K.set_card_lift(0.0,frame=1); K.set_card_lift(1.0,frame=11); K.set_box_lid('box',0.0,frame=1); K.set_box_lid('box',1.0,frame=11)
sl=K.STATE['anim']['big']['slide']; hero=K.STATE['anim']['hero']['root']; hg=K.STATE['anim']['box']['hinge']
sc.frame_set(6); chk('drawer mid', abs(sl.location.y-0.39)<0.02); chk('lift mid', abs(hero.location.z-(0.15+0.17))<0.02); chk('lid mid', abs(hg.rotation_euler.x+3.14159*110/180*0.5)<0.05)
sc.frame_set(11); chk('drawer end', abs(sl.location.y-0.78)<1e-3)
# fan + records drawers
A=K.build(preset='records_desk'); sc=bpy.context.scene
K.set_cards_fan(0.0,frame=1); K.set_cards_fan(1.0,frame=9); c=K.STATE['anim']['fan']['cards'][-1]; sc.frame_set(5); chk('fan mid', 0.01<abs(c.rotation_euler.z)<abs(__import__('math').radians(75/2))) ; sc.frame_set(9); chk('fan end', abs(c.rotation_euler.z-__import__('math').radians(37.5))<0.01)
K.set_drawer('p3',0.0,frame=1); K.set_drawer('p3',1.0,frame=5); sc.frame_set(3); chk('p3 mid', abs(K.STATE['anim']['p3']['slide'].location.y-0.21)<0.01)
# street smoke
A=K.build(preset='street_wide'); K.key_life(1,3, pendulum=False); chk('street smoke sources', len(K.STATE['life']['smoke'])>0)
print('ok',ok,'bad',bad)
