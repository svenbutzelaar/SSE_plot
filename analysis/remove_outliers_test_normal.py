import pandas as pd
from scipy.stats import zscore, shapiro


def remove_outliers(input_csv, output_csv):
    df = pd.read_csv(input_csv)

    # Compute the mean delta_package_energy_j
    df_grouped = df.groupby(["experiment_number", "library"], as_index=False)["delta_package_energy_j"].mean()

    # Compute z-scores for each library type
    df_grouped["z_score"] = df_grouped.groupby("library")["delta_package_energy_j"].transform(lambda x: zscore(x))

    # Filter out outliers (absolute z-score <= 3)
    df_cleaned = df_grouped[abs(df_grouped["z_score"]) <= 3].drop(columns=["z_score"])

    df_cleaned.to_csv(output_csv, index=False)

    # Perform Shapiro-Wilk test for normality
    for library in df_cleaned["library"].unique():
        subset = df_cleaned[df_cleaned["library"] == library]["delta_package_energy_j"]
        stat, p = shapiro(subset)
        print(f"Shapiro-Wilk test for {library}: W={stat:.4f}, p-value={p:.4f}")


# Example usage
input_file = "parsed_results.csv"
output_file = "no_outliers_results.csv"
# Run twice to ensure data is normal
remove_outliers(input_file, output_file)
remove_outliers(output_file, output_file)
