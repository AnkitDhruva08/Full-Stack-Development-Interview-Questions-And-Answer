import requests
from typing import Dict, List, Optional, Tuple
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (BridgeAI-Audit-Bot/1.0)",
    "Accept": "text/html",
    "Accept-Language": "en-US,en;q=0.9",
}
TIMEOUT = 15


# -----------------------------------
# CAPTCHA-aware fetcher (sync with audit)
# -----------------------------------
def fetch_html_for_captcha(url: str) -> Tuple[Optional[BeautifulSoup], Dict]:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        html = resp.text or ""
        soup = BeautifulSoup(html, "html.parser")

        meta = {
            "status_code": resp.status_code,
            "headers": dict(resp.headers),
            "html_lower": html.lower(),
        }
        return soup, meta

    except requests.exceptions.RequestException as e:
        return None, {"error": str(e)}


def _is_trusted_info_domain(url: str) -> bool:
    return any(d in url for d in ["gov.uk", "wikipedia.org"])


# -----------------------------------
# Solution Generator (Synced with CAPTCHA audit V2)
# -----------------------------------
def generate_captcha_presence_solutions(url: str) -> Dict:
    """
    Deterministic solution engine for Captcha Presence.
    Synced 1:1 with updated check_captcha_presence_v2() heuristics.
    Input: url only
    """

    if _is_trusted_info_domain(url):
        return {
            "status": "pass",
            "issues_detected": [],
            "fixes": [],
            "message": "Trusted informational domain detected. CAPTCHA checks skipped.",
        }

    soup, meta = fetch_html_for_captcha(url)

    issues_detected: List[str] = []
    fixes: List[Dict] = []

    def add_fix(issue_key: str, fix_obj: Dict, failed: bool):
        fixes.append(
            {
                "title": fix_obj["title"],
                "location": fix_obj["location"],
                "why": fix_obj["why"],
                "steps": fix_obj["steps"],
                "example": fix_obj["example"],
                "verify": fix_obj["verify"],
                "status": "fail" if failed else "pass",
            }
        )
        if failed:
            issues_detected.append(issue_key)

    # ---------------------------
    # Site blocked / bot firewall
    # ---------------------------
    http_blocked = False
    if meta.get("status_code") in (403, 429, 503) and any(
        k.lower().startswith("cf-") for k in meta.get("headers", {}).keys()
    ):
        http_blocked = True

    add_fix(
        "http_bot_blocking_detected",
        {
            "title": "Relax bot firewall / Cloudflare challenge for agents",
            "location": "Edge protection / WAF (Cloudflare, Akamai, etc.)",
            "why": "HTTP-level bot blocking prevents agents and audits from accessing the site.",
            "steps": [
                "Allowlist BridgeAI-Audit-Bot user agent.",
                "Disable Cloudflare challenge for read-only endpoints.",
                "Provide agent-safe access path (e.g., /agent).",
            ],
            "example": "Allow User-Agent: BridgeAI-Audit-Bot/1.0 in WAF rules.",
            "verify": "Re-run audit and confirm site is reachable without challenge.",
        },
        failed=http_blocked,
    )

    html_lower = meta.get("html_lower", "")
    soup = soup or BeautifulSoup("", "html.parser")

    # ---------------------------
    # Cloudflare challenge pages
    # ---------------------------
    cloudflare_signatures = [
        "challenge-form",
        "/cdn-cgi/challenge-platform/",
        "__cf_chl",
        "cf-turnstile",
        "cf-ray",
    ]
    found_cloudflare_challenge = any(sig in html_lower for sig in cloudflare_signatures)

    add_fix(
        "cloudflare_challenge_detected",
        {
            "title": "Remove Cloudflare challenge pages for agents",
            "location": "Cloudflare Bot Fight Mode / Turnstile",
            "why": "Cloudflare challenges block non-browser agents and automation.",
            "steps": [
                "Disable Bot Fight Mode for read-only endpoints.",
                "Whitelist agent IP ranges or user agents.",
                "Expose an agent-safe route without Turnstile.",
            ],
            "example": "Cloudflare → Security → Bots → Allow verified bots.",
            "verify": "Load page as agent and confirm no challenge-form appears.",
        },
        failed=found_cloudflare_challenge,
    )

    # ---------------------------
    # CAPTCHA scripts
    # ---------------------------
    found_script_captcha = bool(
        soup.select(
            "script[src*='recaptcha'], script[src*='hcaptcha'], script[src*='turnstile'], script[src*='challenges.cloudflare.com']"
        )
    )

    add_fix(
        "captcha_scripts_detected",
        {
            "title": "Remove CAPTCHA scripts",
            "location": "Frontend scripts",
            "why": "CAPTCHA scripts block autonomous agents.",
            "steps": [
                "Remove reCAPTCHA / hCaptcha / Turnstile scripts.",
                "Replace CAPTCHA with server-side rate limiting.",
            ],
            "example": "<!-- Remove --> <script src='https://challenges.cloudflare.com/turnstile/v0/api.js'></script>",
            "verify": "View source and confirm no CAPTCHA scripts remain.",
        },
        failed=found_script_captcha,
    )

    # ---------------------------
    # CAPTCHA UI text
    # ---------------------------
    CAPTCHA_KEYWORDS = [
        "captcha",
        "recaptcha",
        "hcaptcha",
        "turnstile",
        "are you a robot",
        "verify you are human",
    ]
    found_ui_captcha = any(k in html_lower for k in CAPTCHA_KEYWORDS)

    add_fix(
        "captcha_ui_detected",
        {
            "title": "Remove CAPTCHA UI text",
            "location": "Auth flows and forms",
            "why": "CAPTCHA UI blocks agents from completing tasks.",
            "steps": [
                "Remove challenge text from forms.",
                "Avoid presenting CAPTCHA UI to non-browser clients.",
            ],
            "example": "<!-- Remove CAPTCHA UI --> Are you a robot?",
            "verify": "Inspect HTML and confirm no CAPTCHA text exists.",
        },
        failed=found_ui_captcha,
    )

    # ---------------------------
    # Honeypot fields
    # ---------------------------
    honeypots = soup.select(
        "input[type='text'][style*='display:none'], input[type='text'][style*='visibility:hidden'], input[type='hidden']"
    )
    named_traps = soup.select(
        "input[name*='bot'], input[name*='honeypot'], input[name*='spam'], input[name*='robot']"
    )
    has_traps = bool(honeypots or named_traps)

    add_fix(
        "honeypot_traps_detected",
        {
            "title": "Remove honeypot bot traps",
            "location": "Form inputs",
            "why": "Hidden traps cause false negatives for agents.",
            "steps": [
                "Remove hidden inputs used for bot detection.",
                "Avoid bot trap field names.",
            ],
            "example": "<input name='honeypot' style='display:none' />",
            "verify": "Inspect DOM and confirm no hidden trap inputs exist.",
        },
        failed=has_traps,
    )

    # ---------------------------
    # Server-side alternatives (always recommended)
    # ---------------------------
    add_fix(
        "replace_captcha_with_server_side_protection",
        {
            "title": "Replace CAPTCHA with server-side protection",
            "location": "Backend (API / middleware)",
            "why": "Server-side protections secure endpoints without blocking agents.",
            "steps": [
                "Add IP/session rate limiting.",
                "Use behavior scoring on server-side.",
                "Issue short-lived access tokens for agents.",
            ],
            "example": """# FastAPI example
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/submit")
@limiter.limit("10/minute")
async def submit():
    return {"status": "ok"}""",
            "verify": "Confirm abuse is blocked server-side without UI challenges.",
        },
        failed=bool(
            http_blocked
            or found_cloudflare_challenge
            or found_script_captcha
            or found_ui_captcha
            or has_traps
        ),
    )

    return {
        "status": "fail" if issues_detected else "pass",
        "issues_detected": issues_detected,
        "fixes": fixes,
        "message": (
            "CAPTCHA or bot challenges detected. Apply fixes to allow agent access."
            if issues_detected
            else "No CAPTCHA or bot challenges detected. Agent flow is uninterrupted."
        ),
    }
