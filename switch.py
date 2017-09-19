#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Mon Sep 18 15:37:27 2017
#========================================
import maya.cmds as mc
import pymel.core as pm
import maya.OpenMaya as OpenMaya
import dag
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def make_switch_joints(root):
    '''
    '''
    joint_dict = dict()
    for jnt in dag.get_children(root):
        for typ in ('sk', 'ik', 'fk'):
            #- create joint
            new_jnt = pm.createNode('joint')
            joint_dict.setdefault(jnt.name(), dict())[typ] = new_jnt

            #- parent joint
            pnt = joint_dict.get(jnt.getParent().name(), dict()).get(typ)
            if pnt:
                pm.parent(new_jnt, pnt)

            #- match position
            pm.delete(pm.parentConstraint(jnt, new_jnt))
            pm.makeIdentity(new_jnt, a=True, r=True)
    
    return joint_dict
