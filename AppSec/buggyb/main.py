#!/usr/bin/env python3
"""
buggyb/main.py — CLI entrypoint for BuggyB (Exploit Intelligence Engine)

Suporta:
✔ Execução direta com argumento
    python main.py "apache"

✔ Modo interativo
    python main.py
"""

import sys

from intel.exploitdb_client import ExploitDBClient
from intel.exploit_formatter import (
    GREEN,
    print_results,
    print_dataset_missing
)


# -------------------------------
# Core
# -------------------------------
def run_search(client: ExploitDBClient, keyword: str):
    """
    Executa a busca e imprime os resultados formatados.
    """
    if not client.is_available():
        print_dataset_missing(client._csv_path)
        return

    results = client.search(keyword)
    print_results(results, keyword)


def main():
    client = ExploitDBClient()

    # importa cores do colorama
    try:
        from colorama import Fore, Style
        YELLOW = Fore.YELLOW + Style.BRIGHT
        CYAN   = Fore.CYAN + Style.BRIGHT
        BLUE   = Fore.BLUE + Style.BRIGHT
        DIM    = Style.DIM
        RESET  = Style.RESET_ALL
    except ImportError:
        YELLOW = CYAN = BLUE = DIM = RESET = ""

    # ✔ ASCII + header bonito (sem ANSI bugado)
    print(f"""
{GREEN}
       ^^         |         ^^

       ::         |         ::

^^     ::         |         ::     ^^

::     ::         |         ::     ::

 ::     ::        |        ::     ::

   ::    ::       |       ::    ::

     ::    ::   _/~\_   ::    ::

       ::   :::/     \:::   ::

         :::::(       ):::::

               \ ___ /

          :::::/`   `\:::::

        ::    ::\o o/::    ::

      ::     ::  :":  ::     ::

    ::      ::   ` `   ::      ::

   ::      ::           ::      ::

  ::      ::             ::      ::  

  ^^      ::             ::      ^^

          ::             ::

          ^^             ^^
                            
                 
$$$$$$$\                                                $$$$$$$\  
$$  __$$\                                               $$  __$$\ 
$$ |  $$ |$$\   $$\  $$$$$$\   $$$$$$\  $$\   $$\       $$ |  $$ |
$$$$$$$\ |$$ |  $$ |$$  __$$\ $$  __$$\ $$ |  $$ |      $$$$$$$\ |
$$  __$$\ $$ |  $$ |$$ /  $$ |$$ /  $$ |$$ |  $$ |      $$  __$$\ 
$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |      $$ |  $$ |
$$$$$$$  |\$$$$$$  |\$$$$$$$ |\$$$$$$$ |\$$$$$$$ |      $$$$$$$  |
\_______/  \______/  \____$$ | \____$$ | \____$$ |      \_______/ 
                    $$\   $$ |$$\   $$ |$$\   $$ |                
                    \$$$$$$  |\$$$$$$  |\$$$$$$  |                
                     \______/  \______/  \______/                                   

{RESET}
{CYAN}       BuggyB v1.0.0 — Buscador de Exploit [ Educacional / Portfolio ] {RESET}
{DIM} by https://github.com/fernandoalan481-create │ Use com responsabilidade {RESET} 

{RESET}
{DIM}        Uso educacional • Nenhum exploit é executado automaticamente{RESET}
""")

    # ✔ Caso 1: argumento direto
    if len(sys.argv) > 1:
        keyword = " ".join(sys.argv[1:]).strip()
        run_search(client, keyword)
        return

    # ✔ Caso 2: modo interativo
    try:
        while True:
            print("\n🐛 BuggyB — Buscar Exploits")
            keyword = input("Digite o termo (ou 'sair'): ").strip()

            if not keyword:
                continue

            if keyword.lower() in ("sair", "exit", "q"):
                print("\nVoltando ao menu principal...")
                return

            run_search(client, keyword)

    except KeyboardInterrupt:
        print("\n\nSaindo...")


# -------------------------------
# Entry
# -------------------------------
if __name__ == "__main__":
    main()