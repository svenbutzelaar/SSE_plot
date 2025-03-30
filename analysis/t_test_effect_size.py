import pandas as pd
from scipy.stats import ttest_ind
import numpy as np
from itertools import combinations

file_path = "no_outliers_results.csv"
df = pd.read_csv(file_path)

metric = "energy_delay_product"

libraries = ["holoviews", "plotnine", "pygal", "seaborn"]

results = []

print(f"Pairwise Welch's t-tests for metric: '{metric}'\n")

for lib_a, lib_b in combinations(libraries, 2):
    a_data = df[df["library"] == lib_a][metric]
    b_data = df[df["library"] == lib_b][metric]

    t_stat, p_value = ttest_ind(a_data, b_data, equal_var=False)

    mean_a = a_data.mean()
    mean_b = b_data.mean()
    std_a = a_data.std()
    std_b = b_data.std()
    mean_diff = mean_b - mean_a
    percent_change = (mean_diff / mean_a) * 100

    pooled_std = np.sqrt((std_a**2 + std_b**2) / 2)
    cohens_d = mean_diff / pooled_std

    if abs(cohens_d) < 0.2:
        effect = "Small"
    elif abs(cohens_d) < 0.5:
        effect = "Medium"
    else:
        effect = "Large"

    print(f"{lib_a} vs {lib_b}:")
    print(f"  t = {t_stat:.4f}, p = {p_value:.4f} → {'significant' if p_value < 0.05 else 'not significant'}")
    print(f"  mean = {mean_diff:.2f} ({percent_change:.2f}%), Cohen's d = {cohens_d:.2f} ({effect} effect)\n")

    results.append({
        "lib_a": lib_a,
        "lib_b": lib_b,
        "t_stat": t_stat,
        "p_value": p_value,
        "mean_diff": mean_diff,
        "percent_change": percent_change,
        "cohens_d": cohens_d,
        "effect_size": effect
    })

results_df = pd.DataFrame(results)
results_df.to_csv("pairwise_t_test_results.csv", index=False)
print("Results saved to pairwise_t_test_results.csv")
