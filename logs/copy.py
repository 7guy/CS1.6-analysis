import os
import shutil
from datetime import datetime

def copy_and_rename_logs(source_folder, dest_folder):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    # Get a list of all files in the source folder
    log_files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
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
            print(f"Copied and renamed: {log_file} to {new_file_name}")
        else:
            print(f"Skipped: {log_file} (Already exists in destination folder)")

def main():
        # Specify the source folder (game folder) and destination folder (your specified directory)
        game_folder = r"C:/Program Files (x86)/Valve/Counter-Strike/cstrike/logs"
        destination_folder = os.path.expanduser("~/PycharmProjects/cs_analytics/logs/log_files")  # Relative path to your project directory

        copy_and_rename_logs(game_folder, destination_folder)


if __name__ == "__main__":
    main()