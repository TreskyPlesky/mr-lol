import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python (*.py) file within a permitted working directory and returns its output (STDOUT/STDERR). Use this to run calculations, scripts, or tests.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The relative path to the Python file from the root of the working directory (e.g., 'main.py' or 'scripts/calc.py').",
                },
                "args": {
                    "type": "array",
                    "description": "Optional command-line arguments to pass to the Python script. Each argument must be a separate string in the list (e.g., ['3', '+', '5']).",
                    "items": {
                        "type": "string"
                    }
                },
            },
            "required": ["file_path"], # Tímto říkáme, že file_path je povinný, ale args jsou volitelné
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
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
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # 3. Kontrola existence souboru
    if not os.path.isfile(target_file_abs):
        return f'Error: "{file_path}" does not exist or is not a regular file'


    # 4. Kontrola koncovky souboru
    if not target_file_abs.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'

    # 5. Subprocess
    command = ["python", target_file_abs]
    if args:
        command.extend(args)

    try:
        # check=False nám dovolí zpracovat návratový kód ručně bez vyhazování výjimek
        result = subprocess.run(command, check=False, text=True, capture_output=True, timeout=30)

        # Pokud program vrátil chybu (returncode není 0)
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}\nSTDERR: {result.stderr.strip()}"

        # Pokud program doběhl v pořádku, ale nic nevytiskl
        if not result.stdout.strip() and not result.stderr.strip():
            return 'No output produced'

        # Standardní úspěšný výstup
        return f"STDOUT: {result.stdout.strip()} STDERR: {result.stderr.strip()}"

    except subprocess.TimeoutExpired:
        return 'Error: Execution timed out'
    except Exception as e:
        return f"Error: executing Python file: {e}"
