import os
import csv

def get_energy_metrics(file_path: str):
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        first_row = next(reader)
        last_row = None

        for row in reader:
            last_row = row

    if last_row is None:
        last_row = first_row

    energy = float(last_row["PACKAGE_ENERGY (J)"]) - float(first_row["PACKAGE_ENERGY (J)"])
    time_start = int(first_row["Time"])
    time_end = int(last_row["Time"])
    runtime = (time_end - time_start) / 1000
    edp = energy * runtime
    return energy, runtime, edp

folder_path = "../experiment_results"
parsed_results = []

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path) and "Pause" not in filename:
        energy, runtime, edp = get_energy_metrics(file_path)
        _, experiment_number, _, library_name = filename.replace(".csv", "").split("_")
        parsed_results.append([experiment_number, library_name, energy, runtime, edp])

output_file = "parsed_results.csv"
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([
        "experiment_number", "library",
        "delta_package_energy_j", "execution_time_s", "energy_delay_product"
    ])
    writer.writerows(parsed_results)

print(f"Results saved to {output_file}")
