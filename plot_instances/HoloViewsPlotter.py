import holoviews as hv
import io
from BasePlotter import BasePlotter

# Ensure Matplotlib is set as the backend for rendering PNGs
hv.extension("matplotlib")

class HoloViewsPlotter(BasePlotter):
    def line(self, df):
        return hv.Curve(df, "x", "y")

    def scatter_plot(self, df):
        return hv.Scatter(df, "x", "y")

    def bar_plot(self, df):
        return hv.Bars(df, "x", "y")

    def box_plot(self, df):
        return hv.BoxWhisker(df, "x", "y")

    def heatmap(self, df):
        return hv.HeatMap(df)

    def render_plot(self, plot):
        """Render the HoloViews plot as a PNG."""
        img_buffer = io.BytesIO()
        hv.save(plot, img_buffer, fmt="png")
        img_buffer.seek(0)
        return img_buffer.read()