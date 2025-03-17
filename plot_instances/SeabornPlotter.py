from BasePlotter import BasePlotter, FileExtension


import matplotlib.pyplot as plt
import seaborn as sns


import io


class SeabornPlotter(BasePlotter):  # Inherit from MatplotlibPlotter
    def line(self, df):
        fig, ax = plt.subplots()
        sns.lineplot(x=df["x"], y=df["y"], ax=ax)
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png')
        plt.close(fig)
        img_buf.seek(0)
        return img_buf.read(), FileExtension.PNG

    def scatter_plot(self, df):
        fig, ax = plt.subplots()
        sns.scatterplot(x=df["x"], y=df["y"], hue=df["z"], ax=ax)
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png')
        plt.close(fig)
        img_buf.seek(0)
        return img_buf.read(), FileExtension.PNG