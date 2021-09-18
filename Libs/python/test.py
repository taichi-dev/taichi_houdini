import taichi as ti
import numpy as np
import os

# import pure_movement as pu

# ti.init()
n = 0
# arr = np.zeros((0, 3))

for i in range(2):
    import pure_movement as pu
    print("test appending")
    # m = moveClass(1e-6, n)
    P = np.zeros((1, 3))
    # pu.p.n_particles[None] = n
    pu.p.append_from_ext_array(P)
    pu.p.substep()
    n = pu.p.n_particles[None]
    arr = pu.p.export_to_ext_array()
    print(n)

print(arr)