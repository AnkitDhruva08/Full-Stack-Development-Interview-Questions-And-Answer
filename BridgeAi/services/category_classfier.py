import json
import re
from typing import Dict, Any
from utils.featcher import fetch_html_selenium

CATEGORY_WEIGHTS = {
    "e-commerce": {
        "GEO Readiness & Governance": 0.15,
        "Structural & Semantic": 0.2,
        "API Readiness": 0.25,
        "Performance & Reliability": 0.2,
        "Agent Experience": 0.2,
    },
    "saas-platform": {
        "GEO Readiness & Governance": 0.2,
        "Structural & Semantic": 0.1,
        "API Readiness": 0.35,
        "Performance & Reliability": 0.1,
        "Agent Experience": 0.25,
    },
    "News & Media": {
        "GEO Readiness & Governance": 0.3,
        "Structural & Semantic": 0.4,
        "API Readiness": 0.1,
        "Performance & Reliability": 0.05,
        "Agent Experience": 0.15,
    },
    "Healthcare": {
        "GEO Readiness & Governance": 0.35,
        "Structural & Semantic": 0.15,
        "API Readiness": 0.2,
        "Performance & Reliability": 0.15,
        "Agent Experience": 0.15,
    },
    "Travel & Booking": {
        "GEO Readiness & Governance": 0.2,
        "Structural & Semantic": 0.15,
        "API Readiness": 0.25,
        "Performance & Reliability": 0.15,
        "Agent Experience": 0.25,
    },
    "Finance & Fintech": {
        "GEO Readiness & Governance": 0.35,
        "Structural & Semantic": 0.10,
        "API Readiness": 0.2,
        "Performance & Reliability": 0.15,
        "Agent Experience": 0.2,
    },
    "Social Media": {
        "GEO Readiness & Governance": 0.15,
        "Structural & Semantic": 0.10,
        "API Readiness": 0.35,
        "Performance & Reliability": 0.15,
        "Agent Experience": 0.25,
    },
    "Real Estate": {
        "GEO Readiness & Governance": 0.25,
        "Structural & Semantic": 0.40,
        "API Readiness": 0.1,
        "Performance & Reliability": 0.1,
        "Agent Experience": 0.15,
    },
    "Government Services": {
        "GEO Readiness & Governance": 0.35,
        "Structural & Semantic": 0.15,
        "API Readiness": 0.1,
        "Performance & Reliability": 0.25,
        "Agent Experience": 0.15,
    },
    "Education and Research": {
        "GEO Readiness & Governance": 0.3,
        "Structural & Semantic": 0.4,
        "API Readiness": 0.1,
        "Performance & Reliability": 0.05,
        "Agent Experience": 0.15,
    },
    "corporate": {
        "GEO Readiness & Governance": 0.2,
        "Structural & Semantic": 0.2,
        "API Readiness": 0.2,
        "Performance & Reliability": 0.2,
        "Agent Experience": 0.2,
    }
}

def classify_website(model, url: str) -> Dict[str, Any]:
    """
    Classify website category using LLM analysis of content and structure.
    """
    try:
        # Fetch website content
        html_content = fetch_html_selenium(url)
        if not html_content:
            raise Exception("Could not fetch website content")

        content_sample = html_content[:5000]
        categories = list(CATEGORY_WEIGHTS.keys())

        prompt = f"""
            Analyze this website and classify it into ONE of these categories:
            
            CATEGORIES: {', '.join(categories)}
            
            WEBSITE URL: {url}
            WEBSITE CONTENT SAMPLE:
            {content_sample}
            
            Analyze the content, structure, and purpose to determine the category.
            
            Return ONLY a JSON response in this exact format:
            {{
                "category": "<one_of_the_categories>",
                "confidence": <integer_0_to_100>,
                "reasoning": "<brief_explanation>"
            }}
            
            RULES:
            - Choose the MOST FITTING category from the list
            - Confidence should reflect how certain you are (0-100)
            - Keep reasoning brief (1-2 sentences)
            - Return ONLY valid JSON
        """
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.1,
                "max_output_tokens": 200
            }
        )
        
        if not response.text or response.text.strip() == "":
            raise ValueError("Empty response from Gemini")
        
        # Clean markdown formatting
        response_text = response.text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        # Clean up whitespace and newlines
        response_text = re.sub(r'\s+', ' ', response_text)
        response_text = response_text.strip()
        
        result = json.loads(response_text)
        print(f"Category found to be {result['category']}")
        # Validate response
        if result["category"] not in categories:
            raise ValueError(f"Invalid category: {result['category']}")
        
        return result
        
    except Exception as e:
        print(f"Category classification failed: {e}")
        # Fallback to default category
        return {
            "category": "corporate",  # Safe default
            "confidence": 50,
            "reasoning": "Classification failed, using default corporate category"
        }

def get_category_weights(category: str) -> Dict[str, float]:
    """
    Get pillar weights for a specific category.
    """
    return CATEGORY_WEIGHTS.get(category, CATEGORY_WEIGHTS["corporate"])