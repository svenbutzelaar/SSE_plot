# 🎨 Experiment Automation with Plotting Libraries 🚀

## Overview
This script automates experiments to benchmark various Python plotting libraries. It integrates with the EnergiBridge system to measure energy consumption and logs the results. The script iterates through multiple experiments, shuffling the order of plotting libraries, and generating different plot types while collecting performance metrics. 📊⚡

## Features
- Supports multiple plotting libraries (e.g., Matplotlib, Seaborn, Plotly, etc.). 🎨
- Generates line, bar, scatter, box, and heatmap plots from predefined datasets. 📈
- Uses EnergiBridgeManager to measure energy consumption for each test run. 🔋
- Saves generated plots to an output directory (optional). 💾
- Logs all experiment details to `log.txt`. 📝
- Implements a pause period between experiment iterations to ensure consistent measurement. ⏳

## Requirements
- Python 3.x 🐍
- Install dependencies using:

```bash
pip install -r requirements.txt
```

## Usage
At first, the `.env` file should be created and the variables should be set as described in `.env.example`.

Run the script with elevated permissions using:

```bash
python main.py
```

### Configuration ⚙️
- Adjust the number of experiments in the `num_experiments` variable. 🔄
- Set `save_plots = True` to save the generated plots. 🖼️
- Modify `output_dir` to specify where plots should be stored. 📂

### Output 📡
- Plots (if enabled) are saved in the `output_plots` directory, organized by plot type. 🗂️
- Energy consumption data is logged in CSV files. 📊
- Execution logs are recorded in `log.txt`. 📝

## File Structure 📂
- `BasePlotter.py`: Defines the base plotting interface. 🎭
- `energibridge_manager.py`: Handles energy consumption measurement. ⚡
- `plot_factory.py`: Manages the creation of different plotting library instances. 🏭
- `data.py`: Generates synthetic datasets for the experiments. 🔢
- `main.py`: Entry point that runs the experiments. ▶️

## License 📜
This project is for academic research purposes. Modify and distribute as needed. 🤓
## Calculating Maintainbility Index
To calcualte maintainbaility index, first go to the visualization_repos directory and run the `clone_repos.py` file to clone the source code of all the plotting libraries in the visualization_repos directory. The next step is go back to the root directory of the project and run `maintainability.py` to calculate the maintainbility index of each plotting libray.

## Collecting Issue Resolution Metrics
To collect the Issue Resolution Metrics go to the issue_metrics directory and run the `issue_metrics.py` file. This file will print all metrics to the console, it also collects some metrics that were not used in the final report. The results can also be found in results.txt .
