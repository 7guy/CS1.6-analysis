import os
import shutil
from datetime import datetime
import argparse

"""
TODO:
copy.py new logic
1. new files are in source folder
2. copy to uploaded files folder
3. rename and copy to dest folder
4. delete from source folder

parse.py new logic:
add deletion from dest folder after parsing and saving to parsed data folder

msg2db.py new logic:
add deletion from parsed data folder after successful insertion to db

New task: make all logic run under one script
"""

def copy_and_rename_logs(source_folder, dest_folder, print_file_status):
    num_of_new_files = 0

    # Create the destination folder if it doesn't exist
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    # Get a list of all files in the source folder
    log_files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    src_dir_num_of_files = len(log_files)
    for log_file in log_files:
        source_path = os.path.join(source_folder, log_file)

        # Get the creation time of the log file
        creation_time = os.path.getctime(source_path)

        # Convert the creation time to a datetime object
        creation_datetime = datetime.fromtimestamp(creation_time)

        # Format the datetime as a string to use in the new file name
        new_file_name = creation_datetime.strftime("%Y%m%d_%H%M%S") + ".log"

        dest_path = os.path.join(dest_folder, new_file_name)

        # Check if the log file with the same name already exists in the destination folder
        if not os.path.exists(dest_path):
            shutil.copyfile(source_path, dest_path)
            num_of_new_files += 1
            if print_file_status:
                print(f"Copied and renamed: {log_file} to {new_file_name}")
        else:
            if print_file_status:
                print(f"Skipped: {log_file} (Already exists in destination folder)")

    print(f'Out of {src_dir_num_of_files} files, {src_dir_num_of_files-num_of_new_files} already existed '
          f'and {num_of_new_files} new files were copied and renamed')


def parse_arguments():
    parser = argparse.ArgumentParser()

    # Positional arguments
    parser.add_argument("-v","--verbose", action="store_true", help="print details of copied log files.")
    return parser.parse_args()


def main():
    args = parse_arguments()

    # Specify the source folder (game folder) and destination folder (your specified directory)
    game_folder = r"C:/Program Files (x86)/Valve/Counter-Strike/cstrike/logs"
    destination_folder = os.path.expanduser("~/PycharmProjects/cs_analytics/logs/log_files")

    copy_and_rename_logs(game_folder, destination_folder, args.verbose)


if __name__ == "__main__":
    main()
