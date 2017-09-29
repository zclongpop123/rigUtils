#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Tue Sep 19 14:44:30 2017
#========================================
import pymel.core as pm
import maya.OpenMaya as OpenMaya
import dag
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def rig_joint(joint):
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





def rig_joint_tree(root):
    '''
    '''
    controls = dict()
    for i, jnt in enumerate(list(dag.get_dag_tree(root))):
        jnt_mfn = OpenMaya.MFnDagNode(jnt)

        #-
        jnt_ctl  = rig_joint(jnt_mfn.fullPathName())

        #-
        jnt_pnt = jnt_mfn.parent(0)
        if jnt_pnt.apiType() == OpenMaya.MFn.kJoint:
            jnt_pnt_mfn = OpenMaya.MFnDagNode(jnt_pnt)
            jnt_pnt_ctl = controls.get(jnt_pnt_mfn.uuid().asString(), [jnt_pnt_mfn.fullPathName()])
            pm.parent(jnt_ctl[-1], jnt_pnt_ctl[0])

        #-
        jnt_uuid = jnt_mfn.uuid().asString()
        controls[jnt_uuid] = jnt_ctl

    return True
