import json
import os

try:
    import google.generativeai as genai
    _AVAILABLE = True
except ImportError:
    _AVAILABLE = False

# ── Replace this with the exact model ID your professor gave you ──────────────
# Ask your professor: "What is the exact model ID?" (e.g. "gemini-2.0-flash-lite")
MODEL_ID = "gemini-2.0-flash-lite"

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
    Ask Gemini for personalised CV feedback.
    Returns dict with keys: highlights, strengths, gaps, quick_win.
    Returns None silently if the API key is missing or the call fails —
    the app then falls back to the rule-based results automatically.
    """
    if not _AVAILABLE:
        return None
    key = _api_key()
    if not key:
        return None

    genai.configure(api_key=key)
    model = genai.GenerativeModel(MODEL_ID)

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
        response = model.generate_content(prompt)
        text = response.text.strip()
        if "```" in text:
            for part in text.split("```"):
                part = part.strip().lstrip("json").strip()
                if part.startswith("{"):
                    text = part
                    break
        return json.loads(text)
    except Exception:
        return None
