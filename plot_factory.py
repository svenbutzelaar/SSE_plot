
from typing import List
from BasePlotter import BasePlotter
from plot_instances.AltairPlotter import AltairPlotter
from plot_instances.BokehPlotter import BokehPlotter
from plot_instances.HoloViewsPlotter import HoloViewsPlotter
from plot_instances.MatplotlibPlotter import MatplotlibPlotter
from plot_instances.PlotlyPlotter import PlotlyPlotter
from plot_instances.PlotninePlotter import PlotninePlotter
from plot_instances.PygalPlotter import PygalPlotter
from plot_instances.SeabornPlotter import SeabornPlotter

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
        }
        return plotters[library]()
    
    @staticmethod
    def get_plotters_list() -> List[str]:
        return ["matplotlib", "seaborn", "plotly", "bokeh", "altair", "plotnine", "pygal", "holoviews"]
