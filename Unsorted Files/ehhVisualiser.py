import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import time

def update_colors_and_positions(ax, faces, point_colors):
    while True:
        for i, face in enumerate(faces):
            center = np.mean(face, axis=0)
            for j, coord in enumerate(face):
                edge_point = (coord + center) / 2
                ax.scatter(edge_point[0], edge_point[1], edge_point[2], color=point_colors[j], s=30)
            ax.scatter(center[0], center[1], center[2], color='black', s=50)
            plt.pause(5)
            ax.cla()  # Clear current plot

def main():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Define vertices of the cube
    vertices = [
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 1, 1]
    ]

    # Define faces of the cube
    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],
        [vertices[4], vertices[5], vertices[6], vertices[7]],
        [vertices[0], vertices[4], vertices[5], vertices[1]],
        [vertices[2], vertices[6], vertices[7], vertices[3]],
        [vertices[1], vertices[5], vertices[6], vertices[2]],
        [vertices[0], vertices[4], vertices[7], vertices[3]]
    ]

    # Define colors for points
    point_colors = ['red', 'green', 'blue', 'yellow', 'purple']

    # Create a thread to update colors and positions
    import threading
    update_thread = threading.Thread(target=update_colors_and_positions, args=(ax, faces, point_colors))
    update_thread.start()

    plt.show()

if __name__ == '__main__':
    main()
