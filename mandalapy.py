from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from math import pi

"""This function creates mandalas (adaptation from fronkonstin R code)

Change the function _plotutils.py from scipy spatial functions.
In the line 225 of the code (highlighted on the link), change: linestyle = 'dashed' to linestyle = 'solid', and save the function.

Link to the scipy repository:
https://github.com/scipy/scipy/blob/master/scipy/spatial/_plotutils.py#L225

"""

#Modify the following parameters in order to get different figures
it = 4 #Number of iterations (how many times the equidistant points will be generated)
points = 5 #Number of points to draw
radius = 2 #Factor of expansion or compression
f1,f2 = 10,10 #Figure size

def MandalaPy(it,points,radius):
    angles = np.linspace(0,2*pi*(1-1/points), points) + pi/2
    x,y = 0,0
    df = pd.DataFrame([[x,y]], columns = ['x','y']) #Initial center
    #Itearate over centers
    for k in range(it):
        t1 = np.array([])
        t2 = np.array([])
        for i in range(df.shape[0]):
            t1 = np.append(t1,df['x'][i]+radius**(k)*np.cos(angles))
            t2 = np.append(t2,df['y'][i]+radius**(k)*np.sin(angles))
        df = pd.DataFrame(np.column_stack((t1,t2)), columns = ['x','y'])
    mandala = Voronoi(df)
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0], fig_size[1] = f1,f2
    voronoi_plot_2d(mandala, show_points = False, show_vertices = False, ), plt.axis('off'), plt.savefig('mandala1.png', dpi = 100)
    return plt.show()

print(MandalaPy(it,points,radius))


plt.savefig('my_mandala.png', dpi = 80)
