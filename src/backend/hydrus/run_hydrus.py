import subprocess
import os
import time
import sys
import ctypes
import json
import matplotlib.pyplot as plt

# Set directories and paths
HYDRUS_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECTS_DIR = os.path.join(HYDRUS_DIR, "Projects")
hydrus_exe_path = os.path.join(HYDRUS_DIR, "HYDRUS1D.exe")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print("Error checking admin privileges:", e)
        return False

# Option B: Instead of restarting, exit if not run as admin.
if not is_admin():
    print("ERROR: This script must be run as administrator. Please restart the Node server with elevated privileges.")
    sys.exit(1)

def get_arguments():
    if len(sys.argv) < 3:
        print("Usage: run_hydrus.py <port_number> <sensor_data_json>")
        sys.exit(1)
    port_number = sys.argv[1]
    sensor_data_json = sys.argv[2]
    try:
        sensor_data = json.loads(sensor_data_json)
    except Exception as e:
        print("Invalid sensor data JSON:", e)
        sys.exit(1)
    # Generate a unique project name using the port number and current timestamp.
    project_name = f"Project_{port_number}_{int(time.time())}"
    return project_name, port_number, sensor_data

def generate_selector_file(project_path, sensor_data):
    selector_file = os.path.join(project_path, "InputSelector.txt")
    with open(selector_file, "w") as file:
        file.write(f"{sensor_data['water_content']} {sensor_data['soil_temp']} {sensor_data['bulk_ec']}\n")
    print(f"InputSelector.txt generated at {selector_file}")
    return selector_file

def run_hydrus(project_path):
    print(f"Running HYDRUS in: {project_path}")
    process = subprocess.Popen(
        [hydrus_exe_path],
        cwd=project_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    if stdout:
        print(f"HYDRUS Output: {stdout.decode()}")
    if stderr:
        print(f"HYDRUS Error: {stderr.decode()}")
    results_file = os.path.join(project_path, "Results.out")
    for _ in range(15):  # Wait up to 15 seconds for Results.out to appear
        if os.path.exists(results_file):
            print("Results.out detected!")
            return results_file
        print("Waiting for Results.out...")
        time.sleep(1)
    print("Error: HYDRUS did not generate Results.out.")
    sys.exit(1)

def process_results(results_file, project_path):
    try:
        with open(results_file, "r") as file:
            lines = file.readlines()
        # Example parsing logic; adjust based on your actual results file format.
        data = [line.strip().split() for line in lines if line.strip()]
        time_steps = [row[0] for row in data]
        moisture_levels = [row[1] for row in data]
        plt.figure(figsize=(10, 5))
        plt.plot(time_steps, moisture_levels, marker='o', linestyle='-')
        plt.xlabel("Time Steps")
        plt.ylabel("Moisture Content")
        plt.title("HYDRUS Simulation Results")
        plt.grid(True)
        plt.savefig(os.path.join(project_path, "hydrus_results.png"))
        plt.show()
        print("Graph generated successfully!")
    except Exception as e:
        print(f"Error processing results: {e}")
        sys.exit(1)

if __name__ == "__main__":
    project_name, port_number, sensor_data = get_arguments()
    project_path = os.path.join(PROJECTS_DIR, project_name)
    os.makedirs(project_path, exist_ok=True)
    generate_selector_file(project_path, sensor_data)
    results_file = run_hydrus(project_path)
    print(results_file)  # Print the path to Results.out so the caller can use it.
    process_results(results_file, project_path)
