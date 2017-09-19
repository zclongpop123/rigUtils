#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Tue Sep 19 14:44:24 2017
#========================================
import maya.cmds as mc
import pymel.core as pm
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def create_spline_ik(start_jnt, end_jnt, ik_curve=None):
    '''
    '''
    if not ik_curve:
        ik_curve = pm.curve(d=1, p=[pm.xform(jnt, q=True, ws=True, t=True) for jnt in (start_jnt, end_jnt)])

    result = pm.ikHandle(sj=start_jnt, ee=end_jnt, c=ik_curve, ccv=False, sol='ikSplineSolver')

    return result[0]





def set_ik_advance_twist(ikHandle, start_object, end_object):
    '''
    '''
    ik_pml_node = pm.PyNode(ikHandle)
    ik_pml_node.dtce.set(1, l=True)
    ik_pml_node.dwut.set(4, l=True)
    ik_pml_node.dwua.set(3, l=True)
    ik_pml_node.dwuv.set(0, 0, 1, l=True)
    ik_pml_node.dwve.set(0, 0, 1, l=True)
    pm.PyNode(start_object).wm[0] >> ik_pml_node.dwum
    pm.PyNode(end_object).wm[0] >> ik_pml_node.dwue





def change_spline_ik_curve(ikHandle, new_curve):
    '''
    '''
    old_curve = pm.PyNode(pm.PyNode(ikHandle).getCurve()).getParent().name()
    pm.ikHandle(ikHandle, e=True, c=new_curve)

    pm.delete(old_curve)
    pm.rename(new_curve, old_curve)

    return True
