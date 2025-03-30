import pandas as pd
from scipy.stats import zscore, shapiro


def remove_outliers(input_csv, output_csv):
    df = pd.read_csv(input_csv)

    # Compute the mean energy_delay_product
    df_grouped = df.groupby(["experiment_number", "library"], as_index=False)["energy_delay_product"].mean()

    # Compute z-scores for each library type
    df_grouped["z_score"] = df_grouped.groupby("library")["energy_delay_product"].transform(lambda x: zscore(x))

    # Filter out outliers (absolute z-score <= 3)
    df_cleaned = df_grouped[abs(df_grouped["z_score"]) <= 3].drop(columns=["z_score"])

    df_cleaned.to_csv(output_csv, index=False)

    # Perform Shapiro-Wilk test for normality
    for library in df_cleaned["library"].unique():
        subset = df_cleaned[df_cleaned["library"] == library]["energy_delay_product"]
        stat, p = shapiro(subset)
        print(f"Shapiro-Wilk test for {library}: W={stat:.4f}, p-value={p:.4f}")


# Example usage
input_file = "parsed_results.csv"
output_file = "no_outliers_results.csv"
# Run twice to ensure data is normal
remove_outliers(input_file, output_file)
remove_outliers(output_file, output_file)
# Output:
# First run:
# Shapiro-Wilk test for holoviews: W=0.5366, p-value=0.0000
# Shapiro-Wilk test for matplotlib: W=0.7985, p-value=0.0001
# Shapiro-Wilk test for plotly: W=0.8033, p-value=0.0001
# Shapiro-Wilk test for plotnine: W=0.9699, p-value=0.5789
# Shapiro-Wilk test for pygal: W=0.9374, p-value=0.0855
# Shapiro-Wilk test for seaborn: W=0.9510, p-value=0.1794
# Second run:
# Shapiro-Wilk test for holoviews: W=0.9414, p-value=0.1197
# Shapiro-Wilk test for matplotlib: W=0.7985, p-value=0.0001
# Shapiro-Wilk test for plotly: W=0.8033, p-value=0.0001
# Shapiro-Wilk test for plotnine: W=0.9699, p-value=0.5789
# Shapiro-Wilk test for pygal: W=0.9374, p-value=0.0855
# Shapiro-Wilk test for seaborn: W=0.9510, p-value=0.1794

