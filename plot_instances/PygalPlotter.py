import io

import cairosvg
from BasePlotter import BasePlotter


import pygal


class PygalPlotter(BasePlotter):
    def line(self, df):
        chart = pygal.Line()
        chart.add("sin(x)", df["y"].tolist())  # Ensure this is a list of numbers
        return chart

    def scatter_plot(self, df):
        chart = pygal.XY()
        chart.add("Scatter plot", [(float(x), float(y)) for x, y in zip(df["x"], df["y"])])  # Convert to float
        return chart

    def bar_plot(self, df):
        chart = pygal.Bar()
        chart.add("Bar plot", df["y"].tolist())  # Pass only values, not tuples
        chart.x_labels = df["x"].astype(str).tolist()  # Explicitly set x_labels
        return chart
    
    def heatmap(self, df):
        """Simulate a heatmap using an XY chart with varying dot sizes."""
        chart = pygal.XY(stroke=False)
        chart.title = "Simulated Heatmap"

        # Normalize sizes
        max_size = 20
        min_size = 5
        z_min, z_max = df["z"].min(), df["z"].max()

        def scale_size(z):
            return min_size + (max_size - min_size) * ((z - z_min) / (z_max - z_min))

        # Add points with scaled sizes
        heatmap_data = [{"value": (x, y), "node": {"r": scale_size(z)}} for x, y, z in zip(df["x"], df["y"], df["z"])]
        chart.add("Heatmap", heatmap_data)
        return chart

    def box_plot(self, df):
        """Pygal does not have a native box plot, so we approximate using a grouped bar chart."""
        chart = pygal.Box()
        chart.add("Box", df["y"].tolist())  # Box plots require a list of values
        return chart

    def render_plot(self, chart):
        """Render Pygal charts as PNG binary content."""
        svg_content = chart.render()  # Get SVG as bytes (not a string)

        img_buffer = io.BytesIO()
        
        # Convert SVG to PNG and write to buffer
        cairosvg.svg2png(bytestring=svg_content, write_to=img_buffer)
        
        return img_buffer.getvalue()  # Return PNG binary content