import hou
import numpy as np


def read_solver_pars():
    print('reading parameters')
    use_gpu = hou.ch("../../../use_gpu")
    print('use gpu ', use_gpu)
    res = hou.ch("../../../res")
    print('Resoultion ', res)
    dx = hou.ch("../../../dx")
    print('dx ', dx)
    dt = hou.ch("../../../dt")
    print('dt ', dt)
    dim = hou.ch("../../../dim")
    print('dim ', dim)
    g = [hou.ch("../../../gx"), hou.ch("../../../gy"), hou.ch("../../../gz")]
    print('gravity ', g)
    unbounded = hou.ch("../../../unbounded")
    print('unbounded ', unbounded)
    size = dx * res
    print('size ', size)
    return {
        'use_gpu': use_gpu,
        'dx': dx,
        'dt': dt,
        'res': res,
        'dim': dim,
        'g': g,
        'unbounded': unbounded,
        'size': size
    }


def read_analytical_collisions(input_merge_node, dim):
    analytical_walls = []
    analytical_spheres = []
    try:
        # input_merge_node = inputs[1]
        # NOTE is it possible to wrap a func for getting all input (as node), which can help move make material inside the advance node
        null_path = input_merge_node.parm("objpath1").eval()
        null_input_merge_node = hou.node(null_path).inputs()[0]
        path = null_input_merge_node.path() + "/"
        print(path)
        dim_attr = ["x", "y", "z"]
        if (dim == 2):
            dim_attr = ["x", "y"]
        # read wall
        print(path + "wall_num")
        wall_num = hou.ch(path + "wall_num")
        print("wall num ", wall_num)
        for i in range(wall_num):
            type = hou.ch(path + "wall_type" + str(i + 1))
            print("type ", type)
            point = [
                hou.ch(path + "wall_point" + str(i + 1) + d) for d in dim_attr
            ]
            print("point ", point)
            normal = [
                hou.ch(path + "wall_normal" + str(i + 1) + d) for d in dim_attr
            ]
            print("normal ", normal)
            f = hou.ch(path + "wall_f" + str(i + 1))
            print("f ", f)
            analytical_walls.append({
                "type": type,
                "point": point,
                "normal": normal,
                "f": f
            })

        # read sphere
        print(path + "sp_num")
        sp_num = hou.ch(path + "sp_num")
        print("sp num ", sp_num)
        for i in range(sp_num):
            type = hou.ch(path + "sp_type" + str(i + 1))
            print("type ", type)
            center = [
                hou.ch(path + "sp_center" + str(i + 1) + d) for d in dim_attr
            ]
            print("center ", center)
            r = hou.ch(path + "sp_r" + str(i + 1))
            print("radius ", r)
            f = hou.ch(path + "sp_f" + str(i + 1))
            print("f ", f)
            analytical_spheres.append({
                "type": type,
                "center": center,
                "r": r,
                "f": f
            })

    except IndexError:
        print("No analytical collision, continuing")

    return analytical_walls, analytical_spheres


def read_attribs(geo, dim):
    print('reading attribs')
    P = np.array(geo.pointFloatAttribValues("P"))
    print('read pos')
    v = np.array(geo.pointFloatAttribValues("v"))
    print('read v')
    F = np.array(geo.pointFloatAttribValues("F"))
    print('read F')
    Jp = np.array(geo.pointFloatAttribValues("Jp"))
    print('read pJ')
    C = np.array(geo.pointFloatAttribValues("C"))
    print('read C')
    material = np.array(geo.pointFloatAttribValues("material"))
    print('read mattype')
    density = np.array(geo.pointFloatAttribValues("density"))
    print('read density')
    E = np.array(geo.pointFloatAttribValues("E"))
    print('read E')
    nu = np.array(geo.pointFloatAttribValues("nu"))
    print('read nu')
    f_angle = np.array(geo.pointFloatAttribValues("f_angle"))
    print('read f_angle')
    H = np.array(geo.pointFloatAttribValues("H"))
    print('read H')
    print('reshape')
    pnum = np.size(Jp)
    print('particle num ', pnum)
    P = np.reshape(P, (pnum, 3))
    v = np.reshape(v, (pnum, 3))
    F = F.reshape((pnum, dim, dim))
    C = C.reshape((pnum, dim, dim))

    return P, v, F, Jp, C, material, density, E, nu, f_angle, H
