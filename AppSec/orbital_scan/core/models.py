"""
models.py — Estruturas centrais do Web Vulnerability Scanner

Este módulo define as estruturas de dados principais usadas pelo scanner,
incluindo a representação de vulnerabilidades, níveis de severidade e o
resultado consolidado de uma varredura.

O uso de `dataclasses` mantém o código simples, legível e tipado, sem
dependência de bibliotecas externas adicionais.

## Responsabilidades

- Padronizar como uma vulnerabilidade é representada no sistema
- Garantir consistência entre todos os analisadores
- Facilitar o cálculo e agregação de risco no relatório final

## Design

A abordagem prioriza:

- Simplicidade estrutural
- Facilidade de extensão
- Clareza para manutenção futura
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class Severity(str, Enum):

    LOW = "BAIXO"
    MEDIUM = "MÉDIO"
    HIGH = "ALTO"
    CRITICAL = "CRÍTICO"


@dataclass
class Vulnerability:
    """
    Representa uma vulnerabilidade ou configuração de segurança incorreta identificada.

    Campos principais
    -----------------
    title           : Identificador curto, ex: "Ausência de Content-Security-Policy"
    severity        : Um dos valores do enum Severity
    description     : Explicação técnica do motivo pelo qual isso é um problema
    evidence        : Artefato bruto extraído do alvo que comprova a ocorrência

    Campos de análise estruturada (todos opcionais, exibidos apenas quando preenchidos)
    ------------------------------------------------------------------------------------
    impact          : O que um atacante poderia alcançar caso explore esta falha
    condition       : Pré-condições necessárias para que a exploração seja possível
    validation      : Como um testador pode confirmar manualmente que a falha é real
    exploitability  : Classificação qualitativa + fatores contextuais (ex: "BAIXA isoladamente")
    remediation     : Orientações específicas e acionáveis para correção
    """

    title: str
    severity: Severity
    description: str
    evidence: str
    
    recommendation: Optional[str] = None
   
    impact: Optional[str] = None
    condition: Optional[str] = None
    validation: Optional[str] = None
    exploitability: Optional[str] = None
    remediation: Optional[str] = None

    def __eq__(self, other: object) -> bool:
        
        if not isinstance(other, Vulnerability):
            return NotImplemented
        return self.title == other.title

    def __hash__(self) -> int:
        return hash(self.title)


@dataclass
class ScanResult:
    
    target_url: str
    status_code: int
    response_time_ms: float
    vulnerabilities: List[Vulnerability] = field(default_factory=list)
    risk_score: int = 100
    risk_label: str = "BAIXO"

    def add_vulnerability(self, vuln: Vulnerability) -> None:
       
        if vuln not in self.vulnerabilities:
            self.vulnerabilities.append(vuln)

    @property
    def critical_count(self) -> int:
        return sum(1 for v in self.vulnerabilities if v.severity == Severity.CRITICAL)

    @property
    def high_count(self) -> int:
        return sum(1 for v in self.vulnerabilities if v.severity == Severity.HIGH)

    @property
    def medium_count(self) -> int:
        return sum(1 for v in self.vulnerabilities if v.severity == Severity.MEDIUM)

    @property
    def low_count(self) -> int:
        return sum(1 for v in self.vulnerabilities if v.severity == Severity.LOW)
