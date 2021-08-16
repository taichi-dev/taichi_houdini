import taichi as ti

ti.init(arch=ti.gpu)


@ti.data_oriented
class fractalClass:
    def __init__(self, n):
        self.res = n
        self.pixels = ti.field(dtype=float, shape=(2 * self.res, self.res))

    @ti.func
    def complex_sqr(self, z):
        return ti.Vector([z[0]**2 - z[1]**2, z[1] * z[0] * 2])

    @ti.kernel
    def paint(self, t: float):
        for i, j in self.pixels:  # Parallized over all pixels
            c = ti.Vector([-0.8, ti.cos(t) * 0.2])
            z = ti.Vector([i / self.res - 1, j / self.res - 0.5]) * 2
            iterations = 0
            while z.norm() < 20 and iterations < 50:
                z = self.complex_sqr(z) + c
                iterations += 1
            self.pixels[i, j] = 1 - iterations * 0.02
