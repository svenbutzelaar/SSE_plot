from BasePlotter import BasePlotter


import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


import io


class MatplotlibPlotter(BasePlotter):
    def line(self, df):
        fig, ax = plt.subplots()
        ax.plot(df["x"], df["y"])
        return fig

    def bar_plot(self, df):
        fig, ax = plt.subplots()
        ax.bar(df["x"], df["y"])
        return fig

    def box_plot(self, df):
        fig, ax = plt.subplots()
        ax.boxplot([df[df["x"] == cat]["y"] for cat in df["x"].unique()])
        plt.xticks(range(1, len(df["x"].unique()) + 1), df["x"].unique())
        return fig

    def heatmap(self, df):
        fig, ax = plt.subplots()
        sns.heatmap(df, annot=True, ax=ax)
        return fig

    def scatter_plot(self, df):
        fig, ax = plt.subplots()
        ax.scatter(df["x"], df["y"])
        return fig

    def contour_plot(self, df):
        x, y = np.meshgrid(df["x"], df["y"])
        z = np.sin(x) * np.cos(y)
        fig, ax = plt.subplots()
        cs = ax.contour(x, y, z)
        plt.clabel(cs, inline=True)
        return fig
    
    def render_plot(self, fig):
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png')
        plt.close(fig)
        img_buf.seek(0)
        return img_buf.read()
        