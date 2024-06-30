import glob
import os
import shutil

CATEGORIES = ["profile", "world", "room", "objective"]
EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff']


def path_to_url(path: str) -> str:
    # Remove the 'static/' prefix if present
    if path.startswith('static/'):
        path = path[7:]

    # Replace backslashes with forward slashes
    url_path = path.replace('\\', '/')

    return url_path


def file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1][1:]


def file_name_without_extension(filename: str) -> str:
    return os.path.splitext(filename)[0]


def build_path(category: str, filename: str, extension: str) -> str | None:
    if category in CATEGORIES and extension in EXTENSIONS:
        return os.path.join(f'static/uploads/{category}/', filename) + "." + extension


def create_path(category: str, path: str):
    if category in CATEGORIES:
        os.makedirs(os.path.join(f'static/uploads/{category}/', path), exist_ok=True)


def get_image(category: str, image_id: int) -> str:
    if category in CATEGORIES:
        patterns = [os.path.join(f'static/uploads/{category}/', f"{image_id}.{ext}") for ext in EXTENSIONS]
        for pattern in patterns:
            for file_path in glob.glob(pattern):
                try:
                    return path_to_url(file_path)
                except OSError as e:
                    print(f"FILE: Error selecting {file_path}: {e}")


def get_all_images(category: str) -> dict[int, str] | None:
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


def get_sub_images(category: str, path: str) -> list[str] | None:
    if category in CATEGORIES:
        patterns = [os.path.join(f'static/uploads/{category}/{path}', f"*.{ext}") for ext in EXTENSIONS]
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


def delete_sub_image(category: str, path: str, filename: str) -> None:
    short_name = file_name_without_extension(filename)
    if category in CATEGORIES:
        patterns = [os.path.join(f'static/uploads/{category}/{path}', f"{short_name}.{ext}") for ext in EXTENSIONS]
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
            rename_file(category, temp_file, str(image_id), file_extension(temp_file))

            print(f"INFO: Image changed for {category}:{image_id}")


def rename_file(category: str, old_filename: str, filename: str, extension: str):
    if category in CATEGORIES:
        delete_image(category, int(filename))
        shutil.move(old_filename, os.path.join(f'static/uploads/{category}/', filename + "." + extension))
        print(f"FILE: Renamed {old_filename} to {os.path.join(f'static/uploads/{category}/', filename + "." + 
                                                              extension)}")


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


def save_file(file, category: str, filename: str):
    if category in CATEGORIES:
        full_path = build_path(category, filename, file_extension(file.filename))
        if full_path:
            file.save(full_path)
            print(f"FILE: Saved new file {full_path}")


def save_sub_file(file, category: str, path: str):
    if category in CATEGORIES:
        full_path = build_path(category, path + "/" + file_name_without_extension(file.filename),
                               file_extension(file.filename))
        if full_path:
            file.save(full_path)
            print(f"FILE: Saved sub file {full_path}")
