import numpy as np
import pandas as pd


def get_df_line():
    df_line = pd.DataFrame({
        "x": pd.date_range("2023-01-01", periods=100, freq="D"),
        "y": np.random.normal(20, 5, 100).cumsum()  # Cumulative sum to simulate temperature trend
    })
    return df_line

def get_df_scatter():
    df_scatter = pd.DataFrame({
        "x": np.random.uniform(0, 10, 100),
        "y": np.random.uniform(0, 10, 100),
        "z": np.random.choice(['A', 'B', 'C'], 100)
    })
    return df_scatter

def get_df_bar():
    df_bar = pd.DataFrame({
        "x": ["A", "B", "C", "D", "E"],
        "y": [30, 45, 60, 80, 25]
    })
    return df_bar

def get_df_box():
    df_box = pd.DataFrame({
        "x": np.random.choice(["Group 1", "Group 2", "Group 3"], 100),
        "y": np.random.normal(0, 1, 100)
    })
    return df_box

def get_df_heatmap():
    df_heatmap = pd.DataFrame({
        "x": np.random.randn(100),
        "y": np.random.randn(100),
        "z": np.random.randn(100)
    })
    df_heatmap_corr = df_heatmap.corr()  # Correlation matrix
    return df_heatmap_corr

def get_df_contour():
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X**2 + Y**2)  # Example function for contour plot

    df_contour = pd.DataFrame({
        "x": X.flatten(),
        "y": Y.flatten(),
        "z": Z.flatten()
    })
    return df_contour
