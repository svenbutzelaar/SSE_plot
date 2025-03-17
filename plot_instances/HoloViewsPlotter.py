from BasePlotter import BasePlotter
from BasePlotter import FileExtension


import holoviews as hv


class HoloViewsPlotter(BasePlotter):
    def line(self, df):
        plot = hv.Curve(df, 'x', 'y')
        html_content = hv.save(plot, fmt='html')
        return html_content.encode('utf-8'), FileExtension.HTML

    def scatter_plot(self, df):
        plot = hv.Scatter(df, 'x', 'y')
        html_content = hv.save(plot, fmt='html')
        return html_content.encode('utf-8'), FileExtension.HTML

    def bar_plot(self, df):
        plot = hv.Bar(df, 'x', 'y')
        html_content = hv.save(plot, fmt='html')
        return html_content.encode('utf-8'), FileExtension.HTML

    def box_plot(self, df):
        plot = hv.BoxWhisker(df, 'x', 'y')
        html_content = hv.save(plot, fmt='html')
        return html_content.encode('utf-8'), FileExtension.HTML

    def heatmap(self, df):
        plot = hv.HeatMap(df)
        html_content = hv.save(plot, fmt='html')
        return html_content.encode('utf-8'), FileExtension.HTML