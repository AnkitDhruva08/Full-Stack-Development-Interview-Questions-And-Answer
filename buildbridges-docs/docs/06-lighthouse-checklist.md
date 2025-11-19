# Lighthouse & Agentic Checklist

## Performance
- [ ] LCP < 2.5s
- [ ] robots.txt present


# Lighthouse & Agentic Checklist

The **Lighthouse & Agentic Checklist** ensures that a website meets both:
- Traditional **web performance standards** (Lighthouse Core Web Vitals), and  
- **AI-Agent compatibility standards** (BuildBridges Agentic Web readiness).

---

## ⚡ Performance
Performance metrics focus on how quickly content loads and becomes interactive.

- [ ] **LCP < 2.5s** — Largest Contentful Paint under 2.5 seconds  
- [ ] **FID < 100ms** — First Input Delay less than 100ms  
- [ ] **CLS < 0.1** — Cumulative Layout Shift within 0.1  
- [ ] **TTFB < 800ms** — Time to First Byte optimized  
- [ ] **robots.txt present** and not blocking essential content  
- [ ] **sitemap.xml accessible** and properly linked in robots.txt  
- [ ] **Preload key assets** (fonts, CSS, hero images)  
- [ ] **Serve images in next-gen formats (WebP/AVIF)**  
- [ ] **Use lazy loading** for offscreen content  
- [ ] **Compress static assets (Gzip/Brotli)**  
- [ ] **Enable caching headers** for static resources  

---

## 🧠 Agentic Readiness
These checks ensure the website is **machine-understandable and agent-compatible.**

- [ ] **Structured data (JSON-LD / schema.org)** present on all key pages  
- [ ] **OpenGraph & Twitter meta tags** correctly implemented  
- [ ] **Clear canonical URLs** on every page  
- [ ] **Consistent semantic HTML structure** (`<header>`, `<main>`, `<footer>`)  
- [ ] **Accessible language and title tags** (`<html lang="">`, `<title>`)  
- [ ] **Detectable API endpoints** (REST or GraphQL) for data or interaction  
- [ ] **Public data accessible via standardized endpoints** (e.g. `/api/info`)  
- [ ] **No heavy JS obfuscation** that prevents crawlers from parsing  
- [ ] **Meaningful ALT text** for images  
- [ ] **Visible structured content hierarchy** (H1 → H2 → H3 properly nested)  

---

## 🧩 Discoverability
Ensure AI agents, crawlers, and search engines can *find and index* content effectively.

- [ ] **robots.txt allows indexing of key content**  
- [ ] **Linked sitemap.xml** lists all major pages  
- [ ] **Breadcrumbs present and marked up (schema.org/BreadcrumbList)**  
- [ ] **Pagination handled properly with rel="next" / rel="prev"**  
- [ ] **Meta description and title present** for every page  
- [ ] **OpenGraph images correctly referenced and sized**  
- [ ] **Language tags and alternate links** (`hreflang`) for multilingual pages  

---

## 🧬 Semantic Integrity
Ensures the website conveys meaning accurately to AI systems.

- [ ] **Entities represented using schema.org types** (Organization, Product, Service, etc.)  
- [ ] **Rich snippets (FAQ, HowTo, Review)** structured correctly  
- [ ] **JSON-LD data validates via Google’s Structured Data Tool**  
- [ ] **Avoid duplicated or conflicting schema definitions**  
- [ ] **Use consistent naming for content identifiers (slug, ID, etc.)**  
- [ ] **Meta and schema data synchronized** (same business name, address, etc.)  
- [ ] **No misleading structured data (penalty risk)**  

---

## 🧰 Actionability
Ensures an AI agent can not only *read* the site but also *act* upon it safely.

- [ ] **Clear “Call to Action” endpoints** (book, buy, contact) defined via structured markup  
- [ ] **APIs or endpoints** for performing basic interactions  
- [ ] **Webhook or callback URLs** for integrations  
- [ ] **Accessible micro-actions** (like `/subscribe`, `/quote`, `/api/contact`)  
- [ ] **Authenticated routes clearly defined** with OAuth or API key headers  
- [ ] **Minimal hidden inputs or form traps**  
- [ ] **Agent-safe POST endpoints** (with clear schemas and predictable responses)  

---

## ♿ Accessibility & Inclusiveness
Accessibility enhances both user experience and AI parsing.

- [ ] **WCAG 2.1 compliance** checked  
- [ ] **ARIA labels and roles** implemented  
- [ ] **Keyboard navigability** confirmed  
- [ ] **High color contrast** maintained  
- [ ] **Descriptive link text** instead of “click here”  
- [ ] **Alt attributes on all images**  
- [ ] **Readable font sizes (>16px)**  
- [ ] **Page titles are descriptive and unique**  

---

## 🧱 Security & Reliability
Agentic systems need secure and predictable environments.

- [ ] **HTTPS enforced sitewide**  
- [ ] **HSTS header active**  
- [ ] **No mixed-content warnings**  
- [ ] **CSRF & XSS protection** enabled  
- [ ] **CORS headers properly configured**  
- [ ] **Rate-limiting and auth tokens** for API routes  
- [ ] **No sensitive data in client-side JS**  
- [ ] **404 and error pages return proper HTTP status codes**  

---

## 🧮 Scoring Guidelines

| Category | Weight | Description |
|-----------|--------|-------------|
| Performance | 20% | Page load and optimization |
| Agentic Readiness | 25% | Structured data and API presence |
| Discoverability | 20% | Metadata and indexing |
| Semantic Integrity | 15% | Schema and data clarity |
| Actionability | 10% | Machine interaction support |
| Accessibility | 5% | Inclusive and readable |
| Security | 5% | Safe and robust APIs |

---

## 🚀 Summary

This checklist combines **Google Lighthouse** metrics and **BuildBridges’ Agentic Standards**  
to form a *comprehensive readiness framework* for both human users and AI agents.

> “A truly modern website must serve two audiences — humans and intelligent machines.”
