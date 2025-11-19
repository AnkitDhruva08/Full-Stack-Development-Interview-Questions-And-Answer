# API Reference

```yaml
openapi: 3.0.0
info:
  title: BuildBridges Agentic Assessment API
  version: 1.0.0
paths:
  /api/analyze:
    post:
      summary: Analyze a website
```
# API Reference

The **BuildBridges Agentic Assessment API** enables developers to programmatically analyze websites for AI readiness, retrieve ARI scores, and access structured recommendations.

---

## ⚙️ Overview

The API is RESTful and returns responses in **JSON format**.  
It is primarily used by the BuildBridges frontend dashboard, but third-party systems can also integrate with it to embed **agentic web analysis** features.

**Base URL (example):**





**Content-Type:** `application/json`

---

## 🧱 OpenAPI Specification

```yaml
openapi: 3.0.0
info:
  title: BuildBridges Agentic Assessment API
  version: 1.0.0
  description: |
    This API allows you to analyze websites, retrieve Agent Readiness Index (ARI) scores,
    and access machine-readable audit reports for agentic web readiness.
servers:
  - url: https://api.buildbridges.co/v1
    description: Production API
  - url: https://staging.buildbridges.co/v1
    description: Staging environment

paths:
  /api/analyze:
    post:
      summary: Analyze a website for agentic readiness
      description: Submits a website URL for ARI analysis and returns an analysis ID or immediate result.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - url
              properties:
                url:
                  type: string
                  format: uri
                  example: "https://example.com"
                deep_scan:
                  type: boolean
                  description: "If true, performs a deep multi-page crawl."
                  default: false
      responses:
        '200':
          description: Analysis completed successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: "completed"
                  ari_score:
                    type: number
                    example: 84.6
                  recommendations:
                    type: array
                    items:
                      type: string
                      example: "Add schema.org Product markup"
                  report_id:
                    type: string
                    example: "rep_7843a12"
        '400':
          description: Invalid request or malformed URL
        '500':
          description: Internal server error or crawl timeout

  /api/report/{report_id}:
    get:
      summary: Get a detailed ARI report
      description: Retrieves a full structured report for a previously analyzed website.
      parameters:
        - in: path
          name: report_id
          required: true
          schema:
            type: string
            example: "rep_7843a12"
      responses:
        '200':
          description: Report retrieved successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  url:
                    type: string
                    example: "https://example.com"
                  ari_score:
                    type: number
                    example: 84.6
                  dimensions:
                    type: object
                    properties:
                      structure_readiness:
                        type: number
                        example: 90
                      discoverability:
                        type: number
                        example: 80
                      actionability:
                        type: number
                        example: 70
                      semantic_integrity:
                        type: number
                        example: 88
                      performance_accessibility:
                        type: number
                        example: 85
                  recommendations:
                    type: array
                    items:
                      type: string
                      example: "Expose sitemap.xml in robots.txt"
        '404':
          description: Report not found

  /api/compare:
    post:
      summary: Compare two or more websites by ARI score
      description: Returns side-by-side comparisons of ARI metrics for competitive benchmarking.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - urls
              properties:
                urls:
                  type: array
                  items:
                    type: string
                  example: ["https://example.com", "https://competitor.com"]
      responses:
        '200':
          description: Comparison successful
          content:
            application/json:
              schema:
                type: object
                properties:
                  comparison:
                    type: array
                    items:
                      type: object
                      properties:
                        url:
                          type: string
                          example: "https://example.com"
                        ari_score:
                          type: number
                          example: 82.3
                        rank:
                          type: integer
                          example: 1
        '400':
          description: Invalid URL list




🧪 Example API Usage (Python)

import requests

url = "https://api.buildbridges.co/v1/api/analyze"
payload = {"url": "https://example.com", "deep_scan": False}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
print(response.json())



Example Response:
{
  "status": "completed",
  "ari_score": 87.2,
  "recommendations": [
    "Add JSON-LD schema for Organization.",
    "Optimize robots.txt for agentic crawling."
  ],
  "report_id": "rep_7843a12"
}



⚡ Rate Limits 
| Plan       | Requests per Minute | Notes                         |
| ---------- | ------------------- | ----------------------------- |
| Free       | 10                  | For testing and demo          |
| Pro        | 100                 | Includes full-page deep scans |
| Enterprise | Custom              | SLA + custom pipelines        |


🔒 Authentication (Optional)

If authentication is enabled, use a Bearer token: 
curl -X POST https://api.buildbridges.co/v1/api/analyze \
  -H "Authorization: Bearer <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'


🚨 Error Codes

| Code | Meaning               | Example                            |
| ---- | --------------------- | ---------------------------------- |
| 400  | Bad Request           | Invalid URL format                 |
| 404  | Not Found             | Report ID does not exist           |
| 429  | Too Many Requests     | Exceeded rate limit                |
| 500  | Internal Server Error | Unexpected failure during analysis |


🧠 Developer Notes

All reports are cached for 24 hours by default.

Each crawl is sandboxed — no JS execution beyond headless analysis.

ARI scoring logic is versioned (ari_v1, ari_v2, etc.) for model evolution.

🚀 Summary

The BuildBridges API enables full automation of website AI-readiness audits.
It empowers developers, SEO specialists, and organizations to programmatically measure, benchmark, and improve the Agent Readiness Index (ARI) of any site.

“BuildBridges API — Your gateway to the Agentic Web.”