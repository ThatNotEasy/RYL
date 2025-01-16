import os
import csv
import re
import shutil

def is_valid_ryl2_txt(file_path):
    # Menentukan pola format parameter dan value yang benar untuk game RYL2
    pattern = re.compile(r'^[A-Z_]+\s*=\s*[0-9a-zA-Z_]+\s*$')

    with open(file_path, 'r') as file:
        for line in file:
            if not pattern.match(line.strip()):
                return False
    return True

def convert_to_csv(file_path, output_folder):
    csv_filename = os.path.splitext(os.path.basename(file_path))[0] + ".csv"
    csv_path = os.path.join(output_folder, csv_filename)

    with open(file_path, 'r') as txt_file, open(csv_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for line in txt_file:
            param, value = line.strip().split('=')
            csv_writer.writerow([param.strip(), value.strip()])

def process_txt_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_folder, filename)
            if is_valid_ryl2_txt(input_file_path):
                convert_to_csv(input_file_path, output_folder)
                print(f"File {filename} berhasil dikonversi dan disimpan di folder output.")

def auto_detect_convert_and_save(input_folder, output_folder):
    if not os.path.exists(input_folder):
        print("Folder input tidak ditemukan.")
        return

    process_txt_files(input_folder, output_folder)

input_folder = 'INPUT'  # Ganti dengan alamat folder input sebenarnya
output_folder = 'OUTPUT'  # Ganti dengan alamat folder output sebenarnya

auto_detect_convert_and_save(input_folder, output_folder)