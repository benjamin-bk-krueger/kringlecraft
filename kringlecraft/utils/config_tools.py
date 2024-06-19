import json


def parse_config(file_path: str) -> dict | None:
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        print(f"{file_path} file not found")
    except Exception as e:
        print(f"An error occurred when reading the {file_path} file: ", str(e))
