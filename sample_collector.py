import csv
import os
import random


def find_csv_files(folder_path):
    csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]
    return csv_files

def collect_random_ids(csv_files, num_ids=16):
    collected_ids = []

    for csv_file in csv_files:
        file_path = os.path.join("outputs", csv_file)

        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            ids = random.sample(set(row['ID'] for row in csv_reader if row.get('ID')), min(num_ids, 16))
            collected_ids.extend(ids)

    return collected_ids

def write_sample_product_csv(input_csv, output_csv, selected_ids):
    with open(input_csv, 'r', newline='', encoding='utf-8') as input_file:
        csv_reader = csv.DictReader(input_file)

        # Filter rows with the selected IDs
        selected_rows = [row for row in csv_reader if row.get('ID') in selected_ids]

    with open(output_csv, 'w', newline='', encoding='utf-8') as output_file:
        csv_writer = csv.DictWriter(output_file, fieldnames=csv_reader.fieldnames)

        # Write header
        csv_writer.writeheader()

        # Write selected rows
        csv_writer.writerows(selected_rows)

if __name__ == "__main__":
    files = find_csv_files("outputs")
    collected_ids = collect_random_ids(files, 16)

    input_csv = "marged_final.csv"
    output_csv = "sample_product_500.csv"

    write_sample_product_csv(input_csv, output_csv, collected_ids)
