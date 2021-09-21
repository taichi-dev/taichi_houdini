import taichi as ti
import numpy as np
from taichi_elements.engine.mpm_solver import MPMSolver

# NOTE how do we control gpu or cpu
ti.init()


@ti.data_oriented
class MPMSolverShell:
    def __init__(self, res, dim):
        assert (dim == 2 or dim == 3), "dim error"
        self.dim = dim
        res_array = dim * [res]
        self.solver = MPMSolver(res_array,
                                size=1,
                                unbounded=True,
                                use_voxelizer=False)
        self.frame = 0

    # TODO use the built in dynamic copy func, avoid making your own whell
    # refer to the particle_info()
    @ti.func
    def write_channel_data(self, i, channel: ti.template(),
                           data: ti.template()):
        channel[i] = data

    @ti.kernel
    def write_scalar_channel(self, new_pnum: ti.i32, channel: ti.template(),
                             data: ti.ext_arr()):
        for i in range(self.solver.n_particles[None],
                       self.solver.n_particles[None] + new_pnum):
            self.write_channel_data(i, channel, data[i])

    @ti.kernel
    def write_vector_channel(self, new_pnum: ti.i32, channel: ti.template(),
                             data: ti.ext_arr()):
        for i in range(self.solver.n_particles[None],
                       self.solver.n_particles[None] + new_pnum):
            vec = ti.Vector([data[i, d] for d in range(self.dim)])
            self.write_channel_data(i, channel, vec)

    @ti.kernel
    def write_matrix_channel(self, new_pnum: ti.i32, channel: ti.template(),
                             data: ti.ext_arr()):
        for i in range(self.solver.n_particles[None],
                       self.solver.n_particles[None] + new_pnum):
            mat = ti.Matrix.zero(ti.f32, self.dim, self.dim)
            for r in ti.static(range(self.dim)):
                for c in ti.static(range(self.dim)):
                    mat[r, c] = data[i, r, c]
            self.write_channel_data(i, channel, mat)

    @ti.kernel
    def read_scalar_channel(self, channel: ti.template(),
                            ext_channel: ti.ext_arr()):
        for i in range(self.solver.n_particles[None]):
            ext_channel[i] = channel[i]

    @ti.kernel
    def read_vector_channel(self, channel: ti.template(),
                            ext_channel: ti.ext_arr()):
        for i in range(self.solver.n_particles[None]):
            for d in ti.static(range(self.dim)):
                ext_channel[i, d] = channel[i][d]

    @ti.kernel
    def read_matrix_channel(self, channel: ti.template(),
                            ext_channel: ti.ext_arr()):
        for i in range(self.solver.n_particles[None]):
            for d in ti.static(range(self.dim)):
                for d2 in ti.static(range(self.dim)):
                    ext_channel[i, d, d2] = channel[i][d, d2]

    def detailed_append_from_ext_array(self, P, v, F, Jp, C, material, density,
                                       E, nu, f_angle, H):

        new_pnum = np.size(material)
        print('assert pnum correct for all attribs')
        assert np.shape(P)[0] == new_pnum, "wrong num for P"
        assert np.shape(v)[0] == new_pnum, "wrong num for v"
        assert np.shape(F)[0] == new_pnum, "wrong num for F"
        assert np.shape(Jp)[0] == new_pnum, "wrong num for Jp"
        assert np.shape(C)[0] == new_pnum, "wrong num for C"
        assert np.shape(material)[0] == new_pnum, "wrong num for material"
        assert np.shape(density)[0] == new_pnum, "wrong num for density"
        assert np.shape(E)[0] == new_pnum, "wrong num for E"
        assert np.shape(nu)[0] == new_pnum, "wrong num for nu"
        assert np.shape(f_angle)[0] == new_pnum, "wrong num for f_angle"
        assert np.shape(H)[0] == new_pnum, "wrong num for H"

        print('append channels')
        self.write_vector_channel(new_pnum, self.solver.x, P)
        self.write_vector_channel(new_pnum, self.solver.v, v)
        self.write_matrix_channel(new_pnum, self.solver.F, F)
        self.write_scalar_channel(new_pnum, self.solver.Jp, Jp)
        self.write_matrix_channel(new_pnum, self.solver.C, C)
        self.write_scalar_channel(new_pnum, self.solver.material, material)
        # TODO until ti end support per particle parameters
        # NOTE remember to convert parameters
        # self.write_scalar_channel(new_pnum, self.solver.density,
        #                                       density)
        # self.write_scalar_channel(new_pnum, self.solver.E, E)
        # self.write_scalar_channel(new_pnum, self.solver.nu, nu)
        # self.write_scalar_channel(new_pnum, self.solver.f_angle,
        #                                       f_angle)
        # self.write_scalar_channel(new_pnum, self.solver.H, H)

        self.solver.n_particles[None] += new_pnum

    def detailed_export_to_ext_array(self):
        p_num = self.solver.n_particles[None]
        print("resize ext arr")
        P = np.zeros((p_num, self.dim))
        v = np.zeros((p_num, self.dim))
        F = np.zeros((p_num, self.dim, self.dim))
        C = np.zeros((p_num, self.dim, self.dim))
        Jp = np.zeros(p_num)
        material = np.zeros(p_num)
        density = np.zeros(p_num)
        E = np.zeros(p_num)
        nu = np.zeros(p_num)
        f_angle = np.zeros(p_num)
        H = np.zeros(p_num)

        print('export channels')
        self.read_vector_channel(self.solver.x, P)
        self.read_vector_channel(self.solver.v, v)
        self.read_matrix_channel(self.solver.F, F)
        self.read_scalar_channel(self.solver.Jp, Jp)
        self.read_matrix_channel(self.solver.C, C)
        self.read_scalar_channel(self.solver.material, material)
        # TODO until ti end support per particle parameters
        # NOTE remember to convert parameters
        # self.read_scalar_channel(self.solver.density, density)
        # self.read_scalar_channel(self.solver.E, E)
        # self.read_scalar_channel(self.solver.nu, nu)
        # self.read_scalar_channel(self.solver.f_angle, f_angle)
        # self.read_scalar_channel(self.solver.H, H)

        return P, v, F, Jp, C, material, density, E, nu, f_angle, H

    def set_solver_pars(self, pars, analytical_walls, analytical_spheres):
        use_gpu = pars['use_gpu']
        dx = pars['dx']
        dt = pars['dt']
        res = pars['res']
        dim = pars['dim']
        g = pars['g']
        if (self.dim == 2):
            g = [g[0], g[1]]
        unbounded = pars['unbounded']
        size = pars['size']

        self.default_dt = dt
        self.solver.set_gravity(g)
        self.solver.clear_grid_postprocess()
        # add bbox
        if not unbounded:
            self.solver.add_bounding_box(unbounded)
        # add walls
        for wall in analytical_walls:
            print(wall)
            self.solver.add_surface_collider(wall["point"], wall["normal"],
                                             wall["type"], wall["f"])
        # add spheres
        for sp in analytical_spheres:
            print(sp)
            # TODO wait for the backend to support fractional friction for sphere
            self.solver.add_sphere_collider(sp["center"], sp["r"], sp["type"])


# NOTE currently the size and resolution are hard coded
# TODO have to support editing these parameters in the element-back-end
shell2d = MPMSolverShell(128, 2)
shell3d = MPMSolverShell(128, 3)

if __name__ == "__main__":
    print("test MPM solver shell")
    ms2 = MPMSolverShell(128, 2, True)
    ms3 = MPMSolverShell(128, 3, True)
    P = np.zeros((160, 2))
    v = np.zeros((160, 2))
    F = np.zeros((160, 2, 2))
    Jp = np.zeros(160)
    C = np.zeros((160, 2, 2))
    material = np.zeros(160)
    density = np.zeros(160)
    E = np.zeros(160)
    nu = np.zeros(160)
    f_angle = np.zeros(160)
    H = np.zeros(160)
    ms2.detailed_append_from_ext_array(P, v, F, Jp, C, material, density, E,
                                       nu, f_angle, H)
