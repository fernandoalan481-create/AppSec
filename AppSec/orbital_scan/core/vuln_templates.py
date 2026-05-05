"""
core/vuln_templates.py — Modelos reutilizáveis de vulnerabilidades estruturadas.

Cada template é um objeto Vulnerability pré-preenchido cobrindo os achados mais comuns.
Os analisadores importam e clonam esses templates (via dataclasses.replace) para
inserir evidências específicas do contexto sem duplicar textos estáticos.

Racional de design
------------------
  * Mantém o código dos analisadores limpo — sem blocos grandes de strings.
  * Garante consistência: cada ocorrência de "CSP ausente" possui o mesmo
    impacto, condição e correção independentemente do analisador que a detecta.
  * Fácil de expandir: basta adicionar um novo template e importá-lo.
"""

from dataclasses import replace
from core.models import Severity, Vulnerability




def build(template: Vulnerability, *, title: str = None, evidence: str) -> Vulnerability:
   
    overrides = {"evidence": evidence}
    if title is not None:
        overrides["title"] = title
    return replace(template, **overrides)


# ---------------------------------------------------------------------------
# HEADER templates
# ---------------------------------------------------------------------------

CSP_MISSING = Vulnerability(
    title="Missing header: Content-Security-Policy",
    severity=Severity.HIGH,
    description=(
    "Content-Security-Policy (CSP) não foi encontrada na resposta. "
    "Sem a CSP, o navegador não possui uma lista de fontes de conteúdo confiáveis."
),
    evidence="",  
    impact=(
        "Pode permitir a execução de scripts maliciosos injetados via XSS, "
        "carregamento de recursos de origens não confiáveis e ataques de "
        "data-injection contra os usuários da aplicação."
    ),
    condition=(
        "Requer que o atacante consiga injetar conteúdo na página "
        "(ex: via XSS refletido, armazenado ou via injeção de parâmetros). "
        "A ausência de CSP amplia o impacto de outras vulnerabilidades."
    ),
    validation=(
        "Inspecionar os headers da resposta HTTP e confirmar que o header "
        "'Content-Security-Policy' está ausente. Ferramentas: DevTools "
        "(Network > Headers), curl -I <url> | grep -i csp."
    ),
    exploitability="MÉDIA isoladamente / ALTA se combinada com XSS",
    remediation=(
        "Implementar uma política restritiva: "
        "Content-Security-Policy: default-src 'self'; script-src 'self'; "
        "object-src 'none'; base-uri 'self'. "
        "Usar o cabeçalho Content-Security-Policy-Report-Only em staging "
        "antes de aplicar em produção."
    ),
)

HSTS_MISSING = Vulnerability(
    title="Missing header: Strict-Transport-Security",
    severity=Severity.HIGH,
    description=(
        "HTTP Strict-Transport-Security (HSTS) está ausente. "
        "Sem HSTS, browsers podem aceitar conexões HTTP em downgrade."
    ),
    evidence="",
    impact=(
        "Pode permitir ataques de SSL-stripping onde um intermediário "
        "força o browser a usar HTTP, expondo credenciais e tokens de sessão "
        "em texto claro."
    ),
    condition=(
        "Requer posição de man-in-the-middle na rede do usuário "
        "(ex: rede Wi-Fi pública, ARP spoofing em rede local) e que o "
        "browser não tenha visitado o site via HTTPS anteriormente."
    ),
    validation=(
        "Verificar ausência do header com: "
        "curl -sI https://<alvo> | grep -i strict-transport. "
        "Testar downgrade manual: acessar http://<alvo> e observar se "
        "o browser aceita a conexão sem redirecionamento automático seguro."
    ),
    exploitability="BAIXA em redes confiáveis / ALTA em redes compartilhadas",
    remediation=(
        "Adicionar: Strict-Transport-Security: max-age=31536000; "
        "includeSubDomains; preload. "
        "Submeter o domínio à HSTS Preload List (hstspreload.org) para "
        "proteção desde a primeira visita."
    ),
)

XFRAME_MISSING = Vulnerability(
    title="Missing header: X-Frame-Options",
    severity=Severity.MEDIUM,
    description=(
        "X-Frame-Options está ausente. A página pode ser embarcada em "
        "um <iframe> por sites de terceiros."
    ),
    evidence="",
    impact=(
        "Pode permitir ataques de Clickjacking onde o usuário é induzido "
        "a clicar em elementos invisíveis sobrepostos à página legítima, "
        "resultando em ações não autorizadas (transferências, mudanças de senha)."
    ),
    condition=(
        "Requer que o alvo seja embarcável em iframe (ausência de X-Frame-Options "
        "ou CSP frame-ancestors). O atacante precisa atrair a vítima para uma "
        "página controlada por ele."
    ),
    validation=(
        "Testar com: <iframe src='https://<alvo>'></iframe> em página local. "
        "Se a página carregar no iframe, a aplicação é vulnerável. "
        "Confirmar ausência do header via DevTools > Network > Headers."
    ),
    exploitability="MÉDIA — depende da existência de ações sensíveis com um clique",
    remediation=(
        "Adicionar: X-Frame-Options: DENY (recomendado) ou SAMEORIGIN. "
        "Alternativa moderna via CSP: Content-Security-Policy: frame-ancestors 'none'."
    ),
)

XCTO_MISSING = Vulnerability(
    title="Missing header: X-Content-Type-Options",
    severity=Severity.LOW,
    description=(
        "X-Content-Type-Options: nosniff está ausente. "
        "Browsers legados podem inferir o tipo de conteúdo e executar arquivos inesperadamente."
    ),
    evidence="",
    impact=(
        "Pode permitir que browsers interpretem respostas com Content-Type incorreto "
        "como scripts executáveis, especialmente em uploads de arquivos onde o "
        "tipo MIME não é rigorosamente validado."
    ),
    condition=(
        "Requer que a aplicação sirva conteúdo com Content-Type ambíguo ou incorreto "
        "e que o browser utilize MIME-sniffing (comportamento comum em IE/Edge legado)."
    ),
    validation=(
        "Confirmar ausência com: curl -sI <url> | grep -i x-content-type. "
        "Verificar se a aplicação aceita upload de arquivos com extensão .txt "
        "contendo conteúdo HTML/JS e se o browser os executa."
    ),
    exploitability="BAIXA — impacto limitado em browsers modernos",
    remediation="Adicionar: X-Content-Type-Options: nosniff em todas as respostas.",
)

XXSS_MISSING = Vulnerability(
    title="Missing header: X-XSS-Protection",
    severity=Severity.LOW,
    description=(
        "X-XSS-Protection está ausente. "
        "Browsers mais antigos ficam sem o filtro XSS embutido."
    ),
    evidence="",
    impact=(
        "Pode reduzir a proteção contra XSS refletido em browsers legados "
        "(IE, Edge antigo) que dependem deste filtro como camada adicional de defesa."
    ),
    condition=(
        "Afeta principalmente usuários de Internet Explorer e versões antigas do Edge. "
        "Browsers modernos (Chrome, Firefox) ignoram este header em favor do CSP."
    ),
    validation=(
        "Confirmar ausência: curl -sI <url> | grep -i x-xss-protection. "
        "O impacto real deve ser avaliado considerando o perfil de browsers "
        "dos usuários da aplicação."
    ),
    exploitability="BAIXA — obsoleto em browsers modernos, relevante apenas em ambientes legados",
    remediation=(
        "Adicionar: X-XSS-Protection: 1; mode=block. "
        "Priorizar a implementação de CSP como proteção primária contra XSS."
    ),
)

REFERRER_MISSING = Vulnerability(
    title="Missing header: Referrer-Policy",
    severity=Severity.LOW,
    description=(
        "Referrer-Policy não está definida. O browser pode enviar a URL completa "
        "como Referer para origens externas."
    ),
    evidence="",
    impact=(
        "Pode expor URLs internas contendo tokens, IDs de sessão ou parâmetros "
        "sensíveis em query strings para domínios terceiros via header Referer."
    ),
    condition=(
        "Requer que a aplicação inclua dados sensíveis em URLs (query strings) "
        "e que a página contenha recursos ou links para domínios externos "
        "que possam observar o header Referer."
    ),
    validation=(
        "Navegar de uma página com parâmetros sensíveis na URL para um recurso "
        "externo. Monitorar com DevTools > Network o header 'Referer' enviado "
        "nas requisições subsequentes."
    ),
    exploitability="BAIXA — depende da presença de dados sensíveis em URLs",
    remediation=(
        "Adicionar: Referrer-Policy: no-referrer-when-downgrade (padrão seguro) "
        "ou Referrer-Policy: strict-origin (mais restritivo)."
    ),
)

PERMISSIONS_MISSING = Vulnerability(
    title="Missing header: Permissions-Policy",
    severity=Severity.LOW,
    description=(
        "Permissions-Policy está ausente. Scripts de terceiros podem solicitar "
        "acesso a APIs sensíveis do browser sem restrição."
    ),
    evidence="",
    impact=(
        "Pode permitir que scripts de terceiros incorporados (ads, analytics, widgets) "
        "acessem câmera, microfone, geolocalização ou outros recursos sensíveis "
        "do dispositivo do usuário."
    ),
    condition=(
        "Requer que a página carregue scripts ou iframes de terceiros com código "
        "malicioso ou comprometido que solicite permissões de browser APIs."
    ),
    validation=(
        "Verificar ausência: curl -sI <url> | grep -i permissions-policy. "
        "Auditar scripts de terceiros carregados e as permissões que eles solicitam "
        "via DevTools > Console > Permissões."
    ),
    exploitability="BAIXA isoladamente — risco cresce proporcionalmente ao número de scripts de terceiros",
    remediation=(
        "Adicionar: Permissions-Policy: geolocation=(), microphone=(), camera=(), "
        "payment=(), usb=(). Restringir apenas o necessário para a funcionalidade."
    ),
)


# ---------------------------------------------------------------------------
# COOKIE templates
# ---------------------------------------------------------------------------

COOKIE_SECURE = Vulnerability(
    title="Cookie sem flag Secure",  
    severity=Severity.MEDIUM,
    description="O cookie pode ser transmitido sobre conexões HTTP não criptografadas.",
    evidence="",
    impact=(
        "Pode expor o valor do cookie (incluindo tokens de sessão) a qualquer "
        "observador passivo na rede caso o browser realize uma requisição HTTP, "
        "mesmo que a aplicação seja primariamente HTTPS."
    ),
    condition=(
        "Requer acesso de leitura ao tráfego de rede do usuário "
        "(ex: sniffing em rede local, posição MITM) e que alguma requisição "
        "HTTP seja realizada pelo browser para o domínio alvo."
    ),
    validation=(
        "Inspecionar o header Set-Cookie na resposta e confirmar ausência "
        "da flag 'Secure'. Ferramentas: DevTools > Application > Cookies, "
        "ou curl -sI <url> | grep -i set-cookie."
    ),
    exploitability="BAIXA em HTTPS puro / MÉDIA se houver qualquer endpoint HTTP no domínio",
    remediation="Adicionar a flag Secure: Set-Cookie: <nome>=<valor>; Secure; Path=/; ...",
)

COOKIE_HTTPONLY = Vulnerability(
    title="Cookie sem flag HttpOnly",
    severity=Severity.MEDIUM,
    description="O cookie é acessível via JavaScript através de document.cookie.",
    evidence="",
    impact=(
        "Pode permitir que um atacante leia o valor do cookie via JavaScript "
        "caso exista uma vulnerabilidade XSS na aplicação, possibilitando "
        "sequestro de sessão sem interação do servidor."
    ),
    condition=(
        "Requer a presença de uma vulnerabilidade XSS (refletido ou armazenado) "
        "na aplicação que permita execução de JavaScript arbitrário no contexto "
        "do usuário autenticado."
    ),
    validation=(
        "Confirmar ausência da flag HttpOnly: DevTools > Application > Cookies "
        "ou curl -sI <url> | grep -i set-cookie. "
        "Verificar se document.cookie retorna o cookie em questão no console."
    ),
    exploitability="BAIXA isoladamente / ALTA se combinada com XSS",
    remediation="Adicionar a flag HttpOnly: Set-Cookie: <nome>=<valor>; HttpOnly; Path=/; ...",
)

COOKIE_SAMESITE = Vulnerability(
    title="Cookie sem atributo SameSite",
    severity=Severity.LOW,
    description="O cookie não define comportamento explícito para requisições cross-site.",
    evidence="",
    impact=(
        "Pode facilitar ataques CSRF em browsers que não aplicam o default Lax "
        "automaticamente, permitindo que páginas maliciosas de terceiros disparem "
        "requisições autenticadas em nome do usuário."
    ),
    condition=(
        "Requer que a aplicação execute ações sensíveis via requisições GET ou POST "
        "sem validação de token CSRF adicional, e que o browser alvo não aplique "
        "SameSite=Lax por padrão (browsers legados)."
    ),
    validation=(
        "Inspecionar Set-Cookie e confirmar ausência do atributo SameSite. "
        "Testar com uma página em domínio diferente fazendo requisição POST "
        "para o alvo e verificar se o cookie é enviado."
    ),
    exploitability="BAIXA em browsers modernos (Lax por padrão) / MÉDIA em browsers legados",
    remediation=(
        "Adicionar: SameSite=Strict (sem envio cross-site) ou "
        "SameSite=Lax (permite navegação GET cross-site). "
        "Evitar SameSite=None sem a flag Secure."
    ),
)


# ---------------------------------------------------------------------------
# FORM templates
# ---------------------------------------------------------------------------

FORM_NO_ACTION = Vulnerability(
    title="Formulário sem atributo action",
    severity=Severity.LOW,
    description="O formulário não especifica um endpoint de destino explícito.",
    evidence="",
    impact=(
        "Pode resultar em envio de dados para URLs inesperadas se a página for "
        "acessada via redirecionamento ou cache, dificultando auditoria de segurança "
        "e rastreamento do fluxo de dados."
    ),
    condition=(
        "O comportamento depende do contexto de carregamento da página. "
        "O impacto direto é baixo, mas a ausência de action explícito indica "
        "falta de controle intencional sobre o destino dos dados."
    ),
    validation=(
        "Inspecionar o elemento <form> no código-fonte e confirmar ausência "
        "do atributo action. Verificar para onde os dados são enviados "
        "monitorando requisições no DevTools > Network."
    ),
    exploitability="BAIXA — impacto indireto, principalmente em auditabilidade",
    remediation="Sempre especificar action='https://dominio.com/endpoint' de forma explícita.",
)

FORM_HTTP_POST = Vulnerability(
    title="Formulário POST via HTTP inseguro",
    severity=Severity.HIGH,
    description="Dados do formulário são transmitidos em texto claro sobre HTTP.",
    evidence="",
    impact=(
        "Pode expor credenciais, dados pessoais e outros campos do formulário "
        "a observadores passivos na rede, incluindo senhas e tokens de autenticação "
        "transmitidos em texto claro."
    ),
    condition=(
        "Requer capacidade de observar o tráfego de rede entre o cliente e o servidor "
        "(ex: sniffing em redes compartilhadas, posição MITM via ARP spoofing). "
        "Especialmente crítico em redes Wi-Fi públicas."
    ),
    validation=(
        "Confirmar que o action do formulário usa http:// ou que a página base "
        "é servida via HTTP. Monitorar requisições POST no DevTools > Network "
        "e verificar o protocolo usado."
    ),
    exploitability="ALTA em redes compartilhadas — dados são visíveis em texto claro",
    remediation=(
        "Servir toda a aplicação via HTTPS. Atualizar o action do formulário para "
        "https://. Implementar HSTS para prevenir downgrade. "
        "Redirecionar todo tráfego HTTP para HTTPS via configuração de servidor."
    ),
)

FORM_NO_CSRF = Vulnerability(
    title="Formulário POST sem token CSRF aparente",
    severity=Severity.LOW,
    description="Nenhum campo com nome típico de token CSRF foi identificado no formulário.",
    evidence="",
    impact=(
        "Pode permitir ataques Cross-Site Request Forgery (CSRF) onde um site "
        "malicioso dispara ações autenticadas em nome do usuário sem seu consentimento, "
        "como alteração de dados, senhas ou configurações de conta."
    ),
    condition=(
        "Requer que a aplicação não utilize proteção CSRF via headers "
        "(ex: verificação de Origin/Referer, tokens em cookies duplos) ou "
        "que a proteção de framework não cubra este endpoint específico."
    ),
    validation=(
        "Verificar os campos do formulário via DevTools > Elements. "
        "Confirmar ausência de campo hidden com nome relacionado a CSRF. "
        "NOTA: Esta é uma verificação heurística — frameworks podem proteger "
        "via outros mecanismos não visíveis no HTML."
    ),
    exploitability="BAIXA (heurística) — verificar manualmente antes de confirmar",
    remediation=(
        "Implementar o Synchroniser Token Pattern: gerar token único por sessão, "
        "incluir em campo hidden e validar no servidor. "
        "Alternativa: Double Submit Cookie ou SameSite=Strict nos cookies de sessão."
    ),
)


# ---------------------------------------------------------------------------
# LINK templates
# ---------------------------------------------------------------------------

LINKS_SHORTENER = Vulnerability(
    title="Links encurtados / redirecionadores detectados",
    severity=Severity.MEDIUM,
    description="URLs encurtadas ocultam o destino real, dificultando avaliação de risco.",
    evidence="",
    impact=(
        "Pode ser utilizado para distribuir links para conteúdo malicioso, "
        "phishing ou malware aproveitando a reputação do domínio legítimo. "
        "Também dificulta auditorias de segurança e políticas de CSP."
    ),
    condition=(
        "O risco depende do contexto: links em conteúdo gerado por usuários "
        "são de alto risco; links em templates de e-mail de marketing são "
        "de risco moderado dependendo do serviço de encurtamento utilizado."
    ),
    validation=(
        "Identificar todos os links encurtados na página. "
        "Expandir manualmente usando serviços como checkshorturl.com ou "
        "adicionando '+' ao final de links bit.ly para visualizar destino. "
        "Verificar se os destinos são legítimos e esperados."
    ),
    exploitability="BAIXA para o servidor / MÉDIA para usuários que clicam nos links",
    remediation=(
        "Substituir links encurtados por URLs diretas e verificáveis. "
        "Se encurtadores forem necessários para analytics, usar soluções "
        "self-hosted que possam ser auditadas e revogadas."
    ),
)

LINKS_MIXED_CONTENT = Vulnerability(
    title="Mixed-content: links HTTP em página HTTPS",
    severity=Severity.MEDIUM,
    description="Recursos HTTP são referenciados a partir de uma página HTTPS.",
    evidence="",
    impact=(
        "Pode permitir que um atacante MITM substitua os recursos HTTP por "
        "conteúdo malicioso (scripts, imagens, iframes), comprometendo a "
        "integridade da página HTTPS e potencialmente executando código no contexto seguro."
    ),
    condition=(
        "Requer posição de man-in-the-middle entre o cliente e o servidor "
        "que serve os recursos HTTP. Browsers modernos bloqueiam mixed-content "
        "ativo automaticamente, mas podem carregar mixed-content passivo."
    ),
    validation=(
        "Abrir DevTools > Console e verificar warnings de 'Mixed Content'. "
        "Ou: grep -i 'http://' no código-fonte da página para identificar "
        "todos os recursos não-HTTPS."
    ),
    exploitability="BAIXA para mixed-content passivo (imagens) / ALTA para ativo (scripts, iframes)",
    remediation=(
        "Atualizar todos os recursos para HTTPS. "
        "Adicionar ao CSP: upgrade-insecure-requests para forçar upgrade automático. "
        "Auditar dependências e CDNs para garantir suporte a HTTPS."
    ),
)

LINKS_TABNAPPING = Vulnerability(
    title="Links target=_blank sem rel=noopener noreferrer",
    severity=Severity.LOW,
    description="Links que abrem nova aba sem proteção contra reverse tabnapping.",
    evidence="",
    impact=(
        "Pode permitir que a página aberta em nova aba acesse window.opener "
        "e redirecione a aba original para uma página de phishing enquanto "
        "o usuário está focado na nova aba."
    ),
    condition=(
        "Requer que o link aponte para uma página controlada ou comprometida "
        "pelo atacante que execute window.opener.location = 'url-phishing'. "
        "O usuário precisa ter clicado no link e não fechado a aba original."
    ),
    validation=(
        "Inspecionar links com target='_blank' e verificar ausência de "
        "rel='noopener noreferrer'. Testar: criar página com "
        "window.opener.location='https://example.com' e verificar se "
        "a aba original é redirecionada."
    ),
    exploitability="BAIXA — requer engenharia social e link para página maliciosa",
    remediation=(
        'Adicionar rel="noopener noreferrer" em todos os links com target="_blank". '
        "Browsers modernos aplicam noopener implicitamente em alguns casos, "
        "mas a declaração explícita garante proteção universal."
    ),
)


# ---------------------------------------------------------------------------
# SSL / TLS template
# ---------------------------------------------------------------------------

SSL_INVALID = Vulnerability(
    title="Certificado SSL inválido ou auto-assinado",
    severity=Severity.HIGH,
    description="O certificado TLS não pôde ser verificado pela cadeia de confiança.",
    evidence="",
    impact=(
        "Pode indicar um certificado expirado, auto-assinado ou uma situação "
        "de man-in-the-middle ativo. Browsers exibem avisos que treinam usuários "
        "a ignorar alertas de segurança (normalização de risco)."
    ),
    condition=(
        "O impacto varia: certificado auto-assinado em ambiente de desenvolvimento "
        "é baixo risco; em produção indica falha de processo. "
        "Um certificado MITM indica comprometimento ativo da infraestrutura de rede."
    ),
    validation=(
        "Verificar detalhes do certificado via: openssl s_client -connect <host>:443 "
        "ou inspecionar no browser (cadeado > Certificado). "
        "Confirmar emissor, validade e cadeia de confiança."
    ),
    exploitability="ALTA se MITM ativo / BAIXA se apenas certificado auto-assinado em dev",
    remediation=(
        "Instalar certificado de CA reconhecida (Let's Encrypt para DV gratuito). "
        "Configurar renovação automática via certbot. "
        "Monitorar expiração com alertas antecipados (30+ dias)."
    ),
)