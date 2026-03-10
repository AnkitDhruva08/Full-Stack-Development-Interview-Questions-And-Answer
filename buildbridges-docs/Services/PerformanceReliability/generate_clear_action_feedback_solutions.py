import requests
from typing import Dict, List
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (Accessibility-Audit-Bot)"}
TIMEOUT = 15


def fetch_html(url: str) -> BeautifulSoup:
    resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def generate_clear_action_feedback_solutions(url: str) -> Dict:
    """
    Solution engine synced with check_clear_action_feedback_v2().
    Applying these fixes deterministically improves V2 score to 100.
    """

    soup = fetch_html(url)

    issues_detected: List[str] = []
    fixes: List[Dict] = []

    def add_fix(issue_key: str, fix_obj: Dict, failed: bool):
        fixes.append(
            {
                "issue_key": issue_key,
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

    # Re-run V2 detection logic (mirrored)
    html = str(soup).lower()

    feedback_nodes = soup.select(
        ".alert, .error, .success, .message, .notice, [role='alert'], [aria-live]"
    )
    visible_feedback = [
        n
        for n in feedback_nodes
        if not (
            n.has_attr("hidden")
            or "display:none" in n.get("style", "").replace(" ", "").lower()
        )
    ]
    text_feedback = [n for n in visible_feedback if n.get_text(strip=True)]
    actions = soup.find_all(["button", "form"])
    contextual_feedback = [
        f
        for f in text_feedback
        if f.find_parent("form")
        or any(f.parent == a.parent for a in actions)
    ]

    has_success = any(
        ("success" in (f.get("class") or [])) or ("success" in f.get_text().lower())
        for f in contextual_feedback
    )
    has_error = any(
        ("error" in (f.get("class") or [])) or ("error" in f.get_text().lower())
        for f in contextual_feedback
    )

    inputs = soup.find_all(["input", "select", "textarea"])
    validation_phrases = [
        "this field is required",
        "please enter",
        "cannot be empty",
        "must be",
        "invalid",
        "incorrect",
    ]
    validation_near_inputs = False
    for inp in inputs:
        parent_text = inp.parent.get_text(" ", strip=True).lower() if inp.parent else ""
        if any(p in parent_text for p in validation_phrases):
            validation_near_inputs = True
            break

    aria_nodes = soup.find_all(attrs={"role": "alert"}) + soup.find_all(
        attrs={"aria-live": True}
    )
    aria_with_text = [n for n in aria_nodes if n.get_text(strip=True)]

    # -------------------------------------------------
    add_fix(
        "no_contextual_feedback_near_actions",
        {
            "title": "Place feedback near actions",
            "location": "Forms and action buttons",
            "why": "Feedback must be contextual to the action that triggered it.",
            "steps": [
                "Place success/error messages inside the same <form> as the submit button.",
                "Or place feedback containers as siblings of action buttons.",
            ],
            "example": """<form>
  <input />
  <span class="error" role="alert">Invalid input</span>
  <span class="success" aria-live="polite">Saved successfully</span>
  <button>Submit</button>
</form>""",
            "verify": "Inspect DOM and confirm feedback elements are near buttons/forms.",
        },
        failed=not bool(contextual_feedback),
    )

    add_fix(
        "missing_success_or_error_feedback",
        {
            "title": "Provide both success and error feedback",
            "location": "Feedback containers near actions",
            "why": "Agents and users need clear outcomes for both success and failure.",
            "steps": [
                "Add a success message container.",
                "Add an error message container.",
            ],
            "example": """<span class="success">Saved successfully</span>
<span class="error">Something went wrong</span>""",
            "verify": "Confirm both success and error feedback exist near actions.",
        },
        failed=not (has_success and has_error),
    )

    add_fix(
        "no_validation_feedback_near_inputs",
        {
            "title": "Add inline validation messages near inputs",
            "location": "Form fields",
            "why": "Validation feedback must be close to the input it refers to.",
            "steps": [
                "Place validation text next to inputs.",
                "Use clear phrases like 'This field is required'.",
            ],
            "example": """<label>Email</label>
<input />
<span class="error">This field is required</span>""",
            "verify": "Inspect DOM and confirm validation messages appear near inputs.",
        },
        failed=not validation_near_inputs and bool(inputs),
    )

    add_fix(
        "aria_regions_empty",
        {
            "title": "Ensure ARIA feedback regions contain text",
            "location": "ARIA feedback containers",
            "why": "Empty ARIA regions provide no usable feedback to agents or assistive tech.",
            "steps": [
                "Add descriptive text inside role='alert' containers.",
                "Add meaningful text inside aria-live regions.",
            ],
            "example": """<div role="alert">Invalid password</div>""",
            "verify": "Inspect DOM and confirm ARIA regions are not empty.",
        },
        failed=bool(aria_nodes) and not bool(aria_with_text),
    )

    return {
        "status": "fail" if issues_detected else "pass",
        "issues_detected": issues_detected,
        "fixes": fixes,
        "message": (
            "Clear action feedback V2 needs improvements."
            if issues_detected
            else "Clear action feedback is contextually and semantically correct. ✅"
        ),
    }
