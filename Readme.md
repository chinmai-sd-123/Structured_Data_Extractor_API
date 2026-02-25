Structured Company Information Extractor
========================================

A production-oriented AI backend system that extracts structured company information from websites or raw text using LLMs with strict schema enforcement, validation, retry logic, and confidence scoring.

Project Overview
----------------

This project builds a robust structured data extraction pipeline using:

- FastAPI (API layer)
- Web scraping (data ingestion)
- LLM (Gemini via OpenAI-compatible API)
- Pydantic (schema validation)
- JSON repair + retry logic
- Defensive pipeline design

Unlike basic LLM demos, this system is designed with production engineering principles.

What Problem It Solves
----------------------

Extract structured company information from:

- Website URLs
- Raw text

And return strictly formatted JSON:

{
  "company_name": "Hugging Face",
  "industry": "Artificial Intelligence",
  "pricing_model": "Tiered",
  "target_audience": "Developers and enterprises",
  "key_features": ["Model hosting", "Datasets", "Spaces"],
}

Architecture
------------

User Input
   ↓
FastAPI Endpoint
   ↓
Scraper (with timeout + fallback)
   ↓
Content Cleaning
   ↓
LLM (Strict JSON Prompt)
   ↓
Markdown Cleanup
   ↓
JSON Parse
   ↓
Pydantic Validation
   ↓
Auto-Repair (Retry if needed)
   ↓
Return Structured Output

Core Engineering Features
--------------------------

1) Strict JSON Enforcement

The model is instructed to return output in exact schema format:

{
  "company_name": string,
  "industry": string,
  "pricing_model": string,
  "target_audience": string,
  "key_features": [string],
}

Temperature is set to 0 for deterministic output.

2) Output Sanitization

Removes:

Markdown code fences

Formatting artifacts

Prevents JSON parsing failures.

3) Automatic Retry & Repair

If JSON parsing fails:

The raw output is sent back to LLM

A repair prompt is used

System attempts a second parse

If repair fails:

Error is returned safely

Raw outputs logged

This prevents crashes and increases reliability.

4) Schema Validation with Pydantic

Pydantic enforces:

Correct field types

Required fields


Prevents malformed AI output from propagating.


5) Defensive Scraping

Scraper includes:

Timeout handling

User-Agent spoofing

HTML size limits

Error detection

Early stop if content insufficient

Prevents unnecessary LLM calls.

Engineering Insights Learned
----------------------------

This project emphasizes:

1. Data Quality > Model Quality

Most failures were due to:

Poor scraping

Dynamic websites

Timeout issues

Not model capability.

2. Upstream Fixes Have Highest Leverage

Improving scraping:

Reduced retries

Increased confidence

Lowered cost

Improved accuracy

3. LLMs Require Defensive Programming

Never trust model output.

Always:

Sanitize

Validate

Retry

Guard

4. Observability Is Critical

Important metrics for production:

Scrape success rate

Retry rate

Confidence distribution

LLM latency

Timeout percentage

Cost per 1000 extractions

AI systems are infrastructure systems.

Known Limitations
-----------------

Cannot scrape heavy JavaScript-rendered sites (e.g., BMW homepage)

Does not use headless browser

Not yet asynchronous scraping

No background queue system implemented

Future Improvements
-------------------

Async scraping with httpx

Job queue (Redis / Celery)

Automatic fallback path detection (/about, /company)

Domain intelligence layer

Cost tracking

Rate limiting control

Distributed worker pool

Dynamic schema extraction

Testing Strategy
----------------

Test with:

Static company websites

Startup landing pages

Blog pages

Dynamic JS-heavy sites (expect graceful failure)

Very short input (expect validation error)

Tech Stack
----------

Python

FastAPI

Requests

BeautifulSoup

Gemini API (OpenAI-compatible endpoint)

Pydantic

JSON

Regex sanitization

Scalability Considerations
--------------------------

For 10,000+ URLs/day:

Recommended architecture:

API → Task Queue → Worker Pool → LLM → Database


Not synchronous blocking requests.

