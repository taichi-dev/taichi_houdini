import taichi as ti
import numpy as np
from taichi_elements.engine.mpm_solver import MPMSolver


@ti.data_oriented
class MPMSolverShell:
    def __init__(self, res, dim):
        assert dim == 2 or dim == 3, "dim error"
        self.dim = dim
        res_array = dim * [res]
        self.solver = MPMSolver(res_array)

    @ti.func
    def detailed_seed_one_channel_data(self, i, channel: ti.template(),
                                       data: ti.template()):
        channel[i] = data

    @ti.kernel
    def detailed_seed_one_scalar_channel(self, new_pnum: ti.i32,
                                         channel: ti.template(),
                                         data: ti.ext_arr()):
        for i in range(self.solver.n_particles[None],
                       self.solver.n_particles[None] + new_pnum):
            self.detailed_seed_one_channel_data(i, channel, data[i])

    @ti.kernel
    def detailed_seed_one_vector_channel(self, new_pnum: ti.i32,
                                         channel: ti.template(),
                                         data: ti.ext_arr()):
        for i in range(self.solver.n_particles[None],
                       self.solver.n_particles[None] + new_pnum):
            vec = ti.Vector([data[i, d] for d in range(self.dim)])
            self.detailed_seed_one_channel_data(i, channel, vec)

    @ti.kernel
    def detailed_seed_one_matrix_channel(self, new_pnum: ti.i32,
                                         channel: ti.template(),
                                         data: ti.ext_arr()):
        for i in range(self.solver.n_particles[None],
                       self.solver.n_particles[None] + new_pnum):
            mat = ti.Matrix.zero(ti.f32, self.dim, self.dim)
            for r in ti.static(range(self.dim)):
                for c in ti.static(range(self.dim)):
                    mat[r, c] = data[i, r, c]
            self.detailed_seed_one_channel_data(i, channel, mat)

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
        self.detailed_seed_one_vector_channel(new_pnum, self.solver.x, P)
        self.detailed_seed_one_vector_channel(new_pnum, self.solver.v, v)
        self.detailed_seed_one_matrix_channel(new_pnum, self.solver.F, F)
        self.detailed_seed_one_scalar_channel(new_pnum, self.solver.Jp, Jp)
        self.detailed_seed_one_matrix_channel(new_pnum, self.solver.C, C)
        self.detailed_seed_one_scalar_channel(new_pnum, self.solver.material,
                                              material)
        # TODO until ti end support per particle parameters
        # NOTE remember to convert parameters
        # self.detailed_seed_one_scalar_channel(new_pnum, self.solver.density,
        #                                       density)
        # self.detailed_seed_one_scalar_channel(new_pnum, self.solver.E, E)
        # self.detailed_seed_one_scalar_channel(new_pnum, self.solver.nu, nu)
        # self.detailed_seed_one_scalar_channel(new_pnum, self.solver.f_angle,
        #                                       f_angle)
        # self.detailed_seed_one_scalar_channel(new_pnum, self.solver.H, H)

        self.solver.n_particles[None] += new_pnum


if __name__ == "__main__":
    print("test MPM solver shell")
    ti.init()
    ms2 = MPMSolverShell(128, 2)
    ms3 = MPMSolverShell(128, 3)
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