# cv_keywords.py — Nova Career Path Simulator
# Keyword database for CV scoring per career path

# ---------------------------------------------------------------------------
# CAREER KEYWORDS
# Words and phrases recruiters / ATS systems look for in CVs.
# Matched case-insensitively against the CV text.
# ---------------------------------------------------------------------------

CAREER_KEYWORDS = {
    "consulting": [
        "consulting", "consultant", "strategy", "case", "client",
        "stakeholder", "framework", "analysis", "analytical", "insight",
        "recommendation", "mckinsey", "bcg", "bain", "deloitte", "roland berger",
        "oliver wyman", "problem solving", "structured", "presentation",
        "powerpoint", "excel", "project management", "due diligence",
        "business case", "kpi", "benchmark", "deliverable",
    ],
    "investment_banking": [
        "financial modelling", "financial modeling", "valuation", "dcf",
        "m&a", "mergers", "acquisitions", "lbo", "ebitda", "pitch book",
        "bloomberg", "capital markets", "equity", "debt", "ipo",
        "investment banking", "deal", "transaction", "cfa",
        "excel", "vba", "financial analysis", "due diligence",
        "goldman sachs", "jp morgan", "morgan stanley", "bnp paribas",
        "private equity", "hedge fund", "asset management",
    ],
    "tech": [
        "python", "sql", "java", "javascript", "react", "api",
        "agile", "scrum", "product management", "roadmap",
        "a/b testing", "data analysis", "machine learning", "analytics",
        "kpi", "user stories", "sprint", "dashboard", "tableau",
        "google analytics", "data-driven", "growth", "startup",
        "saas", "b2b", "b2c", "conversion", "retention", "funnel",
    ],
    "entrepreneurship": [
        "startup", "venture", "founder", "co-founder", "mvp",
        "business model", "pitch", "fundraising", "investor", "seed",
        "series a", "growth", "lean", "b2b", "b2c", "go-to-market",
        "traction", "scaling", "revenue", "churn", "product-market fit",
        "accelerator", "incubator", "y combinator", "beta-i",
        "innovation", "entrepreneurship",
    ],
    "marketing": [
        "brand", "campaign", "seo", "sem", "digital marketing",
        "social media", "content strategy", "crm", "analytics",
        "consumer insights", "roi", "kpi", "segmentation",
        "a/b testing", "conversion", "email marketing", "influencer",
        "brand management", "market research", "fmcg", "go-to-market",
        "unilever", "p&g", "loreal", "l'oréal", "nestlé",
        "advertising", "copywriting", "brand equity",
    ],
    "sustainability": [
        "esg", "sustainability", "impact", "csr", "carbon",
        "carbon footprint", "net zero", "climate", "circular economy",
        "reporting", "gri", "sdg", "un", "ngos", "ngo",
        "stakeholder engagement", "policy", "development",
        "environmental", "social impact", "responsible",
        "world bank", "european commission", "edp", "renewable",
        "green finance", "impact investing",
    ],
}

# ---------------------------------------------------------------------------
# BAD BUZZWORDS
# Overused phrases that recruiters dislike and ATS systems ignore.
# ---------------------------------------------------------------------------

BAD_BUZZWORDS = [
    "team player",
    "hardworking",
    "hard working",
    "passionate",
    "motivated",
    "results-driven",
    "results driven",
    "go-getter",
    "detail-oriented",
    "detail oriented",
    "self-starter",
    "self starter",
    "dynamic",
    "synergy",
    "outside the box",
    "thought leader",
    "guru",
    "ninja",
    "rockstar",
    "rock star",
    "proactive",
    "fast learner",
    "quick learner",
    "multitasker",
    "multi-tasker",
    "people person",
    "driven individual",
    "seasoned professional",
]

# ---------------------------------------------------------------------------
# STRUCTURE SECTIONS
# Words that signal a well-structured CV.
# ---------------------------------------------------------------------------

EXPECTED_SECTIONS = [
    "education",
    "experience",
    "skills",
    "languages",
    "activities",
    "extracurricular",
    "certifications",
    "volunteering",
    "projects",
    "achievements",
    "awards",
    "publications",
    "references",
]
