import os
import csv

def process_line(line):
    # Process the values as needed, correcting or formatting them
    values = line.strip().split()
    corrected_values = [value.upper() for value in values]  # Example: Convert to uppercase
    return corrected_values

def convert_txt_to_csv(txt_file, csv_file):
    with open(txt_file, 'r') as txt_input, open(csv_file, 'w', newline='') as csv_output:
        csv_writer = csv.writer(csv_output)
        error_log = []

        for line_number, line in enumerate(txt_input, start=1):
            try:
                corrected_values = process_line(line)
                csv_writer.writerow(corrected_values)
            except Exception as e:
                error_log.append(f"[Ex-Error processing data. Line:{line_number}] {str(e)}")

        if error_log:
            with open("error_log.txt", "w") as log_file:
                log_file.write("\n".join(error_log))

def main():
    input_folder = "INPUT"
    output_folder = "OUTPUT"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    txt_files = [file for file in os.listdir(input_folder) if file.endswith(".txt")]

    for txt_file in txt_files:
        txt_file_path = os.path.join(input_folder, txt_file)
        csv_file_path = os.path.join(output_folder, txt_file.replace(".txt", ".csv"))

        convert_txt_to_csv(txt_file_path, csv_file_path)

# Main execution moved to main.py - only run if this file is executed directly
# if __name__ == "__main__":
#     main()
