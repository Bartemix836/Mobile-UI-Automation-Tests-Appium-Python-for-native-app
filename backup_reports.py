import os
import shutil
from datetime import datetime


def move_files_from_arch_reports(date_str=None):
    # If no argument is provided, use today's date
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')

    # Define paths to the 'arch_reports' and 'reports' folders
    current_directory = os.getcwd()
    arch_reports_folder = os.path.join(current_directory, 'arch_reports')
    reports_folder = os.path.join(current_directory, 'reports')

    # Convert the date from string format to a datetime object
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return

    # Check if the 'arch_reports' folder exists
    if os.path.exists(arch_reports_folder) and os.path.isdir(arch_reports_folder):
        files_moved = 0  # Counter for moved files

        # Iterate through all files in the 'arch_reports' folder
        for filename in os.listdir(arch_reports_folder):
            file_path = os.path.join(arch_reports_folder, filename)

            # Check if it is a file
            if os.path.isfile(file_path):
                # Get the file modification date
                file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))

                # Check if the file modification date is greater than or equal to the given date
                if file_mod_time >= target_date:
                    # Create the destination path in the 'reports' folder
                    destination_path = os.path.join(reports_folder, filename)
                    try:
                        # Move the file to the 'reports' folder
                        shutil.move(file_path, destination_path)
                        print(f"Moved {file_path} to {destination_path}")
                        files_moved += 1  # Increment the counter of moved files
                    except Exception as e:
                        print(f"Failed to move file {file_path}: {e}")

        # Display the final message
        if files_moved > 0:
            print(f"Moved {files_moved} files.")
        else:
            print("No files were moved because no modification date matched.")
    else:
        print(f"Folder {arch_reports_folder} does not exist.")


# Call the function without an argument – it will use today's date
move_files_from_arch_reports()
``
