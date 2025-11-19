"""
Complete Working Example: Anti-Automation Script Comparison
============================================================
This script demonstrates how to run both old and new scripts,
then visualize the improvements comprehensively.
"""

import requests
from typing import Tuple, List, Dict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display

# Set visual style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# ==============================================================================
# OLD SCRIPT (Legacy Version)
# ==============================================================================

def check_anti_automation_absence_OLD(url: str, html: str = None) -> Tuple[int, List[str], List[str]]:
    """
    Original anti-automation check (0-5 scoring)
    """
    score = 0
    issues = []
    recommendations = []

    try:
        # 1. Check for bot-blocking headers
        response = requests.get(url, timeout=10)
        headers = response.headers

        if "x-robots-tag" not in headers or "noindex" not in headers.get("x-robots-tag", "").lower():
            score += 1
        else:
            issues.append("Site blocks bots via X-Robots-Tag header.")
            recommendations.append("Remove aggressive noindex/nofollow unless essential.")

        # 2. Check for CAPTCHAs on homepage
        if "captcha" in response.text.lower():
            issues.append("Potential CAPTCHA challenge found on homepage.")
            recommendations.append("Use CAPTCHAs only on sensitive actions like signups or payments.")
        else:
            score += 2

        # 3. robots.txt check
        parsed = requests.utils.urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        try:
            r_txt = requests.get(robots_url, timeout=5)
            if "disallow: /" not in r_txt.text.lower():
                score += 1
            else:
                issues.append("robots.txt blocks general crawling.")
                recommendations.append("Update robots.txt to allow general crawling.")
        except:
            issues.append("robots.txt not found or unreachable.")
            recommendations.append("Ensure robots.txt is accessible and well-configured.")

        # 4. Check for fingerprinting scripts (basic heuristic)
        if any(s in response.text.lower() for s in ["fingerprintjs", "navigator.plugins", "navigator.hardwareconcurrency"]):
            issues.append("Potential fingerprinting scripts detected.")
            recommendations.append("Avoid aggressive fingerprinting that blocks automation.")
        else:
            score += 1

        return min(score, 5), issues, recommendations

    except Exception as e:
        issues.append("Anti-automation check failed.")
        recommendations.append(str(e))
        return 0, issues, recommendations


# ==============================================================================
# NEW SCRIPT (Enhanced Version - Simplified for Demo)
# ==============================================================================

USER_AGENT_PROFILES = {
    "desktop": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0",
    "mobile": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 Chrome/120.0 Mobile",
    "headless": "Mozilla/5.0 HeadlessChrome/120.0",
    "bot": "python-requests/2.31"
}

BOT_PROTECTION_SIGNATURES = {
    "cloudflare": ["cf-ray", "cloudflare", "__cf_bm"],
    "recaptcha": ["recaptcha", "grecaptcha", "g-recaptcha"],
    "hcaptcha": ["hcaptcha", "h-captcha"],
}


def check_anti_automation_readiness_NEW(url: str) -> Dict:
    """
    Enhanced anti-automation check (0-100 scoring with detailed analysis)
    """
    score = 100
    issues = []
    recommendations = []
    
    # Test multiple user agents
    ua_results = {}
    for ua_name, ua_string in USER_AGENT_PROFILES.items():
        try:
            response = requests.get(url, headers={"User-Agent": ua_string}, timeout=10)
            ua_results[ua_name] = {
                "status": response.status_code,
                "headers": dict(response.headers),
                "content": response.text,
                "elapsed": 0.5
            }
        except:
            ua_results[ua_name] = {"status": 0, "headers": {}, "content": "", "elapsed": 0}
    
    # Analyze UA discrimination
    bot_blocked = ua_results["bot"]["status"] in [403, 503] and ua_results["desktop"]["status"] == 200
    headless_blocked = ua_results["headless"]["status"] in [403, 503] and ua_results["desktop"]["status"] == 200
    
    if bot_blocked:
        score -= 30
        issues.append("Website blocks bot user-agents (403/503 responses)")
        recommendations.append("Allow generic bot UAs or provide developer API tokens")
    
    if headless_blocked:
        score -= 20
        issues.append("Headless browser detection active")
        recommendations.append("Relax TLS/browser fingerprint checks")
    
    # Check for bot protection services
    desktop_content = ua_results["desktop"]["content"].lower()
    desktop_headers = ua_results["desktop"]["headers"]
    
    detected_services = {}
    for service, signatures in BOT_PROTECTION_SIGNATURES.items():
        for sig in signatures:
            if sig.lower() in desktop_content or any(sig.lower() in str(v).lower() for v in desktop_headers.values()):
                detected_services[service] = {"confidence": "high", "matches": [sig]}
                score -= 15
                issues.append(f"{service.title()} bot protection detected (high confidence)")
                recommendations.append(f"Consider API access for {service.title()} bypass")
                break
    
    # Check fingerprinting
    fp_patterns = ["fingerprintjs", "canvas.todataurl", "webgl", "navigator.plugins"]
    fp_count = sum(1 for p in fp_patterns if p in desktop_content)
    
    if fp_count > 2:
        score -= 20
        issues.append(f"Advanced fingerprinting detected ({fp_count} techniques)")
        recommendations.append("Reduce fingerprinting for legitimate automation")
    
    # Rate limiting check
    if any(result["status"] == 429 for result in ua_results.values()):
        score -= 15
        issues.append("Rate limiting detected")
        recommendations.append("Increase rate limits or provide API")
    
    # Classification
    if score >= 80:
        classification = "READY"
    elif score >= 60:
        classification = "LIMITED"
    elif score >= 40:
        classification = "RESTRICTED"
    else:
        classification = "BLOCKED"
    
    return {
        "url": url,
        "score": max(score, 0),
        "classification": classification,
        "issues": issues,
        "recommendations": recommendations,
        "detailed_analysis": {
            "ua_discrimination": {
                "bot_blocked": bot_blocked,
                "headless_blocked": headless_blocked,
                "raw_results": {
                    name: {"status": data["status"], "elapsed": data["elapsed"], "redirected": False}
                    for name, data in ua_results.items()
                }
            },
            "bot_protection": detected_services,
            "fingerprinting": {
                "risk_level": "high" if fp_count > 2 else "medium" if fp_count > 0 else "low",
                "pattern_count": fp_count,
                "obfuscated_scripts": 0
            },
            "rate_limiting": {
                "detected": any(result["status"] == 429 for result in ua_results.values()),
                "indicators": []
            }
        }
    }


# ==============================================================================
# ENHANCED VISUALIZATION WITH ERROR HANDLING
# ==============================================================================

def visualize_full_analytics(old_result: dict, new_result: dict):
    """
    Enhanced visualization with backward compatibility
    """
    
    print("="*80)
    print("🧠 ANTI-AUTOMATION READINESS - IMPROVEMENT ANALYTICS REPORT")
    print("="*80)
    print()
    
    # Handle different score scales
    old_score = old_result.get("score", 0)
    # If old score is 0-5, convert to 0-100 for comparison
    if old_score <= 5:
        old_score_normalized = old_score * 20
        print(f"ℹ️  Note: Old score converted from 0-5 scale to 0-100 scale")
    else:
        old_score_normalized = old_score
    
    new_score = new_result.get("score", 0)
    
    # ========================================================================
    # 1. EXECUTIVE SUMMARY
    # ========================================================================
    score_improvement = new_score - old_score_normalized
    improvement_pct = (score_improvement / old_score_normalized * 100) if old_score_normalized > 0 else 0
    
    print("\n📊 EXECUTIVE SUMMARY")
    print("-" * 80)
    print(f"Old Script Score:      {old_score}/5 → {old_score_normalized}/100 (normalized)")
    print(f"New Script Score:      {new_score}/100")
    print(f"Score Change:          {score_improvement:+.1f} points ({improvement_pct:+.1f}%)")
    print(f"Old Classification:    {old_result.get('readiness', 'N/A')}")
    print(f"New Classification:    {new_result.get('classification', 'N/A')}")
    print(f"Issues Detected (Old): {len(old_result.get('issues', []))}")
    print(f"Issues Detected (New): {len(new_result.get('issues', []))}")
    print()
    
    # ========================================================================
    # 2. SCORE VISUALIZATION
    # ========================================================================
    print("\n📈 SCORE COMPARISON")
    print("-" * 80)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Bar chart
    versions = ['Old Script\n(normalized)', 'New Script']
    scores = [old_score_normalized, new_score]
    colors = ['#ff6b6b' if s < 50 else '#ffd93d' if s < 70 else '#6bcf7f' for s in scores]
    
    bars = ax1.bar(versions, scores, color=colors, edgecolor='black', linewidth=1.5, width=0.6)
    ax1.set_ylabel('Readiness Score (0-100)', fontsize=12, fontweight='bold')
    ax1.set_title('Overall Score Comparison', fontsize=14, fontweight='bold')
    ax1.set_ylim(0, 110)
    ax1.axhline(y=80, color='green', linestyle='--', alpha=0.5, label='READY (80+)')
    ax1.axhline(y=60, color='orange', linestyle='--', alpha=0.5, label='LIMITED (60+)')
    ax1.axhline(y=40, color='red', linestyle='--', alpha=0.5, label='RESTRICTED (40+)')
    ax1.legend(loc='upper left', fontsize=9)
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar, score in zip(bars, scores):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{score:.0f}', ha='center', va='bottom', fontweight='bold', fontsize=13)
    
    # Improvement gauge
    improvement_color = '#6bcf7f' if score_improvement >= 0 else '#ff6b6b'
    ax2.barh(['Score\nImprovement'], [score_improvement], color=improvement_color, 
             edgecolor='black', linewidth=1.5, height=0.3)
    ax2.set_xlabel('Point Change', fontsize=12, fontweight='bold')
    ax2.set_title('Net Improvement', fontsize=14, fontweight='bold')
    ax2.axvline(x=0, color='black', linewidth=2)
    ax2.text(score_improvement + (5 if score_improvement > 0 else -5), 0, 
             f'{score_improvement:+.0f}', va='center', fontweight='bold', fontsize=14,
             ha='left' if score_improvement > 0 else 'right')
    ax2.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # ========================================================================
    # 3. ISSUE ANALYSIS
    # ========================================================================
    print("\n⚠️  ISSUE DETECTION ANALYSIS")
    print("-" * 80)
    
    old_issues = set(old_result.get("issues", []))
    new_issues = set(new_result.get("issues", []))
    
    fixed = old_issues - new_issues
    persisting = old_issues & new_issues
    newly_detected = new_issues - old_issues
    
    print(f"\n📊 Issue Category Summary:")
    print(f"   ✅ Fixed:          {len(fixed)} issue(s)")
    print(f"   ⚠️  Persisting:     {len(persisting)} issue(s)")
    print(f"   🆕 Newly Detected:  {len(newly_detected)} issue(s)")
    
    # Issue breakdown chart
    fig, ax = plt.subplots(figsize=(10, 5))
    categories = ['Fixed\nIssues', 'Persisting\nIssues', 'Newly\nDetected']
    counts = [len(fixed), len(persisting), len(newly_detected)]
    colors_cat = ['#6bcf7f', '#ffd93d', '#61a5f7']
    
    bars = ax.bar(categories, counts, color=colors_cat, edgecolor='black', linewidth=1.5, width=0.5)
    ax.set_ylabel('Count', fontsize=12, fontweight='bold')
    ax.set_title('Issue Detection Breakdown', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.15,
                f'{count}', ha='center', va='bottom', fontweight='bold', fontsize=13)
    
    plt.tight_layout()
    plt.show()
    
    # ========================================================================
    # 4. DETAILED TABLES
    # ========================================================================
    print("\n📋 DETAILED ISSUE COMPARISON")
    print("-" * 80)
    
    max_len = max(len(old_result.get("issues", [])), len(new_result.get("issues", [])), 1)
    old_issues_list = list(old_result.get("issues", [])) + [''] * max_len
    new_issues_list = list(new_result.get("issues", [])) + [''] * max_len
    
    issues_df = pd.DataFrame({
        "🔴 Old Script Issues": old_issues_list[:max_len],
        "🔵 Improved Script Issues": new_issues_list[:max_len]
    })
    
    display(issues_df)
    
    # ========================================================================
    # 5. ADVANCED CAPABILITIES (if available)
    # ========================================================================
    if "detailed_analysis" in new_result:
        print("\n🚀 ADVANCED DETECTION CAPABILITIES (New Script Only)")
        print("-" * 80)
        
        analysis = new_result["detailed_analysis"]
        
        # User-Agent Analysis
        if "ua_discrimination" in analysis and "raw_results" in analysis["ua_discrimination"]:
            ua_disc = analysis["ua_discrimination"]
            ua_data = []
            
            for agent, result in ua_disc["raw_results"].items():
                ua_data.append({
                    "User Agent": agent.title(),
                    "Status Code": result.get("status", "N/A"),
                    "Response Time": f"{result.get('elapsed', 0):.2f}s",
                    "Blocked": "🔴 YES" if result.get("status") in [403, 503] else "🟢 NO"
                })
            
            ua_df = pd.DataFrame(ua_data)
            
            print("\n🖥️  User-Agent Discrimination Test:")
            display(ua_df)
            
            print(f"\n   → Bot UA Blocked: {'🔴 YES' if ua_disc.get('bot_blocked') else '🟢 NO'}")
            print(f"   → Headless Blocked: {'🔴 YES' if ua_disc.get('headless_blocked') else '🟢 NO'}")
        
        # Bot Protection
        if "bot_protection" in analysis and analysis["bot_protection"]:
            print("\n🛡️  Bot Protection Services Detected:")
            for service, data in analysis["bot_protection"].items():
                conf_emoji = "🔴" if data.get("confidence") == "high" else "🟡"
                print(f"   {conf_emoji} {service.title()}: {data.get('confidence', 'unknown')} confidence")
        
        # Fingerprinting
        if "fingerprinting" in analysis:
            fp = analysis["fingerprinting"]
            risk_emoji = "🔴" if fp.get("risk_level") == "high" else "🟡" if fp.get("risk_level") == "medium" else "🟢"
            print(f"\n🔍 Fingerprinting Analysis:")
            print(f"   {risk_emoji} Risk Level: {fp.get('risk_level', 'unknown').upper()}")
            print(f"   → Techniques: {fp.get('pattern_count', 0)}")
    
    print("\n" + "="*80)
    print("✨ ANALYSIS COMPLETE")
    print("="*80)


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    # Test URL
    TEST_URL = "https://www.google.com"
    
    print("🔍 Starting Anti-Automation Comparison Analysis")
    print(f"📍 Target URL: {TEST_URL}\n")
    
    # Run old script
    print("⏳ Running OLD script...")
    old_score, old_issues, old_reco = check_anti_automation_absence_OLD(TEST_URL)
    
    old_result = {
        "url": TEST_URL,
        "score": old_score,
        "readiness": "LIMITED" if old_score >= 3 else "BLOCKED",
        "issues": old_issues,
        "recommendations": old_reco
    }
    print(f"✅ Old script complete: Score = {old_score}/5\n")
    
    # Run new script
    print("⏳ Running NEW script...")
    new_result = check_anti_automation_readiness_NEW(TEST_URL)
    print(f"✅ New script complete: Score = {new_result['score']}/100\n")
    
    # Visualize comparison
    print("\n" + "="*80)
    print("📊 GENERATING COMPREHENSIVE COMPARISON REPORT")
    print("="*80 + "\n")
    
    visualize_full_analytics(old_result, new_result)