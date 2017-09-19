#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Tue Sep 19 15:59:31 2017
#========================================
import pymel.core as pm
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def add_shape(shape, transform):
    '''
    '''
    new_shapes = pm.PyNode(shape).getShapes()
    pm.parent(new_shapes, transform, s=True, r=True)
    pm.delete(shape)





def replace_shape(shape, transform):
    '''
    '''
    old_shapes = pm.PyNode(transform).getShapes()
    add_shape(shape, transform)
    pm.delete(old_shapes)
