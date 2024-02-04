import csv
import os


def merge_csv_files(input_folder, output_filename):
    csv_files = [file for file in os.listdir(input_folder) if file.endswith(".csv")]

    if not csv_files:
        print("No CSV files found in the 'outputs' folder.")
        return

    # Initialize a list to store rows from all CSV files
    all_rows = []

    # Iterate through each CSV file
    for csv_file in csv_files:
        file_path = os.path.join(input_folder, csv_file)

        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            
            # Remove rows where Product Title is blank
            rows = [row for row in csv_reader if row['Product Title'].strip()]

            # Extend the list with rows from the current CSV file
            all_rows.extend(rows)

    # Prompt for the name of the merged CSV file
    output_file_path = os.path.join(input_folder, output_filename)

    # Write the merged rows to a new CSV file
    with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = all_rows[0].keys() if all_rows else []
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header only if there are rows
        if all_rows:
            csv_writer.writeheader()

        # Write rows to the CSV file
        csv_writer.writerows(all_rows)

    print(f"Merged CSV file '{output_filename}' created successfully.")

if __name__ == "__main__":
    # Specify the folder containing CSV files
    input_folder = "outputs"

    # Prompt for the merged CSV file name
    output_filename = input("Enter the name for the merged CSV file (including .csv extension): ")

    # Call the function to merge CSV files
    merge_csv_files(input_folder, output_filename)
