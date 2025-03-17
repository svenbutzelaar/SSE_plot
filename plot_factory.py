
from BasePlotter import BasePlotter
from plot_instances.AltairPlotter import AltairPlotter
from plot_instances.BokehPlotter import BokehPlotter
from plot_instances.HoloViewsPlotter import HoloViewsPlotter
from plot_instances.MatplotlibPlotter import MatplotlibPlotter
from plot_instances.Mpld3Plotter import Mpld3Plotter
from plot_instances.PlotlyPlotter import PlotlyPlotter
from plot_instances.PlotninePlotter import PlotninePlotter
from plot_instances.PygalPlotter import PygalPlotter
from plot_instances.SeabornPlotter import SeabornPlotter
from plot_instances.VisPyPlotter import VisPyPlotter

class PlotFactory:
    @staticmethod
    def get_plotter(library) -> BasePlotter:
        plotters = {
            "matplotlib": MatplotlibPlotter,
            "seaborn": SeabornPlotter,
            "plotly": PlotlyPlotter,
            "bokeh": BokehPlotter,
            "altair": AltairPlotter,
            "plotnine": PlotninePlotter,
            "pygal": PygalPlotter,
            "holoviews": HoloViewsPlotter,
            "vispy": VisPyPlotter,
            "mpld3": Mpld3Plotter,
        }
        return plotters[library]()
