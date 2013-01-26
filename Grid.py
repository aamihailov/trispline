__author__ = 'Mihailov'

from scipy.spatial import Delaunay

from matplotlib import pyplot as plt

class Grid(Delaunay):
    def __init__(self, coords):
        super(Grid, self).__init__(coords)

    def plot(self):
        plt.triplot(self.points[:,0], self.points[:,1], self.vertices, '-.')
        return plt
