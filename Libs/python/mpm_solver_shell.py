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

    def restart(self, pos, vel, F, Jp, C, mattype, density, la, mu, alpha, H):
        self.solver.x.from_numpy(pos)
        self.solver.v.from_numpy(pos)
        self.solver.F.from_numpy(pos)
        self.solver.Jp.from_numpy(pos)
        self.solver.C.from_numpy(pos)
        self.solver.material.from_numpy(pos)
        # TODO release after the engine support
        # self.solver_shell.p_rho.from_numpy(density)
        # self.solver_shell.la.from_numpy(la)
        # self.solver_shell.mu.from_numpy(mu)
        # TODO convert to friction,E,nu to alpha,la,mu here not in houdini aspect
        # in the houdni review, user needs to inspect if they inputted correctly, so dont convert
        # math.sqrt(2 / 3) * 2 * sin_phi / (3 - sin_phi)
        # self.solver_shell.alpha.from_numpy(alpha)
        # self.solver_shell.H.from_numpy(H)


if __name__ == "__main__":
    ti.init()
    ms2 = MPMSolverShell(128, 2)
    ms3 = MPMSolverShell(128, 3)
