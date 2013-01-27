__author__ = 'Mihailov'

import numpy as np

class Triangle(object):
    def __init__(self, coords):
        self._x = coords[:,0]
        self._y = coords[:,1]
        self._z = None
        self._n = None
        self._updateDerivatives()

    def _updateDerivatives(self):
        x = self._x
        y = self._y
        z = self._z

        self.zdx   = None
        self.zdy   = None
        self._n    = [0]*3
        self._n[2] = (x[1]-x[0])*(y[2]-y[0]) - (x[2]-x[0])*(y[1]-y[0])
        if z is not None:
            self._n[0] = (y[1]-y[0])*(z[2]-z[0]) - (z[1]-z[0])*(y[2]-y[0])
            self._n[1] = (x[2]-x[0])*(z[1]-z[0]) - (x[1]-x[0])*(z[2]-z[0])
            self.zdx   = self._n[0] / self._n[2]
            self.zdy   = self._n[1] / self._n[2]

    def set_z(self, z):
        self._z = z
        self._updateDerivatives()

    def set_transform(self, transform):
        self._transform = transform

    def dec2bc(self, coords):
        b = self._transform[:2].dot(coords - self._transform[2])
        return np.r_[b[0], b[1], 1-b[0]-b[1]]

    def value(self, coords):
        return sum(np.multiply(self.dec2bc(coords), self._z)) if self._z is not None else 1.0

    def check_bypass(self):
        x = self._x
        y = self._y

        return (y[0]-y[1])*(x[2]-x[0]) + (x[1]-x[0])*(y[2]-y[0]) > 0



from scipy.spatial import Delaunay
from matplotlib import pyplot as plt

class Grid(Delaunay):
    def __init__(self, coords):
        super(Grid, self).__init__(coords)
        self._init_neighbors()
        self._init_triangles()

    def _init_neighbors(self):
        self.neigh_vertices = [set()] * self.npoints
        for tri in self.vertices:
            self.neigh_vertices[tri[0]].update([ tri[1], tri[2] ])
            self.neigh_vertices[tri[1]].update([ tri[0], tri[2] ])
            self.neigh_vertices[tri[2]].update([ tri[0], tri[1] ])

    def _init_triangles(self):
        self._triangles = []
        for i in xrange(self.nsimplex):
            t = Triangle(self.points[self.vertices[i]])
            t.set_transform(self.transform[i])
            self._triangles.append(t)

    def plot(self):
        # triplot has a bug: side-effect for an anticlockwise triangles
        # https://github.com/matplotlib/matplotlib/pull/1576
        p = self.points.copy()
        v = self.vertices.copy()
        plt.triplot(p[:,0], p[:,1], v, '-')
        return plt

    def value(self, coords):
        ti = int(self.find_simplex(coords))
        return self._triangles[ti].value(coords) if ti >= 0 else 0.0
