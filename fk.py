#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Tue Sep 19 14:44:30 2017
#========================================
import maya.cmds as mc
import pymel.core as pm
import dag
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def rig_joint_fk(joint):
    '''
    '''
    #- create
    ctl = pm.createNode('transform', name='XXnamespaceXX_ctl_0')
    cth = pm.createNode('transform', name='XXnamespaceXX_cth_0')
    ctg = pm.createNode('transform', name='XXnamespaceXX_ctg_0')
    grp = pm.createNode('transform', name='XXnamespaceXX_grp_0')

    #- parent
    pm.parent(ctl, cth)
    pm.parent(cth, ctg)
    pm.parent(ctg, grp)

    #- match positions
    pm.delete(pm.parentConstraint(joint, grp))

    #- constraint
    pm.parentConstraint(ctl, joint)

    #- control shape
    circle = pm.circle(nr=(1, 0, 0), ch=False)[0]
    pm.parent(circle.getShape(), ctl, s=True, r=True)
    pm.delete(circle)

    return ctl, cth, ctg, grp





def rig_joints_fk(root):
    '''
    '''
    for jnt in list(dag.get_children(root)):
        rig_joint_fk(jnt)
