#!/usr/bin/env python3
"""
AppSec Launcher — Menu principal para ferramentas

Fácil de expandir: basta adicionar novos itens no dict TOOLS.
"""

import subprocess
import sys
import os

# ------------------------------------------------------------------
# CORES (colorama opcional)
# ------------------------------------------------------------------
try:
    from colorama import Fore, Style, init
    init(autoreset=True)

    RED    = Fore.RED + Style.BRIGHT
    GREEN  = Fore.GREEN + Style.BRIGHT
    YELLOW = Fore.YELLOW + Style.BRIGHT
    CYAN   = Fore.CYAN + Style.BRIGHT
    BLUE   = Fore.BLUE + Style.BRIGHT
    WHITE  = Fore.WHITE + Style.BRIGHT
    DIM    = Style.DIM
    RESET  = Style.RESET_ALL

except ImportError:
    RED = GREEN = YELLOW = CYAN = BLUE = WHITE = DIM = RESET = ""


# ------------------------------------------------------------------
# CONFIGURAÇÃO DAS FERRAMENTAS (FÁCIL DE EXPANDIR)
# ------------------------------------------------------------------
TOOLS = {
    "1": {
        "name": "Orbital Scan",
        "desc": "Web Vulnerability Scanner",
        "path": "orbital_scan/main.py"
    },
    "2": {
        "name": "BuggyB",
        "desc": "Exploit Intelligence Engine",
        "path": "buggyb/main.py"
    },
}


# ------------------------------------------------------------------
# ASCII ART PRINCIPAL
# ------------------------------------------------------------------
def print_banner():
    print(f"""
{RED}
                                           
                                          
▄████▄ █████▄ █████▄ ▄█████ ██████ ▄█████ 
██▄▄██ ██▄▄█▀ ██▄▄█▀ ▀▀▀▄▄▄ ██▄▄   ██     
██  ██ ██     ██     █████▀ ██▄▄▄▄ ▀█████ 
                                          
{RESET}
{WHITE} AppSec Toolkit — Offensive Security Suite │ by https://github.com/fernandoalan481-create{RESET}
{DIM}           Uso educacional • Apenas ambientes autorizados{RESET}
""")


# ------------------------------------------------------------------
# MENU
# ------------------------------------------------------------------
def print_menu():
    print(f"\n{YELLOW}Selecione uma ferramenta:\n{RESET}")

    for key, tool in TOOLS.items():
        print(f"{CYAN}[{key}]{RESET} {WHITE}{tool['name']}{RESET} {DIM}— {tool['desc']}{RESET}")

    print(f"\n{RED}[0]{RESET} Sair")


# ------------------------------------------------------------------
# EXECUTOR
# ------------------------------------------------------------------
def run_tool(path):
    full_path = os.path.join(os.path.dirname(__file__), path)

    if not os.path.exists(full_path):
        print(f"{RED}[ERRO]{RESET} Arquivo não encontrado: {full_path}")
        return

    try:
        subprocess.run([sys.executable, full_path])
    except Exception as e:
        print(f"{RED}[ERRO]{RESET} Falha ao executar: {e}")


# ------------------------------------------------------------------
# MAIN LOOP
# ------------------------------------------------------------------
def main():
    while True:
        print_banner()
        print_menu()

        choice = input(f"\n{BLUE}>>> {RESET}").strip()

        if choice == "0":
            print(f"\n{DIM}Saindo...{RESET}")
            break

        tool = TOOLS.get(choice)

        if not tool:
            print(f"\n{RED}Opção inválida.{RESET}")
            continue

        print(f"\n{GREEN}Abrindo {tool['name']}...{RESET}\n")
        run_tool(tool["path"])
        print(f"\n{DIM}Retornando ao menu principal...{RESET}")
        os.system("cls" if os.name == "nt" else "clear")


# ------------------------------------------------------------------
# ENTRY
# ------------------------------------------------------------------
if __name__ == "__main__":
    main()
