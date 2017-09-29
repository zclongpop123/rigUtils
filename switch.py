#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Mon Sep 18 15:37:27 2017
#========================================
import pymel.core as pm
import maya.OpenMaya as OpenMaya
import dag
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def make_switch_joints(root):
    '''
    '''
    LAB = ['_SK', '_FK', '_IK']

    root_pml_node = pm.PyNode(root)
    sk_root, fk_root, ik_root = [root_pml_node.duplicate(rc=True)[0] for i in range(3)]

    for base, sk, fk, ik in zip(dag.get_dag_tree(root), dag.get_dag_tree(sk_root), dag.get_dag_tree(fk_root), dag.get_dag_tree(ik_root)):
        base_name = OpenMaya.MFnDagNode(base).partialPathName()

        for i, j in enumerate((sk, fk, ik)):
            OpenMaya.MFnDagNode(j).setName(base_name + LAB[i])

    return sk_root, fk_root, ik_root





def make_position_switch(sk_root, fk_root, ik_root):
    '''
    '''
    for sk, fk, ik in zip(dag.get_dag_tree(sk_root), dag.get_dag_tree(fk_root), dag.get_dag_tree(ik_root)):
        pm.pointConstraint(OpenMaya.MFnDagNode(fk).fullPathName(),
                           OpenMaya.MFnDagNode(ik).fullPathName(),
                           OpenMaya.MFnDagNode(sk).fullPathName())

    return True





def make_orient_switch(sk_root, fk_root, ik_root):
    '''
    '''
    for sk, fk, ik in zip(dag.get_dag_tree(sk_root), dag.get_dag_tree(fk_root), dag.get_dag_tree(ik_root)):
        pm.orientConstraint(OpenMaya.MFnDagNode(fk).fullPathName(),
                            OpenMaya.MFnDagNode(ik).fullPathName(),
                            OpenMaya.MFnDagNode(sk).fullPathName())

    return True




def make_scale_switch(sk_root, fk_root, ik_root):
    '''
    '''
    for sk, fk, ik in zip(dag.get_dag_tree(sk_root), dag.get_dag_tree(fk_root), dag.get_dag_tree(ik_root)):
        pm.scaleConstraint(OpenMaya.MFnDagNode(fk).fullPathName(),
                           OpenMaya.MFnDagNode(ik).fullPathName(),
                           OpenMaya.MFnDagNode(sk).fullPathName())

    return True
