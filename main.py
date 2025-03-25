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
    num_experiments = 30

    # Global setting for saving plots
    save_plots = True # Change to False to stop saving plots
    output_dir = "output_plots" # Directory to save the plots when debugging

    # Ensure output directory exists
    if save_plots:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for subfolder in PlotType.list():
            subfolder_path = os.path.join(output_dir, subfolder)
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)

    # ["matplotlib", "seaborn", "plotly", "plotnine", "pygal", "holoviews"]
    libraries = PlotFactory.get_plotters_list()
    # libraries = ["pygal"]

    data_frames = {
        "line": data.get_df_line(),
        "bar": data.get_df_bar(),
        "scatter": data.get_df_scatter(),
        "box": data.get_df_box(),
        "heatmap": data.get_df_heatmap(),
    }

    energibridge = EnergiBridgeManager()
    energibridge.setup_service()

    for experiment in range(1, num_experiments + 1):
        print(f"Starting iteration {experiment}/{num_experiments}...")

        # Shuffle libraries for each iteration to ensure random order
        random.shuffle(libraries)

        for i, lib in enumerate(libraries):
            print(f"Experiment {experiment}, Test {i + 1}/{len(libraries)}: Testing {lib}...")
            plotter = PlotFactory.get_plotter(lib)

            iteration_name = f"Experiment_{experiment}_{i + 1}_{lib}.csv"
            energibridge.start(iteration_name)

            for plot_type, df in data_frames.items():
                print(f"Plotting {plot_type}...")
                plot = plotter.plot(plot_type, df)
                plot_binary = plotter.render_plot(plot)

                if save_plots:
                    plotter_name = lib.capitalize()
                    plotter.save_plot(plot_binary, f"{output_dir}/{plot_type}/{plotter_name}_{plot_type}.png")

            energibridge.stop()

            plotter.close_all()
            plt.close("all")

        # Wait for 60 seconds between test runs
        time.sleep(60)

# Running the factory
if __name__ == "__main__":
    main()