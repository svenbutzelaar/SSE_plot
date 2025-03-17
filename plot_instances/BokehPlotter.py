from BasePlotter import BasePlotter
from BasePlotter import FileExtension


import bokeh.plotting as bkp


import tempfile


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