""" Widget that allows to show maps of results in GUI """

from PySide2.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.figure import Figure

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors


class MplWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)

    def make_map(self, data):

        self.canvas.axes.clear()
        fig, ax = plt.subplots(1, 2)
        cmap = cm.get_cmap(name='jet', lut=40)
        norm = matplotlib.colors.Normalize()
        mappable = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
        mappable.set_array(data)
        mappable.autoscale()
        matplotlib.pyplot.colorbar(mappable, ax[1])
        ax[0].imshow(data, extent=(0, 50, 0, 50), interpolation='hermite', cmap=cmap)
        mappable.changed()
        self.canvas.axes.plot(ax)
        self.canvas.draw()
