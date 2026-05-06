"""
analyzers/headers.py — Módulo de análise de headers de segurança HTTP

Este módulo avalia os headers da resposta HTTP com foco na ausência ou
configuração fraca de diretivas de segurança importantes.

Cada header ausente ou mal configurado é convertido em uma vulnerabilidade
com severidade definida, baseada no impacto real que esse tipo de falha
pode ter em ataques web comuns.

## O que é analisado

- Headers de proteção contra XSS, clickjacking e MIME sniffing
- Política de segurança de conteúdo (CSP)
- Força de transporte via HTTPS (HSTS)
- Outras diretivas de hardening de navegador

## Abordagem

A análise é baseada em comparação direta entre headers esperados e os
retornados pelo servidor, priorizando simplicidade e confiabilidade.

## Referências

- OWASP Secure Headers Project
  https://owasp.org/www-project-secure-headers/

- Mozilla Observatory
  https://observatory.mozilla.org/
"""

from dataclasses import replace
from typing import Dict, List

from core.models import Vulnerability
from core import vuln_templates as T


_HEADER_TEMPLATES = {
    "content-security-policy": T.CSP_MISSING,
    "strict-transport-security": T.HSTS_MISSING,
    "x-frame-options": T.XFRAME_MISSING,
    "x-content-type-options": T.XCTO_MISSING,
    "x-xss-protection": T.XXSS_MISSING,
    "referrer-policy": T.REFERRER_MISSING,
    "permissions-policy": T.PERMISSIONS_MISSING,
}


def analyze(headers: Dict[str, str]) -> List[Vulnerability]:
   
    normalised = {k.lower(): v for k, v in headers.items()}
    findings: List[Vulnerability] = []

    for header_name, template in _HEADER_TEMPLATES.items():
        if header_name not in normalised:
           
            header_display = template.title.split(": ", 1)[-1]
            findings.append(
                T.build(
                    template,
                    evidence=f"Header '{header_display}' não presente na resposta HTTP.",
                )
            )

    return findings
