
import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Adds string to a file in a specified directory relative to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to file relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "String to be added to file",
                },
            },
        },
    },
}


def write_file(working_directory: str, file_path: str, content: str) -> str:

    # 1. Příprava absolutních cest
    working_dir_abs = os.path.abspath(working_directory)
    # Spojíme pracovní složku s cestou k souboru
    target_file_abs = os.path.abspath(os.path.join(working_dir_abs, file_path))

    # 2. Kontrola bezpečnosti
    try:
        is_safe = os.path.commonpath([working_dir_abs, target_file_abs]) == working_dir_abs
    except Exception:
        is_safe = False

    if not is_safe:
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

    # 3. Kontrola existence souboru
    if os.path.isdir(target_file_abs):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    # 4. Tvorba cesty k souboru
    try:
        os.makedirs(os.path.dirname(target_file_abs), exist_ok=True)
    except Exception as e:
        return f'Error: Failed to create directory for "{file_path}": {str(e)}'

    # 5. Zapisování obsahu do souboru
    try:
        with open(target_file_abs, 'w') as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: Failed to write to "{file_path}": {str(e)}'
