import csv
import re

import os as _os
_DIR = _os.path.dirname(_os.path.abspath(__file__))
ALUMNI_CSV   = _os.path.join(_DIR, "Alumni Research Database(Alumni Data).csv")
EMPLOYER_CSV = _os.path.join(_DIR, "Employer_Database_CV_Screening(Consulting).csv")
COURSES_CSV  = _os.path.join(_DIR, "nova_courses&clubs_database_v3(MNG).csv")

INDUSTRY_MAP = {
    "consulting":         "Consulting",
    "investment_banking": "Finance",
    "tech":               "Tech",
    "entrepreneurship":   "Entrepreneurship",
    "marketing":          "Marketing",
    "sustainability":     "Sustainability",
}

COURSE_KEYWORDS = {
    "consulting": [
        "strategy", "consulting", "negotiation", "project management",
        "corporate", "analytics", "competitive", "management consulting",
        "persuasion", "case", "modeling", "modelling",
    ],
    "investment_banking": [
        "finance", "financial", "banking", "mergers", "acquisitions",
        "valuation", "private equity", "investment", "derivatives",
        "capital", "corporate finance", "fintech", "venture",
    ],
    "tech": [
        "programming", "data", "digital", "machine learning", "product",
        "analytics", "ai", "blockchain", "technology", "algorithmic",
        "network", "cybersecurity", "e-commerce",
    ],
    "entrepreneurship": [
        "entrepreneurship", "venture", "innovation", "business model",
        "startup", "fintech", "social entrepreneurship", "science-based",
    ],
    "marketing": [
        "marketing", "brand", "consumer", "social media", "digital marketing",
        "crm", "advertising", "content", "shopper", "luxury",
    ],
    "sustainability": [
        "sustainability", "environment", "climate", "esg", "impact",
        "energy", "circular", "regenerative", "sustainable",
    ],
}

EMPLOYER_CRITERIA = {
    "gpa":            [r"\b1[6-9][,.]?\d*\b", r"\b20\b", r"\bgpa\b"],
    "internship":     ["internship", "intern ", "stage ", "traineeship", "working student"],
    "leadership":     ["led ", "managed ", "president", "vice president", "founder",
                       "director", "head of", "captain", "chair", "organis"],
    "case_prep":      ["case", "consulting club", "case team", "competition", "hackathon"],
    "extracurricular":["club", "society", "association", "volunteer", "committee"],
}

# Nationalities that signal the student is studying abroad (i.e. at Nova SBE as a foreign national)
FOREIGN_NATIONALITIES = [
    "german", "austrian", "french", "british", "spanish", "italian",
    "dutch", "swiss", "belgian", "swedish", "danish", "norwegian",
    "finnish", "polish", "czech", "slovak", "hungarian", "romanian",
    "bulgarian", "greek", "croatian", "slovenian", "estonian", "latvian",
    "lithuanian", "irish", "american", "canadian", "australian",
    "indian", "chinese", "brazilian", "argentinian", "mexican",
    "colombian", "chilean", "turkish", "russian", "ukrainian",
    "south african", "nigerian", "kenyan", "egyptian", "moroccan",
    "lebanese", "singaporean", "malaysian", "thai", "japanese", "korean",
]

ABROAD_KEYWORDS = [
    "exchange", "erasmus", "abroad", "semester abroad",
    "india", "china", "usa", "united states", "uk", "united kingdom",
    "germany", "france", "spain", "italy", "netherlands", "switzerland",
    "austria", "sweden", "denmark", "norway", "finland", "poland",
    "hong kong", "singapore", "japan", "south korea", "brazil",
    "australia", "canada", "mexico", "argentina",
]


def _load_csv(path):
    rows = []
    try:
        with open(path, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                rows.append({k.strip(): (v or "").strip() for k, v in row.items() if k and k.strip()})
    except Exception:
        pass
    return rows


def _check_criteria(cv_text):
    text        = cv_text.lower()
    first_lines = text[:800]   # nationality usually appears in header

    # International: foreign national studying at Nova SBE, OR explicit abroad experience
    is_foreign = any(nat in first_lines for nat in FOREIGN_NATIONALITIES)
    has_abroad = any(kw in text for kw in ABROAD_KEYWORDS)

    met = {}
    for crit, patterns in EMPLOYER_CRITERIA.items():
        met[crit] = any(
            bool(re.search(p, text, re.IGNORECASE)) if p.startswith(r"\b") else p in text
            for p in patterns
        )
    met["international"] = is_foreign or has_abroad
    return met


def _filter_courses(career_key):
    keywords = COURSE_KEYWORDS.get(career_key, [])
    rows     = _load_csv(COURSES_CSV)
    scored   = []
    for r in rows:
        name  = r.get("Course Name", "").lower()
        score = sum(1 for kw in keywords if kw in name)
        if score > 0:
            scored.append((score, r))
    scored.sort(key=lambda x: -x[0])
    return [r for _, r in scored[:5]]


def _filter_alumni(career_key):
    industry = INDUSTRY_MAP.get(career_key, "")
    rows     = _load_csv(ALUMNI_CSV)
    return [r for r in rows if industry.lower() in r.get("Industry", "").lower()][:5]


def _filter_employers(career_key):
    industry = INDUSTRY_MAP.get(career_key, "")
    rows     = _load_csv(EMPLOYER_CSV)
    return [r for r in rows if industry.lower() in r.get("Category", "").lower()][:5]


def _build_strengths(cv_result, criteria_met):
    imp   = cv_result.get("impact", {})
    brev  = cv_result.get("brevity", {})
    strengths = []

    av_score  = imp.get("action_verbs", {}).get("score", 0)
    qi_lines  = imp.get("quantifying_impact", {}).get("quantified_lines", 0)
    ln_score  = brev.get("length", {}).get("score", 0)

    if av_score >= 8:
        strengths.append("Strong action verbs — your bullet points start with confident, impact-driven language that top employers notice immediately.")
    if qi_lines >= 3:
        strengths.append(f"{qi_lines} quantified lines — you're already showing measurable impact, which is exactly what recruiters look for.")
    if ln_score >= 8:
        strengths.append("Ideal CV length — concise and within the 1-page standard expected by top firms.")
    if criteria_met.get("leadership"):
        strengths.append("Leadership signals detected — a key differentiator for applications at competitive firms.")
    if criteria_met.get("international"):
        strengths.append("International exposure — a significant advantage for globally recruiting firms.")
    if criteria_met.get("extracurricular"):
        strengths.append("Extracurricular involvement — shows initiative and teamwork beyond academics.")
    if not strengths:
        strengths.append("Your CV is structured and readable — a solid foundation to build on.")
    return strengths[:5]


def _build_gaps(cv_result, criteria_met, career_key):
    imp  = cv_result.get("impact", {})
    kw   = cv_result.get("keywords", {})
    gaps = []

    qi_lines = imp.get("quantifying_impact", {}).get("quantified_lines", 0)
    if qi_lines < 2:
        gaps.append("Add numbers to your bullets — firms in this field expect quantified achievements (team size, % impact, revenue, event attendance).")
    if not criteria_met.get("internship"):
        gaps.append("No internship detected — most target employers require at least 1 relevant internship before applying.")
    if not criteria_met.get("leadership"):
        gaps.append("Leadership is a key screening criterion — highlight any role where you led people or took ownership.")
    if career_key == "consulting" and not criteria_met.get("case_prep"):
        gaps.append("No case competition or consulting club experience — this is heavily weighted by MBB and top-tier firms.")
    if not criteria_met.get("international"):
        gaps.append("International experience is preferred — an exchange semester or internship abroad strengthens your profile significantly.")
    missing_kw = kw.get("missing", [])[:4]
    if kw.get("ratio", 1) < 0.4 and missing_kw:
        gaps.append(f"Missing industry keywords — add these naturally: {', '.join(missing_kw)}.")
    return gaps[:5]


def _readiness_score(cv_result, criteria_met):
    cv_pct = cv_result.get("overall_pct", 50)
    weights = {
        "internship": 25, "leadership": 20, "case_prep": 15,
        "international": 15, "extracurricular": 15, "gpa": 10,
    }
    criteria_score = sum(w for k, w in weights.items() if criteria_met.get(k))
    return min(100, max(0, round(cv_pct * 0.5 + criteria_score * 0.5)))


def _quick_win(cv_result, criteria_met, career_key):
    qi = cv_result.get("impact", {}).get("quantifying_impact", {}).get("quantified_lines", 0)
    if qi == 0:
        return "Add at least 2 numbers to your CV (team size, % result, event attendance) — the fastest single improvement you can make."
    if not criteria_met.get("internship"):
        return "Apply for an internship this semester — it is the most critical missing signal for employers in this field."
    if not criteria_met.get("leadership"):
        return "Explicitly name any leadership role you've held (project lead, event organiser, team captain) — firms scan for this first."
    if career_key == "consulting" and not criteria_met.get("case_prep"):
        return "Join Nova Case Team or Nova SBE Social Consulting — consulting firms look for this directly on the CV."
    if not criteria_met.get("international"):
        return "Apply for an exchange semester — it differentiates you from local candidates and is highly valued by international firms."
    return "Reach out to your Student Advisor at Nova SBE — you can get personal guidance and direct feedback on your CV and career planning in a one-on-one session."


def analyze_career_readiness(cv_text, career_key, cv_result):
    criteria_met = _check_criteria(cv_text)
    return {
        "score":        _readiness_score(cv_result, criteria_met),
        "strengths":    _build_strengths(cv_result, criteria_met),
        "gaps":         _build_gaps(cv_result, criteria_met, career_key),
        "courses":      _filter_courses(career_key),
        "alumni":       _filter_alumni(career_key),
        "employers":    _filter_employers(career_key),
        "criteria_met": criteria_met,
        "quick_win":    _quick_win(cv_result, criteria_met, career_key),
    }
