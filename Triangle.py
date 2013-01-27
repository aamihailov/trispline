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

    def L1(self, coords):
        bc = self.dec2bc(coords)
        return bc[0]

    def L2(self, coords):
        bc = self.dec2bc(coords)
        return bc[1]

    def L3(self, coords):
        bc = self.dec2bc(coords)
        return bc[2]

    def dec2cc(self, coords):
        bc = self.dec2bc(coords)
        cc = [
            bc[0] * ( 3 * bc[0] - 2 * bc[0] ** 2 - 7 * bc[1] * bc[2] ),
            bc[1] * ( 3 * bc[1] - 2 * bc[1] ** 2 - 7 * bc[2] * bc[0] ),
            bc[2] * ( 3 * bc[2] - 2 * bc[2] ** 2 - 7 * bc[0] * bc[1] ),
            ]
        return cc

    def value(self, coords):
        return sum(np.multiply(self.dec2bc(coords), self._z)) if self._z is not None else 1.0

    def check_bypass(self):
        x = self._x
        y = self._y

        return (y[0]-y[1])*(x[2]-x[0]) + (x[1]-x[0])*(y[2]-y[0]) > 0

