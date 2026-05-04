import csv
import re

import os as _os
_DIR = _os.path.dirname(_os.path.abspath(__file__))
ALUMNI_CSV   = _os.path.join(_DIR, "Alumni Research Database(Alumni Data).csv")
EMPLOYER_CSV = _os.path.join(_DIR, "Employer_Database_CV_Screening(Consulting).csv")
COURSES_CSV  = _os.path.join(_DIR, "nova_courses&clubs_database_v3(MNG).csv")

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

# Clubs at Nova SBE recommended per career path
CLUBS_BY_CAREER = {
    "consulting": [
        {"name": "Nova Case Team",
         "focus": "Case competitions & MBB prep",
         "why": "Directly listed by McKinsey, BCG, Bain as a top signal on student CVs. Provides real case training and competition experience."},
        {"name": "Nova SBE Social Consulting",
         "focus": "Real consulting projects for NGOs",
         "why": "Hands-on client projects, deliverables, and presentations — the same skills consulting firms test in interviews."},
        {"name": "Nova Entrepreneurs Club",
         "focus": "Strategy, pitching, business cases",
         "why": "Strong overlap with consulting skills — strategy thinking, structured problem-solving, and client communication."},
    ],
    "investment_banking": [
        {"name": "Nova Finance Club",
         "focus": "IB, equity research, valuation",
         "why": "The main pipeline to investment banking internships at Nova — most IB alumni at Goldman, JPMorgan and Rothschild came through this club."},
        {"name": "Nova Investment Group",
         "focus": "Portfolio management & stock pitches",
         "why": "Shows hands-on financial modelling and investment analysis — exactly what IB firms test in applications."},
        {"name": "Nova Fintech",
         "focus": "Digital finance & fintech ventures",
         "why": "Relevant for roles at digital banks, fintech arms of banks, and PE firms focused on tech-enabled financial services."},
    ],
    "tech": [
        {"name": "Nova Data Science Club",
         "focus": "Python, ML, data projects, hackathons",
         "why": "Practical technical portfolio — the fastest way to show coding and analytical skills to tech employers."},
        {"name": "Nova Fintech",
         "focus": "Tech in financial services & product",
         "why": "Bridges business and technology — relevant for product management and tech strategy roles."},
        {"name": "Nova Entrepreneurs Club",
         "focus": "Startup creation & tech products",
         "why": "Product thinking, MVP development, and startup mentality — valued at tech companies and scale-ups."},
    ],
    "entrepreneurship": [
        {"name": "Nova Entrepreneurs Club",
         "focus": "Startup creation, pitching, mentoring",
         "why": "The core entrepreneurship community at Nova — access to mentors, investors, and competitions."},
        {"name": "Nova Fintech",
         "focus": "Fintech ventures & digital products",
         "why": "Fintech is one of the most active startup sectors — builds relevant network and product experience."},
        {"name": "Nova SBE Social Consulting",
         "focus": "Social enterprise & impact projects",
         "why": "Experience managing real projects end-to-end as a student — directly signals execution ability."},
    ],
    "marketing": [
        {"name": "Nova Marketing Club",
         "focus": "Brand strategy, campaigns, FMCG",
         "why": "Top marketing community at Nova — direct connections to P&G, L'Oréal, Unilever, and leading agencies."},
        {"name": "Nova Entrepreneurs Club",
         "focus": "Growth marketing & brand building",
         "why": "Growth marketing for startups is a fast-growing career track — shows initiative and creative thinking."},
        {"name": "Nova Data Science Club",
         "focus": "Marketing analytics & data",
         "why": "Data-driven marketing is the fastest-growing segment — analytics skills set you apart from classic marketers."},
    ],
    "sustainability": [
        {"name": "Nova Sustainability Club",
         "focus": "ESG, climate, circular economy",
         "why": "The main sustainability network at Nova — connects to NGOs, ESG consultancies, and impact investment funds."},
        {"name": "Nova SBE Social Consulting",
         "focus": "Social impact consulting projects",
         "why": "Real client projects with social impact organizations — valued experience for ESG and impact roles."},
        {"name": "Nova Entrepreneurs Club",
         "focus": "Social entrepreneurship & ventures",
         "why": "Many sustainability careers involve starting or scaling impact ventures — this club bridges both worlds."},
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
        "marketing", "brand manager", "digital marketing", "social media manager",
        "campaign manager", "advertising", "content strategy", "seo", "sem",
        "crm manager", "brand strategy", "consumer insights", "market research",
        "media planning", "marketing intern",
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

    # Career-specific experience: does the CV show field-relevant roles/employers?
    exp_kws = CAREER_EXPERIENCE_KEYWORDS.get(career_key, [])
    met["relevant_experience"] = any(kw in text for kw in exp_kws) if exp_kws else True

    return met


def _filter_courses(career_key):
    keywords = COURSE_KEYWORDS.get(career_key, [])
    rows     = _load_courses_csv()
    scored   = []
    for r in rows:
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


def _filter_clubs(career_key):
    return CLUBS_BY_CAREER.get(career_key, [])


def _filter_alumni(career_key):
    industry = INDUSTRY_MAP.get(career_key, "")
    rows     = _load_csv(ALUMNI_CSV)
    return [r for r in rows if industry.lower() in r.get("Industry", "").lower()][:5]


def _filter_employers(career_key):
    industry = INDUSTRY_MAP.get(career_key, "")
    rows     = _load_csv(EMPLOYER_CSV)
    return [r for r in rows if industry.lower() in r.get("Category", "").lower()][:5]


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


def _build_gaps(cv_result, criteria_met, career_key):
    imp  = cv_result.get("impact", {})
    kw   = cv_result.get("keywords", {})
    gaps = []
    industry = INDUSTRY_MAP.get(career_key, career_key)

    # Relevant experience is the most critical gap — show it first
    if not criteria_met.get("relevant_experience"):
        gaps.append(
            f"No {industry}-specific experience detected — employers in this field screen heavily for prior field exposure. "
            f"A CV without a relevant internship or project will rarely pass the first round, regardless of overall quality."
        )

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
    missing_kw = kw.get("missing", [])[:3]
    if kw.get("ratio", 1) < 0.4 and missing_kw:
        gaps.append(f"Missing industry keywords — add these naturally: {', '.join(missing_kw)}.")
    return gaps[:5]


def _readiness_score(cv_result, criteria_met):
    cv_pct = cv_result.get("overall_pct", 50)
    # relevant_experience carries the most weight — no field exposure = major penalty
    weights = {
        "relevant_experience": 35,
        "internship":          20,
        "leadership":          15,
        "international":       10,
        "extracurricular":      8,
        "case_prep":            7,
        "gpa":                  5,
    }
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
    criteria_met = _check_criteria(cv_text, career_key)
    return {
        "score":        _readiness_score(cv_result, criteria_met),
        "strengths":    _build_strengths(cv_result, criteria_met, career_key),
        "gaps":         _build_gaps(cv_result, criteria_met, career_key),
        "courses":      _filter_courses(career_key),
        "clubs":        _filter_clubs(career_key),
        "alumni":       _filter_alumni(career_key),
        "employers":    _filter_employers(career_key),
        "criteria_met": criteria_met,
        "quick_win":    _quick_win(cv_result, criteria_met, career_key),
    }
