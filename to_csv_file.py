import csv
import json
import os
import unicodedata

TARGET_DIR = "C:\\Users\\koezgen\\Desktop\\dir\\to_csv"

def write_json_to_csv(target_dir, output_csv_path):
    # Get list of all text files in the target directory
    files_list = [os.path.join(target_dir, file) for file in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, file)) and file.endswith(".txt")]

    data = []

    # Read all JSON data from the text files
    for file_path in files_list:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
            json_objects = file_content.split('}')
            for obj in json_objects:
                if obj.strip():
                    try:
                        json_obj = json.loads(obj.strip() + '}')
                        # Create a dictionary to map Turkish characters to non-Turkish
                        tr_chars = {
                            'ı': 'i',
                            'ş': 's',
                            'ğ': 'g',
                            'ü': 'u',
                            'ö': 'o',
                            'ç': 'c',
                            'İ': 'I',
                            'Ş': 'S',
                            'Ğ': 'G',
                            'Ü': 'U',
                            'Ö': 'O',
                            'Ç': 'C'
                        }
                        # Create a new dictionary to store modified keys and values
                        updated_obj = {}
                        # Convert all dictionary keys to uppercase and replace Turkish characters
                        for key, value in json_obj.items():
                            new_key = key.translate(str.maketrans(tr_chars)).upper()
                            updated_obj[new_key] = value
                        data.append(updated_obj)
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON object: {obj}")
                        print(f"Error message: {e}")

    if data:
        # Get the keys from the first dictionary as the column headers
        headers = list(data[0].keys())

        # Write data to CSV file
        with open(output_csv_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)

# Usage:
write_json_to_csv(TARGET_DIR, 'output.csv')