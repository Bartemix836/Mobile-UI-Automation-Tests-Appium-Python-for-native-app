import os
import shutil
from datetime import datetime


def move_files_from_arch_reports(date_str=None):
    # Jeśli argument nie został podany, użyj dzisiejszej daty
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')

    # Określenie ścieżek do folderów 'arch_reports' i 'reports'
    current_directory = os.getcwd()
    arch_reports_folder = os.path.join(current_directory, 'arch_reports')
    reports_folder = os.path.join(current_directory, 'reports')

    # Konwertowanie daty z formatu str na obiekt datetime
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print("Nieprawidłowy format daty. Użyj formatu YYYY-MM-DD.")
        return

    # Sprawdzenie, czy folder 'arch_reports' istnieje
    if os.path.exists(arch_reports_folder) and os.path.isdir(arch_reports_folder):
        files_moved = 0  # Zmienna do liczenia przeniesionych plików

        # Przechodzimy przez wszystkie pliki w folderze 'arch_reports'
        for filename in os.listdir(arch_reports_folder):
            file_path = os.path.join(arch_reports_folder, filename)

            # Sprawdzamy, czy to jest plik
            if os.path.isfile(file_path):
                # Pobieramy datę modyfikacji pliku
                file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))

                # Sprawdzamy, czy data modyfikacji pliku jest większa lub równa podanej dacie
                if file_mod_time >= target_date:
                    # Tworzymy ścieżkę docelową w folderze 'reports'
                    destination_path = os.path.join(reports_folder, filename)
                    try:
                        # Przenosimy plik do folderu 'reports'
                        shutil.move(file_path, destination_path)
                        print(f"Przeniesiono {file_path} do {destination_path}")
                        files_moved += 1  # Zwiększamy licznik przeniesionych plików
                    except Exception as e:
                        print(f"Nie udało się przenieść pliku {file_path}: {e}")

        # Wyświetlanie komunikatu końcowego
        if files_moved > 0:
            print(f"Przeniesiono {files_moved} plików.")
        else:
            print("Nie przeniesiono żadnego pliku, ponieważ żadna data modyfikacji nie pasowała.")
    else:
        print(f"Folder {arch_reports_folder} nie istnieje.")


# Wywołanie funkcji bez argumentu – użyje dzisiejszej daty
move_files_from_arch_reports()
