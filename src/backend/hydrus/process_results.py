import json
import sys

def extract_results(results_file):
    with open(results_file, "r") as file:
        lines = file.readlines()
    results = [line.strip().split() for line in lines if line.strip()]
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Results file path not provided")
        sys.exit(1)
    results_file = sys.argv[1]
    print(json.dumps(extract_results(results_file)))
