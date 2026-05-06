# 🛡️ AppSec Toolkit — Offensive Security Suite

O **AppSec Toolkit** é um conjunto modular de ferramentas CLI focadas em segurança de aplicações web, desenvolvido para aprendizado, prática e portfólio em segurança ofensiva.

O projeto integra múltiplas ferramentas em um único launcher, permitindo executar análises e coletar inteligência de segurança de forma centralizada.

> ⚠️ Uso estritamente educacional e em ambientes autorizados.

---

## 🚀 Ferramentas incluídas

### 🌐 Orbital Scan — Web Vulnerability Scanner

Scanner de vulnerabilidades web focado em análise de superfícies de ataque.

**Funcionalidades:**
- 🔐 Análise de headers HTTP (CSP, HSTS, etc.)
- 🍪 Inspeção de cookies (Secure, HttpOnly, SameSite)
- 🧾 Detecção de formulários HTML sensíveis
- 🔗 Identificação de links suspeitos e padrões de phishing
- ⚠️ Score de risco baseado em severidade

---

### 🐛 BuggyB — Exploit Intelligence Engine

Motor de busca de exploits baseado em dataset local do Exploit-DB.

**Funcionalidades:**
- 🔎 Busca por palavra-chave em exploits
- 📊 Resultados estruturados no terminal
- ⚡ Alta performance com dataset local
- 🎯 Uso informativo (não executa exploits)

---

## 🧱 Arquitetura do Projeto


AppSec/
│
├── start.py # Launcher principal
│
├── orbital-scan/
│ ├── main.py
│ ├── http_client.py
│ │
│ ├── analyzers/
│ │ ├── headers.py
│ │ ├── cookies.py
│ │ ├── forms.py
│ │ └── links.py
│ │
│ ├── core/
│ │ ├── scanner_engine.py
│ │ ├── risk_classifier.py
│ │ └── models.py
│ │
│ └── output/
│ └── cli_formatter.py
│
├── buggyb/
│ ├── main.py
│ └── intel/
│ ├── exploitdb_client.py
│ ├── exploit_formatter.py
│ └── files_exploits.csv
│
└── requirements.txt


---

## ▶️ Como usar

Execute o launcher principal:

```bash
python start.py
🎛️ Menu interativo
[1] Orbital Scan — Web Vulnerability Scanner
[2] BuggyB — Exploit Intelligence Engine
[0] Sair

Selecione uma ferramenta e siga as instruções no terminal.

📦 Instalação

Clone o repositório:

git clone https://github.com/fernandoalan481-create/orbitall-scan
cd AppSec

Instale as dependências:

pip install requests beautifulsoup4 colorama
⚙️ Configuração adicional (BuggyB)

Baixe o dataset oficial do Exploit-DB:

👉 https://gitlab.com/exploit-database/exploitdb/-/raw/main/files_exploits.csv

E salve em:

buggyb/intel/files_exploits.csv
🎯 Objetivo do projeto

Este projeto foi desenvolvido com foco em:

🛡️ Segurança ofensiva (Red Team)
🌐 AppSec (Application Security)
🧠 Desenvolvimento de ferramentas de segurança
📁 Portfólio técnico profissional
🚧 Roadmap
🔗 Integração Orbital Scan → BuggyB (correlação automática)
💻 Modo CLI avançado estilo framework (tipo Metasploit)
📄 Exportação de relatórios (JSON / HTML)
🎯 Suporte a múltiplos alvos simultâneos
🔌 Sistema de plugins para novas ferramentas
🧠 Inspiração

Ferramentas que inspiraram este projeto:

Burp Suite
OWASP ZAP
Metasploit Framework
⚠️ Aviso ético

Este software deve ser usado apenas para:

Ambientes controlados
Testes autorizados
Fins educacionais

O uso indevido pode violar legislações como:

Computer Fraud and Abuse Act (CFAA)
Marco Civil da Internet
LGPD (Brasil)
👨‍💻 Autor

Desenvolvido por: fernandoalan481-create
GitHub: https://github.com/fernandoalan481-create
