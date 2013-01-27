__author__ = 'Mihailov'

import numpy as np
import matplotlib.pyplot as plt
import pylab

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
        raise NotImplemented

    def plot(self, steps=(100,100)):
        xstep = ( self._grid.max_bound[0] - self._grid.min_bound[0] ) / steps[0]
        x = np.arange(self._grid.min_bound[0], self._grid.max_bound[0], xstep)

        ystep = ( self._grid.max_bound[1] - self._grid.min_bound[1] ) / steps[1]
        y = np.arange(self._grid.min_bound[1], self._grid.max_bound[1], ystep)

        X, Y  = pylab.meshgrid(x,y)
        Z = np.array([[self.value([xi, yi]) for xi in x] for yi in y ])

        plt.pcolor(X, Y, Z)

        return plt


class LinearInterpolation(Spline):
    def __init__(self, grid, f):
        super(LinearInterpolation, self).__init__(grid, f)

    def value(self, coords):
        return self._grid.value(coords)

