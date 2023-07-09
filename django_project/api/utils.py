

def check_file_extension(file):
    """Функция для проверки расширения файла

    Args:
        file (File): Обьект файла для проверки

    Returns:
        bool:
            - True: Если файл расширения csv
            - False: Во всех других случаях
    """
    try:
        file_name = file.name
        file_extension = file_name.split('.')[-1]
        if file_extension in ['csv']:
            return True
        return False
    except Exception:
        return False