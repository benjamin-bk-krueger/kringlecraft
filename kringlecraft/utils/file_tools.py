import glob
import os
import shutil

from typing import Dict, List

CATEGORIES = ["profile", "world", "room", "objective"]
EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff']


def path_to_url(file_path):
    # Remove the 'static/' prefix if present
    if file_path.startswith('static/'):
        file_path = file_path[7:]

    # Replace backslashes with forward slashes
    url_path = file_path.replace('\\', '/')

    return url_path


def file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1][1:]


def file_name_without_extension(filename: str) -> str:
    return os.path.splitext(filename)[0]


def build_path(category: str, file_name: str, extension: str) -> str | None:
    if category in CATEGORIES and extension in EXTENSIONS:
        return os.path.join(f'static/uploads/{category}/', file_name) + "." + extension


def create_path(category: str, object_id: int):
    if category in CATEGORIES:
        os.makedirs(os.path.join(f'static/uploads/{category}/', str(object_id)), exist_ok=True)


def get_image(category: str, image_id: int) -> str:
    if category in CATEGORIES:
        patterns = [os.path.join(f'static/uploads/{category}/', f"{image_id}.{ext}") for ext in EXTENSIONS]
        for pattern in patterns:
            for file_path in glob.glob(pattern):
                try:
                    return path_to_url(file_path)
                except OSError as e:
                    print(f"FILE: Error selecting {file_path}: {e}")


def get_all_images(category: str) -> Dict[int, str] | None:
    if category in CATEGORIES:
        patterns = [os.path.join(f'static/uploads/{category}/', f"*.{ext}") for ext in EXTENSIONS]
        image_dict = {}
        for pattern in patterns:
            for file_path in glob.glob(pattern):
                try:
                    file_name = os.path.basename(file_path)
                    file_number, _ = os.path.splitext(file_name)
                    if file_number != "_temp":
                        image_dict[int(file_number)] = path_to_url(file_path)
                except OSError as e:
                    print(f"FILE: Error selecting {file_path}: {e}")
        return image_dict


def get_sub_images(category: str, object_id) -> List[str] | None:
    if category in CATEGORIES:
        patterns = [os.path.join(f'static/uploads/{category}/{object_id}', f"*.{ext}") for ext in EXTENSIONS]
        image_list = []
        for pattern in patterns:
            for file_path in glob.glob(pattern):
                try:
                    file_name = os.path.basename(file_path)
                    file_number, _ = os.path.splitext(file_name)
                    if file_number != "_temp":
                        image_list.append(path_to_url(file_path))
                except OSError as e:
                    print(f"FILE: Error selecting {file_path}: {e}")
        return image_list


def delete_image(category: str, image_id: int) -> None:
    if category in CATEGORIES:
        patterns = [os.path.join(f'static/uploads/{category}/', f"{image_id}.{ext}") for ext in EXTENSIONS]
        deleted_files = []
        for pattern in patterns:
            for file_path in glob.glob(pattern):
                try:
                    os.remove(file_path)
                    deleted_files.append(os.path.basename(file_path))
                    print(f"FILE: Deleted {file_path}")
                except OSError as e:
                    print(f"FILE: Error deleting {file_path}: {e}")


def enable_image(category: str, image_id: int):
    if category in CATEGORIES:
        temp_file = get_temp_file(category)
        if temp_file:
            new_filename = f"{image_id}.{file_extension(temp_file)}"
            rename_temp_file(category, temp_file, str(image_id), file_extension(temp_file))

            print(f"INFO: Image changed for {category}:{image_id}")


def get_temp_file(category: str) -> str | None:
    if category in CATEGORIES:
        temp_files = glob.glob(os.path.join(f'static/uploads/{category}/', "_temp.*"))
        if temp_files:
            # Return the first match; you can modify this to return all matches if needed
            return temp_files[0]


def delete_temp_files(category: str):
    if category in CATEGORIES:
        temp_files = glob.glob(os.path.join(f'static/uploads/{category}/', "_temp.*"))
        for file_path in temp_files:
            try:
                os.remove(file_path)
                print(f"INFO: Deleted {file_path}")
            except Exception as e:
                print(f"FILE: Error deleting {file_path}: {e}")


def rename_temp_file(category: str, temp_file: str, file_name: str, ending: str):
    if category in CATEGORIES:
        delete_image(category, int(file_name))
        shutil.move(temp_file, os.path.join(f'static/uploads/{category}/', file_name + "." + ending))
        print(f"FILE: Renamed {temp_file} to {os.path.join(f'static/uploads/{category}/', file_name + "." + ending)}")


def get_image_files(category: str) -> list | None:
    if category in CATEGORIES:
        image_files = glob.glob(os.path.join('static', 'uploads', category, "*.*"))
        if image_files:
            # Convert backslashes to forward slashes and ensure the path starts with 'static'
            return ['/'.join(path.split(os.sep)[1:]) for path in image_files]


def save_file(file, category: str):
    if category in CATEGORIES:
        full_path = build_path(category, file_name_without_extension(file.filename), file_extension(file.filename))
        if full_path:
            file.save(full_path)
            print(f"FILE: Saved file {full_path}")


def save_new_file(file, category: str, file_name: str):
    if category in CATEGORIES:
        full_path = build_path(category, file_name, file_extension(file.filename))
        if full_path:
            file.save(full_path)
            print(f"FILE: Saved new file {full_path}")


def save_sub_file(file, category: str, object_id: str):
    if category in CATEGORIES:
        full_path = build_path(category, object_id + "/" + file_name_without_extension(file.filename), file_extension(file.filename))
        if full_path:
            file.save(full_path)
            print(f"FILE: Saved sub file {full_path}")
