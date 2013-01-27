__author__ = 'Mihailov'

from scipy.spatial import Delaunay
from matplotlib import pyplot as plt

from Triangle import Triangle

class Grid(Delaunay):
    def __init__(self, coords):
        super(Grid, self).__init__(coords)
        self._init_tri_vertices()
        self._init_triangles()

    def _init_tri_vertices(self):
        self.tri_vertices = [set()] * self.npoints
        for i in xrange(self.nsimplex):
            tri = self.vertices[i]
            self.tri_vertices[tri[0]].update([ i ])
            self.tri_vertices[tri[1]].update([ i ])
            self.tri_vertices[tri[2]].update([ i ])

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
        img = plt.triplot(p[:,0], p[:,1], v, '-')
        return img

    def value(self, coords):
        ti = int(self.find_simplex(coords))
        return self._triangles[ti].value(coords) if ti >= 0 else 0.0
