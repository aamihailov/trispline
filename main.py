__author__ = 'Mihailov'

import random
import numpy
from gen import generate_uniform, generate_nonuniform, save_to_file

f = lambda x, y: y*x**2 - y**3

def eps():
    return random.normalvariate(0, 0.00)

def rand():
    return random.uniform(-1, 1)

def coordgen():
    for x in numpy.arange(-1,1,0.2):
        for y in numpy.arange(-1,1,0.2):
            yield (x + eps(), y + eps())

xs   = numpy.arange(-1, 1, 0.25)
ys   = numpy.arange(-1, 1, 0.25)

data = generate_uniform(xs, ys, f, eps)

coords = numpy.matrix([[rand() for j in range(2)] for i in range(100)])
data   = generate_nonuniform(coordgen, f, eps)

save_to_file("tests/t0.dat", data)




from gen    import load_from_file, plot_points
from Grid   import Grid
from Spline import LinearInterpolation, CubicHermiteSpline

coords, f = load_from_file('tests/t0.dat')
grid      = Grid(coords)
#img       = grid.plot()
#img       = plot_points(coords, f)

spline    = CubicHermiteSpline(grid, f)
img       = spline.plot((200,200))
#img       = spline.plot_x_cut(0.15, 200)
img.show()

