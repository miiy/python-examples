import shutil
from pathlib import Path
import argparse

def split_files(source_dir, files_per_folder):
    """
    Split files from source directory into multiple subdirectories with specified number of files

    Args:
        source_dir (str): Source directory path
        files_per_folder (int): Maximum number of files per folder
    """
    # Get all files from source directory
    source_path = Path(source_dir)
    files = [f for f in source_path.iterdir() if f.is_file()]

    if not files:
        print(f"No files found in {source_dir}")
        return

    # Calculate number of folders needed
    total_files = len(files)
    # example: 101 files, 100 files per folder
    # (101 + 100 - 1) // 100 = 2
    folder_count = (total_files + files_per_folder - 1) // files_per_folder

    # Get parent directory for creating new folders
    parent_dir = source_path.parent

    for folder_index in range(folder_count):
        # Create new folder
        source_path_name = source_path.name
        new_folder = parent_dir / f"{source_path_name}_{folder_index + 1}"
        new_folder.mkdir(exist_ok=True)

        # Calculate file range for current folder
        start_idx = folder_index * files_per_folder
        end_idx = min((folder_index + 1) * files_per_folder, total_files)

        # Move files to new folder
        for file_path in files[start_idx:end_idx]:
            destination = new_folder / file_path.name
            shutil.move(str(file_path), str(destination))
            print(f"Moving file: {file_path.name} -> {destination}")

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Split files from a directory into multiple subdirectories')
    parser.add_argument('--source_dir', type=str, help='Source directory path')
    parser.add_argument('--files_per_folder', type=int, help='Number of files per folder')

    args = parser.parse_args()

    # Call function with command line arguments
    split_files(args.source_dir, args.files_per_folder)


if __name__ == "__main__":
    main()