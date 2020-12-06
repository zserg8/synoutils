"""
This script reorganizes the photos uploaded by Synology Moments photo backup function in the mobile app.

By default, the Mobile app creates the following folder structure on the server:
- a folder "Mobile"
- a subfolder with the name of the device
- a subfolder with the name of backed-up folder from the device
- a subfolder for each day

This results in overcomplicated folder structure like Moments/Mobile/SM-G930F/DCIM/2020-01-01

The current script collects all the files underneath <folder_from> and moves them over to <folder_to>
"""

from glob import glob
import os
import sys
from shutil import move

folder_from = "c:/Users/zserg/Desktop/Moments/Mobile"
folder_to = "c:/Users/zserg/Desktop/Moments"



def move_files(fr, to):
    # Normalize paths
    fr = os.path.abspath(fr)
    to = os.path.abspath(to)

    # Find all files
    full_path = os.path.abspath(fr)
    full_path = os.path.join(full_path, "**")
    print(f"Searching photos in {full_path} and all subfolders")
    files = glob(full_path, recursive=True)
    # Filter out files only
    files = [f for f in files if os.path.isfile(f)]
    ans = input(f"Preparing to move {len(files)} files from {to} to {to}. Continue (Y/N)?")
    if ans not in "yY":
        sys.exit(0)

    # Copy over with renaming duplicates
    for f in files:
        target = os.path.split(f)[1]
        # Check if filename already exists
        suffix = 0
        while os.path.isfile(os.path.join(to, target)):
            suffix = suffix + 1
            filename, ext = os.path.splitext(os.path.split(f)[1])
            filename = f"{filename}_{suffix:02d}"
            print(f"\n!!! File {f} already exists in destination, trying {filename+ext}")
            target = os.path.join(to, filename + ext)
        # Move file with metadata
        target = os.path.join(to, target)
        print(f"Moving {f} to {target}")
        move(f, target)

    print("Copying done")

if __name__ == "__main__":
    move_files(folder_from, folder_to)
