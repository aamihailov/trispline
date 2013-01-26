__author__ = 'Anastassia'

from gen import *

f = lambda x, y: x + y

def eps():
    return random.normalvariate(0, 0.01)

def rand():
    return random.uniform(-1, 1)

coords = numpy.matrix([[rand() for j in range(2)] for i in range(100)])
data   = generate_nonuniform(coords, f, eps)

#xs   = numpy.arange(0, 10, 1)
#ys   = numpy.arange(0, 10, 1)

#data = generate_uniform(xs, ys, f, eps)
save_to_file("test.dat", data)

points, func = load_from_file("test.dat")
#print points

p = plot_points(points, func)
p.show()
