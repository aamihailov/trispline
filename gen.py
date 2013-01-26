__author__ = 'Anastassia'

import numpy
import random
import matplotlib.pyplot as plt


f = lambda x, y: x + y

def eps():
    return random.normalvariate(0, 1)

def rand():
    return random.uniform(-1, 1)


def generate_uniform(xs, ys, f, eps):
    """Generates function field on the uniform grid

    :param  xs:  one-dimensional x grid
    :type   xs:  numpy.arange
    :param  ys:  one-dimensional y grid
    :type   ys:  numpy.arange
    :param   f:  target function        x,y  -> value
    :param eps:  error distribution     none -> value
    :returns  :  matrix with n*m rows, 3 columns: (x, y, f)
    """
    n = xs.size
    m = ys.size
    return numpy.matrix([[xs[i%n], ys[i/n], f(xs[i%n], ys[i/n]) + eps()] for i in range( n * m )])


def generate_nonuniform(coords, f, eps):
    """Generates function field on the nonuniform grid

    :param  coords:  dot generator          none  -> (x,y)
    :param       f:  target function        (x,y) -> value
    :param     eps:  error distribution     none  -> value
    :returns      :  matrix with n*m rows, 3 columns: (x, y, f)
    """
    return numpy.matrix([[coords[i,0], coords[i,1], f(coords[i,0], coords[i,1]) + eps()] for i in range(len(coords))])


def save_to_file(filename, data):
    """Write the generated matrix to the filename

    :param filename: name of filename
    :param     data: matrix with n*m rows, 3 columns: (x, y, f)
    :returns       : None
    """
    f1 = open(filename, 'w')
    for i in range(len(data)):
        buf = ''
        for j in range(data[i].size):
            buf += "%e\t" % (data[i,j])
        f1.write(buf+'\n')
    f1.close()


def load_from_file(filename):
    """Read the generated matrix from the filename

    :param filename: name of filename
    :returns       : points (coods), f (x,y -> f)
    """
    buf    = numpy.loadtxt(filename)
    points = numpy.matrix([[buf[i,j] for j in range(2)] for i in range(len(buf))])
    return points, buf[:,2]

def plot_points(coords, f):
    """Print the generated coords and values of function

    :param  coords:  dot generator          none  -> (x,y)
    :param       f:  target function        (x,y) -> value
    :returns      :  None
    """

    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator, FormatStrFormatter

    plt.figure("test")
    #    plt.plot(coords[:,0], coords[:,1], 'wo')
    #    plt.grid(True)
    #    plt.xlabel('x')
    #    plt.ylabel('y')
    #    plt.xlim(min(coords[:,0] -0.5), max(coords[:,0] +0.5))
    #    plt.ylim(min(coords[:,1] -0.5), max(coords[:,1] +0.5))

    x = [coords[i,0] for i in range(len(coords))]
    y = [coords[i,1] for i in range(len(coords))]
    z = [f for i in range(f.size)]
    plt.imshow(z)
    plt.clim()

    return plt.show()





coords = numpy.matrix([[rand() for j in range(2)] for i in range(10)])
data   = generate_nonuniform(coords, f, eps)

#xs   = numpy.arange(0, 10, 1)
#ys   = numpy.arange(0, 10, 1)

#data = generate_uniform(xs, ys, f, eps)
save_to_file("test.dat", data)

points, func = load_from_file("test.dat")
#print points

p = plot_points(points, func)



