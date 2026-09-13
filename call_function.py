import json
from collections.abc import Callable

# Importujeme schémata (to už máš správně)
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

# Seznam schémat pro LLM
available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
]

# Definujeme mapování jmen (stringů) na skutečné spustitelné funkce
# Tento slovník dáme mimo funkci (nebo na její začátek), aby byl vždy po ruce
function_map: dict[str, Callable[..., str]] = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

def call_function(tool_call, verbose: bool = False) -> dict:
    # 1. Naparsujeme jméno a argumenty z JSONu
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments or "{}")

    # 2. Vypíšeme info podle nastavení verbose
    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    # 3. Kontrola, zda funkci vůbec známe
    if function_name not in function_map:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": f"Error: Unknown function: {function_name}",
        }

    # 4. Injekce pracovního adresáře (LLM o něm neví, ale naše funkce ho vyžadují)
    function_args["working_directory"] = "./calculator"

    # 5. Získání funkce ze slovníku a její samotné zavolání
    # Syntaxe **function_args rozbalí slovník na klíčové argumenty (např. arg="hodnota")
    actual_function = function_map[function_name]
    result = actual_function(**function_args)

    # 6. Vrácení výsledku ve formátu, kterému LLM rozumí (tzv. tool message)
    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result,
    }
