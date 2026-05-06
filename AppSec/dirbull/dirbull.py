import os
import re
import sys
import time
import threading
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from colorama import Fore, Back, Style, init

# Inicializa colorama para compatibilidade com Windows/Linux
init(autoreset=True)

# ─── Paleta de cores e símbolos ───────────────────────────────────────────────
OK    = f"{Fore.GREEN}✔{Style.RESET_ALL}"
WARN  = f"{Fore.YELLOW}⚠{Style.RESET_ALL}"
ERR   = f"{Fore.RED}✘{Style.RESET_ALL}"
INFO  = f"{Fore.CYAN}ℹ{Style.RESET_ALL}"
ARROW = f"{Fore.MAGENTA}›{Style.RESET_ALL}"

# ─── Banner ASCII ─────────────────────────────────────────────────────────────
BANNER = f"""
{Style.BRIGHT}{Fore.RED}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣴⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣦⡀⠀
⠀⢸⣿⣧⣀⣀⠀⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⢀⣀⣼⣿⡧⠀
⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⠿⠁⠀
⠀⠀⠀⠀⠙⠛⠿⠿⠿⠿⣿⠀⠀⠀⠀⠀⠀⠀⠀⣿⡿⠿⠿⠿⠛⠋⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣤⡄⠀⠀⠀⠀⠀⠀⢀⣤⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⠿⠀⠀⠀⠀⠀⠀⠿⠿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡆⠀⠀⢠⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⣿⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠷⣦⣤⡾⠋⠀⠀⠀⠀⠀⠀


⠀⠀⠀⠀⠀⠀
⠀DirBull v1.0.0 — Bruteforce de diretórios [ Educacional / Portfolio ]
 by https://github.com/fernandoalan481-create │ Use com responsabilidade⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

{Style.RESET_ALL}"""

# ─── Helpers visuais ──────────────────────────────────────────────────────────

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def linha(char="─", largura=72, cor=Fore.MAGENTA):
    print(f"{cor}{char * largura}{Style.RESET_ALL}")


def caixa_erro(titulo, mensagem, dica=None):
    """Exibe um bloco de erro visual com título, mensagem e dica opcional."""
    largura = 68
    print()
    print(f"  {Fore.RED}╔{'═' * largura}╗{Style.RESET_ALL}")
    print(f"  {Fore.RED}║{Style.RESET_ALL}  {Style.BRIGHT}{Fore.RED}✘  {titulo:<{largura - 5}}{Style.RESET_ALL}{Fore.RED}║{Style.RESET_ALL}")
    print(f"  {Fore.RED}╠{'═' * largura}╣{Style.RESET_ALL}")
    # Quebra mensagem longa em múltiplas linhas
    palavras = mensagem.split()
    linhas_msg = []
    linha_atual = ""
    for p in palavras:
        if len(linha_atual) + len(p) + 1 > largura - 4:
            linhas_msg.append(linha_atual)
            linha_atual = p
        else:
            linha_atual = f"{linha_atual} {p}".strip()
    if linha_atual:
        linhas_msg.append(linha_atual)
    for l in linhas_msg:
        print(f"  {Fore.RED}║{Style.RESET_ALL}  {Fore.WHITE}{l:<{largura - 2}}{Style.RESET_ALL}{Fore.RED}║{Style.RESET_ALL}")
    if dica:
        print(f"  {Fore.RED}╠{'═' * largura}╣{Style.RESET_ALL}")
        print(f"  {Fore.RED}║{Style.RESET_ALL}  {Fore.YELLOW}Dica:{Style.RESET_ALL} {dica:<{largura - 7}}{Fore.RED}║{Style.RESET_ALL}")
    print(f"  {Fore.RED}╚{'═' * largura}╝{Style.RESET_ALL}")
    print()


def caixa_aviso(titulo, mensagem):
    """Exibe um bloco de aviso amarelo."""
    largura = 68
    print()
    print(f"  {Fore.YELLOW}╔{'═' * largura}╗{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}║{Style.RESET_ALL}  {Style.BRIGHT}{Fore.YELLOW}⚠  {titulo:<{largura - 5}}{Style.RESET_ALL}{Fore.YELLOW}║{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}╠{'═' * largura}╣{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}║{Style.RESET_ALL}  {Fore.WHITE}{mensagem:<{largura - 2}}{Style.RESET_ALL}{Fore.YELLOW}║{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}╚{'═' * largura}╝{Style.RESET_ALL}")
    print()


def caixa_info(mensagem):
    """Exibe uma linha informativa simples."""
    print(f"  {Fore.CYAN}│{Style.RESET_ALL}  {INFO}  {mensagem}")


# ─── Cores por status HTTP ────────────────────────────────────────────────────
STATUS_COR = {
    200: Fore.GREEN,
    301: Fore.CYAN,
    302: Fore.CYAN,
    403: Fore.YELLOW,
}

STATUS_LABEL = {
    200: "OK",
    301: "MOVED",
    302: "FOUND",
    403: "FORBID",
}

# Lock para acesso thread-safe à lista de resultados
_lock = threading.Lock()
resultados = []  

_wildcard_status = None
_wildcard_len    = None


# ─── Validações ───────────────────────────────────────────────────────────────

def validar_url(url):
    url = url.strip()
    if not url:
        return False
    if not re.match(r'^https?://', url):
        return False
    return url.rstrip('/')


def obter_wordlist():
    while True:
        print(f"\n  {ARROW}  ", end="")
        caminho = input(
            f"{Fore.YELLOW}Caminho da wordlist{Style.RESET_ALL} "
            f"{Fore.WHITE}(ex: /usr/share/wordlists/common.txt){Style.RESET_ALL}: "
        ).strip()

        if not os.path.exists(caminho):
            caixa_erro(
                "Wordlist não encontrada",
                f"O arquivo '{caminho}' não existe no sistema.",
                dica="Verifique o caminho ou use Tab para autocompletar."
            )
            continue

        try:
            with open(caminho, 'rb') as f:
                total_linhas = sum(1 for _ in f)
        except Exception as e:
            caixa_erro("Erro ao abrir wordlist", str(e))
            continue

        print()
        caixa_info(f"Wordlist carregada: {Fore.CYAN}{caminho}{Style.RESET_ALL}")
        caixa_info(f"Total de entradas:  {Fore.CYAN}{total_linhas:,}{Style.RESET_ALL}")

        print(f"\n  {ARROW}  ", end="")
        confirmacao = input(
            f"{Fore.YELLOW}Confirmar e iniciar?{Style.RESET_ALL} {Fore.WHITE}[S/n]{Style.RESET_ALL}: "
        ).strip().lower()

        if confirmacao not in ('', 's', 'sim'):
            caixa_aviso("Operação cancelada", "Escolha outra wordlist ou pressione Ctrl+C para sair.")
            continue

        return caminho, total_linhas


# ─── Worker ───────────────────────────────────────────────────────────────────

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def detectar_wildcard(alvo):

    url_fake = f"{alvo}/isso_nao_existe_xkq7z9w3"
    try:
        r = requests.get(url_fake, timeout=8, headers=HEADERS, allow_redirects=True)
        return r.status_code, len(r.text)
    except requests.RequestException:
        return None, None


def _fazer_requisicao(url):

    resposta = requests.head(url, timeout=5, allow_redirects=True, headers=HEADERS)
    if resposta.status_code in (405, 501):

        resposta = requests.get(url, timeout=5, allow_redirects=True, headers=HEADERS)
    return resposta


def testar_diretorio(args):
    alvo, palavra = args
    url = f"{alvo}/{palavra}"

    try:
        resposta = _fazer_requisicao(url)
        status   = resposta.status_code
        corpo_len = len(resposta.text) if hasattr(resposta, 'text') else 0

        # ── Filtro de wildcard ──────────────────────────────────────────────
        # Se o servidor responde igual a qualquer URL fake, é falso positivo
        if (
            _wildcard_status is not None
            and status == _wildcard_status
            and corpo_len == _wildcard_len
        ):
            return  # ignora silenciosamente

        redirecionado = (resposta.url != url and status == 200)

        if status in STATUS_COR and not redirecionado:
            cor   = STATUS_COR[status]
            label = STATUS_LABEL.get(status, str(status))
            tqdm.write(
                f"  {cor}[{label:>6}]{Style.RESET_ALL}  "
                f"{Fore.WHITE}/{palavra}{Style.RESET_ALL}  "
                f"{Fore.WHITE}{url}{Style.RESET_ALL}"
            )
            with _lock:
                resultados.append({"palavra": palavra, "url": url, "status": status})

        elif redirecionado:
            tqdm.write(
                f"  {Fore.YELLOW}[REDIR ]{Style.RESET_ALL}  "
                f"{Fore.WHITE}/{palavra}{Style.RESET_ALL}  "
                f"{Fore.YELLOW}→ {resposta.url}{Style.RESET_ALL}"
            )

    except requests.ConnectionError:
        tqdm.write(f"  {ERR}  {Fore.RED}Conexão recusada:{Style.RESET_ALL} /{palavra}")
    except requests.Timeout:
        tqdm.write(f"  {WARN}  {Fore.YELLOW}Timeout:{Style.RESET_ALL} /{palavra}")
    except requests.RequestException as e:
        tqdm.write(f"  {ERR}  {Fore.RED}Erro em /{palavra}:{Style.RESET_ALL} {e}")


# ─── Tabela de resultados ─────────────────────────────────────────────────────

def exibir_tabela(alvo, total_testado, duracao):
    limpar_tela()
    print(BANNER)

    largura = 72
    col_status = 8
    col_path   = 28
    col_url    = largura - col_status - col_path - 6

    linha("═", largura)
    print(f"  {Style.BRIGHT}{Fore.MAGENTA}RELATÓRIO FINAL{Style.RESET_ALL}")
    linha("═", largura)

    print(f"  {INFO}  Alvo           : {Fore.CYAN}{alvo}{Style.RESET_ALL}")
    print(f"  {INFO}  Testados       : {Fore.CYAN}{total_testado:,}{Style.RESET_ALL}")
    print(f"  {INFO}  Encontrados    : {Fore.GREEN}{len(resultados)}{Style.RESET_ALL}")
    print(f"  {INFO}  Tempo total    : {Fore.CYAN}{duracao:.1f}s{Style.RESET_ALL}")
    wc_info = (
        f"{Fore.YELLOW}ativo (filtro de falso positivo ligado){Style.RESET_ALL}"
        if _wildcard_status == 200
        else f"{Fore.GREEN}não detectado{Style.RESET_ALL}"
    )
    print(f"  {INFO}  Wildcard       : {wc_info}")
    linha("─", largura)

    if not resultados:
        print(f"\n  {WARN}  Nenhum diretório encontrado.\n")
        linha("═", largura)
        return

    # Cabeçalho da tabela
    print(
        f"  {Style.BRIGHT}"
        f"{'STATUS':<{col_status}}  "
        f"{'CAMINHO':<{col_path}}  "
        f"{'URL COMPLETA':<{col_url}}"
        f"{Style.RESET_ALL}"
    )
    linha("─", largura)

    # Ordena por status depois por path
    for r in sorted(resultados, key=lambda x: (x["status"], x["palavra"])):
        status = r["status"]
        cor    = STATUS_COR.get(status, Fore.WHITE)
        label  = STATUS_LABEL.get(status, str(status))
        path   = f"/{r['palavra']}"
        url    = r["url"]

        # Trunca URL se muito longa
        if len(url) > col_url:
            url = url[:col_url - 3] + "..."

        print(
            f"  {cor}{label:<{col_status}}{Style.RESET_ALL}  "
            f"{Fore.WHITE}{path:<{col_path}}{Style.RESET_ALL}  "
            f"{Fore.CYAN}{url:<{col_url}}{Style.RESET_ALL}"
        )

    linha("═", largura)
    print(f"\n  {OK}  Varredura concluída.\n")


# ─── Brute-force principal ───────────────────────────────────────────────────

def bruteforce_dir(alvo, wordlist_path, workers=20):
    global resultados, _wildcard_status, _wildcard_len
    resultados       = []
    _wildcard_status = None
    _wildcard_len    = None

    palavras = []
    try:
        with open(wordlist_path, 'rb') as f:
            palavras = [
                line.decode('utf-8', errors='ignore').strip()
                for line in f if line.strip()
            ]
    except Exception as e:
        caixa_erro("Erro ao ler wordlist", str(e))
        return

    if not palavras:
        caixa_erro("Wordlist vazia", "O arquivo não contém entradas válidas.")
        return

    linha()
    caixa_info(f"Iniciando varredura em {Fore.CYAN}{alvo}{Style.RESET_ALL}")
    caixa_info(f"Threads ativas: {Fore.CYAN}{workers}{Style.RESET_ALL}")

    # ── Detecção de wildcard ───────────────────────────────────────────────
    print(f"\n  {INFO}  {Fore.WHITE}Verificando wildcard...{Style.RESET_ALL}", end=" ", flush=True)
    _wildcard_status, _wildcard_len = detectar_wildcard(alvo)
    if _wildcard_status is not None:
        if _wildcard_status == 200:
            print(
                f"{Fore.YELLOW}⚠  Wildcard detectado!{Style.RESET_ALL}  "
                f"Servidor retorna {Fore.YELLOW}200{Style.RESET_ALL} para URLs inexistentes "
                f"(body={_wildcard_len} bytes). Falsos positivos serão filtrados."
            )
        else:
            print(
                f"{Fore.GREEN}✔  OK{Style.RESET_ALL}  "
                f"Servidor retorna {Fore.CYAN}{_wildcard_status}{Style.RESET_ALL} para URLs inexistentes."
            )
    else:
        print(f"{Fore.YELLOW}⚠  Não foi possível verificar (sem conexão?). Prosseguindo sem filtro.{Style.RESET_ALL}")

    linha()

    tarefas    = [(alvo, p) for p in palavras]
    inicio     = time.time()

    try:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            list(tqdm(
                executor.map(testar_diretorio, tarefas),
                total=len(tarefas),
                desc=f"  {Fore.MAGENTA}Varrendo{Style.RESET_ALL}",
                unit=" req",
                ncols=72,
                bar_format=(
                    "  {desc}: {percentage:3.0f}%"
                    " {bar} {n_fmt}/{total_fmt}"
                    " [{elapsed}<{remaining}, {rate_fmt}]"
                )
        ))
    except KeyboardInterrupt:
        caixa_aviso("Interrompido", "Parando varredura...")
    return

    duracao = time.time() - inicio
    exibir_tabela(alvo, len(palavras), duracao)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    limpar_tela()
    print(BANNER)
    linha()

    # 1. URL alvo
    while True:
        print(f"\n  {ARROW}  ", end="")
        alvo_input = input(
            f"{Fore.YELLOW}Alvo{Style.RESET_ALL} "
            f"{Fore.WHITE}(ex: https://exemplo.com){Style.RESET_ALL}: "
        )
        alvo = validar_url(alvo_input)
        if alvo:
            break
        caixa_erro(
            "URL inválida",
            f"'{alvo_input.strip()}' não é uma URL válida.",
            dica="A URL deve começar com http:// ou https://"
        )

    limpar_tela()
    print(BANNER)
    linha()
    caixa_info(f"Alvo confirmado: {Fore.CYAN}{alvo}{Style.RESET_ALL}")

    # 2. Wordlist
    wordlist_path, _ = obter_wordlist()

    limpar_tela()
    print(BANNER)

    # 3. Executa
    bruteforce_dir(alvo, wordlist_path)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print()

        caixa_aviso(
            "Interrompido pelo usuário",
            "Voltando ao menu principal..."
        )

        resultados.clear()

        sys.exit(0)