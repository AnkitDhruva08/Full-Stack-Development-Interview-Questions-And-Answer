import asyncio
from datetime import datetime
import json
import re
from typing import Dict, Any
from celery_app import celery_app
from services.axo.axo_auditor import AxoAuditor
from services.automation.automation_auditor import AutomationAuditor
from services.geo_readiness.geo_auditor import GeoReadinessAnalyzer
from services.modularity_api.modularity_auditor import ModularityApiAnalyzer
from services.semantic.semantic_auditor import SemanticAuditor
from services.category_classfier import classify_website, get_category_weights
from core.scan_service import scan_service
import google.generativeai as genai
import time
from celery.result import AsyncResult
import traceback

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def run_single_pillar(self, pillar_name: str, url: str, api_key: str, scan_id: str) -> Dict[str, Any]:
    """
    Run a single pillar audit as an independent celery task.
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash-lite')

        print(f"Running {pillar_name} audit for {url}")

        auditor_map = {
            "Agent Experience": AxoAuditor,
            "GEO Readiness & Governance": GeoReadinessAnalyzer,
            "API Readiness": ModularityApiAnalyzer,
            "Performance & Reliability": AutomationAuditor,
            "Structural & Semantic": SemanticAuditor,
        }

        auditor_cls = auditor_map.get(pillar_name)
        if not auditor_cls:
            raise ValueError(f"Invalid pillar name: {pillar_name}")
        
        if auditor_cls is AxoAuditor:
            result = auditor_cls(base_url=url, model=model).run_all()
        else:
            result = auditor_cls(base_url=url).run_all()

        print(f"Completed {pillar_name} audit successfully")
        
        return {
            "pillar": pillar_name,
            "result": result,
            "status": "completed"
        }
    
    except Exception as e:
        error_msg = f"Error running {pillar_name} audit: {str(e)}"
        print(f"Error in {pillar_name}: {traceback.format_exc()}")
        return {
            "pillar": pillar_name,
            "result": {"error": error_msg, "traceback": traceback.format_exc()},
            "status": "failed"
        }

@celery_app.task(bind=True, time_limit=900)
def run_audit_parallel(self, scan_id: str, url: str, api_key: str) -> Dict[str, Any]:
    """
    Run comprehensive audit with parallel pillar execution.
    Fallback to sequential execution if parallel fails.
    """
    if not url or not scan_id:
        raise ValueError("URL and Scan ID are required")

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash-lite')

        print(f"Classifying website category for {url}")
        category_result = classify_website(model, url)
        category = category_result["category"]
        pillar_weights = get_category_weights(category)

        print(f"Using weights for {category}: {pillar_weights}")

        asyncio.run(scan_service.update_scan_from_task(
                scan_id=scan_id,
                result={"status": "Parallel Processing",  "category": category},
                status="PROGRESS"
            )
        )
        pillars = [
            ("Agent Experience", AxoAuditor),
            ("GEO Readiness & Governance", GeoReadinessAnalyzer),
            ("API Readiness", ModularityApiAnalyzer),
            ("Performance & Reliability", AutomationAuditor),
            ("Structural & Semantic", SemanticAuditor),
        ]
        try:
            print("Starting parallel audit tasks")
            start = datetime.now()

            pillar_tasks = []
            for name, _ in pillars:
                task = run_single_pillar.apply_async((name, url, api_key, scan_id))
                pillar_tasks.append((name, task))

            reports = {}
            failed_pillars = []
            timeout_seconds = 900
            check_interval = 2
            elapsed = 0
            while len(reports) + len(failed_pillars) < len(pillar_tasks) and elapsed < timeout_seconds:
                for pillar_name, pillar_task in pillar_tasks:
                    if pillar_name in reports or pillar_name in failed_pillars:
                        continue
                    if pillar_task.ready():
                        try:
                            pillar_result = pillar_task.result
                            if pillar_result and pillar_result["status"] == "completed":
                                reports[pillar_name] = pillar_result["result"]
                            else:
                                failed_pillars.append(pillar_name)
                                print(f"Failed to complete {pillar_name} audit")
                        except Exception as e:
                            failed_pillars.append(pillar_name)
                            print(f"Failed to complete {pillar_name} audit")

                if len(failed_pillars) > 0:
                    print(f"Pillars failed: {failed_pillars}, falling back to sequential execution")
                    for _, pillar_task in pillar_tasks:
                        pillar_task.revoke(terminate=True)
                        failed_pillars.append(pillar_name)
                        print(f"Failed to complete {pillar_name} audit")
                
                if len(failed_pillars) > 0:
                    print(f"Pillars failed: {failed_pillars}, falling back to sequential execution")
                    for _, pillar_task in pillar_tasks:
                        pillar_task.revoke(terminate=True)
                    
                    return run_audit.delay(scan_id, url, api_key)

                if len(reports) == len(pillar_tasks):
                    print(f"All pillars completed successfully")
                    break
                
                time.sleep(check_interval)
                elapsed += check_interval
                if elapsed%10 == 0:
                    completed = len(reports)
                    asyncio.run(scan_service.update_scan_from_task(
                        scan_id=scan_id,
                        result={"current": completed, "total": len(pillar_tasks), "last_completed": "Parallel Processing"},
                        status="PROGRESS"
                    ))

            
            final = aggregate_scans(
                model,
                category,
                pillar_weights,
                reports["Agent Experience"],
                reports["GEO Readiness & Governance"],
                reports["API Readiness"],
                reports["Performance & Reliability"],
                reports["Structural & Semantic"],
            )
            end = datetime.now()
            exec_time = round((end - start).total_seconds() / 60, 2)
            final["duration_minutes"] = exec_time
            final["assessed_on"] = start.strftime("%Y-%m-%d")
            final["website_category"] = category
            final["execution_type"] = "parallel"

        except Exception as e:
            print(f"Parallel execution failed, falling back to sequential execution")
            return run_audit.delay(scan_id, url, api_key)

        
        asyncio.run(scan_service.update_scan_from_task(
            scan_id=scan_id,
            result=final,
            status="completed"
        ))
        return {"status": "completed", "scan_id": scan_id}
    
    except Exception as e:
        error_report = {"error": str(e)}
        asyncio.run(scan_service.update_scan_from_task(
            scan_id=scan_id,
            result=error_report,
            status="failed"
        ))
        raise e

@celery_app.task(bind=True, time_limit=900)
def run_audit(self, scan_id: str, url: str, api_key: str) -> Dict[str, Any]:
    """
    Run a comprehensive audit based on the provided URL and API key.
    """
    if not url or not scan_id:
        raise ValueError("URL and Scan ID are required")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash-lite')

        print(f"Classifying website category for {url}")
        category_result = classify_website(model, url)
        category = category_result["category"]

        pillar_weights = get_category_weights(category)
        print(f"Using weights for {category}: {pillar_weights}")

        reports = {}
        # Pillars in order, mapping to auditor classes
        pillars = [
            ("Agent Experience",   AxoAuditor),
            ("GEO Readiness & Governance", GeoReadinessAnalyzer),
            ("API Readiness",      ModularityApiAnalyzer),
            ("Performance & Reliability", AutomationAuditor),
            ("Structural & Semantic", SemanticAuditor),
        ]
        start = datetime.now()

        for idx, (name, AuditorCls) in enumerate(pillars, start=1):
            # update progress
            self.update_state(
                state="PROGRESS",
                meta={"current": idx, "total": len(pillars), "last_completed": name}
            )

            # run each auditor
            if AuditorCls is AxoAuditor:
                rpt = AuditorCls(base_url=url, model=model).run_all()
            else:
                rpt = AuditorCls(base_url=url).run_all()
            reports[name] = rpt

            asyncio.run(scan_service.update_scan_from_task(
                scan_id=scan_id,
                result={"current": idx, "total": len(pillars), "last_completed": name}, # Store the partial results
                status="PROGRESS"
            ))
            

        # combine via your aggregate_scans logic
        final = aggregate_scans(
            model,
            category,
            pillar_weights,
            reports["Agent Experience"],
            reports["GEO Readiness & Governance"],
            reports["API Readiness"],
            reports["Performance & Reliability"],
            reports["Structural & Semantic"],
        )

        end = datetime.now()
        final["duration_minutes"] = round((end - start).total_seconds() / 60, 2)
        final["assessed_on"] = start.strftime("%Y-%m-%d")
        final["website_category"] = category
        final["execution_type"] = "sequential"

        asyncio.run(scan_service.update_scan_from_task(
            scan_id=scan_id,
            result=final,
            status="completed"
        ))

        return {"status": "completed", "scan_id": scan_id}
    
    except Exception as e:
        error_report = {"error": str(e)}
        asyncio.run(scan_service.update_scan_from_task(
            scan_id=scan_id, 
            result=error_report, 
            status="failed"
        ))
        raise e


def aggregate_scans(
    model, 
    category: str,
    pillar_weights: Dict[str, float],
    axo_report: dict, 
    geo_report: dict, 
    modular_report: dict, 
    automation_report: dict, 
    semantic_report: dict
) -> dict:
    """
    Sends combined reports to LLM for unified formatting and total aggregate scoring.
    """
    
    # Validate inputs first
    reports = {
        "Agent Experience": axo_report,
        "GEO Readiness & Governance": geo_report, 
        "API Readiness": modular_report,
        "Performance & Reliability": automation_report,
        "Structural & Semantic": semantic_report
    }

    pillar_scores = {}
    
    # Check for None/empty reports
    for name, report in reports.items():
        score = report.get("overall_score", 0)
        pillar_scores[name] = score

    overall_score = sum(
        pillar_scores[name] * pillar_weights[name]
        for name in pillar_weights.keys()
    )

    overall_score = int(round(overall_score))

    grade = calculate_grade(overall_score)

    llm_analysis = llm_content_analysis(model, pillar_scores, reports)

    return {
        "overall_score": overall_score,
        "grade": grade,
        "website_category": category,
        "pillars": [
            {
                "name": pillar_name,
                "score": pillar_scores[pillar_name],
                "weight": pillar_weights[pillar_name]*100,
                "grade": calculate_grade(pillar_scores[pillar_name]),
            }
            for pillar_name in pillar_weights.keys()
        ],
        "detailed_pillar_analysis": llm_analysis.get("detailed_analysis", []),
        "combined_recommendations": llm_analysis.get("recommendations", [])
    }

def llm_content_analysis(model, pillar_scores: Dict[str, float], reports: Dict[str, dict]) -> dict:
    """
    Ask LLM ONLY for content analysis, not structure
    """
    prompt = f"""
    You are an API & web-intelligence auditor. Analyze these five audit reports and provide insights:

    PILLAR SCORES:
    {json.dumps(pillar_scores, indent=2)}

    DETAILED REPORTS:
    {json.dumps(reports, indent=2)}


    Provide analysis in this EXACT format:
    {{
        "detailed_analysis": [
            {{
                "pillar": "GEO Readiness & Governance",
                "sub_components": [
                    {{
                        "name": "<specific_component_found_in_report>",
                        "score": <score_from_report>,
                        "status": "<good|warning|error>",
                        "description": "<your_analysis_of_this_component>"
                    }}
                    // ... for each sub-component
                ]
            }}
            // ... for each pillar
        ],
        "recommendations": [
            "<actionable_recommendation_1>",
            "<actionable_recommendation_2>",
            // max 5 recommendations
        ]
    }}
    
    Focus on:
    1. Extract actual sub-components from the detailed reports
    2. Provide meaningful descriptions of issues found
    3. Give actionable recommendations
    4. Use the exact pillar names I provided
    5. Stick to the exact format and structure
    6. Return ONLY valid JSON, no markdown or extra text
    """
    
    try:
        response = model.generate_content(
            prompt
        )
        
        print(f"🤖 LLM Analysis Raw Response: '{response.text}'")
        
        if not response.text or response.text.strip() == "":
            raise ValueError("Empty response from Gemini")
        
        # Clean response (same as category classifier)
        response_text = response.text.strip()
        
        # Remove markdown formatting
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        response_text = re.sub(r'\s+', ' ', response_text)
        response_text = response_text.strip()
        
        print(f"🧹 LLM Analysis Cleaned Response: '{response_text}'")
        
        result = json.loads(response_text)
        print(f"✅ LLM Analysis parsed successfully")
        return result
    except Exception as e:
        print(f"Error during LLM content analysis: {e}")
        return generate_fallback_analysis(pillar_scores, reports)

def calculate_grade(score: int) -> str:
    """Calculate letter grade from numeric score"""
    if score >= 90: return "A"
    elif score >= 80: return "B" 
    elif score >= 70: return "C"
    elif score >= 60: return "D"
    else: return "F"

# Alternative approach if the above still fails
def generate_fallback_analysis(pillar_scores: Dict[str, float], reports: Dict[str, dict]) -> dict:
    """
    Fallback method that extracts scores manually and creates a simpler aggregation
    """
    return {
        "detailed_analysis": [
            {
                "pillar": pillar_name,
                "sub_components": [
                    {
                        "name": "Overall Assessment",
                        "score": pillar_scores[pillar_name],
                        "status": "good" if pillar_scores[pillar_name] >= 80 else "warning" if pillar_scores[pillar_name] >= 60 else "error",
                        "description": f"Overall {pillar_name} score analysis"
                    }
                ]
            }
            for pillar_name in pillar_scores.keys()
        ],
        "recommendations": [
            "Review and improve areas with scores below 80",
            "Monitor performance metrics regularly",
            "Consider implementing suggested optimizations"
        ]
    }