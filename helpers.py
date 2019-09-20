from scipy.spatial._plotutils import _held_figure, _adjust_bounds
import numpy as np

@_held_figure
def voronoi_plot_2d(vor, ax=None, **kw):
    """
    Plot the given Voronoi diagram in 2-D
    Parameters
    ----------
    vor : scipy.spatial.Voronoi instance
        Diagram to plot
    ax : matplotlib.axes.Axes instance, optional
        Axes to plot on
    show_points: bool, optional
        Add the Voronoi points to the plot.
    show_vertices : bool, optional
        Add the Voronoi vertices to the plot.
    line_colors : string, optional
        Specifies the line color for polygon boundaries
    line_width : float, optional
        Specifies the line width for polygon boundaries
    line_alpha: float, optional
        Specifies the line alpha for polygon boundaries
    point_size: float, optional
        Specifies the size of points
    Returns
    -------
    fig : matplotlib.figure.Figure instance
        Figure for the plot
    See Also
    --------
    Voronoi
    Notes
    -----
    Requires Matplotlib.
    Examples
    --------
    Set of point:
    >>> import matplotlib.pyplot as plt
    >>> points = np.random.rand(10,2) #random
    Voronoi diagram of the points:
    >>> from scipy.spatial import Voronoi, voronoi_plot_2d
    >>> vor = Voronoi(points)
    using `voronoi_plot_2d` for visualisation:
    >>> fig = voronoi_plot_2d(vor)
    using `voronoi_plot_2d` for visualisation with enhancements:
    >>> fig = voronoi_plot_2d(vor, show_vertices=False, line_colors='orange',
    ...                 line_width=2, line_alpha=0.6, point_size=2)
    >>> plt.show()
    """
    from matplotlib.collections import LineCollection

    if vor.points.shape[1] != 2:
        raise ValueError("Voronoi diagram is not 2-D")

    if kw.get('show_points', True):
        point_size = kw.get('point_size', None)
        ax.plot(vor.points[:,0], vor.points[:,1], '.', markersize=point_size)
    if kw.get('show_vertices', True):
        ax.plot(vor.vertices[:,0], vor.vertices[:,1], 'o')

    line_colors = kw.get('line_colors', 'k')
    line_width = kw.get('line_width', 1.0)
    line_alpha = kw.get('line_alpha', 1.0)

    center = vor.points.mean(axis=0)
    ptp_bound = vor.points.ptp(axis=0)

    finite_segments = []
    infinite_segments = []
    for pointidx, simplex in zip(vor.ridge_points, vor.ridge_vertices):
        simplex = np.asarray(simplex)
        if np.all(simplex >= 0):
            finite_segments.append(vor.vertices[simplex])
        else:
            i = simplex[simplex >= 0][0]  # finite end Voronoi vertex

            t = vor.points[pointidx[1]] - vor.points[pointidx[0]]  # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[pointidx].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            # if (vor.furthest_site):  Had to comment this out to bypass error
            if hasattr(vor, 'furthest_site'):
                direction = -direction
            far_point = vor.vertices[i] + direction * ptp_bound.max()

            infinite_segments.append([vor.vertices[i], far_point])

    ax.add_collection(LineCollection(finite_segments,
                                     colors=line_colors,
                                     lw=line_width,
                                     alpha=line_alpha,
                                     linestyle='solid'))
    ax.add_collection(LineCollection(infinite_segments,
                                     colors=line_colors,
                                     lw=line_width,
                                     alpha=line_alpha,
                                     linestyle='solid'))

    _adjust_bounds(ax, vor.points)

    return ax.figure