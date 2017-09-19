#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Mon Sep 18 11:06:36 2017
#========================================
import pymel.core as pm
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def get_joint_axis(joint):
    '''
    '''
    child = joint.getChildren(path=True, typ='joint')
    axis = 'xyz'
    if not child:
        return axis[0]

    position = [abs(v) for v in child[0].t.get()]
    index = position.index(max(position))
    return axis[index]





def make_spline_streatch(ikHandle):
    '''
    '''
    joints = pm.ikHandle(ikHandle, q=True, jl=True)
    curve  = pm.PyNode(pm.ikHandle(ikHandle, q=True, c=True)).getParent()

    if not curve.hasAttr('global_scale'):
        pm.addAttr(curve, ln='global_scale', dv=1, k=True)

    arcn = pm.arclen(curve, ch=True)
    mult = pm.createNode('multDoubleLinear')
    devi = pm.createNode('multiplyDivide')

    arcn.al >> devi.i1x

    curve.global_scale >> mult.i1
    arcn.al >> mult.i2
    arcn.al // mult.i2

    mult.o >> devi.i2x

    devi.op.set(2)

    for jnt in joints:
        devi.ox >> pm.PyNode('{0}.s{1}'.format(jnt, get_joint_axis(jnt)))

    return True
