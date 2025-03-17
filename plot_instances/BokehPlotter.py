import io
import tempfile
from BasePlotter import BasePlotter


import bokeh.plotting as bkp
from bokeh.io import export_png
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class BokehPlotter(BasePlotter):
    def __init__(self):
        # Configure Chrome to run in headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
        chrome_options.add_argument("--no-sandbox")  # Disable sandboxing
        self.driver = webdriver.Chrome(options=chrome_options)
        super().__init__()
    
    def close_all(self):
        self.driver.quit()
        return super().close_all()

    def line(self, df):
        p = bkp.figure(title="Bokeh Line Plot", x_axis_label="x", y_axis_label="y",
               x_range=(df["x"].min(), df["x"].max()),
               y_range=(df["y"].min(), df["y"].max()))
        p.line(df["x"], df["y"], legend_label="Line", line_width=2)
        return p

    def scatter_plot(self, df):
        p = bkp.figure(title="Bokeh Scatter Plot", x_axis_label="x", y_axis_label="y",
               x_range=(df["x"].min(), df["x"].max()),
               y_range=(df["y"].min(), df["y"].max()))
        p.scatter(df["x"], df["y"], fill_color=df["z"], size=10, legend_label="Scatter")
        return p

    def bar_plot(self, df):
        p = bkp.figure(title="Bokeh Bar Plot", x_axis_label="x", y_axis_label="y",
               x_range=(df["x"].min(), df["x"].max()),
               y_range=(df["y"].min(), df["y"].max()))
        p.vbar(x=df["x"], top=df["y"], width=0.5, legend_label="Bar", color="blue")
        return p

    def box_plot(self, df):
        # Bokeh does not have a built-in box plot, so we use a workaround
        p = bkp.figure(title="Bokeh Box Plot", x_axis_label="x", y_axis_label="y",
               x_range=(df["x"].min(), df["x"].max()),
               y_range=(df["y"].min(), df["y"].max()))
        # Dummy implementation for illustration
        p.rect(x=df["x"], y=df["y"], width=0.1, height=0.1, color="orange", legend_label="Box")
        return p

    def heatmap(self, df):
        p = bkp.figure(title="Bokeh Heatmap", x_axis_label="x", y_axis_label="y",
               x_range=(df["x"].min(), df["x"].max()),
               y_range=(df["y"].min(), df["y"].max()))
        # Heatmap implementation using rect glyphs
        p.rect(x=df["x"], y=df["y"], width=1, height=1, fill_color="green", line_color=None)
        return p

    def render_plot(self, p):
        # Create a temporary file for storing the PNG output
        with tempfile.NamedTemporaryFile(suffix=".png", delete=True) as tmpfile:
            # Export the plot to the temporary file
            export_png(p, filename=tmpfile.name, webdriver=self.driver)

            # Read the image back into a BytesIO buffer
            with open(tmpfile.name, "rb") as f:
                img_buffer = io.BytesIO(f.read())

        # Return the binary content of the PNG image
        return img_buffer.getvalue()