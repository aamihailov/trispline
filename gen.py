import matplotlib

__author__ = 'Anastassia'

import numpy
import matplotlib.pyplot as plt



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
    return numpy.matrix([[xsi, ysi, f(xsi, ysi) + eps()] for xsi in xs for ysi in ys])



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
    numpy.savetxt(filename, data, delimiter='\t')


def load_from_file(filename):
    """Read the generated matrix from the filename

    :param filename: name of filename
    :returns       : points (coods), f (x,y -> f)
    """
    buf    = numpy.loadtxt(filename)
    points = numpy.matrix([[buf[i,j] for j in range(2)] for i in range(len(buf))])
    return points, buf[:,2]


from matplotlib.cm import get_cmap
from matplotlib.colors import Normalize as c_normalize
def plot_points(coords, f):
    """Print the generated coords and values of function

    :param  coords:  points (x,y)
    :param       f:  value of function f(x,y)
    :returns      :  None
    """

    cnorm   = c_normalize(min(f), max(f))
    cmap    = get_cmap('cool')      # try one of this: http://www.scipy.org/Cookbook/Matplotlib/Show_colormaps
    for i in range(f.size):
        plt.scatter(coords[i,0], coords[i,1], s=100, color = cmap(cnorm(f[i])) )
    plt.grid(True)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(min(coords[:,0] -0.25), max(coords[:,0] +0.25))
    plt.ylim(min(coords[:,1] -0.25), max(coords[:,1] +0.25))

    return plt