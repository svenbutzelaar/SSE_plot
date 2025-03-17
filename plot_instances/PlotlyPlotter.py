from BasePlotter import BasePlotter
import plotly.express as px

class PlotlyPlotter(BasePlotter):
    def line(self, df):
        fig = px.line(df, x="x", y="y")
        return fig

    def scatter_plot(self, df):
        fig = px.scatter(df, x="x", y="y", color="z")
        return fig

    def bar_plot(self, df):
        fig = px.bar(df, x="x", y="y")
        return fig

    def box_plot(self, df):
        fig = px.box(df, x="x", y="y")
        return fig

    def heatmap(self, df):
        fig = px.imshow(df, text_auto=True)
        return fig

    def render_plot(self, fig):
        # Convert the Plotly figure to a PNG image
        img_bytes = fig.to_image(format="png")

        # Return the binary content of the PNG image
        return img_bytes