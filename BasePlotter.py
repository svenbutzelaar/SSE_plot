from enum import Enum


class BasePlotter:
    def plot(self, plot_type, df):
        """
        Main entry point for plotting functionality.

        Args:
            plot_type (str): The type of plot to generate ("line", "scatter", "bar", "box", "heatmap")
            df (DataFrame): The dataframe to plot

        Returns:
            The rendered plot object
        """
        plot_methods = {
            "line": self.line,
            "scatter": self.scatter_plot,
            "bar": self.bar_plot,
            "box": self.box_plot,
            "heatmap": self.heatmap
        }

        if plot_type not in plot_methods:
            raise ValueError(f"Unsupported plot type: {plot_type}. Supported types: {', '.join(plot_methods.keys())}")

        return plot_methods[plot_type](df)

    def save_plot(self, content, file_path):
        """ Helper function to handle saving and rendering plots in the background """
        with open(file_path, 'wb') as f:
            f.write(content)
        print(f"Plot saved as: {file_path}")

    def render_plot(self, chart):
        """ Returns the rendered plot as binary content and its extension. """
        return chart


    def line(self, df):
        raise NotImplementedError

    def scatter_plot(self, df):
        raise NotImplementedError

    def bar_plot(self, df):
        raise NotImplementedError

    def box_plot(self, df):
        raise NotImplementedError

    def heatmap(self, df):
        raise NotImplementedError


# Enum for file extensions
class FileExtension(Enum):
    PNG = ".png"
    HTML = ".html"


class PlotType(Enum):
    LINE = "line"
    BAR = "bar"
    SCATTER = "scatter"
    BOX = "box"
    HEATMAP = "heatmap"

    @classmethod
    def list(cls):
        """Returns a list of all plot type values"""
        return [t.value for t in cls]

    @classmethod
    def from_string(cls, s):
        """Convert string to enum member, case-insensitive"""
        try:
            return cls(s.lower())
        except ValueError:
            valid_types = ", ".join(cls.list())
            raise ValueError(f"Invalid plot type: '{s}'. Valid types are: {valid_types}")