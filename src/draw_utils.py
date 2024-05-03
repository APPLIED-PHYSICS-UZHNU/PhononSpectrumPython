import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np
import matplotlib.pyplot as plt

def draw_positions(flattened_positions):
    plt.rcParams['grid.color'] = (0.1, 0.1, 0.1, 0.1)
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(projection='3d')
    ax.azim = 0
    ax.dist = 10
    ax.elev = 90
    transparency = False
    # transparency = True
    size_a = 1
    color_a = '#666666'
    color_a_border = 'black'
    atoms_positions = np.array(flattened_positions)
    ax.scatter(atoms_positions[:, 0], atoms_positions[:, 1], atoms_positions[:, 2], s=size_a * 100, c=color_a, edgecolors=color_a_border, depthshade=transparency)