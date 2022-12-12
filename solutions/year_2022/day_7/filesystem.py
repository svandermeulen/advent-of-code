"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 09/12/2022
"""
import itertools
import os
import operator
from collections import defaultdict

from functools import reduce  # forward compatibility for Python 3
from typing import Any, List, Dict

from solutions.config import Config
from solutions.utils.file_manager import read_txt_file


def get_by_path(root: dict, items: List) -> Any:
    """Access a nested object in root by item sequence."""
    return reduce(operator.getitem, items, root)


def try_get_by_path(root: dict, items: List) -> Any:
    try:
        return get_by_path(root=root, items=items)
    except (KeyError, TypeError):
        return None


def set_by_path(root: dict, items: List, value: Any):
    """Set a value in a nested object in root by item sequence."""
    get_by_path(root, items[:-1])[items[-1]] = value


def build_filesystem(filesystem: dict, folder_names: List) -> dict:
    if folder_names:
        if folder_names[0] in filesystem:
            filesystem[folder_names[0]].update(
                build_filesystem(filesystem[folder_names[0]], folder_names=folder_names[1:]))
            return filesystem
        if filesystem:
            filesystem[folder_names[0]] = build_filesystem(filesystem=filesystem, folder_names=folder_names[1:])
            return filesystem
        return {folder_names[0]: build_filesystem(filesystem=filesystem, folder_names=folder_names[1:])}
    return {}


def extract_filesystem(data: List[str]) -> dict:
    folder_names = []
    filesystem = {}

    for line in data:
        if line.startswith("$ cd "):
            if line != "$ cd ..":
                directory = line.replace("$ cd ", "")
                folder_names.append(directory)
                filesystem = build_filesystem(filesystem=filesystem, folder_names=folder_names)
            else:
                folder_names.pop(-1)
        elif line.startswith("$ ls"):
            continue
        elif line.startswith("dir"):
            continue
        else:
            size, filename = line.split(" ")
            size = int(size)
            current_value = get_by_path(root=filesystem, items=folder_names)
            if not current_value:
                set_by_path(root=filesystem, items=folder_names, value={filename: size})
            else:
                set_by_path(root=filesystem, items=folder_names, value=dict(current_value, **{filename: size}))
    return filesystem


def find_all_folders(filesystem: dict, folders: List[List[str]] = None, folder_parent: List[str] = None) -> List[
    List[str]]:
    folders = folders if folders is not None else []
    for key, val in filesystem.items():
        if isinstance(val, dict):
            folder = [key] if folder_parent is None else folder_parent + [key]
            folders.append(folder)
            folders = find_all_folders(filesystem=val, folders=folders, folder_parent=folder)
    return folders


def compute_folder_size(filesystem: dict, folder_size: int = 0):
    for key, value in filesystem.items():
        if isinstance(value, int):
            folder_size += value
        if isinstance(value, dict):
            folder_size = compute_folder_size(filesystem[key], folder_size)
    return folder_size


def find_folder_sizes(filesystem: dict) -> Dict[str, int]:
    folders_sizes = {}
    folders = find_all_folders(filesystem=filesystem)
    for folder_path in folders:
        items = get_by_path(root=filesystem, items=folder_path)
        folders_sizes["|".join(folder_path)] = compute_folder_size(filesystem=items)
    return folders_sizes


def compute_part_one(folder_sizes: Dict[str, int], size: int) -> int:
    total_size = 0
    for folder_path, folder_size in folder_sizes.items():
        if folder_size < size:
            total_size += folder_size
    return total_size


def compute_part_two(folder_sizes: Dict[str, int], size: int) -> (str, int):
    folders = {}
    for folder_path, folder_size in folder_sizes.items():
        if folder_size >= size:
            folders[folder_path] = folder_size

    folder = min(folders, key=folders.get)

    return folder, folders[folder]


def main():
    config = Config(year=2022, day=7)

    # Test case
    path_file = os.path.join(config.path_data, "filesystem_test.txt")
    data = read_txt_file(path_file=path_file)
    filesystem = extract_filesystem(data=data)
    folder_sizes = find_folder_sizes(filesystem=filesystem)
    total_size = compute_part_one(folder_sizes=folder_sizes, size=100000)
    assert total_size == 95437

    # Part one
    path_file = os.path.join(config.path_data, "filesystem.txt")
    data = read_txt_file(path_file=path_file)
    filesystem = extract_filesystem(data=data)
    folder_sizes = find_folder_sizes(filesystem=filesystem)
    total_size = compute_part_one(folder_sizes=folder_sizes, size=100000)
    print(f"The total size of all folders below 100000 equals: {total_size}")
    assert total_size == 1350966

    # Part two
    total_disk_space = 70000000
    minimum_free_disk_space = 30000000
    total_used_space = folder_sizes["/"]
    space_to_free_up = minimum_free_disk_space - (total_disk_space - total_used_space)
    folder, size = compute_part_two(folder_sizes=folder_sizes, size=space_to_free_up)
    print(f"The smallest directory to free up enough space has a size of: {size}")
    assert size == 6296435
    return True


if __name__ == "__main__":
    main()
