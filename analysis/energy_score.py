import pandas as pd
import numpy as np

df = pd.read_csv("no_outliers_results.csv")

mean_energy = df.groupby("library")["delta_package_energy_j"].mean().reset_index()
mean_energy.columns = ["library", "mean_energy_j"]

E_min = mean_energy["mean_energy_j"].min()
E_max = mean_energy["mean_energy_j"].max()

k = 2

mean_energy["energy_efficiency_score"] = 100 * np.exp(
    -k * ((mean_energy["mean_energy_j"] - E_min) / (E_max - E_min))
)

mean_energy = mean_energy.sort_values(by="energy_efficiency_score", ascending=False)

print(mean_energy)
mean_energy.to_csv("energy_efficiency_scores.csv", index=False)