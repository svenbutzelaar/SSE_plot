import pandas as pd
from scipy.stats import mannwhitneyu
from itertools import combinations

df = pd.read_csv("no_outliers_results.csv")

metric = "delta_package_energy_j"

libraries = df["library"].unique()

results = []

print(f"\nMann-Whitney U Test Results for Metric: '{metric}'\n")

for lib_a, lib_b in combinations(libraries, 2):
    a_values = df[df["library"] == lib_a][metric]
    b_values = df[df["library"] == lib_b][metric]

    stat, p_value = mannwhitneyu(a_values, b_values, alternative='two-sided')

    results.append({
        "Library A": lib_a,
        "Library B": lib_b,
        "U-statistic": stat,
        "p-value": p_value,
        "Significant": "YES" if p_value < 0.05 else "NO"
    })

    print(f"{lib_a} vs {lib_b}: U = {stat:.2f}, p = {p_value:.4f} → {'Significant' if p_value < 0.05 else 'Not Significant'}")

results_df = pd.DataFrame(results)
results_df.to_csv("mann_whitney_results.csv", index=False)
print("\nResults saved to 'mann_whitney_results.csv'")
