__author__ = 'Mihailov'

import random
import numpy
from gen import generate_uniform, generate_nonuniform, save_to_file

f = lambda x, y: x + y

def eps():
    return random.normalvariate(0, 0.1)

def rand():
    return random.uniform(-1, 1)

xs   = numpy.arange(0, 10, 1)
ys   = numpy.arange(0, 10, 1)

data = generate_uniform(xs, ys, f, eps)

coords = numpy.matrix([[rand() for j in range(2)] for i in range(100)])
data   = generate_nonuniform(coords, f, eps)

save_to_file("tests/t0.dat", data)




from gen    import load_from_file, plot_points
from Grid   import Grid
from Spline import build_spline, plot_spline

coords, f = load_from_file('tests/t0.dat')
grid      = Grid(coords)
img       = grid.plot()
img       = plot_points(coords, f)
img.show()
spline    = build_spline(grid, f)
image     = plot_spline(spline)
