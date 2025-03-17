from BasePlotter import BasePlotter
from BasePlotter import FileExtension


import numpy as np
import vispy.scene


class VisPyPlotter(BasePlotter):
    def line(self, df):
        canvas = vispy.scene.SceneCanvas(keys='interactive')
        view = canvas.central_widget.add_view()
        plot = vispy.scene.visuals.Line(pos=np.column_stack((df['x'], df['y'])))
        canvas.show()
        return b"VisPy Line plot", FileExtension.PNG