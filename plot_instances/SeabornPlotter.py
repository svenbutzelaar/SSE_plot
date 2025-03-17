from BasePlotter import BasePlotter


import matplotlib.pyplot as plt
import seaborn as sns


import io

class SeabornPlotter(BasePlotter):
    def line(self, df):
        fig, ax = plt.subplots()
        sns.lineplot(x=df["x"], y=df["y"], ax=ax)
        return fig

    def scatter_plot(self, df):
        fig, ax = plt.subplots()
        sns.scatterplot(x=df["x"], y=df["y"], hue=df["z"], ax=ax)
        return fig

    def bar_plot(self, df):
        fig, ax = plt.subplots()
        sns.barplot(x=df["x"], y=df["y"], ax=ax)
        return fig

    def box_plot(self, df):
        fig, ax = plt.subplots()
        sns.boxplot(x=df["x"], y=df["y"], ax=ax)
        return fig

    def heatmap(self, df):
        fig, ax = plt.subplots()
        sns.heatmap(df, annot=True, ax=ax)
        return fig

    def render_plot(self, fig):
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png')
        plt.close(fig)
        img_buf.seek(0)
        return img_buf.read()