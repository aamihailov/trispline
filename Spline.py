__author__ = 'Mihailov'

class Spline(object):
    def __init__(self, grid, f):
        self._grid = grid
        self._f    = f
        self._init_f()

    def _init_f(self):
        for i in xrange(self._grid.nsimplex):
            tri = self._grid._triangles[i]
            z   = self._f[self._grid.vertices[i]]
            tri.set_z(z)

    def value(self, coords):
        return self._grid.value(coords)

    def plot(self):
        pass
