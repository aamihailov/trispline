__author__ = 'Mihailov'

from gen    import load_from_file
from Grid   import build_grid
from Spline import build_spline, plot_spline

points, f = load_from_file('tests/t1.dat')
grid      = build_grid(points)
spline    = build_spline(grid, f)
image     = plot_spline(spline)
