import glob
import hashlib
import os
import shutil


def file_hash(filename: str) -> str:
    return hashlib.md5(filename.encode('utf-8')).hexdigest()


def build_path(category: str, hash_value: str, ending: str):
    return os.path.join(f'static/uploads/{category}/', hash_value) + "." + ending


def check_path(category: str, filename: str) -> bool:
    return os.path.isfile(os.path.join(f'static/uploads/{category}/', filename))


def web_path(category: str, filename: str) -> str:
    return os.path.join(f'uploads/{category}/', filename)


def dummy_path() -> str:
    return "img/not_found.jpg"


def file_ending(filename: str) -> str:
    return os.path.splitext(filename)[1][1:]


def file_name_without_extension(filename: str) -> str:
    return os.path.splitext(filename)[0]


def get_temp_file(category: str) -> str | None:
    temp_files = glob.glob(os.path.join(f'static/uploads/{category}/', "_temp.*"))
    if temp_files:
        # Return the first match; you can modify this to return all matches if needed
        return temp_files[0]


def delete_temp_files(category: str):
    temp_files = glob.glob(os.path.join(f'static/uploads/{category}/', "_temp.*"))
    for file_path in temp_files:
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"FILE: Error deleting {file_path}: {e}")


def rename_temp_file(category: str, temp_file: str, hash_value: str, ending: str):
    shutil.move(temp_file, os.path.join(f'static/uploads/{category}/', hash_value + "." + ending))


def get_image_files(category: str) -> list | None:
    image_files = glob.glob(os.path.join('static', 'uploads', category, "*.*"))
    if image_files:
        # Convert backslashes to forward slashes and ensure the path starts with 'static'
        return ['/'.join(path.split(os.sep)[1:]) for path in image_files]
