🛡️ AppSec Toolkit — Offensive Security Suite

O AppSec Toolkit é um conjunto modular de ferramentas CLI focadas em segurança de aplicações web, desenvolvido para aprendizado, prática e portfólio em segurança ofensiva.

O projeto integra múltiplas ferramentas em um único launcher, permitindo executar análises e coletar inteligência de vulnerabilidades de forma centralizada.

🚀 Ferramentas incluídas
🌐 Orbital Scan

Scanner de vulnerabilidades web que identifica falhas comuns de segurança.

🔐 Headers HTTP (CSP, HSTS, etc.)
🍪 Cookies (Secure, HttpOnly, SameSite)
🧾 Formulários HTML
🔗 Links suspeitos e padrões de phishing
⚠️ Score de risco baseado em severidade
🐛 BuggyB

Motor de busca de exploits baseado no dataset do Exploit-DB.

🔎 Busca por palavra-chave
📊 Resultados estruturados no terminal
⚡ Alta performance (dataset local)
🎯 Uso informativo (não executa exploits)
🧱 Arquitetura
AppSec/
│
├── start.py              # Launcher principal
│
├── orbital-scan/
├── main.py
├── http_client.py
│
├── analyzers/
│   ├── headers.py
│   ├── cookies.py
│   ├── forms.py
│   └── links.py
│
├── core/
│   ├── scanner_engine.py
│   ├── risk_classifier.py
│   └── models.py
│
├── output/
│   └── cli_formatter.py
│
└── requirements.txt
│
└── buggyb/
    ├── main.py
    └── intel/
        ├── exploitdb_client.py
        ├── exploit_formatter.py
        └── files_exploits.csv
▶️ Como usar

Execute o launcher principal:

python start.py
🎛️ Menu interativo
[1] Orbital Scan — Web Vulnerability Scanner
[2] BuggyB      — Exploit Intelligence Engine
[0] Sair

Selecione a ferramenta desejada e utilize normalmente.

📦 Instalação
git clone https://github.com/fernandoalan481-create/orbitall-scan
cd AppSec

Dependências:

pip install requests beautifulsoup4 colorama
⚠️ Configuração adicional (BuggyB)

Baixe o dataset do Exploit-DB:

👉 https://gitlab.com/exploit-database/exploitdb/-/raw/main/files_exploits.csv

Salve em:

buggyb/intel/files_exploits.csv
🎯 Objetivo do projeto

Este projeto foi desenvolvido com foco em:

Segurança ofensiva (Red Team)
AppSec (Application Security)
Desenvolvimento de ferramentas de segurança
Construção de portfólio técnico
⚠️ Aviso ético

Use apenas em ambientes autorizados.

O uso indevido pode violar leis como:

Computer Fraud and Abuse Act (EUA)
LGPD / Marco Civil da Internet (Brasil)
🚧 Roadmap
 Integração Orbital → BuggyB (correlação automática)
 Modo console interativo (estilo metasploit)
 Exportação de relatórios (JSON / HTML)
 Suporte a múltiplos alvos
 Plugin system para novas ferramentas
🧠 Inspiração

Ferramentas que inspiraram o projeto:

Burp Suite
OWASP ZAP
Metasploit Framework