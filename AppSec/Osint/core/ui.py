"""UI components: banner, tables, colors."""
import re
from colorama import Fore, Style, init
from pyfiglet import figlet_format as figlet_format

init(autoreset=True)

def gerar_banner(texto: str, font: str = "slant") -> str:
    """Generate ASCII banner."""
    try:
        ascii_art = figlet_format(texto, font=font)
        return f"{Fore.CYAN}{ascii_art}{Style.RESET_ALL}"
    except Exception as e:
        print(f"[UI] Banner font error: {e}")
        return f"{Fore.CYAN}{texto.upper()}{Style.RESET_ALL}\n{'=' * len(texto.upper())}\n"

from colorama import Fore, Style

def show_banner():
    banner = r"""⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠷⠛⠿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣷⠼⠶⠳⠾⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣏⣤⣄⣶⡤⢤⣹⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠏⠁⠉⠁⡀⠀⡈⠛⠹⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡟⠓⠚⠓⠘⠋⠘⠛⠙⠓⢿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠤⣴⢦⡦⠄⠾⠇⢸⡷⣤⣤⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡾⠗⠾⢋⣀⡀⠀⣤⡄⢀⣀⣀⣉⠈⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡿⠗⠈⣭⣄⣀⣤⣤⣤⣄⠀⣤⣙⡛⠻⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣯⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⡟⠛⠻⡟⠋⠉⠉⠉⢉⣽⡿⠛⠻⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣟⠻⠷⡆⢀⣀⣀⣀⣤⣤⣾⣁⣀⣀⡴⠋⣈⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣟⣿⢿⣋⣻⠿⠚⠛⠉⠁⠀⠤⠀⠺⠦⠬⣽⣿⣦⣾⡋⠀⠹⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣷⡾⠋⠁⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⡀⠀⠉⢙⠻⣿⣷⣤⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⠃⠀⠀⢀⣠⣤⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣝⠾⣝⠿⣿⠿⡄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢠⣾⡿⠀⢁⣠⣴⣿⡟⣿⣽⢻⡇⠀⢰⣿⣿⣿⣿⢸⡿⢹⢻⣿⣿⣿⡶⣾⣿⣳⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⡞⠉⣣⣶⣿⣿⣯⢻⡇⢹⣷⣟⢷⣦⣬⣽⣿⣿⢏⣿⢇⡏⠘⠋⢻⣿⣿⣿⣿⠹⣿⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣾⠛⠛⢿⣿⣿⡿⡜⡄⢻⡌⠻⣝⠃⢉⠛⠛⠋⣵⣿⣫⠟⢰⡆⢀⣾⣿⣿⣯⡿⢿⣆⢳⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣼⣅⠈⢻⠶⠆⠀⠉⠳⣽⠄⠙⠦⠈⠓⠾⠦⠽⠿⠷⠋⠁⠀⠏⠀⠘⢛⣿⣵⣿⠿⣶⡌⠛⢷⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣼⣥⣿⣏⡋⠀⠦⠀⣀⡀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣤⡴⣺⣿⣷⠻⠿⠆⠋⣈⣳⣬⣧⠀⠀⠀⠀
⠀⠀⠀⢰⣉⣹⣯⠉⠙⠒⢠⣀⠈⠁⠀⠀⠈⠛⠓⠒⠒⠒⠒⠛⠛⠉⠩⣥⢾⣻⣥⣬⡿⠄⠀⠒⢾⡉⢀⣉⣹⣧⠀⠀⠀
⠀⠀⢰⢻⣧⣉⠉⢻⣿⠦⢤⣉⣈⠉⠛⠒⠲⠶⠶⠶⣶⠶⣶⠶⠶⠶⣾⣛⣛⣙⣽⣿⡷⠴⠶⠲⡟⠉⠻⣧⡀⠘⣇⠀⠀
⠀⢠⣿⡙⠛⠛⣿⣿⢦⡀⠀⣈⡉⠀⠉⢻⡟⠛⠶⠶⠟⠿⢾⡿⠚⡛⠛⢛⣋⠉⣠⣤⠀⣤⡦⠼⠿⠶⣿⡛⢿⢻⣿⣆⠀
⠠⣿⣬⣽⣿⣴⣿⣯⣬⣤⣤⣽⣿⣦⣤⣴⣥⣤⣧⣦⣴⣴⣿⣷⣤⣯⣤⣾⣿⣦⣿⣧⣤⣥⣴⣤⣤⣤⣤⣽⣿⣿⣿⣿⡆"""
    print(Fore.GREEN + banner + Style.RESET_ALL)

    print(Fore.RED + "\n   [ All Seeying Eye OSINT FRAMEWORK | (v1.0.0) ]\n" + Style.RESET_ALL)
    print(Fore.WHITE + "        Modular Reconnaissance System\n" + Style.RESET_ALL)
    print(Fore.YELLOW + "Author: Alan Fernando | GitHub: https://github.com/fernandoalan481-create\n" + Style.RESET_ALL)
    print("=" * 90)

def criar_separador(titulo: str = "") -> str:
    """Create section separator."""
    largura = 90
    if titulo:
        resto = largura - len(titulo) - 4
        esquerda = "=" * (resto // 2)
        direita = "=" * (resto - resto // 2)
        return f"{Fore.WHITE}{esquerda} {Fore.MAGENTA}{titulo.upper()}{Fore.WHITE} {direita}{Style.RESET_ALL}"
    return f"{Fore.WHITE}{'=' * largura}{Style.RESET_ALL}"

def formatar_tabela(dados: dict) -> str:
    """Format data as colored table."""
    if not dados:
        return f"{Fore.RED}No data available.{Style.RESET_ALL}"
    
    itens = list(dados.items())
    if not itens:
        return f"{Fore.RED}No data.{Style.RESET_ALL}"
    
    max_key = max(len(str(k)) for k, _ in itens)
    max_val = min(60, max(len(str(v)) for _, v in itens))
    
    linhas = []
    border = f"{Fore.YELLOW}+{'-' * (max_key + 2)}+{'-' * (max_val + 2)}+{Style.RESET_ALL}"
    header = f"{Fore.YELLOW}| {str('KEY').ljust(max_key)} | {str('VALUE').ljust(max_val)} |{Style.RESET_ALL}"
    
    linhas.append(border)
    linhas.append(header)
    linhas.append(border)
    
    for k, v in itens:
        val_str = str(v).replace('\n', ' ')
        val_display = val_str[:max_val-3] + '..' if len(val_str) > max_val else val_str.ljust(max_val)
        linha = f"{Fore.YELLOW}|{Style.RESET_ALL} {str(k).ljust(max_key)} {Fore.YELLOW}| {Fore.CYAN}{val_display}{Fore.YELLOW} |{Style.RESET_ALL}"
        linhas.append(linha)
    
    linhas.append(border)
    return "\n".join(linhas)

def strip_ansi(text: str) -> str:
    """Remove ANSI colors from text."""
    return re.sub(r'\x1B(?:[0-9]{1,3}[;]?[0-9]{0,3}[m|K]|\\].*?(?:\x07|\x1B\\))', '', str(text))

