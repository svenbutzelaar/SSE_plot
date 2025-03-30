import pandas as pd

df = pd.read_csv("no_outliers_results.csv")

mean_energy = df.groupby("library")["energy_delay_product"].mean().reset_index()
mean_energy.columns = ["library", "mean_energy_j"]

E_min = mean_energy["mean_energy_j"].min()
E_max = mean_energy["mean_energy_j"].max()

mean_energy["energy_efficiency_score"] = 100 * (E_max - mean_energy["mean_energy_j"]) / (E_max - E_min)

mean_energy = mean_energy.sort_values(by="energy_efficiency_score", ascending=False)

print(mean_energy)
mean_energy.to_csv("energy_efficiency_scores.csv", index=False)

# Output:
#      library  mean_energy_j  energy_efficiency_score
#  matplotlib     271.820368               100.000000 x
#   holoviews    2483.148254                94.864212
#     seaborn    3593.486141                92.285463
#    plotnine   16961.212345                61.239046
#       pygal   18897.745986                56.741465
#      plotly   43329.047829                 0.000000 x
