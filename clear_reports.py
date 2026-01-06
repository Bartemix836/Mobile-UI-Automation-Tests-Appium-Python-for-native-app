import os
import shutil

def clear_reports_folder():
    # Define the path to the 'reports' folder, assuming it is in the same directory as the script
    reports_folder = os.path.join(os.getcwd(), 'reports')

    # Check if the folder exists
    if os.path.exists(reports_folder) and os.path.isdir(reports_folder):
        # Iterate through all files and subfolders in the 'reports' folder
        for filename in os.listdir(reports_folder):
            file_path = os.path.join(reports_folder, filename)
            try:
                # Remove a file or a directory
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                print(f"Removed: {file_path}")
            except Exception as e:
                print(f"Failed to remove {file_path}: {e}")
    else:
        print(f"Folder {reports_folder} does not exist.")

clear_reports_folder()
