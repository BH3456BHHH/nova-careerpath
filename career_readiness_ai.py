import csv
import re

import os as _os
_DIR = _os.path.dirname(_os.path.abspath(__file__))
ALUMNI_CSV   = _os.path.join(_DIR, "Alumni Research Database(Alumni Data).csv")
EMPLOYER_CSV = _os.path.join(_DIR, "Employer_Database_CV_Screening(Consulting).csv")
COURSES_CSV  = _os.path.join(_DIR, "nova_courses&clubs_database_v3(MNG).csv")
CLUBS_CSV    = _os.path.join(_DIR, "nova_courses&clubs_database_v3(Student Clubs).csv")

INDUSTRY_MAP = {
    "consulting":         "Consulting",
    "investment_banking": "Investment Banking",
    "tech":               "Tech",
    "entrepreneurship":   "Entrepreneurship",
    "marketing":          "Marketing",
    "sustainability":     "Sustainability",
}

COURSE_KEYWORDS = {
    "consulting": [
        "strategy consulting", "management consulting", "competitive strategy",
        "corporate strategy", "persuasion and negotiation", "negotiation",
        "advanced strategy", "project management", "corporate valuation",
        "strategy", "analytics", "case",
    ],
    "investment_banking": [
        "corporate finance", "applied corporate finance", "financial management",
        "advanced financial management", "banking", "mergers", "acquisitions",
        "corporate valuation", "private equity", "derivatives",
        "financial statement", "venture capital", "fintech ventures",
        "fixed income", "credit risk", "asset management", "corporate financial risk",
    ],
    "tech": [
        "introduction to programming", "machine learning", "big data",
        "data visualization", "digital strategy", "blockchain", "cybersecurity",
        "ai ", "product management in technology", "e-commerce",
        "network analytics", "technology strategy", "algorithmic",
        "data", "digital", "programming",
    ],
    "entrepreneurship": [
        "applied entrepreneurship", "applied social entrepreneurship",
        "science-based entrepreneurship", "entrepreneurial strategy",
        "entrepreneurship", "business model innovation", "venture simulation",
        "fintech ventures", "innovation", "venture capital", "startup",
    ],
    "marketing": [
        "marketing management", "advanced marketing", "brand management",
        "digital marketing", "social media marketing", "integrated marketing",
        "international marketing", "marketing analytics", "consumer behavior",
        "luxury and fashion", "shopper marketing", "customer relationship",
        "marketing", "brand", "consumer", "advertising",
    ],
    "sustainability": [
        "fundamentals on environment", "energy and climate", "circular economy",
        "regenerative business", "finance and the transition to net zero",
        "sustainability evaluation", "sustainable marketing", "sustainable operations",
        "impact investments", "sustainability", "climate", "environment",
        "sustainable", "circular", "net zero", "esg",
    ],
}

def _load_clubs_from_csv():
    """Load all clubs from the Student Clubs CSV into a list of dicts."""
    clubs = []
    try:
        with open(CLUBS_CSV, encoding="utf-8-sig") as f:
            reader = csv.reader(f, delimiter=";")
            headers = None
            for row in reader:
                if not row or not row[0].strip():
                    continue
                if row[0].strip().startswith("Nova SBE") and "Source" in row[0]:
                    continue
                if row[0].strip().startswith("Skills and career"):
                    continue
                if row[0].strip() == "Club Name":
                    headers = [c.strip() for c in row]
                    continue
                if headers is None:
                    continue
                rec = {headers[i]: row[i].strip() if i < len(row) else "" for i in range(len(headers))}
                clubs.append(rec)
    except FileNotFoundError:
        pass
    return clubs

_CLUBS_CACHE = None

def _get_all_clubs():
    global _CLUBS_CACHE
    if _CLUBS_CACHE is None:
        _CLUBS_CACHE = _load_clubs_from_csv()
    return _CLUBS_CACHE

EMPLOYER_CRITERIA = {
    # GPA is handled separately via _gpa_meets_threshold() — needs per-path logic
    "internship":     ["internship", "intern ", "stage ", "traineeship", "working student",
                       "summer analyst", "summer associate", "graduate analyst",
                       "graduate associate", "graduate programme", "graduate program",
                       "rotation program", "rotational program", "trainee", "werkstudent"],
    "leadership":     ["led ", "managed ", "president", "vice president", "founder",
                       "director", "head of", "captain", "chair", "organis"],
    "case_prep":      ["case", "consulting club", "case team", "competition", "hackathon"],
    "extracurricular":["club", "society", "association", "volunteer", "committee"],
}

# Keywords that signal field-specific experience for each career path
CAREER_EXPERIENCE_KEYWORDS = {
    "consulting": [
        "consulting", "consultant", "mckinsey", "bcg", "bain", "deloitte",
        "accenture", "strategy&", "roland berger", "oliver wyman", "kpmg",
        "pwc", "ey ", "ernst & young", "advisory", "horvath", "ey-parthenon",
        "management consulting", "strategy consulting", "strategy project",
        "strategic recommendation", "case team",
    ],
    "investment_banking": [
        "investment banking", "investment bank", "goldman sachs", "jpmorgan",
        "jp morgan", "morgan stanley", "barclays", "ubs", "credit suisse",
        "deutsche bank", "citi", "citigroup", "rothschild", "lazard",
        "jefferies", "nomura", "hsbc", "bnp paribas", "societe generale",
        "m&a", "mergers and acquisitions", "debt capital", "equity capital",
        "ipo", "financial modelling", "financial modeling", "lbo",
        "leveraged buyout", "dcf", "leveraged finance", "pitchbook",
        "deal execution", "transaction", "capital markets",
    ],
    "tech": [
        "google", "microsoft", "amazon", "meta", "apple", "netflix",
        "software engineer", "software developer", "product manager",
        "data scientist", "machine learning", "artificial intelligence",
        "engineering", "developer", "programmer", "coding", "tech company",
        "saas", "fintech platform", "e-commerce platform", "product owner",
    ],
    "entrepreneurship": [
        "founder", "co-founder", "cofounder", "bootstrapped", "entrepreneur",
        "startup", "raised funding", "seed round", "pitch", "mvp",
        "product launch", "own business", "own company", "revenue in",
    ],
    "marketing": [
        "marketing", "brand manager", "brand specialist", "brand intern",
        "brand coordinator", "brand analyst", "brand assistant",
        "digital marketing", "social media manager", "social media",
        "campaign manager", "campaign", "advertising", "content strategy",
        "content marketing", "growth marketing", "performance marketing",
        "seo", "sem", "crm manager", "brand strategy", "consumer insights",
        "market research", "media planning", "marketing intern",
        "fmcg", "consumer goods", "unilever", "l'oreal", "loreal",
        "p&g", "procter", "lvmh", "nestle", "henkel", "beiersdorf",
        "noma marketing", "marketing consulting",
    ],
    "sustainability": [
        "sustainability", "esg", "climate", "environmental", "renewable energy",
        "green", "impact investing", "circular economy", "carbon", "net zero",
        "social impact", "csr", "corporate responsibility", "sustainable",
        "impact fund", "green finance",
    ],
}

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


def _load_courses_csv():
    """Load courses CSV — skips the title row so real column headers are used."""
    import io
    rows = []
    try:
        for enc in ("utf-8-sig", "utf-8", "latin-1"):
            try:
                with open(COURSES_CSV, encoding=enc) as f:
                    lines = f.readlines()
                break
            except UnicodeDecodeError:
                continue
        # The first line is a title row; the second is the real header
        content = "".join(lines[1:])
        reader  = csv.DictReader(io.StringIO(content), delimiter=";")
        for row in reader:
            rows.append({k.strip(): (v or "").strip() for k, v in row.items() if k and k.strip()})
    except Exception:
        pass
    return rows


def _gpa_meets_threshold(text: str, career_key: str) -> bool:
    """True if the CV mentions a GPA that meets the path-specific minimum.

    Thresholds reflect the labels shown in the UI:
      consulting 16/20, investment_banking 17/20, marketing 16/20,
      tech / entrepreneurship / sustainability 14/20 (rigour signal only).

    Latin honors / first-class always count, regardless of path.
    """
    THRESHOLDS_20 = {
        "consulting":         16.0,
        "investment_banking": 17.0,
        "tech":               14.0,
        "entrepreneurship":   14.0,
        "marketing":          16.0,
        "sustainability":     14.0,
    }
    # ~equivalent US 4-scale thresholds
    THRESHOLDS_4 = {
        "consulting":         3.5,
        "investment_banking": 3.7,
        "tech":               3.0,
        "entrepreneurship":   3.0,
        "marketing":          3.5,
        "sustainability":     3.0,
    }
    threshold_20 = THRESHOLDS_20.get(career_key, 14.0)
    threshold_4  = THRESHOLDS_4.get(career_key, 3.0)

    text_lower = text.lower()

    # Latin honors / UK first-class always pass (signal top performance)
    honors = [
        r"\bsumma\s+cum\s+laude\b",
        r"\bmagna\s+cum\s+laude\b",
        r"\bcum\s+laude\b",
        r"\bfirst[-\s]class\s+honou?rs?\b",
        r"\bwith\s+distinction\b",
    ]
    if any(re.search(p, text_lower) for p in honors):
        return True

    # Portuguese 20-scale: X/20 or X,Y/20 or X.Y/20
    for m in re.finditer(r"\b(\d{1,2})(?:[,.](\d+))?\s*/\s*20\b", text_lower):
        whole = int(m.group(1))
        frac_str = m.group(2) or ""
        frac = int(frac_str) / (10 ** len(frac_str)) if frac_str else 0.0
        value = whole + frac
        if 0 < value <= 20 and value >= threshold_20:
            return True

    # US 4-scale: X.Y/4 or X.Y/4.0
    for m in re.finditer(r"\b(\d)[,.](\d+)\s*/\s*4(?:\.0)?\b", text_lower):
        whole = int(m.group(1))
        frac_str = m.group(2)
        frac = int(frac_str) / (10 ** len(frac_str))
        value = whole + frac
        if value >= threshold_4:
            return True

    return False


def _check_criteria(cv_text, career_key=""):
    text        = cv_text.lower()
    first_lines = text[:800]

    is_foreign = any(nat in first_lines for nat in FOREIGN_NATIONALITIES)
    has_abroad = any(kw in text for kw in ABROAD_KEYWORDS)

    met = {}
    for crit, patterns in EMPLOYER_CRITERIA.items():
        met[crit] = any(
            bool(re.search(p, text, re.IGNORECASE)) if p.startswith(r"\b") else p in text
            for p in patterns
        )
    met["international"] = is_foreign or has_abroad
    met["gpa"]           = _gpa_meets_threshold(cv_text, career_key)

    # Career-specific experience: does the CV show field-relevant roles/employers?
    exp_kws = CAREER_EXPERIENCE_KEYWORDS.get(career_key, [])
    met["relevant_experience"] = any(kw in text for kw in exp_kws) if exp_kws else True

    return met


def _filter_courses(career_key):
    keywords = COURSE_KEYWORDS.get(career_key, [])
    rows     = _load_courses_csv()
    scored   = []
    for r in rows:
        if r.get("Type", "").strip() != "Elective":
            continue
        name  = r.get("Course Name", "").lower()
        if not name:
            continue
        score = sum(1 for kw in keywords if kw in name)
        if score > 0:
            scored.append((score, r))
    scored.sort(key=lambda x: -x[0])
    # Deduplicate by course name (same course in multiple periods)
    seen, result = set(), []
    for _, r in scored:
        n = r.get("Course Name", "")
        if n not in seen:
            seen.add(n)
            result.append(r)
        if len(result) >= 6:
            break
    return result


def _filter_clubs(career_key, limit=5):
    primary, secondary = [], []
    for club in _get_all_clubs():
        relevance = [r.strip() for r in club.get("Career Relevance", "").split(",")]
        if career_key not in relevance:
            continue
        entry = {
            "name":  club.get("Club Name", ""),
            "focus": club.get("Category", ""),
            "why":   club.get("Description", ""),
        }
        if relevance[0] == career_key:
            primary.append(entry)
        else:
            secondary.append(entry)
    combined = primary + secondary
    return combined[:limit]


def _filter_alumni(career_key, limit=5):
    industry = INDUSTRY_MAP.get(career_key, "")
    alt = "finance" if career_key == "investment_banking" else ""
    rows = _load_csv(ALUMNI_CSV)
    candidates = [
        r for r in rows
        if industry.lower() in r.get("Industry", "").lower()
        or (alt and alt in r.get("Industry", "").lower())
    ]
    # Pick one alumni per company first, then fill remaining slots
    seen_companies, result = set(), []
    for r in candidates:
        company = r.get("Company", "").strip()
        if company not in seen_companies:
            seen_companies.add(company)
            result.append(r)
        if len(result) >= limit:
            break
    # Fill up to limit if not enough unique companies
    if len(result) < limit:
        for r in candidates:
            if r not in result:
                result.append(r)
            if len(result) >= limit:
                break
    return result


_EMPLOYER_META = {
    "consulting": {
        "criteria": "GPA above 16, case interview skills, consulting internship, leadership role",
        "timing":   "6–12 months before start date (rolling for some firms)",
        "reqs":     "Case prep, extracurricular leadership, international experience recommended",
    },
    "investment_banking": {
        "criteria": "GPA above 17, financial modelling skills, IB or finance internship, attention to detail",
        "timing":   "9–12 months before start date — most deadlines in September–November",
        "reqs":     "Finance internship, Excel/modelling skills, strong GPA, networking events",
    },
    "tech": {
        "criteria": "Technical skills (coding/data/product), project portfolio, analytical thinking",
        "timing":   "Rolling basis — apply 3–6 months before desired start date",
        "reqs":     "Relevant internship or project, technical skills, curiosity and initiative",
    },
    "entrepreneurship": {
        "criteria": "Own venture or startup experience, leadership, execution ability, network",
        "timing":   "Rolling basis — accelerators and incubators have specific cohort deadlines",
        "reqs":     "Business idea or venture, proof of execution, pitch deck or prototype",
    },
    "marketing": {
        "criteria": "Marketing or brand internship, creative campaigns, digital skills (SEO/analytics)",
        "timing":   "6–9 months before start date for large FMCG firms; rolling for agencies",
        "reqs":     "Marketing internship, creative portfolio, data-driven mindset",
    },
    "sustainability": {
        "criteria": "ESG or sustainability experience, analytical skills, values alignment",
        "timing":   "Rolling basis — NGOs and impact funds recruit year-round",
        "reqs":     "Relevant internship or volunteer work, academic knowledge of ESG frameworks",
    },
}

def _club_names_lower():
    """Return a set of all Nova SBE club names in lowercase for employer filtering."""
    names = set()
    for club in _get_all_clubs():
        name = club.get("Club Name", "").strip().lower()
        if name:
            names.add(name)
    return names

def _is_valid_employer(company: str, club_names: set) -> bool:
    """Return False for student clubs, stealth/unnamed startups, or empty names."""
    c = company.strip().lower()
    if not c:
        return False
    if c in club_names:
        return False
    # Generic non-employer placeholders
    if c in ("stealth startup", "stealth", "self-employed", "freelance", "n/a", "-"):
        return False
    return True

def _filter_employers(career_key):
    industry = INDUSTRY_MAP.get(career_key, "")
    rows     = _load_csv(EMPLOYER_CSV)
    csv_results = [r for r in rows if industry.lower() in r.get("Category", "").lower()][:5]
    if csv_results:
        return csv_results

    # Fall back to companies extracted from ALL alumni for this path (no limit)
    meta       = _EMPLOYER_META.get(career_key, {})
    alt        = "finance" if career_key == "investment_banking" else ""
    club_names = _club_names_lower()
    all_alumni = [
        r for r in _load_csv(ALUMNI_CSV)
        if industry.lower() in r.get("Industry", "").lower()
        or (alt and alt in r.get("Industry", "").lower())
    ]
    seen, results = set(), []
    for a in all_alumni:
        company = a.get("Company", "").strip()
        if company not in seen and _is_valid_employer(company, club_names):
            seen.add(company)
            results.append({
                "Company":               company,
                "Key Evaluation Criteria": meta.get("criteria", ""),
                "Application Timing":    meta.get("timing", ""),
                "Typical Requirements":  meta.get("reqs", ""),
            })
    return results[:5]


def _build_strengths(cv_result, criteria_met, career_key):
    imp   = cv_result.get("impact", {})
    brev  = cv_result.get("brevity", {})
    strengths = []

    av_score  = imp.get("action_verbs", {}).get("score", 0)
    qi_lines  = imp.get("quantifying_impact", {}).get("quantified_lines", 0)
    ln_score  = brev.get("length", {}).get("score", 0)

    if criteria_met.get("relevant_experience"):
        industry = INDUSTRY_MAP.get(career_key, career_key)
        strengths.append(f"Relevant {industry} experience detected — you have direct field exposure, which is the #1 screening criterion at top firms.")
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


_EXPERIENCE_GAP = {
    "consulting":         "No consulting experience detected — MBB and strategy firms screen heavily for advisory experience. A consulting internship or case team involvement is the single most important CV signal.",
    "investment_banking": "No finance or IB experience detected — banks filter almost exclusively by prior finance internships. Add any financial modelling, valuation, or IB internship experience to your CV.",
    "tech":               "No tech experience or project portfolio detected — employers expect a GitHub repo, Kaggle entry, hackathon, or technical internship. Add any hands-on technical work.",
    "entrepreneurship":   "No venture or startup activity detected — even a small side project, freelance client, or pitch competition shows the execution mindset that matters most here.",
    "marketing":          "No brand or campaign experience detected — add a social media project, FMCG internship, brand competition, or digital marketing certificate to your CV.",
    "sustainability":     "No ESG or sustainability experience detected — a sustainability internship, thesis on ESG topics, or volunteer role in an impact org is the primary screening signal.",
}

_PATH_EXTRA_GAP = {
    "consulting":         (lambda c: not c.get("case_prep"),
                           "No case competition or consulting club found — MBB firms weight this heavily. Join Nova Case Team or enter a case competition this semester."),
    "investment_banking": (lambda c: not c.get("internship"),
                           "No finance internship detected — even a non-IB finance role (audit, FP&A, corporate finance) counts and significantly improves your application."),
    "tech":               (lambda c: not c.get("extracurricular"),
                           "No coding club, hackathon, or tech competition found — these are a fast signal of genuine technical passion beyond coursework."),
    "entrepreneurship":   (lambda c: not c.get("leadership"),
                           "No initiative ownership found — explicitly name any project where you were in charge, not just a contributor."),
    "marketing":          (lambda c: not c.get("extracurricular"),
                           "No marketing club or creative project found — NOMA Marketing Consulting or a brand case competition would directly strengthen your profile."),
    "sustainability":     (lambda c: not c.get("extracurricular"),
                           "No sustainability club or volunteer work found — Oikos Lisbon or Leadership for Impact are strong signals for ESG employers."),
}


def _build_gaps(cv_result, criteria_met, career_key):
    imp  = cv_result.get("impact", {})
    kw   = cv_result.get("keywords", {})
    gaps = []

    # Relevant experience — path-specific message
    if not criteria_met.get("relevant_experience"):
        gaps.append(_EXPERIENCE_GAP.get(
            career_key,
            f"No {INDUSTRY_MAP.get(career_key, career_key)}-specific experience detected — "
            "employers screen heavily for prior field exposure before inviting to interviews."
        ))

    qi_lines = imp.get("quantifying_impact", {}).get("quantified_lines", 0)
    if qi_lines < 2:
        gaps.append("Add numbers to your bullets — firms in this field expect quantified achievements (team size, % impact, revenue, event attendance).")
    if not criteria_met.get("internship"):
        gaps.append("No internship detected — most target employers require at least 1 relevant internship before applying.")
    if not criteria_met.get("leadership"):
        gaps.append("Leadership is a key screening criterion — highlight any role where you led people or took ownership.")

    # Path-specific extra gap (different criterion per path)
    check_fn, message = _PATH_EXTRA_GAP.get(career_key, (lambda c: False, ""))
    if check_fn(criteria_met) and message not in gaps:
        gaps.append(message)

    if not criteria_met.get("international"):
        gaps.append("International experience is preferred — an exchange semester or internship abroad strengthens your profile significantly.")
    missing_kw = kw.get("missing", [])[:3]
    if kw.get("ratio", 1) < 0.4 and missing_kw:
        gaps.append(f"Missing industry keywords — add these naturally: {', '.join(missing_kw)}.")
    return gaps[:5]


def _readiness_score(cv_result, criteria_met, career_key=""):
    cv_pct = cv_result.get("overall_pct", 50)
    weights = {
        "relevant_experience": 35,
        "internship":          20,
        "leadership":          15,
        "international":       10,
        "extracurricular":      8,
        "gpa":                  5,
    }
    # case_prep only counts for consulting — irrelevant for other paths
    if career_key == "consulting":
        weights["case_prep"] = 7
    criteria_score = sum(w for k, w in weights.items() if criteria_met.get(k))
    return min(100, max(0, round(cv_pct * 0.35 + criteria_score * 0.65)))


def _quick_win(cv_result, criteria_met, career_key):
    industry = INDUSTRY_MAP.get(career_key, career_key)
    qi = cv_result.get("impact", {}).get("quantifying_impact", {}).get("quantified_lines", 0)

    if not criteria_met.get("relevant_experience"):
        return (
            f"Secure a {industry}-specific internship or project as your top priority — "
            f"without field-relevant experience, your application will face major screening barriers "
            f"regardless of your CV quality or grades."
        )
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
    from gemini_ai import generate_alumni, generate_employers, assess_career_readiness

    criteria_met = _check_criteria(cv_text, career_key)

    # Career readiness score — try Gemini first, fall back to rule-based
    gemini_readiness = assess_career_readiness(
        cv_text, career_key, cv_result.get("overall_pct", 50), criteria_met
    )
    if gemini_readiness:
        score        = gemini_readiness["score"]
        score_ai     = True
        score_explanation = gemini_readiness.get("explanation", "")
    else:
        score        = _readiness_score(cv_result, criteria_met, career_key)
        score_ai     = False
        score_explanation = ""

    alumni = _filter_alumni(career_key)
    alumni_ai = False
    if not alumni:
        ai = generate_alumni(career_key)
        if ai:
            alumni = ai
            alumni_ai = True

    employers = _filter_employers(career_key)
    employers_ai = False
    if not employers:
        ai = generate_employers(career_key)
        if ai:
            employers = ai
            employers_ai = True

    return {
        "score":             score,
        "score_ai":          score_ai,
        "score_explanation": score_explanation,
        "strengths":    _build_strengths(cv_result, criteria_met, career_key),
        "gaps":         _build_gaps(cv_result, criteria_met, career_key),
        "courses":      _filter_courses(career_key),
        "clubs":        _filter_clubs(career_key),
        "alumni":       alumni,
        "alumni_ai":    alumni_ai,
        "employers":    employers,
        "employers_ai": employers_ai,
        "criteria_met": criteria_met,
        "quick_win":    _quick_win(cv_result, criteria_met, career_key),
    }
