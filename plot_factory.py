import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import bokeh.plotting as bkp
import altair as alt
import plotnine as p9
import pygal
import holoviews as hv
import vispy.scene
import mpld3
import pandas as pd
import numpy as np
import tempfile
import time
import io
from enum import Enum

import data

# Global setting for saving plots
save_plots = True  # Change to False to stop saving plots
output_dir = "output_plots"  # Directory to save the plots when debugging

# Ensure output directory exists
if save_plots:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for subfolder in ["line", "bar", "scatter", "box", "heatmap"]:
        subfolder_path = f"{output_dir}\\{subfolder}"
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)

# Sample dataset
df = pd.DataFrame({
    "x": np.linspace(0, 10, 100),
    "y": np.sin(np.linspace(0, 10, 100)),
    "z": np.random.randn(100),
    "category": np.random.choice(['A', 'B', 'C'], 100),
})

# Enum for file extensions
class FileExtension(Enum):
    PNG = ".png"
    HTML = ".html"
    SVG = ".svg"

class PlotFactory:
    @staticmethod
    def get_plotter(library):
        plotters = {
            "matplotlib": MatplotlibPlotter,
            "seaborn": SeabornPlotter,
            "plotly": PlotlyPlotter,
            "bokeh": BokehPlotter,
            "altair": AltairPlotter,
            "plotnine": PlotninePlotter,
            "pygal": PygalPlotter,
            "holoviews": HoloViewsPlotter,
            "vispy": VisPyPlotter,
            "mpld3": Mpld3Plotter,
        }
        return plotters[library]()

class BasePlotter:
    def line(self, df):
        raise NotImplementedError
    
    def get_time_to_wait(self):
        return 5
    
    def save_plot(self, content, plotter_name, file_extension):
        """ Helper function to handle saving and rendering plots in the background """
        if save_plots:
            file_path = os.path.join(output_dir, f"{plotter_name}{file_extension.value}")
            with open(file_path, 'wb') as f:
                f.write(content)
            print(f"Plot saved as: {file_path}")
        else:
            print(f"Plot rendered by {plotter_name}, but saving is disabled.")
    
    def render_plot(self):
        """ Returns the rendered plot as binary content and its extension. """
        raise NotImplementedError

# Matplotlib
class MatplotlibPlotter(BasePlotter):
    def line(self, df):
        fig, ax = plt.subplots()
        ax.plot(df["x"], df["y"])  # Line plot
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png')
        plt.close(fig)
        img_buf.seek(0)
        return img_buf.read(), FileExtension.PNG  # Return binary content and extension

    def bar_plot(self, df):
        fig, ax = plt.subplots()
        ax.bar(df["x"], df["y"])
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png')
        plt.close(fig)
        img_buf.seek(0)
        return img_buf.read(), FileExtension.PNG

    def box_plot(self, df):
        fig, ax = plt.subplots()
        ax.boxplot([df[df["x"] == cat]["y"] for cat in df["x"].unique()])
        plt.xticks(range(1, len(df["x"].unique()) + 1), df["x"].unique())
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png')
        plt.close(fig)
        img_buf.seek(0)
        return img_buf.read(), FileExtension.PNG

    def heatmap(self, df):
        fig, ax = plt.subplots()
        sns.heatmap(df, annot=True, ax=ax)
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png')
        plt.close(fig)
        img_buf.seek(0)
        return img_buf.read(), FileExtension.PNG

    def scatter_plot(self, df):
        fig, ax = plt.subplots()
        ax.scatter(df["x"], df["y"])
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png')
        plt.close(fig)
        img_buf.seek(0)
        return img_buf.read(), FileExtension.PNG

    def contour_plot(self, df):
        x, y = np.meshgrid(df["x"], df["y"])
        z = np.sin(x) * np.cos(y)
        fig, ax = plt.subplots()
        cs = ax.contour(x, y, z)
        plt.clabel(cs, inline=True)
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png')
        plt.close(fig)
        img_buf.seek(0)
        return img_buf.read(), FileExtension.PNG

# Seaborn
class SeabornPlotter(MatplotlibPlotter):  # Inherit from MatplotlibPlotter
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

# Plotly
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

# Bokeh
class BokehPlotter(BasePlotter):
    def line(self, df):
        p = bkp.figure(title="Bokeh Line Plot")
        p.line(df["x"], df["y"])

        # Use a temporary file to store the content
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
            file_path = f.name
            bkp.output_file(file_path)  # Now pass the file path to output_file
            bkp.save(p, filename=file_path)  # Save the plot to the temporary file
            with open(file_path, 'rb') as file:
                file_content = file.read()  # Read the content of the file

        return file_content, FileExtension.HTML

    def scatter_plot(self, df):
        p = bkp.figure(title="Bokeh Scatter Plot")
        p.scatter(df["x"], df["y"], color=df["z"])
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
            file_path = f.name
            bkp.output_file(file_path)
            bkp.save(p, filename=file_path)
            with open(file_path, 'rb') as file:
                file_content = file.read()

        return file_content, FileExtension.HTML

    def bar_plot(self, df):
        p = bkp.figure(title="Bokeh Bar Plot")
        p.vbar(x=df["x"], top=df["y"], width=0.9)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
            file_path = f.name
            bkp.output_file(file_path)
            bkp.save(p, filename=file_path)
            with open(file_path, 'rb') as file:
                file_content = file.read()

        return file_content, FileExtension.HTML

    def heatmap(self, df):
        p = bkp.figure(title="Bokeh Heatmap")
        # Heatmap code here (using quad or rect glyphs to represent heatmap)
        # Dummy implementation for illustration
        p.rect(x=df["x"], y=df["y"], width=0.1, height=0.1, color="green")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
            file_path = f.name
            bkp.output_file(file_path)
            bkp.save(p, filename=file_path)
            with open(file_path, 'rb') as file:
                file_content = file.read()

        return file_content, FileExtension.HTML

# Altair
class AltairPlotter(BasePlotter):
    def line(self, df):
        chart = alt.Chart(df).mark_line().encode(x='x', y='y')
        html_content = chart.to_html()
        return html_content.encode('utf-8'), FileExtension.HTML

    def scatter_plot(self, df):
        chart = alt.Chart(df).mark_point().encode(x='x', y='y', color='z')
        html_content = chart.to_html()
        return html_content.encode('utf-8'), FileExtension.HTML

    def bar_plot(self, df):
        chart = alt.Chart(df).mark_bar().encode(x='x', y='y')
        html_content = chart.to_html()
        return html_content.encode('utf-8'), FileExtension.HTML

    def box_plot(self, df):
        chart = alt.Chart(df).mark_boxplot().encode(x='x', y='y')
        html_content = chart.to_html()
        return html_content.encode('utf-8'), FileExtension.HTML

    def heatmap(self, df):
        chart = alt.Chart(df).mark_rect().encode(
            x='x:O', y='y:O', color='z:Q')
        html_content = chart.to_html()
        return html_content.encode('utf-8'), FileExtension.HTML

# Plotnine
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

# Pygal
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

# HoloViews
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

# VisPy
class VisPyPlotter(BasePlotter):
    def line(self, df):
        canvas = vispy.scene.SceneCanvas(keys='interactive')
        view = canvas.central_widget.add_view()
        plot = vispy.scene.visuals.Line(pos=np.column_stack((df['x'], df['y'])))
        canvas.show()
        return b"VisPy Line plot", FileExtension.PNG

# Mpld3
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

# Running the factory
if __name__ == "__main__":
    libraries = ["matplotlib", "seaborn", "plotly", "bokeh", "altair", "plotnine", "pygal", "holoviews", "vispy", "mpld3"]

    df_line = data.get_df_line()
    df_bar = data.get_df_bar()
    df_scatter = data.get_df_scatter()
    df_box = data.get_df_box()
    df_heatmap = data.get_df_heatmap()
    
    for lib in libraries:
        print(f"Testing {lib}...")
        plotter = PlotFactory.get_plotter(lib)
        
        plot_binary, extension = plotter.line(df)  # Line plot (default)
        plotter_name = lib.capitalize()  # Use the capitalized name of the plotter
        plotter.save_plot(plot_binary, f"line/{plotter_name}line", extension)  # Save or ignore

        # Testing additional plot types
        if hasattr(plotter, 'bar_plot'):
            plot_binary, extension = plotter.bar_plot(df_bar)
            plotter.save_plot(plot_binary, f"bar/{plotter_name}_bar", extension)

        if hasattr(plotter, 'scatter_plot'):
            plot_binary, extension = plotter.scatter_plot(df_scatter)
            plotter.save_plot(plot_binary, f"scatter/{plotter_name}_scatter", extension)

        if hasattr(plotter, 'box_plot'):
            plot_binary, extension = plotter.box_plot(df_box)
            plotter.save_plot(plot_binary, f"box/{plotter_name}_box", extension)

        if hasattr(plotter, 'heatmap'):
            plot_binary, extension = plotter.heatmap(df_heatmap)
            plotter.save_plot(plot_binary, f"heatmap/{plotter_name}_heatmap", extension)
