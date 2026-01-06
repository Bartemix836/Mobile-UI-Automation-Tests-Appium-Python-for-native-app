import os
import shutil

def move_files_to_arch_reports():
    # Określenie ścieżek do folderów 'reports' i 'arch_reports'
    current_directory = os.getcwd()
    reports_folder = os.path.join(current_directory, 'reports')
    arch_reports_folder = os.path.join(current_directory, 'arch_reports')

    # Sprawdzenie, czy folder 'arch_reports' istnieje, jeśli nie, tworzymy go
    if not os.path.exists(arch_reports_folder):
        os.makedirs(arch_reports_folder)
        print(f"Folder {arch_reports_folder} został utworzony.")

    # Sprawdzenie, czy folder 'reports' istnieje
    if os.path.exists(reports_folder) and os.path.isdir(reports_folder):
        # Przechodzimy przez wszystkie pliki w folderze 'reports'
        for filename in os.listdir(reports_folder):
            file_path = os.path.join(reports_folder, filename)

            # Sprawdzamy, czy to jest plik
            if os.path.isfile(file_path):
                # Tworzymy ścieżkę docelową w folderze 'arch_reports'
                destination_path = os.path.join(arch_reports_folder, filename)
                try:
                    # Przenosimy plik do folderu 'arch_reports'
                    shutil.move(file_path, destination_path)
                    print(f"Przeniesiono {file_path} do {destination_path}")
                except Exception as e:
                    print(f"Nie udało się przenieść pliku {file_path}: {e}")
    else:
        print(f"Folder {reports_folder} nie istnieje.")

# Wywołanie funkcji
move_files_to_arch_reports()
