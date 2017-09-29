#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Tue Sep 19 14:40:48 2017
#========================================
import pymel.core as pm
import maya.OpenMaya as OpenMaya
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def get_dag_tree(root):
    '''
    '''
    root_pml_node = pm.PyNode(root)
    iterator = OpenMaya.MItDag()
    iterator.reset(root_pml_node.__apiobject__())

    while not iterator.isDone():
        yield iterator.item()
        iterator.next()
