import glob
import hashlib
import os


def file_hash(filename: str) -> str:
    return hashlib.md5(filename.encode('utf-8')).hexdigest()


def check_path(category: str, filename: str) -> bool:
    return os.path.isfile(os.path.join(f'static/uploads/{category}/', filename))


def web_path(category: str, filename: str) -> str:
    return os.path.join(f'uploads/{category}/', filename)


def dummy_path() -> str:
    return "img/not_found.jpg"


def file_ending(filename: str) -> str:
    return os.path.splitext(filename)[1][1:]


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
