import taichi as ti
import numpy as np
import os

ti.init()
n = 0
arr = np.zeros((0, 3))

for i in range(2):
    from pure_movement import moveClass
    print("test appending")
    m = moveClass(1e-6, n)
    P = np.zeros((1, 3))
    m.append_from_ext_array(P)
    m.substep()
    n = m.n_particles[None]
    arr = m.export_to_ext_array()
    print(n)

print(arr)