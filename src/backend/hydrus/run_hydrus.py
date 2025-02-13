import subprocess
import os
import time
import sys
import ctypes

HYDRUS_DIR = os.path.abspath(os.path.dirname(__file__))  # Backend/hydrus directory
PROJECT_DIR = os.path.join(HYDRUS_DIR, "Projects")  # Force HYDRUS to save here
hydrus_exe_path = os.path.join(HYDRUS_DIR, "HYDRUS1D.exe")

NODE_SERVER_URL = "http://localhost:5000"  # Node.js backend URL
#RESULTS_FILE = os.path.join(PROJECT_DIR, "Results.out")  # Ensure HYDRUS writes here

def is_admin():
    """ Checks if the script is running with admin privileges. """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def restart_as_admin():
    """ Relaunches the script as Administrator and continues execution. """
    print("Restarting HYDRUS script as Administrator...")
    script = os.path.abspath(__file__)
    subprocess.run(["powershell", "Start-Process", "python", f"'{script}'", "-Verb", "runAs"], shell=True)
    sys.exit()

def get_user_input():
    """ Asks the user for project details and port number. """
    project_name = input("Enter project name: ").strip()
    description = input("Enter project description: ").strip()
    port_number = input("Enter sensor port number (1, 2, or 3): ").strip()

    if port_number not in ["1", "2", "3"]:
        print("Invalid port number. Use 1, 2, or 3.")
        sys.exit(1)

    project_path = os.path.join(Projects_DIR, project_name)
    os.makedirs(project_path, exist_ok=True)
    return project_name, description, port_number, project_path

def fetch_sensor_data(port_number):
    """ Fetches sensor data from Node.js backend API instead of connecting to the database directly. """
    try:
        response = requests.get(f"{NODE_SERVER_URL}/api/sensor/{port_number}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching sensor data: {e}")
        sys.exit(1)

def generate_selector_file(project_path, sensor_data):
    """ Generates the Selector.in file for HYDRUS. """
    selector_file = os.path.join(project_path, "Selector.in")
    with open(selector_file, "w") as file:
        file.write(f"{sensor_data['water_content']} {sensor_data['soil_temp']} {sensor_data['bulk_ec']}\n")
    print(f"Selector.in file generated at {selector_file}")

def run_hydrus(project_path):
    """ Runs HYDRUS-1D inside the project directory. """
    print(f"Running HYDRUS in: {project_path}")
    process = subprocess.Popen(
        [hydrus_exe_path],
        cwd=project_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )

    stdout, stderr = process.communicate()

    if stdout:
        print(f"HYDRUS Output: {stdout.decode()}")
    if stderr:
        print(f"HYDRUS Error: {stderr.decode()}")

    results_file = os.path.join(project_path, "Results.out")
    for _ in range(15):  # Wait up to 15 seconds
        if os.path.exists(results_file):
            print("Results.out detected!")
            return results_file
        print("Waiting for Results.out...")
        time.sleep(1)
    print("Error: HYDRUS did not generate Results.out.")
    sys.exit(1)

def process_results(results_file):
    """ Extracts and visualizes HYDRUS results. """
    try:
        with open(results_file, "r") as file:
            lines = file.readlines()
        
        # Assume data is structured in columns (modify based on actual format)
        data = [list(map(float, line.strip().split())) for line in lines if line.strip()]
        time_steps = [row[0] for row in data]  # First column as time
        moisture_levels = [row[1] for row in data]  # Second column as moisture content

        # Plot results
        plt.figure(figsize=(10, 5))
        plt.plot(time_steps, moisture_levels, marker='o', linestyle='-')
        plt.xlabel("Time Steps")
        plt.ylabel("Moisture Content")
        plt.title("HYDRUS Simulation Results")
        plt.grid(True)
        plt.savefig("hydrus_results.png")  # Save the plot
        plt.show()

        print("Graph generated successfully!")

    except Exception as e:
        print(f"Error processing results: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if not is_admin():
        restart_as_admin()

    project_name, description, port_number, project_path = get_user_input()
    sensor_data = fetch_sensor_data(port_number)  # Fetch data from Node.js API
    generate_selector_file(project_path, sensor_data)
    results_file = run_hydrus(project_path)
    process_results(results_file)