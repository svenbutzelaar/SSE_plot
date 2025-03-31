import pandas as pd
import numpy as np

df = pd.read_csv("no_outliers_results.csv")

mean_energy = df.groupby("library")["energy_delay_product"].mean().reset_index()
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

# Output:
#      library  mean_energy_j  energy_efficiency_score
#  matplotlib     271.820368               100.000000
#   holoviews    2483.148254                90.238343
#     seaborn    3593.486141                85.702281
#    plotnine   16961.212345                46.060286
#       pygal   18897.745986                42.097969
#      plotly   43329.047829                13.533528
