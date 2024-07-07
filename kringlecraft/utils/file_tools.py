import glob
import os
import shutil
import re

EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff']


def file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1][1:]


def file_name_without_extension(filename: str) -> str:
    return os.path.splitext(filename)[0]


def translate_folder_name(encoded_name: str) -> str | None:
    # Check if the name format is correct
    if not re.match(r'^(profile|world|room|objective)(_\d+)*$', encoded_name):
        # raise ValueError(f"Invalid encoded name format: {encoded_name}")
        return None

    parts = encoded_name.split('_')
    name = parts[0]
    numbers = parts[1:]

    # Check if all numbers are integers (if there are any)
    if numbers and not all(num.isdigit() for num in numbers):
        # raise ValueError(f"Invalid number format in: {encoded_name}")
        return None

    return f"{name}/{'/'.join(numbers)}" if numbers else name


def is_valid_filename(filename) -> bool:
    pattern = r'^[\w\-. ]+$'
    return bool(re.match(pattern, filename)) and not any(char in filename for char in r'\/:*?"<>|')


def read_file_without_extension(path: str, filename_without_extension) -> list[str] | None:
    for extension in EXTENSIONS:
        pattern = os.path.join(f'static/uploads/{path}/', f"{filename_without_extension}.{extension}")
        if os.path.exists(pattern):
            return [path, f"{filename_without_extension}.{extension}"]
    return None


def read_all_files_without_extension(path: str) -> dict[int, list[str]] | None:
    all_files = {}
    full_path = os.path.join(f'static/uploads/{path}/')

    if os.path.exists(full_path):
        count = 0
        for filename in os.listdir(full_path):
            if any(filename.endswith(ext) for ext in EXTENSIONS):
                if file_name_without_extension(filename).isdigit():
                    all_files[int(file_name_without_extension(filename))] = [path, filename]
                else:
                    all_files[count] = [path, filename]
                    count += 1

    return all_files


def store_file(file, path: str, filename: str, use_original_name: bool = False) -> bool:
    new_filename = file.filename if use_original_name else filename + "." + file_extension(file.filename)
    full_path = os.path.join(f'static/uploads/{path}/')
    os.makedirs(full_path, exist_ok=True)
    if os.path.isdir(full_path):
        try:
            file.save(f"{full_path}/{new_filename}")
            print(f"FILE: Save file {full_path}/{new_filename}")
            return True
        except OSError as e:
            print(f"FILE: Error saving {full_path}/{new_filename}: {e}")
    else:
        return False


def remove_image(path: str, filename: str) -> bool:
    full_filename = os.path.join(f'static/uploads/{path}', filename)
    try:
        os.remove(full_filename)
        print(f"FILE: Deleted {full_filename}")
        return True
    except OSError as e:
        print(f"FILE: Error deleting {full_filename}: {e}")
        return False


def remove_all_images(path: str, filename_without_extension: str) -> bool:
    for extension in EXTENSIONS:
        pattern = os.path.join(f'static/uploads/{path}/', f"{filename_without_extension}.{extension}")
        if os.path.exists(pattern):
            try:
                os.remove(pattern)
                print(f"FILE: Deleted {pattern}")
                return True
            except OSError as e:
                print(f"FILE: Error deleting {pattern}: {e}")
                return False
    return False


def enable_image(path: str, image_id: int):
    temp_file = get_temp_file(path)
    if temp_file:
        patterns = [os.path.join(f'static/uploads/{path}/', f"{image_id}.{ext}") for ext in EXTENSIONS]
        deleted_files = []
        for pattern in patterns:
            for file_path in glob.glob(pattern):
                try:
                    os.remove(file_path)
                    deleted_files.append(os.path.basename(file_path))
                    print(f"FILE: Deleted {file_path}")
                except OSError as e:
                    print(f"FILE: Error deleting {file_path}: {e}")

        shutil.move(temp_file, os.path.join(f'static/uploads/{path}/', str(image_id) + "." +
                                            file_extension(temp_file)))
        print(f"FILE: Renamed {temp_file} to {os.path.join(f'static/uploads/{path}/', str(image_id) + '.' + file_extension(temp_file))}")


def get_temp_file(path: str) -> str | None:
    temp_files = glob.glob(os.path.join(f'static/uploads/{path}/', "_temp.*"))
    if temp_files:
        # Return the first match; you can modify this to return all matches if needed
        return temp_files[0]


def create_markdown_file(filename: str, md_output: str) -> str | None:
    local_file = os.path.join(f'static/downloads/', filename)
    try:
        with open(local_file, 'w', encoding='utf-8') as f:
            f.write(md_output)

        return local_file
    except OSError as e:
        print(f"FILE: Error saving {local_file}: {e}")
