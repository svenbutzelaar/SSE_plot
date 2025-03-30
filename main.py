from datetime import datetime
from BasePlotter import PlotType
from energibridge_manager import EnergiBridgeManager
from plot_factory import PlotFactory
import matplotlib.pyplot as plt
import logging
import random
import time
import data
import os

# Simple implementation of the fibonacci sequence used for warm up
def fibonacci(n):
  if n <= 1:
    return n
  else:
    return fibonacci(n-1) + fibonacci(n-2)

# Do some warm up before actually running the experiment
# The warm-up is done by running a CPU intensive task (fibonacci)
def warm_up():
  print("Start warm up")
  # Warm up for 5 minutes
  warm_up_time = 300
  start_time = time.time()

  i = 1
  while time.time() - start_time < warm_up_time:
    print(fibonacci(i), " ")
    i = i + 1

  print("Warm up completed")
  time.sleep(1)

  return

def main():
    # number of iterations of the experiment
    num_experiments = 30

    # Global setting for saving plots
    save_plots = False # Change to False to stop saving plots
    output_dir = "output_plots" # Directory to save the plots when debugging

    # Ensure output directory exists
    if save_plots:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for subfolder in PlotType.list():
            subfolder_path = os.path.join(output_dir, subfolder)
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)

    logging.basicConfig(filename="log.txt", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    msg = f"Starting measurements at {current_time}."
    print(msg)
    logging.info(msg)

    for experiment in range(1, num_experiments + 1):
        msg = f"# Starting experiment {experiment}/{num_experiments}..."
        print(msg)
        logging.info(msg)

        # Shuffle libraries for each iteration to ensure random order
        random.shuffle(libraries)
        for i, lib in enumerate(libraries):
            msg = f"Experiment {experiment}, Test {i + 1}/{len(libraries)}: Testing {lib}..."
            print(msg)
            logging.info(msg)

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
        msg = "# Starting Pause..."
        print(msg)
        logging.info(msg)

        output_file_name = f"Pause_{experiment}.csv"
        energibridge.start(output_file_name)
        time.sleep(60)
        energibridge.stop()

        msg = f"# Finished experiment {experiment}/{num_experiments}..."
        print(msg)
        logging.info(msg)

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    msg = f"Finishing measurements at {current_time}."
    print(msg)
    logging.info(msg)

# Running the factory
if __name__ == "__main__":
    warm_up()
    main()