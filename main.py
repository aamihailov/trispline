from numpy.core.multiarray import arange
from sympy.plotting.plot import plt

__author__ = 'Mihailov'

import random
import numpy
from gen import generate_uniform, generate_nonuniform, save_to_file

prefix = 'sin';       f = lambda x, y: numpy.sin(3*y + 2*x**2)
#prefix = 'quadratic'; f = lambda x, y: x**2 - y**2
#prefix = 'cubic';     f = lambda x, y: x**2 - y**2 + y - y**3
#prefix = 'linear';    f = lambda x, y: x + y

def eps():
    k = 0.05
    d = 0.05 if random.uniform(-k, 1-k) >= 0.00 else 1.00
    return random.normalvariate(0, d)

def rand():
    return random.uniform(-1, 1)

def coordgen():
    for x in numpy.arange(-1,1,0.2):
        for y in numpy.arange(-1,1,0.2):
#            yield (x + eps(), y + eps())
            yield (x, y)

xs   = numpy.arange(-1, 1, 0.9)
ys   = numpy.arange(-1, 1, 0.9)

data = generate_uniform(xs, ys, f, eps)

coords = numpy.matrix([[rand() for j in range(2)] for i in range(100)])
data   = generate_nonuniform(coordgen, f, eps)

save_to_file("tests/t0.dat", data)




from gen    import load_from_file, plot_points
from Grid   import Grid, check_and_filter
from Spline import LinearInterpolation, CubicHermiteSpline

coords, b = load_from_file('tests/t0.dat')
grid      = Grid(coords)
#img       = grid.plot()
g = check_and_filter(grid, b)
g.plot()
plot_points(coords[g.indexes], b[g.indexes])
plt.savefig('tests/%s/grid.png' % prefix)
plt.figure()
#exit()

#spline    = LinearInterpolation(grid, b)
#img       = spline.plot((200,200))
#img.figure()
#img       = spline.plot_y_cut(-0.6, 200)
#img.figure()
#
spline    = CubicHermiteSpline(grid, b)
for y in arange(-1.0, 1.0, 0.2):
    spline.plot_y_cut(y, 200, f)
    plt.savefig('tests/%s/nf%.2f.png' % (prefix, y) )
    plt.figure()
spline.plot((200,200))
plt.savefig('tests/%s/nf-field.png' % prefix)
plt.figure()

spline    = CubicHermiteSpline(g, b[g.indexes])
for y in arange(-1.0, 1.0, 0.2):
    spline.plot_y_cut(y, 200, f)
    plt.savefig('tests/%s/f%.2f.png' % (prefix, y) )
    plt.figure()
spline.plot((200,200))
plt.savefig('tests/%s/f-field.png' % prefix)
