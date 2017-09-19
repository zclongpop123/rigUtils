#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Thu Sep 14 10:19:32 2017
#========================================
import pymel.core as pm
import ik, attach, streatch
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
NAME_SPACE = 'XXnamespaceXX'


def create_twist_joints(start_jnt, end_jnt, count=6):
    '''
    '''
    sp = pm.xform(start_jnt, q=True, ws=True, t=True)
    ep = pm.xform(end_jnt,   q=True, ws=True, t=True)

    #- create joints
    twist_joints = list()
    for i in range(count):
        jnt = pm.createNode('joint', name='{0}twist_jnt_{1}'.format(NAME_SPACE, i+1))

        #- match positions
        ps = sp[0] + (ep[0] - sp[0]) / (count-1) * i, sp[1] + (ep[1] - sp[1]) / (count-1) * i, sp[2] + (ep[2] - sp[2]) / (count-1) * i
        pm.xform(jnt, ws=True, t=ps)

        #- save to list
        twist_joints.append(jnt)

        #- parent
        if i:
            pm.delete(pm.aimConstraint(jnt, twist_joints[i-1], aim=(1, 0, 0), u=(0, 0, 1), wut='objectrotation', wuo=start_jnt, wu=(0, 0, 1)))
            pm.parent(jnt, twist_joints[i-1])
            jnt.setAttr('jo'.format(jnt), 0, 0, 0)            

    #- freeze attributes
    pm.makeIdentity(twist_joints[0], a=True, r=True)

    return twist_joints





def create_noroll_joints(start_jnt, end_jnt, count=2, near_jnt=None):
    '''
    '''
    noro_joints = create_twist_joints(start_jnt, end_jnt, count)

    for attr in ('tx', 'ty', 'tz'):
        for jnt in noro_joints[1:]:
            jnt.setAttr(attr, jnt.getAttr(attr) * 0.1)

    if near_jnt:
        pm.delete(pm.pointConstraint(near_jnt, noro_joints[0]))

    for i, jnt in enumerate(noro_joints):
        jnt.rename('{0}noro_jnt_{1}'.format(NAME_SPACE, i+1))

    return noro_joints





def create_aux_joints(end_jnt):
    '''
    '''
    start_jnt = pm.PyNode(end_jnt).getParent()
    aux_joints = create_noroll_joints(start_jnt, end_jnt, 3, end_jnt)

    for i, jnt in enumerate(aux_joints):
        jnt.rename('{0}aux_jnt_{1}'.format(NAME_SPACE, i+1))

    return aux_joints





def create_twist_rig(start_jnt, end_jnt, count=6, use_aux=False, namespace=None):
    '''
    '''
    if namespace:
        global NAME_SPACE
        NAME_SPACE = namespace

    #- Create Joints and ikHandles
    tws_joints  = create_twist_joints(start_jnt, end_jnt, count)
    tws_jointg  = pm.group(tws_joints[0], name='{0}twist_jng_0'.format(NAME_SPACE))
    tws_ikhandl = pm.rename(ik.create_spline_ik(tws_joints[0], tws_joints[-1]), '{0}twist_ikl_0'.format(NAME_SPACE))
    tws_ikcurve = pm.rename(pm.PyNode(tws_ikhandl.getCurve()).getParent(), '{0}twist_crv_0'.format(NAME_SPACE))

    if use_aux:
        nro_joints = create_noroll_joints(start_jnt, end_jnt, 2, end_jnt)
    else:
        nro_joints = create_noroll_joints(start_jnt, end_jnt, 2, start_jnt)
    nro_jointg  = pm.group(nro_joints[0], name='{0}noro_jng_0'.format(NAME_SPACE))
    nro_ikhandl = pm.rename(ik.create_spline_ik(nro_joints[0], nro_joints[-1]), '{0}noro_ikl_0'.format(NAME_SPACE))
    nro_ikcurve = pm.rename(pm.PyNode(nro_ikhandl.getCurve()).getParent(), '{0}noro_crv_0'.format(NAME_SPACE))

    aux_joints  = use_aux and create_aux_joints(end_jnt)
    aux_jointg  = use_aux and pm.group(aux_joints[0], name='{0}aux_jng_0'.format(NAME_SPACE))
    aux_ikhandl = use_aux and pm.rename(ik.create_spline_ik(aux_joints[0], aux_joints[-1]), '{0}aux_ikl_0'.format(NAME_SPACE))
    aux_ikcurve = use_aux and pm.rename(pm.PyNode(aux_ikhandl.getCurve()).getParent(), '{0}aux_crv_0'.format(NAME_SPACE))
    aux_control = use_aux and pm.parent(pm.duplicate(aux_joints[0], name='{0}aux_ctj_0'.format(NAME_SPACE), po=True)[0], w=True)[0]

    #- set advance twist
    if use_aux:
        ik.set_ik_advance_twist(aux_ikhandl, nro_joints[0], aux_control)
        aux_joints[1].rx >> tws_ikhandl.twi
    else:
        ik.set_ik_advance_twist(tws_ikhandl, nro_joints[0], start_jnt)

    #- bind noroll ik curves
    if use_aux:
        attach.connect_curve_points(aux_control, nro_ikcurve)
        attach.connect_curve_points(aux_control, aux_ikcurve)
    else:
        attach.connect_curve_points(start_jnt, nro_ikcurve)

    #- group and constraint joints
    pm.parentConstraint(start_jnt, tws_jointg, mo=True)
    if use_aux:
        pm.parentConstraint(start_jnt,   nro_jointg,  mo=True)
        pm.parentConstraint(aux_control, aux_jointg,  mo=True)
        pm.parentConstraint(end_jnt,     aux_control, mo=True)
    else:
        pm.parentConstraint(pm.listRelatives(start_jnt, p=True, path=True), nro_jointg, mo=True)

    #- Cleanup hierarchy
    pm.group(tws_jointg,  nro_jointg,  use_aux and aux_jointg or None,
             tws_ikhandl, nro_ikhandl, use_aux and aux_ikhandl or None,
             tws_ikcurve, nro_ikcurve, use_aux and aux_ikcurve or None,
             use_aux and aux_control or None)

    #- 
    NAME_SPACE = 'XXnamespaceXX'
