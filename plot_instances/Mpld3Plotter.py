from BasePlotter import BasePlotter
from BasePlotter import FileExtension


import matplotlib.pyplot as plt
import mpld3
import seaborn as sns


class Mpld3Plotter(BasePlotter):
    def line(self, df):
        fig, ax = plt.subplots()
        ax.plot(df["x"], df["y"])
        return mpld3.fig_to_html(fig).encode('utf-8'), FileExtension.HTML

    def scatter_plot(self, df):
        fig, ax = plt.subplots()
        ax.scatter(df["x"], df["y"], c=df["z"])
        return mpld3.fig_to_html(fig).encode('utf-8'), FileExtension.HTML

    def bar_plot(self, df):
        fig, ax = plt.subplots()
        ax.bar(df["x"], df["y"])
        return mpld3.fig_to_html(fig).encode('utf-8'), FileExtension.HTML

    def box_plot(self, df):
        fig, ax = plt.subplots()
        ax.boxplot([df[df["x"] == cat]["y"] for cat in df["x"].unique()])
        return mpld3.fig_to_html(fig).encode('utf-8'), FileExtension.HTML

    def heatmap(self, df):
        fig, ax = plt.subplots()
        sns.heatmap(df, annot=True, ax=ax)
        return mpld3.fig_to_html(fig).encode('utf-8'), FileExtension.HTML