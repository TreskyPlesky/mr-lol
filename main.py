import os
import json
import sys
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
# Přidali jsme import funkce call_function vedle available_functions
from call_function import available_functions, call_function

def main():
    print("Hello from mr-lol!")

    # Načtení proměnných prostředí uvnitř main
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError("API key was not found in environment variables")

    # Inicializace klienta
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")

    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    verbose = args.verbose

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    max_iterations = 20
    for i in range(max_iterations):

            response = client.chat.completions.create(
                model="openrouter/free",
                messages=messages,
                tools=available_functions,
                temperature=0,
            )

            message = response.choices[0].message
            messages.append(message)

            # Pokud je zapnutý verbose mód, vypíšeme statistiky hned po získání odpovědi
            if verbose:
                usage = response.usage
                if usage is not None:
                    print("Prompt tokens:", usage.prompt_tokens)
                    print("Response tokens:", usage.completion_tokens)

            # Pokud model NECHCE volat funkce -> máme hotovo, vypíšeme výsledek a končíme
            if not message.tool_calls:
                print("Response:", message.content)
                return

            # Pokud model CHCE volat funkce -> zpracujeme je
            for tool_call in message.tool_calls:
                # 1. Zavoláme funkci
                result_message = call_function(tool_call, verbose=verbose)

                # 2. KONTROLA: Pokud je obsah prázdný, vyhodíme výjimku HNED (před uložením do messages)
                if not result_message["content"]:
                    raise Exception("The returned tool message has an empty content")

                # 3. Uložíme validní zprávu do historie
                messages.append(result_message)

                # 4. Pokud je zapnutý verbose mód, vytiskneme výsledek funkce
                if verbose:
                    print(f"-> {result_message['content']}")

    # Pokud cyklus proběhne 20x a neskončí přes "return" nahoře, jsme tady:
    print("Chyba: Agent se zacyklil!")
    sys.exit(1)

if __name__ == "__main__":
    main()
