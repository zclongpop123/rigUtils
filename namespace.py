#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Fri Sep 22 10:50:56 2017
#========================================
import maya.cmds as mc
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def clear_all_namespace():
    '''
    '''
    namespaces = mc.namespaceInfo(listOnlyNamespaces=True, recurse=True)
    namespaces.remove('UI')
    namespaces.remove('shared')
    namespaces.sort(key=lambda x:len(x))
    namespaces.reverse()

    while namespaces:
        mc.namespace(rm=namespaces.pop(0), mnr=True)
