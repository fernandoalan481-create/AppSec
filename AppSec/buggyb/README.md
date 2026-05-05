🐛 BuggyB — Exploit Intelligence Engine

BuggyB é uma ferramenta CLI em Python para busca de exploits públicos baseada no dataset do Exploit-DB.
O objetivo é fornecer inteligência de vulnerabilidades de forma rápida, organizada e segura para fins educacionais e de análise.

🚀 Funcionalidades
🔎 Busca de exploits por palavra-chave (ex: apache, rce, wordpress)
📂 Integração com dataset oficial do Exploit-DB
📊 Output estruturado e legível no terminal
⚡ Busca rápida em memória (dataset carregado localmente)
🎯 Foco em informação, não execução de exploits
📦 Estrutura
buggyb/
│
├── main.py
├── intel/
│   ├── exploitdb_client.py
│   ├── exploit_formatter.py
│   └── files_exploits.csv   # (baixado manualmente)
📥 Instalação

Clone o repositório:

git clone https://github.com/fernandoalan481-create/orbitall-scan
cd AppSec/buggyb

Instale dependências (opcional):

pip install colorama
⚠️ Dataset obrigatório

O BuggyB utiliza o dataset público do Exploit-DB.

1. Baixe o arquivo:

👉 https://gitlab.com/exploit-database/exploitdb/-/raw/main/files_exploits.csv

2. Salve em:
buggyb/intel/files_exploits.csv
📖 Uso
🔹 Modo interativo
python main.py

Exemplo:

🐛 BuggyB — Buscar Exploits
Digite o termo: apache
🔹 Modo direto (CLI)
python main.py apache
📊 Exemplo de saída
[EDB-ID: 50567] Apache Path Traversal
Tipo: remote | Plataforma: linux | Data: 2021-10-06
Link: https://www.exploit-db.com/exploits/50567
⚠️ Aviso ético

Esta ferramenta é exclusivamente informativa.

❌ Não executa exploits
❌ Não automatiza ataques
❌ Não deve ser usada para atividades não autorizadas

Use apenas para:

✔ estudo
✔ análise de vulnerabilidades
✔ construção de relatórios

🧠 Objetivo do projeto

O BuggyB foi desenvolvido como parte de um toolkit de AppSec com foco em:

Segurança ofensiva (Red Team)
OSINT aplicado a vulnerabilidades
Desenvolvimento de ferramentas de segurança
🔗 Integração

O BuggyB faz parte do ecossistema:

Orbital Scan (scanner de vulnerabilidades)
AppSec Launcher (menu central)
🚧 Roadmap
 Filtro por plataforma (linux, windows)
 Filtro por tipo (RCE, LFI, SQLi)
 Ordenação por data / relevância
 Integração com APIs externas (VulnDB)
 Modo avançado tipo console (estilo metasploit)