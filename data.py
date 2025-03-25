import numpy as np
import pandas as pd


def get_df_line(num_points=10**4):
    df_line = pd.DataFrame({
        "x": pd.date_range("2023-01-01", periods=num_points, freq="D"),
        "y": np.random.normal(20, 5, num_points).cumsum()  # Cumulative sum to simulate temperature trend
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
        "x": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
        "y": np.random.randint(20, 100, 10)
    })
    return df_bar

def get_df_box(num_points=10**7):
    df_box = pd.DataFrame({
        "x": np.random.choice(["Group 1", "Group 2", "Group 3", "Group 4"], num_points),
        "y": np.random.normal(0, 10, num_points)
    })
    return df_box

def get_df_heatmap(num_rows=10**7):
    df_heatmap = pd.DataFrame({
        "x": np.random.randn(num_rows),
        "y": np.random.randn(num_rows),
        "z": np.random.randn(num_rows)
    })
    df_heatmap_corr = df_heatmap.corr()
    return df_heatmap_corr

def get_df_contour(num_points=10**7):
    x = np.linspace(-5, 5, num_points)
    y = np.linspace(-5, 5, num_points)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X**2 + Y**2)  # Example function for contour plot

    df_contour = pd.DataFrame({
        "x": X.flatten(),
        "y": Y.flatten(),
        "z": Z.flatten()
    })
    return df_contour
