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

        plt.xlim(self._grid.min_bound[0], self._grid.max_bound[0])
        plt.ylim(self._grid.min_bound[1], self._grid.max_bound[1])

        return plt

    def plot_x_cut(self, x, steps=100, real = None):
        ystep = ( self._grid.max_bound[1] - self._grid.min_bound[1] ) / steps
        y = np.arange(self._grid.min_bound[1], self._grid.max_bound[1], ystep)
        f = np.array([self.value([x, yi]) for yi in y ])
        plt.plot(y, f)
        if real is not None:
            f = np.array([real(x, yi) for yi in y ])
            plt.plot(y, f)
        plt.xlim(self._grid.min_bound[1], self._grid.max_bound[1])
        return plt

    def plot_y_cut(self, y, steps=100, real = None):
        xstep = ( self._grid.max_bound[0] - self._grid.min_bound[0] ) / steps
        x = np.arange(self._grid.min_bound[0], self._grid.max_bound[0], xstep)
        f = np.array([self.value([xi, y]) for xi in x ])
        plt.plot(x, f)
        if real is not None:
            f = np.array([real(xi, y) for xi in x ])
            plt.plot(x, f)
        plt.xlim(self._grid.min_bound[0], self._grid.max_bound[0])
        return plt




class LinearInterpolation(Spline):
    def __init__(self, grid, f):
        super(LinearInterpolation, self).__init__(grid, f)

    def value(self, coords):
        return self._grid.value(coords)



class CubicHermiteSpline(Spline):
    def __init__(self, grid, f):
        super(CubicHermiteSpline, self).__init__(grid, f)
        self._init_derivatives()

    def _init_derivatives(self):
        self._derivatives = [None] * self._grid.npoints
        for i in xrange(self._grid.npoints):
            self._derivatives[i]    = [0, 0]
            tri = [self._grid._triangles[j] for j in self._grid.tri_vertices[i]]
            den = np.sum([np.fabs(t._n[2]) for t in tri])
            self._derivatives[i][0] = np.sum([np.fabs(t._n[2]) * t.zdx for t in tri]) / den
            self._derivatives[i][1] = np.sum([np.fabs(t._n[2]) * t.zdy for t in tri]) / den

    def value(self, coords):
        tri = int(self._grid.find_simplex(coords))
        if tri < 0:
            return 0
        else:
            p   = self._grid.vertices[tri]
            tri = self._grid._triangles[tri]

            L1  = tri.L1(coords);      L2  = tri.L2(coords);     L3  = tri.L3(coords)
            x1  = tri._x[0];           x2  = tri._x[1];          x3  = tri._x[2]
            y1  = tri._y[0];           y2  = tri._y[1];          y3  = tri._y[2]
            f1  = tri._z[0];           f2  = tri._z[1];          f3  = tri._z[2]

            fdx1 = self._derivatives[p[0]][0]; fdy1 = self._derivatives[p[0]][1]
            fdx2 = self._derivatives[p[1]][0]; fdy2 = self._derivatives[p[1]][1]
            fdx3 = self._derivatives[p[2]][0]; fdy3 = self._derivatives[p[2]][1]

            favg = np.average(tri._z)

            c   = [0] * 11      # Coefficients
            psi = [0] * 11      # Values of hermite basis at the current point

            c[1]  = f1;       psi[1]  = L1 * (3*L1  -  2*L1**2  -  7*L2*L3)
            c[2]  = f2;       psi[2]  = L2 * (3*L2  -  2*L2**2  -  7*L3*L1)
            c[3]  = f3;       psi[3]  = L3 * (3*L3  -  2*L3**2  -  7*L1*L2)

            c[4]  = favg;     psi[4]  = 27 * L1 * L2 * L3

            c[5]  = fdx1;     psi[5]  = L1 * ( (x1-x2)*L2*(L3-L1)  +  (x1-x3)*L3*(L2-L1) )
            c[6]  = fdx2;     psi[6]  = L2 * ( (x2-x3)*L3*(L1-L2)  +  (x2-x1)*L1*(L3-L2) )
            c[7]  = fdx3;     psi[7]  = L3 * ( (x3-x1)*L1*(L2-L3)  +  (x3-x2)*L2*(L1-L3) )

            c[8]  = fdy1;     psi[8]  = L1 * ( (y1-y2)*L2*(L3-L1)  +  (y1-y3)*L3*(L2-L1) )
            c[9]  = fdy2;     psi[9]  = L2 * ( (y2-y3)*L3*(L1-L2)  +  (y2-y1)*L1*(L3-L2) )
            c[10] = fdy3;     psi[10] = L3 * ( (y3-y1)*L1*(L2-L3)  +  (y3-y2)*L2*(L1-L3) )

            return np.dot(c, psi)

