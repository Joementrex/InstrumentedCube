import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication
from pyqtgraph.opengl import GLViewWidget, GLBoxItem, GLScatterPlotItem

#To do:
# - Implement a close command 

class CubeVisualizer:
    def __init__(self):
        app = QApplication(sys.argv)
        self.view = GLViewWidget()

        # add a delay to make sure the view is initialized before attempting to add content
        self.view.show()

        # Three custom points to make a triangle inside the top face of a cube
        self.point1 = np.array([0.25, 0.75, 1])
        self.point2 = np.array([0.75, 0.75, 1])
        self.point3 = np.array([0.5, 0.25, 1])
        self.points = np.array([self.point1, self.point2, self.point3])

        # Create GLScatterPlotItem using the points array and specifying initial color
        self.point_item = GLScatterPlotItem(pos=self.points, color=(1, 1, 1, 1), size=10)
        self.view.addItem(self.point_item)

        self.cube = GLBoxItem()
        self.view.addItem(self.cube)

        self.view.show()

        # Change point colors every 1000 ms
        timer = pg.QtCore.QTimer()
        timer.timeout.connect(self.change_point_colors)
        timer.start(1000)

        sys.exit(app.exec_())

    def change_point_colors(self):
        # Change point colors dynamically during runtime
        new_colors = np.random.rand(3, 4)  # Generate random RGB and A values
        print(new_colors)
        self.point_item.setData(color=new_colors, size=10)

        [[0.247, 0.247, 0.247, 1], [0.148, 0.148, 0.148, 1], [0.123, 0.123, 0.123, 1]]

    # function to change the points colour with a given matrix of colours
    def change_point_colors_matrix(self, new_colors):
        self.point_item.setData(color=new_colors, size=10)

    # function that will close the program when the button q is pressed
    def close_program(self):
        print("Program closed")
        sys.exit(app.exec_())

if __name__ == '__main__':
    visualizer = CubeVisualizer()

 
