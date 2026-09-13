import os
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads file in a specified directory relative to the working directory, providing file content as string",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to file relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


def get_file_content(working_directory: str, file_path: str) -> str:
    # 1. Příprava absolutních cest
    working_dir_abs = os.path.abspath(working_directory)
    # Spojíme pracovní složku s cestou k souboru, aby to fungovalo správně relativně i absolutně
    target_file_abs = os.path.abspath(os.path.join(working_dir_abs, file_path))

    # 2. Kontrola bezpečnosti (Path Traversal)
    try:
        is_safe = os.path.commonpath([working_dir_abs, target_file_abs]) == working_dir_abs
    except Exception:
        is_safe = False

    if not is_safe:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # 3. Kontrola existence souboru (používáme absolutní cestu)
    if not os.path.isfile(target_file_abs):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    # 4. Bezpečné čtení a ořezání obsahu
    try:
        with open(target_file_abs, 'r', encoding='utf-8') as f: # Přidáno encoding pro jistotu
            file_content_string = f.read(MAX_CHARS)

            # Pokud po přečtení MAX_CHARS v souboru ještě něco zbylo...
            if f.read(1):
                file_content_string += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except Exception as e:
        return f'Error: Failed to read file "{file_path}": {str(e)}'

    return file_content_string
