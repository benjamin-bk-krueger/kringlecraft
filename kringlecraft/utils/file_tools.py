import glob
import os
import re

EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff']


def file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1][1:]


def extract_number(string):
    parts = string.split('-')
    if len(parts) > 1 and parts[-1].isdigit():
        return int(parts[-1])
    return None


def is_valid_path(path: str) -> bool:
    # Check if the name format is correct
    return True if re.match(r'^(profile|world|room|objective)$', path) else None


def is_valid_sub_path(path: str) -> bool:
    # Check if the name format is correct
    return True if re.match(r'^(logo|challenge|solution)-(\d+)(-(\d+))?$', path) else None


def is_valid_filename(filename) -> bool:
    pattern = r'^[\w\-. ]+$'
    return bool(re.match(pattern, filename)) and not any(char in filename for char in r'\/:*?"<>|')


def read_file(path: str) -> list[str] | None:
    full_path = os.path.join(f'static/uploads/{path}/')

    if os.path.exists(full_path):
        for filename in os.listdir(full_path):
            if any(filename.endswith(ext) for ext in EXTENSIONS):
                return [path, filename]


def read_all_files(path: str) -> dict[int, list[str]] | None:
    all_files = {}
    full_path = os.path.join(f'static/uploads/{path}/')

    if os.path.exists(full_path):
        count = 0
        for filename in os.listdir(full_path):
            if any(filename.endswith(ext) for ext in EXTENSIONS):
                all_files[count] = [path, filename]
                count += 1

    return all_files


def read_all_files_recursive(path: str) -> dict[int, list[str]] | None:
    all_files = {}
    base_path = 'static/uploads'
    full_path_pattern = os.path.join(base_path, path)
    count = 0

    # Use glob to get all matching directories
    matching_dirs = glob.glob(full_path_pattern)

    if not matching_dirs:
        return None

    for dir_path in matching_dirs:
        for root, _, files in os.walk(dir_path):
            for filename in files:
                if any(filename.endswith(ext) for ext in EXTENSIONS):
                    relative_path = os.path.relpath(root, base_path)
                    all_files[extract_number(relative_path)] = [relative_path, filename]
                    count += 1

    return all_files


def store_file(file, path: str) -> bool:
    full_path = os.path.join(f'static/uploads/{path}/')
    os.makedirs(full_path, exist_ok=True)
    if os.path.isdir(full_path):
        try:
            file.save(f"{full_path}/{file.filename}")
            print(f"FILE: Save file {full_path}/{file.filename}")
            return True
        except OSError as e:
            print(f"FILE: Error saving {full_path}/{file.filename}: {e}")
    else:
        return False


def enable_image(path: str, image_id: int):
    base_path = 'static/uploads'
    full_path = os.path.join(base_path, path)

    if not os.path.exists(full_path):
        print(f"FILE: The path {full_path} does not exist.")
        return False

    old_folder_name = 'logo-0'
    new_folder_name = f'logo-{image_id}'

    old_folder_path = os.path.join(full_path, old_folder_name)
    new_folder_path = os.path.join(full_path, new_folder_name)

    # Check if the old folder exists
    if not os.path.exists(old_folder_path):
        print(f"FILE: The folder {old_folder_path} does not exist.")
        return False

    # Check if the new folder name already exists
    if os.path.exists(new_folder_path):
        print(f"FILE: The folder {new_folder_path} already exists.")
        return False

    try:
        # Rename the folder
        os.rename(old_folder_path, new_folder_path)
        print(f"FILE: Successfully renamed {old_folder_path} to {new_folder_path}")
        return True
    except OSError as e:
        print(f"FILE: Error occurred while renaming the folder: {e}")
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


def remove_all_images(path: str) -> bool:
    base_path = os.path.join('static/uploads', path)
    if not os.path.exists(base_path):
        print(f"FILE: Path does not exist: {base_path}")
        return False

    deleted_files = False

    for root, _, files in os.walk(base_path):
        for file in files:
            if any(file.lower().endswith(f".{ext}") for ext in EXTENSIONS):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"FILE: Deleted {file_path}")
                    deleted_files = True
                except OSError as e:
                    print(f"FILE: Error deleting {file_path}: {e}")

    if not deleted_files:
        print(f"FILE: No image files found to delete in {base_path}")

    return deleted_files


def create_markdown_file(filename: str, md_output: str) -> str | None:
    local_file = os.path.join(f'static/downloads/', filename)
    try:
        with open(local_file, 'w', encoding='utf-8') as f:
            f.write(md_output)

        return local_file
    except OSError as e:
        print(f"FILE: Error saving {local_file}: {e}")
