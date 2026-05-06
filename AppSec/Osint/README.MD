# 🛰️ All Seeing Eye OSINT Framework

Modular OSINT framework integrado ao **AppSec Toolkit**, focado em coleta, organização e análise de informações abertas (Open Source Intelligence).

> ⚠️ Uso educacional e em ambientes autorizados apenas.

---

## 📌 Visão Geral

O **All Seeing Eye OSINT** é um módulo do AppSec projetado para facilitar a execução de técnicas de OSINT de forma estruturada, automatizada e extensível.

Ele permite integrar diferentes coletores de dados em um único fluxo, tornando a investigação mais rápida e organizada.

---

## ⚙️ Funcionalidades

- 🔍 Estrutura modular de coletores (scanners)
- 🌐 Integração com múltiplas fontes OSINT
- 🧠 Organização centralizada de resultados
- 🧩 Fácil expansão com novos módulos
- 📊 Saída estruturada para análise
- 🖥️ Interface CLI integrada ao AppSec Launcher

---

## 🧱 Estrutura do Projeto


Osint/
│
├── main.py # Entry point do framework
├── core/ # Núcleo do sistema OSINT
├── collectors/ # Módulos de coleta (expandível)
├── utils/ # Funções auxiliares
└── data/ # Armazenamento de resultados


---

## 🚀 Como usar

Execute pelo launcher principal do AppSec:

```bash
python start.py

Ou execute diretamente:

python Osint/main.py
🧩 Como adicionar novos módulos

Crie um novo collector dentro da pasta:

Osint/collectors/

Exemplo:

def run(target):
    print(f"Coletando dados de {target}")

Depois registre no main.py.
