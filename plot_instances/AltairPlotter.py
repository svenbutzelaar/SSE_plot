from BasePlotter import BasePlotter


import altair as alt
import vl_convert as vlc
from PIL import Image


import io


class AltairPlotter(BasePlotter):
    def line(self, df):
        chart = alt.Chart(df).mark_line().encode(x='x', y='y')
        return chart

    def scatter_plot(self, df):
        chart = alt.Chart(df).mark_point().encode(x='x', y='y', color='z')
        return chart

    def bar_plot(self, df):
        chart = alt.Chart(df).mark_bar().encode(x='x', y='y')
        return chart

    def box_plot(self, df):
        chart = alt.Chart(df).mark_boxplot().encode(x='x', y='y')
        return chart

    def heatmap(self, df):
        chart = alt.Chart(df).mark_rect().encode(
            x='x:O', y='y:O', color='z:Q')
        return chart

    def render_plot(self, chart):

        # Convert chart to PNG using vl-convert-python
        png_data = vlc.vegalite_to_png(chart.to_dict())

        # Display image
        buffer = io.BytesIO(png_data)
        image = Image.open(buffer)
        image.show()

        return buffer.getvalue()