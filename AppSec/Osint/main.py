#!/usr/bin/env python3
"""SKYNET OSINT - Stable CLI + Interactive Mode"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from colorama import Fore

from core.ui import show_banner, criar_separador, formatar_tabela
from core.dependencies import check_dependencies, playwright_browser_check

from collectors.github import GithubCollector
from collectors.google import GoogleCollector
from collectors.instagram import InstagramCollector


# -------------------------
# LOAD FIXO
# -------------------------
def load_collectors():
    return [
        GithubCollector(),
        GoogleCollector(),
        InstagramCollector()
    ]


# -------------------------
# OSINT ENGINE (run_osint)
# -------------------------
def run_osint(nome, user, collector_filter=None):

    print(f"{Fore.CYAN}Target: {nome} (@{user}){Fore.RESET}")
    print(f"{Fore.WHITE}Generated: {datetime.now().strftime('%d/%m/%Y %H:%M')}{Fore.RESET}")
    print("=" * 80)

    # deps
    print(f"\n{Fore.YELLOW}[CHECK] Dependencies...{Fore.RESET}")
    check_dependencies()
    playwright_browser_check()

    # collectors
    collectors = load_collectors()

    if collector_filter and collector_filter.lower().strip() != 'all':
        filter_names = [cf.strip() for cf in collector_filter.split(",")]
        collectors = [c for c in collectors if c.name in filter_names]

    if not collectors:
        print(f"{Fore.RED}[!] Nenhum collector encontrado{Fore.RESET}")
        input("\nENTER para voltar...")
        return

    print(f"\n{Fore.GREEN}Loaded: {', '.join(c.name.upper() for c in collectors)}{Fore.RESET}\n")

    # run
    for collector in collectors:
        print(criar_separador(collector.name.upper()))
        print(f"{Fore.YELLOW}Executando {collector.name.upper()}...{Fore.RESET}")

        try:
            result = collector.collect(nome, user)
            data = result.get("data", [])

            if not data:
                print(f"{Fore.YELLOW}No data{Fore.RESET}")
                continue

            # Google especial
            if collector.name == "google":
                print(f"{Fore.YELLOW}Total resultados: {len(data)}{Fore.RESET}")

                for item in data[:10]:
                    print(f"{Fore.BLUE}• {item.get('title','N/A')}{Fore.RESET}")
                    print(f"  {item.get('url','N/A')}\n")

            else:
                print(formatar_tabela(data[0]))

        except Exception as e:
            print(f"{Fore.RED}ERRO {collector.name}: {e}{Fore.RESET}")

    print(criar_separador("COMPLETE"))
    print(f"{Fore.GREEN}🎯 OSINT COMPLETE{Fore.RESET}")

    input("\nENTER para voltar ao menu...")


# -------------------------
# INTERACTIVE MODE
# -------------------------
def interactive_mode():
    show_banner()

    print("\n All Seeying Eye OSINT - Interactive Mode\n")

    nome = input("Nome alvo: ").strip()
    user = input("Username: ").strip()
    collector = input("Collectors (google,github,instagram / ENTER=all): ").strip()

    run_osint(nome, user, collector or None)


# -------------------------
# MAIN
# -------------------------
def main():

    # ✔ se rodar sem args → modo menu/interativo
    if len(sys.argv) == 1:
        interactive_mode()
        return

    try:
        nome = sys.argv[1]
        user = sys.argv[2]
    except:
        interactive_mode()
        return

    run_osint(nome, user)


if __name__ == "__main__":
    main()

