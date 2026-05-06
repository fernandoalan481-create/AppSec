# 🧨 DirBull — Directory Bruteforcer

DirBull é uma ferramenta de **bruteforce de diretórios web** focada em velocidade, precisão e análise de respostas HTTP.  
Projetada para uso educacional e portfólio de segurança ofensiva.

> ⚠️ Aviso: esta ferramenta deve ser usada apenas em ambientes autorizados e testes controlados.

---

## 📌 Visão Geral

O **DirBull** realiza enumeração de diretórios em aplicações web utilizando wordlists, múltiplas threads e filtros inteligentes para reduzir falsos positivos.

Ele é integrado ao **AppSec Toolkit**, podendo ser executado diretamente pelo launcher principal.

---

## ⚙️ Funcionalidades

- 🚀 Bruteforce de diretórios via wordlist
- 🧵 Execução multithread para alta performance
- 🧠 Detecção de wildcard responses (falsos positivos)
- 🔍 Filtro inteligente de códigos HTTP (200, 301, 302, 403)
- 🔁 Fallback automático HEAD → GET
- 📊 Relatório final estruturado
- 🎨 Interface CLI colorida e interativa
- ⛔ Tratamento de interrupção (Ctrl + C)

---

## 🧱 Estrutura do Projeto


dirbull/
│
├── dirbull.py # Script principal da ferramenta
├── wordlists/ # Wordlists recomendadas (opcional)
└── output/ # Resultados e logs (opcional)


---

## 🚀 Como usar

### 🔹 Via AppSec Launcher (recomendado)

```bash
python start.py

Selecione:

[4] DirBull Directory Bruteforcer
🔹 Execução direta
python dirbull/dirbull.py
📥 Requisitos

Instale as dependências necessárias:

pip install requests tqdm colorama
📊 Exemplo de uso
Alvo: https://exemplo.com
Wordlist: common.txt
Threads: 20

Saída:

[  OK   ] /admin   https://exemplo.com/admin
[ FORBID] /backup  https://exemplo.com/backup
[ MOVED ] /login   https://exemplo.com/login
🧠 Recursos técnicos
Detecção de wildcard baseada em:
Status HTTP
Tamanho de resposta
Evita falsos positivos automaticamente
Prioriza performance com ThreadPoolExecutor
Suporte a servidores que não aceitam HEAD requests
🛡️ Aviso Legal

Este projeto é destinado exclusivamente para:

Testes de segurança autorizados
Ambientes controlados
Fins educacionais

Qualquer uso indevido é de total responsabilidade do usuário.

👨‍💻 Autor

Desenvolvido por: fernandoalan481-create
GitHub: https://github.com/fernandoalan481-create

📌 Futuras melhorias
Exportação de resultados em JSON/CSV
Integração com scanners OSINT
Suporte a proxies
Interface web opcional
Sistema de plugins de wordlist
