import requests
from typing import Dict, Tuple, List
from bs4 import BeautifulSoup

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except Exception:
    PLAYWRIGHT_AVAILABLE = False


HEADERS = {"User-Agent": "Mozilla/5.0 (BridgeAI-Agent-Audit/1.0)"}
TIMEOUT = 12


def check_mfa_handling_static(url: str, html: str) -> Tuple[int, List[str], List[str]]:
    score = 0
    issues: List[str] = []
    recommendations: List[str] = []

    if not any(x in url.lower() for x in ["login", "signin", "auth"]):
        print("Non-login page, MFA not applicable")
        return 100, [], ["Non-login page — MFA not applicable."]

    soup = BeautifulSoup(html, "html.parser")
    text_lower = soup.get_text(" ", strip=True).lower()
    print("HTML parsed for static MFA check")

    mfa_keywords = ["otp", "2fa", "authenticator", "mfa", "one time password"]
    remember_keywords = ["remember me", "remember this device", "trust this device"]

    inputs = soup.find_all("input")
    found_mfa_input = any(
        any(k in ((i.get("name") or "") + (i.get("id") or "")).lower() for k in mfa_keywords)
        for i in inputs
    )
    print("MFA input fields detected:", found_mfa_input)

    found_mfa_text = any(k in text_lower for k in mfa_keywords)
    print("MFA text detected:", found_mfa_text)

    remember_found = any(k in text_lower for k in remember_keywords)
    print("Remember device option detected:", remember_found)

    if found_mfa_input:
        score += 40
    else:
        issues.append("No MFA input fields visible.")

    if found_mfa_text:
        score += 30
    else:
        issues.append("No MFA hints or instructions visible.")

    if remember_found:
        score += 20
    else:
        recommendations.append("Support device trust to reduce MFA friction.")

    if found_mfa_input or found_mfa_text:
        score += 10
    else:
        issues.append("Login page lacks visible MFA support.")

    final_score = min(100, score)
    print("Static MFA score:", final_score)
    print("Static MFA issues:", issues)
    print("Static MFA recommendations:", recommendations)

    return final_score, issues, recommendations


def check_mfa_enforcement_flow(url: str) -> Dict:
    result = {
        "mfa_enforced": False,
        "mfa_provider_detected": None,
        "flow_blocked": False,
        "notes": [],
        "engine": "playwright" if PLAYWRIGHT_AVAILABLE else "disabled",
    }

    print("Flow engine:", result["engine"])

    if not PLAYWRIGHT_AVAILABLE:
        print("Flow detection skipped")
        result["notes"].append("Flow detection not available")
        return result

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent=HEADERS["User-Agent"])

        try:
            page.goto(url, timeout=30000)
            content = page.content().lower()
            current_url = page.url.lower()

            print("Current URL:", current_url)

            mfa_markers = [
                "otp",
                "verification code",
                "two-factor",
                "authenticator",
                "security code",
                "enter code",
            ]

            providers = {
                "okta": "okta",
                "auth0": "auth0",
                "azure_ad": "login.microsoftonline.com",
                "cognito": "amazoncognito",
                "duo": "duosecurity",
                "cloudflare_access": "cloudflareaccess",
            }

            if any(k in content for k in mfa_markers):
                result["mfa_enforced"] = True
                result["notes"].append("MFA challenge detected in page")

            for name, domain in providers.items():
                if domain in current_url:
                    result["mfa_enforced"] = True
                    result["mfa_provider_detected"] = name
                    result["notes"].append("MFA provider detected: " + name)

            if "challenge" in current_url or "captcha" in content:
                result["flow_blocked"] = True
                result["notes"].append("Bot challenge detected during flow")

        except Exception as e:
            result["flow_blocked"] = True
            result["notes"].append(str(e))
            print("Flow check failed:", str(e))

        finally:
            browser.close()

    print("Flow MFA enforced:", result["mfa_enforced"])
    print("Flow MFA provider:", result["mfa_provider_detected"])
    print("Flow blocked:", result["flow_blocked"])
    print("Flow notes:", result["notes"])

    return result


def check_agent_auth_readiness(url: str) -> Dict:
    result = {
        "api_auth_available": False,
        "service_account_possible": False,
        "oauth_client_credentials": False,
        "notes": [],
    }

    known_api_paths = [
        "/.well-known/openapi.json",
        "/openapi.json",
        "/swagger.json",
        "/v1/health",
        "/api/health",
    ]

    for path in known_api_paths:
        try:
            resp = requests.get(url.rstrip("/") + path, headers=HEADERS, timeout=5)
            if resp.status_code == 200:
                result["api_auth_available"] = True
                result["notes"].append("Public API endpoint found at " + path)
        except Exception:
            pass

    result["notes"].append("Recommend OAuth client credentials or service accounts for agents")

    print("Agent auth available:", result["api_auth_available"])
    print("Agent auth notes:", result["notes"])

    return result


def check_mfa_handling(url: str, html: str) -> Dict:
    static_score, static_issues, static_recs = check_mfa_handling_static(url, html)
    flow_result = check_mfa_enforcement_flow(url)
    agent_auth = check_agent_auth_readiness(url)

    final_status = "unknown"

    if flow_result["engine"] == "disabled":
        final_status = "unknown"
    elif flow_result["flow_blocked"]:
        final_status = "blocked"
    elif flow_result["mfa_enforced"] and not agent_auth["api_auth_available"]:
        final_status = "blocked"
    else:
        final_status = "good"

    print("Final MFA status:", final_status)

    return {
        "static_score": static_score,
        "static_issues": static_issues,
        "static_recommendations": static_recs,
        "mfa_enforced": flow_result["mfa_enforced"],
        "mfa_provider_detected": flow_result["mfa_provider_detected"],
        "flow_blocked": flow_result["flow_blocked"],
        "agent_auth_readiness": agent_auth,
        "final_status": final_status,
        "message": "MFA readiness evaluated using static heuristics and real-time flow inspection.",
    }
