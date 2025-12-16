from .transliteration import transliterate

def parse_excel_row(row):
    """Парсит строку Excel"""
    return {
        "fio": str(row[0]).strip() if row[0] else "",
        "email": str(row[1]).strip() if len(row) > 1 and row[1] else "",
        "phone": str(row[2]).strip() if len(row) > 2 and row[2] else None,
        "title": str(row[3]).strip() if len(row) > 3 and row[3] else None,
        "groups_str": str(row[4]).strip() if len(row) > 4 and row[4] else ""
    }

def parse_fio(fio: str):
    """Парсит ФИО и генерирует username. Возвращает (last_name, first_name, username) или None"""
    fio_parts = fio.split()
    if len(fio_parts) < 2:
        return None

    last_name = fio_parts[0]
    first_name = fio_parts[1]
    last_name_en = transliterate(last_name).lower()
    first_name_en = transliterate(first_name).lower()
    username = f"{first_name_en}.{last_name_en}"

    return last_name, first_name, username

def parse_groups(groups_str: str):
    """Парсит строку групп через запятую"""
    if not groups_str:
        return []
    return [g.strip() for g in groups_str.split(',') if g.strip()]