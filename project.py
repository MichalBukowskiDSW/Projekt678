import sys
import json

def parse_arguments():
    if len(sys.argv) != 3:
        print("Usage: program.exe pathFile1.x pathFile2.y")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    return input_file, output_file

def load_json(input_file):
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
        print("JSON data loaded successfully")
        return data
    except Exception as e:
        print(f"Failed to load JSON file: {e}")
        sys.exit(1)

def save_json(data, output_file):
    try:
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
        print("JSON data saved successfully")
    except Exception as e:
        print(f"Failed to save JSON file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    input_file, output_file = parse_arguments()
    if input_file.endswith('.json'):
        data = load_json(input_file)
        if output_file.endswith('.json'):
            save_json(data, output_file)
