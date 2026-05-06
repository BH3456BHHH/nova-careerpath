import json
import os
import requests

# Model ID on OpenRouter — as specified by your professor
MODEL_ID = "google/gemini-3.1-flash-lite-preview"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

_CAREER_LABELS = {
    "consulting":         "Management Consulting",
    "investment_banking": "Investment Banking",
    "tech":               "Tech / Product",
    "entrepreneurship":   "Entrepreneurship",
    "marketing":          "Marketing",
    "sustainability":     "Sustainability / ESG",
}


def _api_key() -> str:
    try:
        import streamlit as st
        key = st.secrets.get("GEMINI_API_KEY", "")
        if key:
            return key
    except Exception:
        pass
    return os.environ.get("GEMINI_API_KEY", "")


def _call(prompt: str) -> str | None:
    """Make one OpenRouter call and return the text content, or None on failure."""
    key = _api_key()
    if not key:
        return None
    try:
        response = requests.post(
            OPENROUTER_URL,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"model": MODEL_ID, "messages": [{"role": "user", "content": prompt}]},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[Gemini] API call failed: {e}")
        return None


def _parse_json(text: str, opening: str = "{") -> dict | list | None:
    """Strip markdown fences and parse JSON."""
    if not text:
        return None
    if "```" in text:
        for part in text.split("```"):
            part = part.strip().lstrip("json").strip()
            if part.startswith(opening):
                text = part
                break
    try:
        return json.loads(text)
    except Exception:
        return None


def enhance_cv_feedback(cv_text: str, career_key: str, scores: dict) -> dict | None:
    """
    Ask Gemini for personalised CV feedback.
    Returns dict: highlights, strengths, gaps, quick_win — or None on failure.
    """
    career_label = _CAREER_LABELS.get(career_key, career_key)
    prompt = f"""You are an expert career advisor at Nova SBE (Nova School of Business and Economics, Portugal).
A student is targeting a career in {career_label}.

Automated CV scores (for context):
- Overall: {scores['overall_pct']}/100
- Impact (action verbs, numbers, accomplishments): {scores['impact']['score']}/40
- Brevity (length, bullets, filler words): {scores['brevity']['score']}/30
- Style (sections, active voice, date consistency): {scores['style']['score']}/30

CV text:
---
{cv_text[:4000]}
---

Give specific, honest feedback referencing actual content from this CV. Be direct and practical.

Return ONLY a JSON object — no markdown, no explanation outside the JSON:
{{
  "highlights": ["actionable CV tip 1", "actionable CV tip 2", "actionable CV tip 3"],
  "strengths": ["specific strength for {career_label} 1", "specific strength 2", "specific strength 3"],
  "gaps": ["specific gap for {career_label} 1", "specific gap 2", "specific gap 3"],
  "quick_win": "one concrete action the student can take today to improve their {career_label} profile"
}}"""

    print(f"[Gemini] Generating CV feedback ({career_label})...")
    result = _parse_json(_call(prompt), "{")
    if result:
        print("[Gemini] CV feedback success!")
    return result


def generate_alumni(career_key: str) -> list | None:
    """
    Generate 5 realistic Nova SBE alumni profiles for careers not in the database.
    Returns a list of dicts matching the alumni CSV column format, or None on failure.
    """
    career_label = _CAREER_LABELS.get(career_key, career_key)
    prompt = f"""You are helping Nova SBE (Nova School of Business and Economics, Portugal) students
find alumni to reach out to for career advice in {career_label}.

Generate 5 realistic but fictional Nova SBE alumni working in {career_label}.
Use plausible Portuguese or European names and real well-known companies in this sector.
Master's program names should be from Nova SBE: e.g. "MSc in Management", "MSc in Finance",
"MSc in Economics", "MSc in Marketing", "MSc in Information Management".

Return ONLY a JSON array — no markdown, no explanation:
[
  {{
    "Full Name": "First Last",
    "Job Title": "Specific Role Title",
    "Company": "Real Company Name",
    "Master's Program Name": "MSc in ...",
    "LinkedIn Profile URL": ""
  }}
]"""

    print(f"[Gemini] Generating alumni for {career_label}...")
    result = _parse_json(_call(prompt), "[")
    if result:
        print(f"[Gemini] Alumni generation success ({len(result)} profiles)!")
    return result if isinstance(result, list) else None


def generate_employers(career_key: str) -> list | None:
    """
    Generate 5 target employers for careers not in the database.
    Returns a list of dicts matching the employer CSV column format, or None on failure.
    """
    career_label = _CAREER_LABELS.get(career_key, career_key)
    prompt = f"""You are helping Nova SBE (Nova School of Business and Economics, Portugal) students
find target employers in {career_label}.

Generate 5 top employers that actively recruit from European business schools for {career_label} roles.
Be specific and realistic about application timing and what they look for.

Return ONLY a JSON array — no markdown, no explanation:
[
  {{
    "Company": "Company Name",
    "Key Evaluation Criteria": "specific things this company looks for: GPA, skills, experience",
    "Application Timing": "e.g. 6-9 months before start date, rolling basis, etc.",
    "Typical Requirements": "internships, specific skills, languages, GPA threshold etc."
  }}
]"""

    print(f"[Gemini] Generating employers for {career_label}...")
    result = _parse_json(_call(prompt), "[")
    if result:
        print(f"[Gemini] Employer generation success ({len(result)} companies)!")
    return result if isinstance(result, list) else None
