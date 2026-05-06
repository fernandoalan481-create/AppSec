"""
analyzers/cookies.py — Módulo de análise de segurança de cookies.

Faz o parsing dos headers Set-Cookie usando o mecanismo padrão do `http.cookiejar`
(via requests), em vez de usar comparação de strings “na mão”. Isso evita falsos positivos
que acontecem quando se procura nomes de flags dentro de valores de cookies ou atributos como path.

Flags de segurança avaliadas
-----------------------------

  Secure   — garante que o cookie só seja enviado via HTTPS
  HttpOnly — impede acesso ao cookie via JavaScript (mitiga roubo via XSS)
  SameSite — controla envio em requisições cross-site (mitiga ataques CSRF)

Referências
------------

- RFC 6265 § 5.2 (Parsing de Set-Cookie)
- OWASP Testing Guide — OTG-SESS-002
"""

from typing import List

from http_client import HttpResponse
from core.models import Vulnerability
from core import vuln_templates as T


def _parse_set_cookie_headers(response: HttpResponse) -> List[dict]:
    cookies = []
    if response.raw is None:
        return cookies

    for cookie in response.raw.cookies:
        raw_rest = {k.lower(): v for k, v in (cookie._rest or {}).items()}
        cookies.append({
            "name": cookie.name,
            "secure": bool(cookie.secure),
            "httponly": cookie.has_nonstandard_attr("HttpOnly"),
            "samesite": raw_rest.get("samesite", None),
        })

    if not cookies:
        for raw_header in _raw_set_cookie_values(response):
            cookies.append(_parse_single_set_cookie(raw_header))

    return cookies


def _raw_set_cookie_values(response: HttpResponse) -> List[str]:
    values = []
    if response.raw and hasattr(response.raw, "raw") and hasattr(response.raw.raw, "headers"):
        try:
            values = response.raw.raw.headers.getlist("Set-Cookie")
        except AttributeError:
            pass
    if not values:
        raw = response.headers.get("Set-Cookie", "")
        if raw:
            values = [raw]
    return values


def _parse_single_set_cookie(header_value: str) -> dict:
    parts = [p.strip() for p in header_value.split(";")]
    name = parts[0].split("=", 1)[0].strip() if parts else "unknown"
    attrs_lower = [p.lower() for p in parts[1:]]
    samesite = None
    for attr in parts[1:]:
        if attr.strip().lower().startswith("samesite"):
            samesite = attr.split("=", 1)[-1].strip() if "=" in attr else "present"
            break
    return {
        "name": name,
        "secure": "secure" in attrs_lower,
        "httponly": "httponly" in attrs_lower,
        "samesite": samesite,
    }


def analyze(response: HttpResponse) -> List[Vulnerability]:
    
    findings: List[Vulnerability] = []
    cookies = _parse_set_cookie_headers(response)

    for cookie in cookies:
        name = cookie["name"]

        if not cookie["secure"]:
            findings.append(
                T.build(
                    T.COOKIE_SECURE,
                    title=f"Cookie sem flag Secure: {name}",
                    evidence=f"Set-Cookie: {name}=...; [flag Secure ausente]",
                )
            )

        if not cookie["httponly"]:
            findings.append(
                T.build(
                    T.COOKIE_HTTPONLY,
                    title=f"Cookie sem flag HttpOnly: {name}",
                    evidence=f"Set-Cookie: {name}=...; [flag HttpOnly ausente]",
                )
            )

        if not cookie["samesite"]:
            findings.append(
                T.build(
                    T.COOKIE_SAMESITE,
                    title=f"Cookie sem atributo SameSite: {name}",
                    evidence=f"Set-Cookie: {name}=...; [atributo SameSite ausente]",
                )
            )

    return findings
