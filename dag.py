#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Tue Sep 19 14:40:48 2017
#========================================
import pymel.core as pm
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def get_children(root):
    '''
    '''
    root = pm.PyNode(root)

    for c in root.getChildren() or []:
        yield c

        for _c in get_children(c):
            yield _c
