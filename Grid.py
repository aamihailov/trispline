__author__ = 'Mihailov'

from scipy.spatial import Delaunay
from matplotlib import pyplot as plt

from Triangle import Triangle

class Grid(Delaunay):
    def __init__(self, coords):
        super(Grid, self).__init__(coords)
        self._init_tri_vertices()
        self._init_triangles()
        self._init_point_neighbors()
        self.indexes = None

    def _init_tri_vertices(self):
        self.tri_vertices = [None] * self.npoints
        for i in xrange(self.npoints):
            self.tri_vertices[i] = set()
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

    def _init_point_neighbors(self):
        self.point_neighbors = [None] * 5

        self.point_neighbors[0] = [None] * self.npoints
        self.point_neighbors[1] = [None] * self.npoints
        for i in xrange(self.npoints):
            self.point_neighbors[0][i] = set([i])
            self.point_neighbors[1][i] = set(v for t in self.tri_vertices[i] for v in self.vertices[t])

        for k in xrange(2,5):
            self.point_neighbors[k] = [None] * self.npoints
            for i in xrange(self.npoints):
                self.point_neighbors[k][i] = self.point_neighbors[k-1][i].copy()
                for j in self.point_neighbors[k-1][i]:
                    self.point_neighbors[k][i].update(self.point_neighbors[k-1][j])

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



import numpy as np

def check_and_filter(grid, f):
    is_okay = [None] * grid.npoints
    for i in xrange(grid.npoints):
        s    = grid.point_neighbors[2][i]
        fs   = f[list(s)]
        fswo = f[list(s.difference([i]))]
        m    = np.mean(fs);    mwo = np.mean(fswo)
        d    = np.var(fs);     dwo = np.var(fswo)
#        is_okay[i] =   m - 3.0*d <= f[i] <= m + 3.0*d
        is_okay[i] =   d / dwo <= 1.05
        print i, is_okay[i], d / dwo
    print 'filtered : [%d, %d]' % (sum([1 if not o else 0 for o in is_okay]), grid.npoints)
    n_indexes = [i for i in xrange(grid.npoints) if is_okay[i]]
    g = Grid(grid.points[n_indexes])
    g.indexes = n_indexes
    return g
