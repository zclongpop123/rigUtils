#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Thu Sep 14 17:17:15 2017
#========================================
import maya.cmds as mc
import pymel.core as pm
import curve
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def connect_curve_cv(joint, curveshape, index, offset=(0, 0, 0)):
    '''
    '''
    matrixNode = pm.createNode('pointMatrixMult')

    pm.PyNode(joint).wm[0] >> matrixNode.im
    matrixNode.ip.set(*offset)

    matrixNode.o >> pm.PyNode(curveshape).cp[index]

    return matrixNode





def connect_curve_points(joint, crv):
    '''
    '''
    temp = pm.createNode('transform')
    pm.parent(temp, joint)

    cv_count = curve.get_curve_cv_count(crv)
    for i in range(cv_count):
        ps = pm.xform('{0}.cv[{1}]'.format(crv, i), q=True, ws=True, t=True)
        pm.xform(temp, ws=True, t=ps)

        connect_curve_cv(joint, crv, i, temp.t.get())

    pm.delete(temp)
