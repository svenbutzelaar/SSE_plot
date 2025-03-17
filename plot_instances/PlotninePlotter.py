from BasePlotter import BasePlotter
from BasePlotter import FileExtension


import matplotlib.pyplot as plt
import plotnine as p9


import io


class PlotninePlotter(BasePlotter):
    def plot_to_buffer(self, p):
        fig = p.draw()
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png')
        plt.close(fig)
        img_buf.seek(0)
        return img_buf.read(), FileExtension.PNG  # Return binary content and extension

    def line(self, df):
        p = p9.ggplot(df, p9.aes(x="x", y="y")) + p9.geom_line()
        return self.plot_to_buffer(p)

    def scatter_plot(self, df):
        p = p9.ggplot(df, p9.aes(x='x', y='y', color='z')) + p9.geom_point()
        return self.plot_to_buffer(p)

    def bar_plot(self, df):
        p = p9.ggplot(df, p9.aes(x='x', y='y')) + p9.geom_bar(stat='identity')
        return self.plot_to_buffer(p)

    def box_plot(self, df):
        p = p9.ggplot(df, p9.aes(x='x', y='y')) + p9.geom_boxplot()
        return self.plot_to_buffer(p)

    def heatmap(self, df):
        p = p9.ggplot(df, p9.aes(x='x', y='y', fill='z')) + p9.geom_tile()
        return self.plot_to_buffer(p)