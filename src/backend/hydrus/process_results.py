import json

def extract_results():
    with open("HYDRUS/Results.out", "r") as file:
        lines = file.readlines()
    results = [line.strip().split() for line in lines]
    return results

if __name__ == "__main__":
    print(json.dumps(extract_results()))
