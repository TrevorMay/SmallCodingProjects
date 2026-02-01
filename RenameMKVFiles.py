# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import os

def rename_folders_and_files(root_directory):
    # Iterate over each item in the root directory
    for folder_name in os.listdir(root_directory):
        folder_path = os.path.join(root_directory, folder_name)
        
        # Ensure the item is a directory
        if os.path.isdir(folder_path):
            # Create the new folder name by replacing underscores and converting to title case
            new_folder_name = folder_name.replace('_', ' ').title()
            new_folder_path = os.path.join(root_directory, new_folder_name)
            
            # Rename the folder if the new name is different
            if new_folder_name != folder_name:
                os.rename(folder_path, new_folder_path)
                folder_path = new_folder_path  # Update folder path to the new name

            # Check for the .mkv file in the folder
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.mkv'):
                    file_path = os.path.join(folder_path, file_name)
                    new_file_name = f"{new_folder_name}.mkv"
                    new_file_path = os.path.join(folder_path, new_file_name)

                    # Rename the .mkv file if it has a different name than the folder
                    if new_file_name != file_name:
                        os.rename(file_path, new_file_path)
                    break  # Stop after finding the first .mkv file

if __name__ == "__main__":
    root_directory = r"C:\Video"
    rename_folders_and_files(root_directory)
    print("Folders and .mkv files have been renamed.")

# %%
import os
import shutil

def rename_and_flatten_files(root_directory, output_directory):
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Iterate over each item in the root directory
    for folder_name in os.listdir(root_directory):
        folder_path = os.path.join(root_directory, folder_name)
        
        # Ensure the item is a directory
        if os.path.isdir(folder_path):
            # Create the new base name by replacing underscores, removing unwanted strings, and converting to title case
            unwanted_strings = ['43', '4x3', '16x9']
            base_name = folder_name.replace('_', ' ')
            for unwanted in unwanted_strings:
                base_name = base_name.replace(unwanted, '')
            base_name = base_name.title().strip()

            # Find .mkv files in the folder
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.mkv'):
                    # Remove unwanted strings and adjust file name
                    new_file_name = f"{base_name}.mkv"
                    new_file_name = new_file_name.replace('  ', ' ')  # Clean up double spaces

                    # Construct source and destination paths
                    source_file_path = os.path.join(folder_path, file_name)
                    destination_file_path = os.path.join(output_directory, new_file_name)

                    # Move the .mkv file to the output directory
                    shutil.move(source_file_path, destination_file_path)
                    print(f"Moved: {source_file_path} -> {destination_file_path}")
                    break  # Stop after processing the first .mkv file

if __name__ == "__main__":
    root_directory = r"C:\Video"
    output_directory = r"C:\to_encode"
    rename_and_flatten_files(root_directory, output_directory)
    print("All .mkv files have been renamed and moved to the output directory.")


# %%
import os
import shutil

def rename_and_flatten_files(root_directory, output_directory):
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Iterate over each item in the root directory
    for folder_name in os.listdir(root_directory):
        folder_path = os.path.join(root_directory, folder_name)

        # Ensure the item is a directory
        if os.path.isdir(folder_path):
            # Clean up and format the base name
            unwanted_strings = ['43', '4x3', '16x9']
            base_name = folder_name.replace('_', ' ')
            for unwanted in unwanted_strings:
                base_name = base_name.replace(unwanted, '')
            base_name = base_name.title().strip()

            # Get all .mkv files in the folder
            mkv_files = [f for f in os.listdir(folder_path) if f.endswith('.mkv')]

            # Rename and move each .mkv file with a numbered suffix
            for idx, file_name in enumerate(sorted(mkv_files), start=1):
                new_file_name = f"{base_name} {idx}.mkv"
                new_file_name = new_file_name.replace('  ', ' ')  # Clean up double spaces

                source_file_path = os.path.join(folder_path, file_name)
                destination_file_path = os.path.join(output_directory, new_file_name)

                # Avoid overwriting files with the same name
                counter = 1
                while os.path.exists(destination_file_path):
                    new_file_name = f"{base_name} {idx}_{counter}.mkv"
                    destination_file_path = os.path.join(output_directory, new_file_name)
                    counter += 1

                shutil.move(source_file_path, destination_file_path)
                print(f"Moved: {source_file_path} -> {destination_file_path}")

if __name__ == "__main__":
    root_directory = r"C:\Video"
    output_directory = r"C:\to_encode"
    rename_and_flatten_files(root_directory, output_directory)
    print("All .mkv files have been renamed and moved to the output directory.")

# %%
import os
import shutil

def rename_folders_and_files(root_directory, destination_directory):
    # Iterate over each item in the root directory
    for folder_name in os.listdir(root_directory):
        folder_path = os.path.join(root_directory, folder_name)

        try:
            # Ensure the item is a directory
            if os.path.isdir(folder_path):

                # Count files inside the folder (ignore subfolders)
                try:
                    file_count = sum(
                        1 for f in os.listdir(folder_path)
                        if os.path.isfile(os.path.join(folder_path, f))
                    )
                except PermissionError:
                    print(f"Permission denied when reading folder: {folder_path}")
                    continue

                # If folder contains more than one file, move it and skip renaming
                try:
                    if file_count > 1:
                        dest_path = os.path.join(destination_directory, folder_name)
                        shutil.move(folder_path, dest_path)
                        continue
                except PermissionError:
                    print(f"Permission denied when moving: {folder_path}")
                    continue

                # Create the new folder name
                new_folder_name = folder_name.replace('_', ' ').title()
                new_folder_path = os.path.join(root_directory, new_folder_name)

                # Rename the folder if needed
                try:
                    if new_folder_name != folder_name:
                        os.rename(folder_path, new_folder_path)
                        folder_path = new_folder_path  # Update folder path
                except PermissionError:
                    print(f"Permission denied when renaming folder: {folder_path}")
                    continue

                # Check for the .mkv file in the folder
                try:
                    for file_name in os.listdir(folder_path):
                        if file_name.endswith('.mkv'):
                            file_path = os.path.join(folder_path, file_name)
                            new_file_name = f"{new_folder_name}.mkv"
                            new_file_path = os.path.join(folder_path, new_file_name)

                            if new_file_name != file_name:
                                try:
                                    os.rename(file_path, new_file_path)
                                except PermissionError:
                                    print(f"Permission denied when renaming file: {file_path}")
                            break
                except PermissionError:
                    print(f"Permission denied when accessing files in: {folder_path}")
                    continue

        except PermissionError:
            print(f"Permission denied when processing: {folder_path}")
            continue


if __name__ == "__main__":
    root_directory = r"Z:\to_encode"
    destination_directory = r"Z:\to_encode\MultiFileFolders"

    # Create destination folder if missing
    os.makedirs(destination_directory, exist_ok=True)

    rename_folders_and_files(root_directory, destination_directory)
    print("Process completed.")



# %%
import os
import shutil

def process_folders(root_directory):
    for folder_name in os.listdir(root_directory):
        folder_path = os.path.join(root_directory, folder_name)

        if not os.path.isdir(folder_path):
            continue

        try:
            # Get files only (ignore subfolders)
            files = [
                f for f in os.listdir(folder_path)
                if os.path.isfile(os.path.join(folder_path, f))
            ]
        except PermissionError:
            print(f"Permission denied reading: {folder_path}")
            continue

        if len(files) == 0:
            continue

        # Find the largest file
        largest_file = max(
            files,
            key=lambda f: os.path.getsize(os.path.join(folder_path, f))
        )

        largest_path = os.path.join(folder_path, largest_file)
        name, ext = os.path.splitext(largest_file)

        # Rename largest file to match folder name
        new_largest_name = f"{folder_name}{ext}"
        new_largest_path = os.path.join(folder_path, new_largest_name)

        try:
            if largest_file != new_largest_name:
                os.rename(largest_path, new_largest_path)
        except PermissionError:
            print(f"Permission denied renaming: {largest_path}")
            continue

        # Handle remaining files
        other_files = [f for f in files if f != largest_file]

        if other_files:
            other_folder = os.path.join(folder_path, "Other")
            os.makedirs(other_folder, exist_ok=True)

            for file in other_files:
                src = os.path.join(folder_path, file)
                dst = os.path.join(other_folder, file)
                try:
                    shutil.move(src, dst)
                except PermissionError:
                    print(f"Permission denied moving: {src}")

if __name__ == "__main__":
    root_directory = r"D:\to_encode"
    process_folders(root_directory)
    print("Process completed.")


# %%
