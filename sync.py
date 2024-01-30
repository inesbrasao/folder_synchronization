import argparse
import hashlib
import logging
import os
import shutil
import time
from pathlib import Path


def set_args():
    parser = argparse.ArgumentParser(
        description="Synchronize contents between two dirs"
    )
    parser.add_argument("--source_path", type=str, help="Path to the source dir")
    parser.add_argument("--replica_path", type=str, help="Path to the replica dir")
    parser.add_argument("--log_path", type=str, help="Path to the log file")
    parser.add_argument("--interval", type=int, help="Sync interval (seconds)")
    args = parser.parse_args()
    return args


def get_path_contents(path: str) -> list:
    """
    Get all files and directories recursively from a given path
    """
    files = []
    paths = Path(path).glob("**/*")
    for p in paths:
        files.append(p.relative_to(path))
    return files


def open_file(path: str) -> bytes:
    """
    Open file and return file content. If path is a directory, return empty
    string
    """
    file_content = b""
    if Path(path).is_file():
        with open(path, "rb") as file_obj:
            file_content = file_obj.read()
    return file_content


def compute_hash(content: bytes) -> str:
    """
    Compute md5 hash of a given content
    """
    return hashlib.md5(content).hexdigest()


def add_or_copy(src: str, dst: str):
    """
    If src is a file, copy the file. If src is a directory, copy the directory
    tree. If the file already exists in dst, overwrites it.
    """
    if os.path.isdir(src):
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)


def remove(file: str):
    """
    Removes a given file
    """
    if os.path.exists(file):
        os.remove(file)


def generate_file_hashmap(path_content: list, path: str) -> dict:
    """
    Create a file md5 hash map
    """
    files_dict = {}
    for file in path_content:
        file_content = open_file(f"{path}/{file}")
        file_hash = compute_hash(file_content)
        files_dict[file] = file_hash
    return files_dict


def sync_dirs_by_hashmap(
    source_path: str,
    replica_path: str,
    source_hashmap: dict,
    replica_hashmap: dict,
    remove_function=remove,
    add_or_copy_function=add_or_copy,
):
    """
    Syncs two directories by comparing the md5 hash of each file
    If a file exists in source but not in replica, copy the file to replica
    If a file exists in replica but not in source, remove the file from replica
    If a file exists in both source and replica but has different hash, copy the
    file to replica
    """
    for key in replica_hashmap:
        if key not in source_hashmap:
            remove_function(f"{replica_path}/{key}")
            logging.info(f"Removed {key} in replica folder: {replica_path}")
        elif key in source_hashmap and replica_hashmap[key] != source_hashmap[key]:
            add_or_copy_function(f"{source_path}/{key}", f"{replica_path}/{key}")
            logging.info(f"Updated {key} in replica folder: {replica_path}")
    for key in source_hashmap:
        if key not in replica_hashmap:
            add_or_copy_function(f"{source_path}/{key}", f"{replica_path}/{key}")
            logging.info(f"Created {key} in replica folder: {replica_path}")


def create_replica_folder(path: str):
    """
    Creates replica folder if it doesn't exist
    """
    if os.path.exists(path):
        return
    else:
        os.makedirs(path, exist_ok=True)
        logging.info(f"Created replica folder: {path}")


if __name__ == "__main__":
    args = set_args()
    source_path = args.source_path
    replica_path = args.replica_path
    log_path = args.log_path
    interval = args.interval

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(message)s",
        handlers=[logging.FileHandler(log_path, mode="a"), logging.StreamHandler()],
    )

    # Create replica folder if it doesn't exist
    create_replica_folder(replica_path)

    while True:
        source_contents = get_path_contents(source_path)
        replica_contents = get_path_contents(replica_path)
        source_hashmap = generate_file_hashmap(
            path_content=source_contents, path=source_path
        )
        replica_hashmap = generate_file_hashmap(
            path_content=replica_contents, path=replica_path
        )
        sync_dirs_by_hashmap(
            source_path=source_path,
            replica_path=replica_path,
            source_hashmap=source_hashmap,
            replica_hashmap=replica_hashmap,
        )
        time.sleep(interval)
