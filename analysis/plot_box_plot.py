import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("no_outliers_results.csv")

selected_libraries = ["holoviews", "plotnine", "pygal", "seaborn", "plotly", "matplotlib"]

df = df[df["library"].isin(selected_libraries)]

df = df[df["energy_delay_product"] > 0]

order = df.groupby("library")["energy_delay_product"].median().sort_values().index

plt.figure(figsize=(10, 5))
sns.violinplot(
    x="library", y="energy_delay_product", data=df,
    inner=None, alpha=0.6, order=order
)
sns.boxplot(
    x="library", y="energy_delay_product", data=df,
    width=0.2, showfliers=False, order=order
)

for i, lib in enumerate(order):
    plt.text(i, df[df["library"] == lib]["energy_delay_product"].max() * 1.05,
             lib, ha="center", fontsize=9, color="black")
plt.xlabel("Library")
plt.ylabel("Energy Delay Product")
plt.title("Energy Delay Product of Plotting Libraries")
plt.xticks(rotation=15)
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()
