import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication
from pyqtgraph.opengl import GLViewWidget, GLBoxItem, GLScatterPlotItem

class CubeVisualizer:
    def __init__(self):
        app = QApplication(sys.argv)
        self.view = GLViewWidget()

        self.cube = GLBoxItem()
        self.view.addItem(self.cube)

        # Define cube vertices
        vertices = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [1, 1, 0],
            [0, 1, 0],
            [0, 0, 1],
            [1, 0, 1],
            [1, 1, 1],
            [0, 1, 1]
        ])

        # Define cube faces
        faces = np.array([
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [0, 4, 5, 1],
            [2, 6, 7, 3],
            [1, 5, 6, 2],
            [0, 4, 7, 3]
        ])

        # Define colors for each face point
        colors = np.array([
            [1, 0, 0, 0.3],
            [0, 1, 0, 0.3],
            [0, 0, 1, 0.3],
            [1, 1, 0, 0.3],
            [1, 0, 1, 0.3],
            [0, 1, 1, 0.3]
        ])

        # Draw points
        for i, face in enumerate(faces):
            center = vertices[face].mean(axis=0)
            color = colors[i]
            point = GLScatterPlotItem(pos=center, color=color, size=10)
            self.view.addItem(point)
            # now the centre point is drawn, draw other points to make it look like a 5 on a dice
            # travel half way to the centre point from each vertex
            for vertex in vertices[face]:
                point = GLScatterPlotItem(pos=(vertex + center) / 2, color=color, size=10)
                self.view.addItem(point)


        self.view.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    visualizer = CubeVisualizer()
