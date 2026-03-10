from typing import Tuple, List
from bs4 import BeautifulSoup


def check_clear_action_feedback(
    url: str, html: str
) -> Tuple[int, List[str], List[str]]:
    """
    Clear Action Feedback V2 (Deterministic, Static DOM)
    - Requires feedback near actions
    - Requires visible feedback
    - Requires ARIA regions with text
    - Requires both success + error coverage
    """

    _ = url
    issues: List[str] = []
    recs: List[str] = []
    score = 100

    soup = BeautifulSoup(html, "html.parser")

    # Find feedback containers
    feedback_nodes = soup.select(
        ".alert, .error, .success, .message, .notice, [role='alert'], [aria-live]"
    )

    # Rule B: visible only
    visible_feedback = [
        n
        for n in feedback_nodes
        if not (
            n.has_attr("hidden")
            or "display:none" in n.get("style", "").replace(" ", "").lower()
        )
    ]

    # Rule C: ARIA must contain text
    text_feedback = [n for n in visible_feedback if n.get_text(strip=True)]

    # Find actions
    actions = soup.find_all(["button", "form"])

    # Rule A: feedback near actions (same parent or inside form)
    contextual_feedback = [
        f
        for f in text_feedback
        if f.find_parent("form")
        or any(f.parent == a.parent for a in actions)
    ]

    if not contextual_feedback:
        score -= 30
        issues.append("no_contextual_feedback_near_actions")
        recs.append("Place feedback containers near buttons or inside forms.")

    # Rule D: success + error coverage
    has_success = any(
        ("success" in (f.get("class") or [])) or ("success" in f.get_text().lower())
        for f in contextual_feedback
    )
    has_error = any(
        ("error" in (f.get("class") or [])) or ("error" in f.get_text().lower())
        for f in contextual_feedback
    )

    if not (has_success and has_error):
        score -= 20
        issues.append("missing_success_or_error_feedback")
        recs.append("Provide both success and error feedback states near actions.")

    # Rule E: validation near inputs
    validation_phrases = [
        "this field is required",
        "please enter",
        "cannot be empty",
        "must be",
        "invalid",
        "incorrect",
    ]

    inputs = soup.find_all(["input", "select", "textarea"])
    validation_near_inputs = False

    for inp in inputs:
        parent_text = inp.parent.get_text(" ", strip=True).lower() if inp.parent else ""
        if any(p in parent_text for p in validation_phrases):
            validation_near_inputs = True
            break

    if not validation_near_inputs and inputs:
        score -= 20
        issues.append("no_validation_feedback_near_inputs")
        recs.append("Add inline validation messages next to inputs.")

    # Rule C (explicit): ARIA regions must have text
    aria_nodes = soup.find_all(attrs={"role": "alert"}) + soup.find_all(
        attrs={"aria-live": True}
    )
    aria_with_text = [n for n in aria_nodes if n.get_text(strip=True)]

    if aria_nodes and not aria_with_text:
        score -= 10
        issues.append("aria_regions_empty")
        recs.append("Ensure ARIA feedback regions contain descriptive text.")

    score = max(0, min(score, 100))
    return score, issues, recs
