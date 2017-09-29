#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Thu Sep 14 10:19:32 2017
#========================================
import pymel.core as pm
import ik
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def create_joints(start_jnt, end_jnt, namespace, description, count, offset=1):
    '''
    Name:
        [namespace][description]_jnt_[0-count]

    Position:
                |----- [count] -----|
        [start] O-->O-->O-->O-->O-->O [end]
                |_____ [offset] ____|
    '''

    sp = pm.xform(start_jnt, q=True, ws=True, t=True)
    ep = pm.xform(end_jnt,   q=True, ws=True, t=True)

    #- create joints
    joints = list()
    for i in range(count):
        jnt = pm.createNode('joint', name='{0}{1}_jnt_{2}'.format(namespace, description, i+1))

        #- match positions
        ps = [ sp[x] + (ep[x] - sp[x]) / (count-1) * i * offset for x in range(3) ]
        pm.xform(jnt, ws=True, t=ps)

        #- save to list
        joints.append(jnt)

        #- parent
        if i:
            pm.delete(pm.aimConstraint(jnt, joints[i-1], aim=(1, 0, 0), u=(0, 0, 1), wut='objectrotation', wuo=start_jnt, wu=(0, 0, 1)))
            pm.parent(jnt, joints[i-1])
            jnt.setAttr('jo'.format(jnt), 0, 0, 0)

    #- freeze attributes
    pm.makeIdentity(joints[0], a=True, r=True)


    return joints





def create_twist_joints(start_jnt, end_jnt, namespace, count=6):
    '''
    '''
    #- create joints
    twist_joints = create_joints(start_jnt, end_jnt, namespace, 'twist', count)

    return twist_joints





def create_noroll_joints(start_jnt, end_jnt, namespace, near_jnt=None):
    '''
    '''
    #- create joints
    noro_joints = create_joints(start_jnt, end_jnt, namespace, 'noro', 2, 0.1)

    #- match position
    if near_jnt:
        pm.delete(pm.pointConstraint(near_jnt, noro_joints[0]))

    return noro_joints





def create_aux_joints(start_jnt, end_jnt, namespace):
    '''
    '''
    #- create joints
    aux_joints = create_joints(start_jnt, end_jnt, namespace, 'aux', 3, 0.1)

    #- match position
    pm.delete(pm.pointConstraint(end_jnt, aux_joints[0]))

    return aux_joints





def create_twist_rig(start_jnt, end_jnt, namespace='XXnamespaceXX', count=6, use_aux=False):
    '''
    '''
    #--- Create Joints ---
    tws_joints = create_twist_joints(start_jnt,  end_jnt, namespace, count)
    nro_joints = create_noroll_joints(start_jnt, end_jnt, namespace, [start_jnt, end_jnt][use_aux])
    aux_joints = use_aux and create_aux_joints(start_jnt, end_jnt, namespace)

    #--- Create IK-handles ---

    #- twist ikhandle
    tws_ikhandl = pm.rename(ik.create_spline_ik(tws_joints[0], tws_joints[-1]), '{0}twist_ikl_0'.format(namespace))
    tws_ikcurve = pm.rename(pm.PyNode(tws_ikhandl.getCurve()).getParent(), '{0}twist_crv_0'.format(namespace))

    #- noroll ikhandle
    nro_ikhandl = pm.rename(ik.create_spline_ik(nro_joints[0], nro_joints[-1]), '{0}noro_ikl_0'.format(namespace))
    nro_ikcurve = pm.rename(pm.PyNode(nro_ikhandl.getCurve()).getParent(), '{0}noro_crv_0'.format(namespace))

    #- aux ikhandle
    aux_ikhandl = use_aux and pm.rename(ik.create_spline_ik(aux_joints[0], aux_joints[-1], nro_ikcurve), '{0}aux_ikl_0'.format(namespace))
    aux_control = use_aux and pm.parent(pm.duplicate(aux_joints[0], name='{0}aux_ctj_0'.format(namespace), po=True)[0], w=True)[0]

    #--- Set Advance Twist ---
    if use_aux:
        ik.set_ik_advance_twist(aux_ikhandl, nro_joints[0], aux_control)
        aux_joints[1].rx >> tws_ikhandl.twi
    else:
        ik.set_ik_advance_twist(tws_ikhandl, nro_joints[0], start_jnt)

    #- bind noroll ik curves
    pm.parentConstraint([start_jnt, aux_control][use_aux], nro_ikcurve, mo=True)

    #- group and constraint joints
    twist_rig_grp = pm.createNode('transform')
    if use_aux:
        pm.parentConstraint(start_jnt, twist_rig_grp)
        pm.parentConstraint(end_jnt,   aux_control,   mo=True)
    else:
        pm.parentConstraint(pm.listRelatives(start_jnt, p=True), twist_rig_grp)

    pm.parent(tws_joints[0], nro_joints[0], use_aux and aux_joints[0] or None,
              tws_ikhandl,   nro_ikhandl,   use_aux and aux_ikhandl   or None,
              tws_ikcurve,   nro_ikcurve,
              use_aux and aux_control or None, 
              twist_rig_grp)
