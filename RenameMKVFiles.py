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
