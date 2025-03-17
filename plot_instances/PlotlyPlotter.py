from BasePlotter import BasePlotter
from BasePlotter import FileExtension


import plotly.express as px


class PlotlyPlotter(BasePlotter):
    def line(self, df):
        fig = px.line(df, x="x", y="y")
        fig_content = fig.to_html(full_html=False).encode('utf-8')
        return fig_content, FileExtension.HTML  # Return HTML binary content and extension

    def scatter_plot(self, df):
        fig = px.scatter(df, x="x", y="y", color="z")
        fig_content = fig.to_html(full_html=False).encode('utf-8')
        return fig_content, FileExtension.HTML

    def bar_plot(self, df):
        fig = px.bar(df, x="x", y="y")
        fig_content = fig.to_html(full_html=False).encode('utf-8')
        return fig_content, FileExtension.HTML

    def box_plot(self, df):
        fig = px.box(df, x="x", y="y")
        fig_content = fig.to_html(full_html=False).encode('utf-8')
        return fig_content, FileExtension.HTML

    def heatmap(self, df):
        fig = px.imshow(df, text_auto=True)
        fig_content = fig.to_html(full_html=False).encode('utf-8')
        return fig_content, FileExtension.HTML