import asyncio
import json
import re
from urllib.parse import urljoin
import httpx
import logging

# --- Basic Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class AgentIdentification:
    """
    Sub-pillar 1: AI Agent Identification (Production Grade)

    Audits a website's agent identification capabilities by gathering evidence
    asynchronously and using an LLM for advanced analysis, scoring, and explanation.
    Combines high-performance probing with intelligent, context-aware analysis.
    """
    def __init__(self, base_url: str, model, timeout: float = 15.0):
        self.base_url = base_url
        self.model = model
        self.timeout = timeout
        self.user_agents = {
            "human_baseline": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "googlebot": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "bingbot": "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
            "gptbot": "Mozilla/5.0 (compatible; GPTBot/1.0; +https://openai.com/gptbot)",
            "claude_bot": "Mozilla/5.0 (compatible; Claude-3/1.0; Anthropic AI Agent)",
            "headless_chrome": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/120.0.0.0 Safari/537.36",
            "human_windows_chrome": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "human_macos_safari": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
            "human_linux_firefox": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0",
            "human_android_chrome": "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36",
            "human_ios_safari": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1",
            "brave_browser": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", # Brave often uses a similar UA to Chrome
            "edge_browser": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
            "duckduckbot": "DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)",
            "slackbot": "Slackbot 1.0 (+https://api.slack.com/robots)",
            "comet": "Mozilla/5.0 (compatible; Comet/1.0; Perplexity AI Agent)",
            "claude": "Mozilla/5.0 (compatible; Claude-3/1.0; Anthropic AI Agent)",
            "gemini": "Mozilla/5.0 (compatible; Gemini/1.0; Google AI Agent)"
        }

    async def _probe(self, client: httpx.AsyncClient, url: str, headers: dict = {}) -> dict:
        """
        Performs a single, safe, asynchronous request.
        """
        try:
            response = await client.get(url, headers=headers, timeout=self.timeout, follow_redirects=True)
            return {
                "status_code": response.status_code,
                "content_length": len(response.content),
                "content_type": response.headers.get("content-type", "unknown"),
                "headers": dict(response.headers),
                "final_url": str(response.url),
                "content_snippet": response.text[:500]  # Snippet for behavioral analysis
            }
        except httpx.RequestError as e:
            logging.warning(f"Request failed for {url}: {e}")
            return {"error": str(e)}

    async def gather_evidence(self) -> dict:
        """
        Gathers all necessary evidence from the target website concurrently.
        """
        logging.info("Gathering evidence...")
        evidence = {}
        tasks = []

        async with httpx.AsyncClient() as client:
            # 1. Create task for agents.json manifest check
            manifest_url = urljoin(self.base_url, "/.well-known/agents.json")
            tasks.append(self._probe(client, manifest_url))

            # 2. Create tasks for probing with different User-Agents
            for ua_string in self.user_agents.values():
                tasks.append(self._probe(client, self.base_url, headers={"User-Agent": ua_string}))

            # 3. Create task for probing with custom agent headers
            custom_headers = {
                "User-Agent": self.user_agents["human_baseline"],
                "X-Agent-Type": "AI-Assistant",
                "X-Requested-By": "AI-Agent"
            }
            tasks.append(self._probe(client, self.base_url, headers=custom_headers))

            logging.info(f"Executing {len(tasks)} probes concurrently...")
            results = await asyncio.gather(*tasks)

        # Structure the results
        evidence['manifest_check'] = results[0]
        evidence['user_agent_probes'] = {name: result for name, result in zip(self.user_agents.keys(), results[1:-1])}
        evidence['custom_header_probe'] = results[-1]

        logging.info("Evidence gathering complete.")
        return evidence

    def run_and_analyze(self) -> dict:
        """
        Gathers evidence and sends it to the LLM for a final analysis.
        """
        evidence = asyncio.run(self.gather_evidence())

        score = self.calculate_deterministic_score(evidence)

        prompt = f"""
        Act as a cybersecurity and web intelligence analyst. Your task is to analyze a website's agent identification capabilities based on the following evidence.

        **Evidence Collected:**
        ```json
        {json.dumps(evidence, indent=2)}
        ```

        **Analysis Instructions:**
        1. **Manifest Analysis:** Review agents.json file availability and content
        2. **Differential Treatment:** Analyze how the site treats different user agents (bots vs humans)
        3. **Custom Headers:** Evaluate recognition of custom agent headers
        4. **Anti-bot Measures:** Identify security measures and detection mechanisms
        5. **Overall Assessment:** Evaluate the sophistication of agent identification

        **Output Format:**
        Provide response as valid JSON only:
        {{"explanation": "<detailed analysis>", "recommendations": ["<suggestions>"]}}
        """

        logging.info("Sending evidence to Gemini for analysis...")
        try:
            response = self.model.generate_content(prompt)
            # A robust way to extract JSON, even if wrapped in markdown
            match = re.search(r"```json\n(.*?)\n```", response.text, re.DOTALL)
            if match:
                json_string = match.group(1)
            else:
                json_string = response.text

            # Parse the JSON to extract explanation and recommendations
            try:
                llm_response = json.loads(json_string)
                explanation = llm_response.get("explanation", "Analysis completed")
                recommendations = llm_response.get("recommendations", [])
            except json.JSONDecodeError:
                explanation = "Deterministic analysis completed. LLM explanation parsing failed."
                recommendations = []
            
            return {
                "score": score,
                "explanation": explanation,
                "recommendations": recommendations
            }
        except Exception as e:
            logging.error(f"An error occurred during Gemini analysis: {e}")
            return {
                "score": score,
                "explanation": f"Deterministic analysis completed. LLM explanation failed: {e}",
                "recommendations": []
            }

    def calculate_deterministic_score(self, evidence: dict) -> int:
        """
        Calculate score based on concrete evidence, not LLM analysis
        """
        score = 0
        
        # Manifest Check (40 points)
        manifest = evidence.get('manifest_check', {})
        if manifest.get('status_code') == 200:
            score += 40
            logging.info("✅ agents.json manifest found: +40 points")
        
        # User Agent Differential Treatment (35 points) - DETERMINISTIC VERSION
        ua_probes = evidence.get('user_agent_probes', {})
        human_baseline = ua_probes.get('human_baseline', {})
        
        # Check for ANY evidence of differential treatment across ALL bots
        has_differential_treatment = False
        rate_limiting_detected = False
        different_responses_detected = False
        
        for bot_name, bot_resp in ua_probes.items():
            if bot_name != 'human_baseline' and bot_resp and human_baseline:
                # Check for rate limiting (429) - strong evidence of bot detection
                if bot_resp.get('status_code') == 429:
                    rate_limiting_detected = True
                    logging.info(f"✅ Rate limiting detected for {bot_name}: 429 response")
                
                # Check for different status codes (excluding 429 which we handle above)
                if (bot_resp.get('status_code') != human_baseline.get('status_code') and 
                    bot_resp.get('status_code') != 429):
                    different_responses_detected = True
                    logging.info(f"✅ Different response for {bot_name}: {bot_resp.get('status_code')} vs {human_baseline.get('status_code')}")
                
                # Check for significant content differences
                content_diff = abs(bot_resp.get('content_length', 0) - human_baseline.get('content_length', 0)) > 1000
                if content_diff:
                    different_responses_detected = True
                    logging.info(f"✅ Content difference for {bot_name}: {abs(bot_resp.get('content_length', 0) - human_baseline.get('content_length', 0))} bytes")
        
        # Deterministic scoring based on evidence types
        if rate_limiting_detected:
            score += 35  # Rate limiting is the strongest evidence
            has_differential_treatment = True
            logging.info("✅ Strong differential treatment (rate limiting): +35 points")
        elif different_responses_detected:
            score += 25  # Other differential responses
            has_differential_treatment = True
            logging.info("✅ Moderate differential treatment (different responses): +25 points")
        
        if not has_differential_treatment:
            logging.info("ℹ️ No clear differential treatment detected")
        
        # Anti-bot Detection (25 points)
        content = human_baseline.get('content_snippet', '')
        anti_bot_indicators = [
            'navigator.webdriver',
            'canvas fingerprinting',
            'recaptcha',
            'cloudflare',
            'bot detection'
        ]
        
        detected_measures = sum(1 for indicator in anti_bot_indicators if indicator.lower() in content.lower())
        if detected_measures >= 2:
            score += 25
            logging.info(f"✅ Anti-bot measures detected: +25 points")
        elif detected_measures == 1:
            score += 15
            logging.info(f"✅ Basic anti-bot measures: +15 points")
        
        return min(score, 100)