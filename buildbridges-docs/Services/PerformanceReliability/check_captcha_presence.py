from typing import Tuple, List
from bs4 import BeautifulSoup


def check_captcha_presence(
    url: str,
    html: str,
    fetch_meta: dict | None = None,
) -> Tuple[int, List[str], List[str]]:
    """
    CAPTCHA Presence V2
    - Uses Selenium HTML when available
    - Detects Cloudflare challenge pages
    - Detects script-based CAPTCHA
    - Detects HTTP-level bot blocking
    """

    score = 30
    issues: List[str] = []
    recommendations: List[str] = []

    print("Detecting CAPTCHA presence V2 for:", url)

    html_lower = (html or "").lower()
    soup = BeautifulSoup(html or "", "html.parser")

    # -----------------------------------------------------------
    # 1. Hard CAPTCHA UI
    # -----------------------------------------------------------
    hard_captcha_signatures = [
        "g-recaptcha",
        "h-captcha",
        "grecaptcha",
        "data-sitekey",
        "please verify you are a human",
        "are you a robot",
        "captcha",
    ]

    found_hard = any(sig in html_lower for sig in hard_captcha_signatures)

    # -----------------------------------------------------------
    # 2. Script-based CAPTCHA
    # -----------------------------------------------------------
    script_signatures = [
        "recaptcha/api.js",
        "hcaptcha.com/1/api.js",
        "cf-turnstile",
        "turnstile.render",
        "grecaptcha.execute",
        "recaptcha.execute",
    ]

    scripts = soup.find_all("script", src=True)
    script_sources = [s.get("src", "").lower() for s in scripts]
    found_script_captcha = any(
        any(sig in src for sig in script_signatures) for src in script_sources
    )

    # -----------------------------------------------------------
    # 3. Cloudflare challenge pages (YOU WERE MISSING THIS)
    # -----------------------------------------------------------
    cloudflare_challenge_signatures = [
        "challenge-form",
        "/cdn-cgi/challenge-platform/",
        "__cf_chl",
        "cf-challenge",
        "cf-turnstile",
        "cf-ray",
    ]

    found_cloudflare_challenge = any(sig in html_lower for sig in cloudflare_challenge_signatures)

    # -----------------------------------------------------------
    # 4. Honeypot fields
    # -----------------------------------------------------------
    honeypot_indicators = ["honeypot", "bot-field", "robot-check", "trap", "spam-check"]
    inputs = soup.find_all("input")

    found_honeypot = any(
        (
            ("display:none" in (inp.get("style") or "").lower())
            or inp.get("type", "").lower() == "hidden"
            or any(h in (inp.get("name") or "").lower() for h in honeypot_indicators)
        )
        for inp in inputs
    )

    # -----------------------------------------------------------
    # 5. HTTP-level bot blocking (YOU WERE MISSING THIS)
    # -----------------------------------------------------------
    found_http_block = False
    if fetch_meta:
        status = fetch_meta.get("status_code")
        headers = fetch_meta.get("headers", {})
        if status in (403, 429, 503) and any(
            h.lower().startswith("cf-") for h in headers.keys()
        ):
            found_http_block = True

    captcha_detected = any(
        [
            found_hard,
            found_script_captcha,
            found_cloudflare_challenge,
            found_honeypot,
            found_http_block,
        ]
    )

    if captcha_detected:
        score = 0

        if found_hard:
            issues.append("Hard CAPTCHA detected.")
            recommendations.append("Replace CAPTCHA with token-based or API-mode verification.")

        if found_script_captcha:
            issues.append("Script-based CAPTCHA detected.")
            recommendations.append("Provide agent-friendly verification alternatives.")

        if found_cloudflare_challenge:
            issues.append("Cloudflare challenge page detected.")
            recommendations.append("Whitelist known agents or provide bot-friendly access paths.")

        if found_honeypot:
            issues.append("Honeypot bot trap detected.")
            recommendations.append("Avoid blocking non-browser agents with honeypots.")

        if found_http_block:
            issues.append("HTTP-level bot blocking detected.")
            recommendations.append("Expose agent access paths without Cloudflare challenges.")

    else:
        recommendations.append("No CAPTCHA or bot challenges detected — agent-friendly.")

    final_score = round((score / 30) * 100)
    return int(final_score), issues, recommendations
