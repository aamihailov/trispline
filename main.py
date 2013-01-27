__author__ = 'Mihailov'

import random
import numpy
from gen import generate_uniform, generate_nonuniform, save_to_file

f = lambda x, y: numpy.sin(3*y + 2*x**2)
#f = lambda x, y: x**2 - y**2
#f = lambda x, y: x**2 - y**2 + y - y**3

def eps():
    return random.normalvariate(0, 0.05)

def rand():
    return random.uniform(-1, 1)

def coordgen():
    for x in numpy.arange(-1,1,0.2):
        for y in numpy.arange(-1,1,0.2):
            yield (x + eps(), y + eps())
#            yield (x, y)

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

spline    = LinearInterpolation(grid, f)
img       = spline.plot((200,200))
#img       = spline.plot_y_cut(-0.5, 200)
img.figure()
spline    = CubicHermiteSpline(grid, f)
img       = spline.plot((200,200))
img.show()

