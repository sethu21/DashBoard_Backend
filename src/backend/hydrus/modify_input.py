import sys
import json
import os

# Get the full path of the current directory
HYDRUS_DIR = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(HYDRUS_DIR, "InputSelector.txt")

# 🔹 Check if file exists, create if missing
if not os.path.exists(file_path):
    print(f"File not found, creating: {file_path}")
    open(file_path, "w").close()  # Create an empty file

def modify_input_file(input_json):
    """ Appends new sensor data to InputSelector.txt """
    with open(file_path, "a") as file:  # 'a' mode appends instead of overwriting
        file.write(f"{input_json['water_content']} {input_json['soil_temp']} {input_json['bulk_ec']}\n")
    print(f"New data appended to {file_path}")

if __name__ == "__main__":
    input_data = json.loads(sys.argv[1])
    modify_input_file(input_data)
