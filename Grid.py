__author__ = 'Mihailov'

from scipy.spatial import Delaunay

class Grid(Delaunay):
    def __init__(self, coords):
        super(Grid, self).__init__(coords)
