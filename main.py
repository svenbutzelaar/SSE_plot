from BasePlotter import PlotType
from energibridge_manager import EnergiBridgeManager
from plot_factory import PlotFactory
import matplotlib.pyplot as plt
import random
import time
import data
import os


def main():
    # number of iterations of the experiment
    num_iterations = 30

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

    # Create a random shuffle for the usage of the different libraries
    test_queue = libraries * num_iterations
    random.shuffle(test_queue)

    data_frames = {
        "line": data.get_df_line(),
        "bar": data.get_df_bar(),
        "scatter": data.get_df_scatter(),
        "box": data.get_df_box(),
        "heatmap": data.get_df_heatmap(),
    }

    energibridge = EnergiBridgeManager()
    energibridge.setup_service()

    for i, lib in enumerate(test_queue):

        print(f"Iteration {i + 1}/{len(test_queue)}: Testing {lib}...")
        plotter = PlotFactory.get_plotter(lib)

        iteration_name = f"Iteration_{i + 1}_{lib}.csv"
        energibridge.start(iteration_name)

        for plot_type, df in data_frames.items():
            plot = plotter.plot(plot_type, df)

            if save_plots:
                plot_binary = plotter.render_plot(plot)
                plotter_name = lib.capitalize()
                plotter.save_plot(plot_binary, f"{output_dir}/{plot_type}/{plotter_name}_{plot_type}.png")

        plotter.close_all()
        plt.close("all")

        energibridge.stop()
        time.sleep(2)


# Running the factory
if __name__ == "__main__":
    main()