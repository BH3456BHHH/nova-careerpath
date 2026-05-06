import json
import os
import requests

# Model ID on OpenRouter — as specified by your professor
MODEL_ID = "google/gemini-2.5-flash-preview"

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


def enhance_cv_feedback(cv_text: str, career_key: str, scores: dict) -> dict | None:
    """
    Ask Gemini via OpenRouter for personalised CV feedback.
    Returns dict with keys: highlights, strengths, gaps, quick_win.
    Returns None silently if the API key is missing or the call fails —
    the app then falls back to the rule-based results automatically.
    """
    key = _api_key()
    if not key:
        return None

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

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL_ID,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=30,
        )
        response.raise_for_status()
        text = response.json()["choices"][0]["message"]["content"].strip()
        if "```" in text:
            for part in text.split("```"):
                part = part.strip().lstrip("json").strip()
                if part.startswith("{"):
                    text = part
                    break
        return json.loads(text)
    except Exception:
        return None
