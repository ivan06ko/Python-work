import os
import random
import string

def get_root_paths():
    # шукаємо всі існуючі диски типу C:\, D:\, E:\ ...
    roots = []
    if os.name == "nt":
        for letter in string.ascii_uppercase:
            path = f"{letter}:\\"
            if os.path.exists(path):
                roots.append(path)
    else:
        # для Linux / Mac
        roots.append("/")
    return roots

def random_file_from_roots(roots=None):
    # резервуарна вибірка: не тримаємо всі файли в памʼяті
    if roots is None:
        roots = get_root_paths()

    def ignore_error(err):
        # ігноруємо помилки доступу
        pass

    chosen_path = None
    seen_files = 0

    for root in roots:
        for dirpath, dirnames, filenames in os.walk(root, onerror=ignore_error):
            for name in filenames:
                full_path = os.path.join(dirpath, name)
                seen_files += 1
                # з ймовірністю 1/seen_files замінюємо обраний файл
                if random.randint(1, seen_files) == 1:
                    chosen_path = full_path

    return chosen_path

if __name__ == "__main__":
    path = random_file_from_roots()
    if path is not None:
        print("Випадковий файл на комп'ютері:")
        print(path)
    else:
        print("Не знайшов жодного файлу.")
