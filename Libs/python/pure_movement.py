import taichi as ti
import numpy as np

# ti.init()

max_num_particles = 2**30
chunk_size = 2**23
particles = ti.root.dynamic(ti.i, max_num_particles, chunk_size)

x = ti.Vector.field(
    3,
    dtype=ti.f32,
)
particles.place(x)
v = 1


@ti.data_oriented
class moveClass:
    def __init__(self, dt, n_particles):
        self.dt = dt
        self.n_particles = ti.field(ti.i32, shape=())
        self.n_particles[None] = n_particles

    @ti.kernel
    def substep(self):
        for i in range(self.n_particles[None]):
            x[i][0] += v * self.dt

    @ti.func
    def write_channel_data(self, i, channel: ti.template(),
                           data: ti.template()):
        channel[i] = data

    @ti.kernel
    def write_vector_channel(self, new_pnum: ti.i32, channel: ti.template(),
                             data: ti.ext_arr()):
        for i in range(self.n_particles[None],
                       self.n_particles[None] + new_pnum):
            vec = ti.Vector([data[i, d] for d in range(3)])
            self.write_channel_data(i, channel, vec)

    @ti.kernel
    def read_vector_channel(self, channel: ti.template(),
                            ext_channel: ti.ext_arr()):
        for i in range(self.n_particles[None]):
            for d in ti.static(range(3)):
                ext_channel[i, d] = channel[i][d]

    def append_from_ext_array(self, P):
        new_pnum = np.size(P) // 3
        print('append channels')
        print(self.n_particles[None])
        print(new_pnum)
        self.write_vector_channel(new_pnum, x, P)
        self.n_particles[None] += new_pnum

    def export_to_ext_array(self):
        n_particles = self.n_particles[None]
        print("resize ext arr")
        P = np.zeros((n_particles, 3))
        print('export channels')
        self.read_vector_channel(x, P)
        return P


# if __name__ == "__main__":
#     print("test move class")
#     m = moveClass(1e-5, 0)
#     P = np.zeros((160, 3))
#     m.append_from_ext_array(P)
#     print(m.n_particles[None])
