import json


def parse_config(file_path: str) -> dict | None:
    """
    Parse the configuration file and return the content as a dictionary.

    :param file_path: The path to the configuration file.
    :type file_path: str
    :return: The content of the configuration file as a dictionary, or None if an error occurred.
    :rtype: dict | None
    """
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        print(f"{file_path} file not found")
    except Exception as e:
        print(f"An error occurred when reading the {file_path} file: ", str(e))
