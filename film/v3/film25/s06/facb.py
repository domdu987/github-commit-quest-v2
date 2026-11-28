"""facb.py -- helpers shared by the factory build-up takes (28-36): dynamic chain slings from the crane hook to a hanging stage."""
import sys
import rig25 as R
F, bpy = R.F, R.bpy
from mathutils import Vector


def slings(rig, sub, pts, hb=(-5.0, 22.0, 11.6), name="sl_dyn", shackle=True):
    """rebuild the chain slings from the (static) crane hook block `hb` to the lifting points `pts` (tank-local) of the hanging stage `sub`"""
    import factory as FA
    H = rig.H
    old = bpy.data.objects.get(name)
    if old:
        me = old.data; bpy.data.objects.remove(old); bpy.data.meshes.remove(me)
    mb = FA.MB(); M = F.S["M"]; hb = Vector(hb)
    for lp in pts:
        wp = H.root.matrix_world @ (sub.matrix_basis @ Vector(lp))
        FA.L.chain(mb, hb + Vector((0, 0, -0.4)), wp, 0.3, 0.05, M["steel"])
        if shackle:
            FA.obox(mb, wp + Vector((0, 0, 0.12)), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.22, 0.22, 0.12, M["p_yellow"])
    FA.mkobj(mb, name)


def clear_slings(name="sl_dyn"):
    old = bpy.data.objects.get(name)
    if old:
        me = old.data; bpy.data.objects.remove(old); bpy.data.meshes.remove(me)


class StencilMask(object):
    """progressive reveal of the paint on `objs` (their 'paint' material slots are copied and masked): visible where the object-space coordinate `axis`
    (0=x, 1=y, 2=z) is on the painted side of a moving threshold.  set(thr, sign): sign +1 shows coord >= thr (brush working down from the top: thr falls),
    sign -1 shows coord <= thr."""
    def __init__(self, objs, axis=2):
        self.nodes = []
        for ob in objs:
            for slot in ob.material_slots:
                m = slot.material
                if m is None or "paint" not in m.name or not m.use_nodes:
                    continue
                m = m.copy(); slot.material = m; nt = m.node_tree
                out = [n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"][0]
                lk = out.inputs["Surface"].links[0]; src = lk.from_socket
                tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ")
                th = nt.nodes.new("ShaderNodeValue"); ge = nt.nodes.new("ShaderNodeMath"); ge.operation = "GREATER_THAN"
                tr = nt.nodes.new("ShaderNodeBsdfTransparent"); mx = nt.nodes.new("ShaderNodeMixShader")
                nt.links.new(tc.outputs["Object"], sp.inputs[0]); nt.links.new(sp.outputs[axis], ge.inputs[0]); nt.links.new(th.outputs[0], ge.inputs[1])
                nt.links.new(ge.outputs[0], mx.inputs[0]); nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(src, mx.inputs[2])
                nt.links.new(mx.outputs[0], out.inputs["Surface"])
                self.nodes.append((th, ge))

    def set(self, thr, sign=1):
        for th, ge in self.nodes:
            ge.operation = "GREATER_THAN" if sign > 0 else "LESS_THAN"
            th.outputs[0].default_value = float(thr)


def paint_crate(col=(0.04, 0.30, 0.46)):
    """repaint the shipping crate planks / beams a flat vivid marine blue (keeps bump); the stencil paint materials stay"""
    done = set()
    for ob in bpy.data.objects:
        if not ob.name.startswith("crate_") or ob.type != "MESH":
            continue
        for i, slot in enumerate(ob.material_slots):
            m = slot.material
            if m is None or "paint" in m.name or not m.use_nodes:
                continue
            if m.name not in done:
                m2 = m.copy(); done.add(m.name)
            else:
                m2 = m
            bs = [n for n in m2.node_tree.nodes if n.type == "BSDF_PRINCIPLED"]
            if bs:
                for l in list(bs[0].inputs["Base Color"].links):
                    m2.node_tree.links.remove(l)
                bs[0].inputs["Base Color"].default_value = (*col, 1.0)
            slot.material = m2
