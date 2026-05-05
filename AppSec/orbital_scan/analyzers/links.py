"""
analyzers/links.py — Módulo de análise de segurança de hyperlinks

Este módulo avalia links presentes no HTML com foco em padrões comuns
utilizados em phishing, injeção de conteúdo e manipulação de navegação.

## O que é detectado

1. URLs encurtadas ou redirecionadas
   - Serviços como bit.ly, t.co, tinyurl.com
   - Podem ocultar o destino real do link, facilitando ataques de phishing

2. Mixed content (conteúdo misto)
   - Links HTTP dentro de páginas HTTPS
   - Podem permitir interceptação ou modificação de conteúdo em trânsito

3. Reverse tabnapping
   - Uso de `target="_blank"` sem `rel="noopener noreferrer"`
   - Permite que a nova aba manipule a página original

## Abordagem

A análise é baseada em inspeção estática do HTML renderizado, focando em
padrões conhecidos de risco em aplicações web modernas.

## Referências

- OWASP Testing Guide — OTG-CLIENT-006
- MDN Web Docs — rel=noopener
"""

from typing import List
from urllib.parse import urlparse

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

from core.models import Severity, Vulnerability
from core import vuln_templates as T

SHORTENER_DOMAINS = {
    "bit.ly", "t.co", "tinyurl.com", "ow.ly", "goo.gl",
    "buff.ly", "is.gd", "rb.gy", "short.io", "rebrand.ly",
    "tiny.cc", "lnkd.in", "bl.ink", "cutt.ly", "su.pr",
}


def _is_shortener(url: str) -> bool:
    try:
        host = urlparse(url).netloc.lower().removeprefix("www.")
        return host in SHORTENER_DOMAINS
    except Exception:
        return False


def analyze(html_body: str, base_url: str) -> List[Vulnerability]:
    if BeautifulSoup is None:
        return [Vulnerability(
            title="Módulo bs4 não instalado — análise de links ignorada",
            severity=Severity.LOW,
            description="Install beautifulsoup4 to enable link analysis.",
            evidence="pip install beautifulsoup4",
        )]

    findings: List[Vulnerability] = []
    soup = BeautifulSoup(html_body, "html.parser")
    base_scheme = urlparse(base_url).scheme.lower()

    shorteners_found: List[str] = []
    mixed_content: List[str] = []
    tabnapping: List[str] = []

    for anchor in soup.find_all("a", href=True):
        href = anchor["href"].strip()
        if not href or href.startswith(("#", "javascript:")):
            continue

        if _is_shortener(href):
            shorteners_found.append(href)

        if base_scheme == "https" and href.startswith("http://"):
            mixed_content.append(href)

        target = anchor.get("target", "").lower()
        rel = anchor.get("rel", [])
        if isinstance(rel, str):
            rel = rel.split()
        rel_lower = {r.lower() for r in rel}
        if target == "_blank" and not {"noopener", "noreferrer"}.intersection(rel_lower):
            tabnapping.append(href)

    if shorteners_found:
        sample = shorteners_found[:5]
        findings.append(T.build(
            T.LINKS_SHORTENER,
            evidence=(
                f"{len(shorteners_found)} link(s) encurtado(s) detectado(s). "
                f"Exemplos: {', '.join(sample)}"
            ),
        ))

    if mixed_content:
        sample = mixed_content[:5]
        findings.append(T.build(
            T.LINKS_MIXED_CONTENT,
            evidence=(
                f"{len(mixed_content)} link(s) HTTP em página HTTPS. "
                f"Exemplos: {', '.join(sample)}"
            ),
        ))

    if tabnapping:
        sample = tabnapping[:5]
        findings.append(T.build(
            T.LINKS_TABNAPPING,
            evidence=(
                f"{len(tabnapping)} link(s) target=_blank sem rel=noopener. "
                f"Exemplos: {', '.join(sample)}"
            ),
        ))

    return findings
