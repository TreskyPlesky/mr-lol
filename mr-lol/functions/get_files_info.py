import os


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    try:
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    except Exception:
        valid_target_dir = False

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    try:
        files = os.listdir(target_dir)
        result = f'Success: "{directory}" is within the working directory\n'

        for file in files:
            full_path = os.path.join(target_dir, file)
            is_dir = os.path.isdir(full_path)
            file_size = os.path.getsize(full_path)

            result += f'- {file}: file_size={file_size} bytes, is_dir={is_dir}\n'
        return result.strip()  # .strip() odstraní poslední prázdný řádek
    except Exception as e:
        return f'Error reading directory: {str(e)}'


def main():
    # Nastavíme jako povolenou složku aktuální adresář
    MY_SAFE_DIR = os.getcwd()




if __name__ == "__main__":
    main()
