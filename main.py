from BasePlotter import PlotType
import data
from plot_factory import PlotFactory


import os


def main():
        # Global setting for saving plots
    save_plots = False  # Change to False to stop saving plots
    output_dir = "output_plots"  # Directory to save the plots when debugging

    # Ensure output directory exists
    if save_plots:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for subfolder in PlotType.list():
            subfolder_path = os.path.join(output_dir, subfolder)
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)

    # ["matplotlib", "seaborn", "plotly", "altair", "plotnine", "pygal", "holoviews", "vispy"]
    libraries = PlotFactory.get_plotters_list()
    # libraries = ["pygal"]

    data_frames = {
        "line": data.get_df_line(),
        "bar": data.get_df_bar(),
        "scatter": data.get_df_scatter(),
        "box": data.get_df_box(),
        "heatmap": data.get_df_heatmap(),
    }

    for lib in libraries:
        print(f"Testing {lib}...")
        plotter = PlotFactory.get_plotter(lib)
        for plot_type, df in data_frames.items():
            plot = plotter.plot(plot_type, df)
            plot_binary = plotter.render_plot(plot)
            plotter_name = lib.capitalize()
            if save_plots:
                plotter.save_plot(plot_binary, f"{output_dir}/{plot_type}/{plotter_name}_{plot_type}.png")
        plotter.close_all()


# Running the factory
if __name__ == "__main__":
    main()