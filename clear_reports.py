import os
import shutil

def clear_reports_folder():
    # Określenie ścieżki do folderu 'reports', zakładając, że jest w tym samym katalogu co skrypt
    reports_folder = os.path.join(os.getcwd(), 'reports')

    # Sprawdzenie, czy folder istnieje
    if os.path.exists(reports_folder) and os.path.isdir(reports_folder):
        # Przechodzimy przez wszystkie pliki i podfoldery w folderze 'reports'
        for filename in os.listdir(reports_folder):
            file_path = os.path.join(reports_folder, filename)
            try:
                # Usuwamy plik lub folder
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                print(f"Usunięto: {file_path}")
            except Exception as e:
                print(f"Nie udało się usunąć {file_path}: {e}")
    else:
        print(f"Folder {reports_folder} nie istnieje.")

clear_reports_folder()
