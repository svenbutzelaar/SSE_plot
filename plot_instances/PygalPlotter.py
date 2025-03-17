from BasePlotter import BasePlotter
from BasePlotter import FileExtension


import pygal


class PygalPlotter(BasePlotter):
    def line(self, df):
        line_chart = pygal.Line()
        line_chart.add("sin(x)", df["y"].tolist())
        svg_content = line_chart.render()
        return svg_content, FileExtension.SVG  # Return SVG binary content and extension

    def scatter_plot(self, df):
        chart = pygal.XY()
        chart.add('Scatter plot', [(x, y) for x, y in zip(df['x'], df['y'])])
        chart_content = chart.render()
        return chart_content, FileExtension.SVG

    def bar_plot(self, df):
        chart = pygal.Bar()
        chart.add('Bar plot', [(category, value) for category, value in zip(df['x'], df['y'])])
        chart_content = chart.render()
        return chart_content, FileExtension.SVG

    def heatmap(self, df):
        chart = pygal.Heatmap()
        chart.add('Heatmap', df.values.tolist())
        chart_content = chart.render()
        return chart_content, FileExtension.SVG