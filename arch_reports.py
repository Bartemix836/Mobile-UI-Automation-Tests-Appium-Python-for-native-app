import os
import shutil

def move_files_to_arch_reports():
    # Define paths to the 'reports' and 'arch_reports' folders
    current_directory = os.getcwd()
    reports_folder = os.path.join(current_directory, 'reports')
    arch_reports_folder = os.path.join(current_directory, 'arch_reports')

    # Check if the 'arch_reports' folder exists; if not, create it
    if not os.path.exists(arch_reports_folder):
        os.makedirs(arch_reports_folder)
        print(f"Folder {arch_reports_folder} has been created.")

    # Check if the 'reports' folder exists
    if os.path.exists(reports_folder) and os.path.isdir(reports_folder):
        # Iterate through all files in the 'reports' folder
        for filename in os.listdir(reports_folder):
            file_path = os.path.join(reports_folder, filename)

            # Check if it is a file
            if os.path.isfile(file_path):
                # Create the destination path in the 'arch_reports' folder
                destination_path = os.path.join(arch_reports_folder, filename)
                try:
                    # Move the file to the 'arch_reports' folder
                    shutil.move(file_path, destination_path)
                    print(f"Moved {file_path} to {destination_path}")
                except Exception as e:
                    print(f"Failed to move file {file_path}: {e}")
    else:
        print(f"Folder {reports_folder} does not exist.")

# Call the function
move_files_to_arch_reports()
