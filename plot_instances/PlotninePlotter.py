from BasePlotter import BasePlotter


import matplotlib.pyplot as plt
import plotnine as p9


import io


class PlotninePlotter(BasePlotter):
    def render_plot(self, p):
        fig = p.draw()
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png')
        plt.close(fig)
        img_buf.seek(0)
        return img_buf.read()

    def line(self, df):
        return p9.ggplot(df, p9.aes(x="x", y="y")) + p9.geom_line()

    def scatter_plot(self, df):
        return p9.ggplot(df, p9.aes(x='x', y='y', color='z')) + p9.geom_point()

    def bar_plot(self, df):
        return p9.ggplot(df, p9.aes(x='x', y='y')) + p9.geom_bar(stat='identity')

    def box_plot(self, df):
        return p9.ggplot(df, p9.aes(x='x', y='y')) + p9.geom_boxplot()

    def heatmap(self, df):
        return p9.ggplot(df, p9.aes(x='x', y='y', fill='z')) + p9.geom_tile()