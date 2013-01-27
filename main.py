__author__ = 'Mihailov'

import random
import numpy
from gen import generate_uniform, generate_nonuniform, save_to_file

f = lambda x, y: numpy.sin(x   +   2*y**2 / (x-0.5))

def eps():
    return 0
    return random.normalvariate(0, 0.01)

def rand():
    return random.uniform(-1, 1)

def coordgen():
    for x in numpy.arange(-1,1,0.2):
        for y in numpy.arange(-1,1,0.2):
            yield (x + eps(), y + eps())

xs   = numpy.arange(-1, 1, 0.2)
ys   = numpy.arange(-1, 1, 0.2)

data = generate_uniform(xs, ys, f, eps)

#coords = numpy.matrix([[rand() for j in range(2)] for i in range(100)])
#data   = generate_nonuniform(coordgen, f, eps)

save_to_file("tests/t0.dat", data)




from gen    import load_from_file, plot_points
from Grid   import Grid
from Spline import Spline

coords, f = load_from_file('tests/t0.dat')
grid      = Grid(coords)
img       = grid.plot()
#img       = plot_points(coords, f)
#img.show()

spline    = Spline(grid, f)



import matplotlib.pyplot as plt
import numpy as np
import pylab

x = y = np.arange(-1.05, 1.05, 0.01)
X, Y  = pylab.meshgrid(x,y)

Z = np.array([[spline.value([xi, yi]) for xi in x] for yi in y ])

plt.pcolor(X, Y, Z)
plt.show()