# cv_score.py — Nova Career Path Simulator
# Multi-dimensional CV scoring — student-friendly version
#   Impact   (40 pts) → Quantifying Impact, Action Verbs, Accomplishments, Repetition
#   Brevity  (30 pts) → Length, Filler Words, Bullet Count, Bullet Length
#   Style    (30 pts) → Sections, Personal Pronouns, Buzzwords, Active Voice, Date Order
#
# Scoring is calibrated for students (not professionals):
#   - Internships, uni projects and society roles count as real experience
#   - Thresholds are lower to reflect limited work history
#   - Highlights are phrased as encouragement, not criticism

import re
import pdfplumber
from collections import Counter
from cv_keywords import CAREER_KEYWORDS, BAD_BUZZWORDS, EXPECTED_SECTIONS


# ---------------------------------------------------------------------------
# ACTION VERBS — strong vs. weak
# ---------------------------------------------------------------------------

STRONG_ACTION_VERBS = [
    # Leadership / Management
    "led", "managed", "directed", "oversaw", "spearheaded", "championed",
    "orchestrated", "supervised", "mentored", "coached",
    # Achievement / Results
    "achieved", "delivered", "exceeded", "surpassed", "outperformed",
    "generated", "grew", "increased", "reduced", "saved", "cut", "doubled",
    "tripled", "improved", "boosted", "accelerated",
    # Building / Creating
    "built", "created", "launched", "developed", "designed", "established",
    "founded", "implemented", "introduced", "initiated", "pioneered",
    "architected", "engineered",
    # Analysis / Strategy
    "analysed", "analyzed", "evaluated", "assessed", "identified",
    "researched", "diagnosed", "optimised", "optimized", "streamlined",
    "restructured", "revamped", "transformed",
    # Collaboration / Influence
    "collaborated", "partnered", "negotiated", "persuaded", "presented",
    "facilitated", "coordinated", "liaised",
    # Student-relevant extras
    "organised", "organized", "volunteered", "represented", "competed",
    "published", "awarded", "selected", "trained", "tutored",
]

WEAK_ACTION_VERBS = [
    "worked", "helped", "assisted", "supported", "responsible for",
    "involved in", "participated in", "took part in", "attended",
    "contributed to", "dealt with",
    "handled", "carried out", "worked on", "was part of",
    "was involved", "tasked with", "duties included",
]

# ---------------------------------------------------------------------------
# ACTION VERB LIBRARY — categorised for browsing
# ---------------------------------------------------------------------------

ACTION_VERB_CATEGORIES = {
    "Strong Accomplishment-Driven Verbs": [
        "Accelerated", "Achieved", "Attained", "Completed", "Conceived",
        "Convinced", "Discovered", "Doubled", "Effected", "Eliminated",
        "Expanded", "Expedited", "Founded", "Improved", "Increased",
        "Initiated", "Innovated", "Introduced", "Invented", "Launched",
        "Mastered", "Overcame", "Overhauled", "Pioneered", "Reduced",
        "Resolved", "Revitalised", "Spearheaded", "Strengthened",
        "Transformed", "Upgraded", "Tripled",
    ],
    "Communication Skills": [
        "Addressed", "Advised", "Arranged", "Authored", "Co-authored",
        "Co-ordinated", "Communicated", "Corresponded", "Counselled",
        "Demonstrated", "Developed", "Directed", "Drafted", "Enlisted",
        "Facilitated", "Formulated", "Guided", "Influenced", "Instructed",
        "Interpreted", "Interviewed", "Lectured", "Led", "Liaised",
        "Mediated", "Moderated", "Motivated", "Negotiated", "Persuaded",
        "Presented", "Promoted", "Proposed", "Publicised", "Recommended",
        "Reconciled", "Recruited", "Resolved", "Taught", "Trained",
        "Translated",
    ],
    "Entrepreneurial Skills": [
        "Composed", "Conceived", "Created", "Designed", "Developed",
        "Devised", "Established", "Founded", "Generated", "Implemented",
        "Initiated", "Instituted", "Introduced", "Launched", "Led",
        "Opened", "Originated", "Pioneered", "Planned", "Prepared",
        "Produced", "Promoted", "Released", "Started",
    ],
    "Management Skills": [
        "Administered", "Analysed", "Assigned", "Chaired", "Consolidated",
        "Contracted", "Co-ordinated", "Delegated", "Developed", "Directed",
        "Evaluated", "Executed", "Guided", "Managed", "Organised",
        "Oversaw", "Planned", "Prioritised", "Produced", "Recommended",
        "Reorganised", "Reviewed", "Scheduled", "Supervised",
    ],
    "Leadership, Mentorship and Teaching Skills": [
        "Accelerated", "Achieved", "Adapted", "Advised", "Allocated",
        "Assessed", "Authored", "Clarified", "Coached", "Conducted",
        "Coordinated", "Counseled", "Demonstrated", "Developed",
        "Diagnosed", "Directed", "Educated", "Enabled", "Encouraged",
        "Evaluated", "Explained", "Facilitated", "Familiarised",
        "Guided", "Illustrated", "Informed", "Instructed", "Lectured",
        "Led", "Managed", "Mentored", "Moderated", "Motivated",
        "Organised", "Participated", "Performed", "Persuaded",
        "Presented", "Provided", "Referred", "Rehabilitated",
        "Reinforced", "Represented", "Revamped", "Spearheaded",
        "Stimulated", "Taught", "Trained", "Verified",
        "Accompanied", "Acquired",
    ],
    "Research and Analysis Skills": [
        "Analysed", "Assessed", "Clarified", "Classified", "Collected",
        "Collated", "Critiqued", "Defined", "Designed", "Devised",
        "Diagnosed", "Established", "Evaluated", "Examined", "Extracted",
        "Forecasted", "Identified", "Inspected", "Interpreted",
        "Interviewed", "Investigated", "Organised", "Researched",
        "Reviewed", "Summarised", "Surveyed", "Systemised", "Tested",
        "Traced", "Uncovered", "Verified",
    ],
    "Problem Solving Skills": [
        "Arranged", "Budgeted", "Composed", "Conceived", "Conducted",
        "Controlled", "Co-ordinated", "Eliminated", "Examined",
        "Improved", "Investigated", "Itemised", "Modernised", "Operated",
        "Organised", "Planned", "Prepared", "Processed", "Produced",
        "Redesigned", "Reduced", "Refined", "Researched", "Resolved",
        "Reviewed", "Revised", "Revamped", "Scheduled", "Simplified",
        "Solved", "Streamlined", "Transformed",
    ],
    "Process Improvement, Consulting and Operations": [
        "Broadened", "Combined", "Consolidated", "Converted", "Cut",
        "Decreased", "Developed", "Devised", "Doubled", "Eliminated",
        "Expanded", "Improved", "Increased", "Innovated", "Minimised",
        "Modernised", "Recommended", "Redesigned", "Reduced", "Refined",
        "Reorganised", "Resolved", "Restructured", "Revised", "Revamped",
        "Saved", "Serviced", "Simplified", "Solved", "Streamlined",
        "Strengthened", "Transformed", "Trimmed", "Tripled", "Unified",
        "Widened",
    ],
    "Financial Skills": [
        "Administered", "Allocated", "Analysed", "Appraised", "Audited",
        "Balanced", "Budgeted", "Calculated", "Computed", "Developed",
        "Managed", "Modelled", "Planned", "Projected", "Researched",
        "Restructured",
    ],
    "Design and Creative Skills": [
        "Acted", "Conceptualised", "Created", "Customised", "Designed",
        "Developed", "Directed", "Established", "Fashioned", "Illustrated",
        "Instituted", "Integrated", "Performed", "Planned", "Proved",
        "Redesigned", "Revised", "Revitalised", "Set up", "Shaped",
        "Streamlined", "Structured", "Tabulated", "Validated",
    ],
    "Clerical or Detail-Oriented Skills": [
        "Approved", "Arranged", "Catalogued", "Classified", "Collected",
        "Compiled", "Dispatched", "Executed", "Filed", "Generated",
        "Implemented", "Inspected", "Monitored", "Operated", "Ordered",
        "Organised", "Prepared", "Processed", "Purchased", "Recorded",
        "Retrieved", "Screened", "Specified", "Systematised",
    ],
}

# Extend the scoring list with every verb in the browse library
_lib_verbs = {v.lower() for vlist in ACTION_VERB_CATEGORIES.values() for v in vlist}
STRONG_ACTION_VERBS = sorted(set(STRONG_ACTION_VERBS) | _lib_verbs)

# ---------------------------------------------------------------------------
# FILLER WORDS
# ---------------------------------------------------------------------------

FILLER_WORDS = [
    "various", "several", "numerous", "a number of", "a variety of",
    "in order to", "due to the fact that", "for the purpose of",
    "with regard to", "in terms of", "on a daily basis",
    "and so on", "and so forth", "etc.", "basically", "essentially",
    "generally speaking", "needless to say",
]

# ---------------------------------------------------------------------------
# PERSONAL PRONOUNS
# ---------------------------------------------------------------------------

PERSONAL_PRONOUNS = [
    r"\bi\b", r"\bme\b", r"\bmy\b", r"\bmine\b", r"\bmyself\b",
    r"\bwe\b", r"\bour\b", r"\bours\b", r"\bourselves\b",
]

# ---------------------------------------------------------------------------
# PASSIVE VOICE
# ---------------------------------------------------------------------------

PASSIVE_INDICATORS = [
    r"\bwas\s+\w+ed\b", r"\bwere\s+\w+ed\b", r"\bbeen\s+\w+ed\b",
    r"\bwas\s+\w+en\b", r"\bwere\s+\w+en\b",
    r"\bis\s+\w+ed\b",  r"\bare\s+\w+ed\b",
]

# ---------------------------------------------------------------------------
# QUANTIFICATION PATTERNS
# ---------------------------------------------------------------------------

QUANTIFICATION_PATTERNS = [
    r"\d+\s*%",
    r"[£$€]\s*\d[\d,\.]*[kKmMbB]?",
    r"\d[\d,\.]*\s*[kKmMbB]\b",
    r"\b\d+\s*x\b",
    r"\b(increased|reduced|grew|saved|cut|boosted|improved)\s+by\s+\d",
    r"\bteam of\s+\d+",
    r"\d+\s*(people|members|students|clients|customers|projects|countries|markets|participants)",
    r"\btop\s+\d+",
    r"\bnumber\s+(1|one)\b",
    r"\b(first|second|third)\s+place\b",
    r"\b\d+\s*(hours|weeks|months)\b",
]

# ---------------------------------------------------------------------------
# DATE FORMATS
# ---------------------------------------------------------------------------

DATE_PATTERNS = {
    "month_year_long":  r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b",
    "month_year_short": r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s+\d{4}\b",
    "mm_yyyy":          r"\b(0?[1-9]|1[0-2])/\d{4}\b",
    "yyyy":             r"\b(20[0-9]{2}|19[0-9]{2})\b",
}

# ---------------------------------------------------------------------------
# ACCOMPLISHMENT SIGNALS
# ---------------------------------------------------------------------------

ACCOMPLISHMENT_SIGNALS = [
    r"\bresult(ed|ing)?\b", r"\bachiev(ed|ing|ement)?\b",
    r"\bimpact(ed|ing)?\b", r"\boutcome\b", r"\bdelivered?\b",
    r"\brecognised?\b",     r"\bawarded?\b", r"\bwon\b",
    r"\bprize\b",           r"\baward\b",    r"\bhonour(ed)?\b",
    r"\bnominated?\b",      r"\brank(ed)?\b", r"\bselected?\b",
    r"\bscholarship\b",     r"\bfellowship\b", r"\bgrant\b",
    r"\bcompetition\b",     r"\bhackathon\b",
]

# ---------------------------------------------------------------------------
# STUDENT BENCHMARK — what an average strong student CV looks like
# Used to contextualise the score ("top X% of student CVs")
# ---------------------------------------------------------------------------

STUDENT_PERCENTILE_THRESHOLDS = [
    (90, "top 10%"),
    (75, "top 25%"),
    (50, "top 50%"),
    (25, "bottom 50%"),
    (0,  "bottom 25%"),
]

def _get_percentile_label(score: int) -> str:
    for threshold, label in STUDENT_PERCENTILE_THRESHOLDS:
        if score >= threshold:
            return label
    return "bottom 25%"


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def _strip_bullet(line: str) -> str:
    return re.sub(r'^[\•\-\–\▪\·\▸\►\■\●\○\◦\✓\*]+\s*', '', line)


# ---------------------------------------------------------------------------
# EXTRACT TEXT
# ---------------------------------------------------------------------------

def extract_text(pdf_file) -> str:
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


# ---------------------------------------------------------------------------
# DIMENSION SCORERS (each 0–10, student-calibrated)
# ---------------------------------------------------------------------------

def _score_quantifying_impact(text: str) -> dict:
    """
    Student calibration: even 1–2 quantified lines scores well.
    Only looks at content lines (not headers, names, contact info).
    A student with any numbers in their CV should score at least 5/10.
    """
    # Only consider longer lines that look like real content, not headers
    lines = [
        l.strip() for l in text.split("\n")
        if len(l.strip()) > 30 and not l.strip().isupper()
    ]
    quantified = sum(
        1 for line in lines
        if any(re.search(p, line) for p in QUANTIFICATION_PATTERNS)
    )
    # Absolute scoring: any quantified line gives at least 5/10
    if quantified == 0:
        score = 0
    elif quantified == 1:
        score = 5
    elif quantified == 2:
        score = 7
    else:
        ratio = quantified / max(len(lines), 1)
        score = min(10, max(7, round(ratio * 40)))
    return {"score": score, "quantified_lines": quantified, "total_lines": len(lines)}


def _score_action_verbs(text: str) -> dict:
    """
    Student calibration: ratio threshold lowered, score scaled more generously.
    """
    lines = [l.strip().lower() for l in text.split("\n") if len(l.strip()) > 15]
    strong_hits = sum(1 for line in lines if any(_strip_bullet(line).startswith(v) for v in STRONG_ACTION_VERBS))
    weak_hits   = sum(1 for line in lines if any(v in _strip_bullet(line)[:40] for v in WEAK_ACTION_VERBS))
    total        = max(strong_hits + weak_hits, 1)
    ratio        = strong_hits / total
    # Student calibration: 40%+ strong → full score (vs 80%+ for professionals)
    score = min(10, round(ratio * 16))
    return {"score": score, "strong": strong_hits, "weak": weak_hits}


def _score_accomplishments(text: str) -> dict:
    """
    Student calibration: 3+ signals → full score (vs 10 for professionals).
    """
    text_lower = text.lower()
    hits = sum(1 for p in ACCOMPLISHMENT_SIGNALS if re.search(p, text_lower))
    score = min(10, round(hits * 2.5))
    return {"score": score, "signals_found": hits}


def _score_repetition(text: str) -> dict:
    lines  = [l.strip().lower() for l in text.split("\n") if len(l.strip()) > 15]
    starts = [re.split(r"[\s,;]", _strip_bullet(l))[0] for l in lines if l]
    freq   = Counter(starts)
    repeats = sum(v - 1 for v in freq.values() if v > 3)  # student: allow up to 3 same starts
    score  = max(0, 10 - repeats * 2)
    return {"score": score, "repeated_starts": repeats}


def _score_length(word_count: int) -> dict:
    """Student CVs are typically 1 page = 300–700 words."""
    if 280 <= word_count <= 800:
        score = 10
    elif 200 <= word_count < 280 or 800 < word_count <= 1100:
        score = 8
    elif word_count < 200:
        score = 5
    else:
        score = 6
    return {"score": score, "word_count": word_count}


def _score_filler_words(text: str) -> dict:
    text_lower = text.lower()
    hits = [fw for fw in FILLER_WORDS if fw in text_lower]
    # Student calibration: allow up to 2 filler words before penalising
    score = max(0, 10 - max(0, len(hits) - 2))
    return {"score": score, "filler_found": hits}


def _score_bullet_count(text: str) -> dict:
    """Student CVs: 8–25 bullets is realistic."""
    bullets = re.findall(r"^[\•\-\–\▪]", text, re.MULTILINE)
    count = len(bullets)
    if 8 <= count <= 25:
        score = 10
    elif 5 <= count < 8 or 25 < count <= 35:
        score = 7
    elif count < 5:
        score = 5
    else:
        score = 6
    return {"score": score, "bullet_count": count}


def _score_bullet_length(text: str) -> dict:
    lines = [l.strip() for l in text.split("\n") if l.strip().startswith(("•", "-", "–", "▪"))]
    if not lines:
        return {"score": 7, "avg_bullet_words": 0}
    lengths = [len(l.split()) for l in lines]
    avg = sum(lengths) / len(lengths)
    if 8 <= avg <= 28:
        score = 10
    elif 5 <= avg < 8 or 28 < avg <= 35:
        score = 7
    else:
        score = 4
    return {"score": score, "avg_bullet_words": round(avg, 1)}


def _score_sections(text: str) -> dict:
    text_lower = text.lower()
    found   = [s for s in EXPECTED_SECTIONS if s in text_lower]
    missing = [s for s in EXPECTED_SECTIONS[:6] if s not in text_lower]
    score   = min(10, round(len(found) / max(len(EXPECTED_SECTIONS), 1) * 14))
    return {"score": score, "sections_found": found, "sections_missing": missing}


def _score_personal_pronouns(text: str) -> dict:
    hits = [p for p in PERSONAL_PRONOUNS if re.search(p, text, re.IGNORECASE)]
    # Student calibration: 1 pronoun is fine, penalise from 2+
    score = max(0, 10 - max(0, len(hits) - 1) * 3)
    return {"score": score, "pronouns_found": len(hits)}


def _score_buzzwords(text: str) -> dict:
    text_lower = text.lower()
    found = [bw for bw in BAD_BUZZWORDS if bw.lower() in text_lower]
    # Student calibration: allow 1 buzzword before penalising
    score = max(0, 10 - max(0, len(found) - 1) * 2)
    return {"score": score, "buzzwords_found": found}


def _score_active_voice(text: str) -> dict:
    passive_hits = sum(1 for p in PASSIVE_INDICATORS if re.search(p, text, re.IGNORECASE))
    # Student calibration: allow 1–2 passive phrases
    score = max(0, 10 - max(0, passive_hits - 1) * 2)
    return {"score": score, "passive_constructions": passive_hits}


def _score_date_consistency(text: str) -> dict:
    matches_per_format = {k: len(re.findall(v, text)) for k, v in DATE_PATTERNS.items()}
    used_formats = {k for k, v in matches_per_format.items() if v > 0}
    if len(used_formats) <= 1:
        score = 10
    elif len(used_formats) == 2:
        score = 7
    else:
        score = 4
    return {"score": score, "formats_detected": list(used_formats)}


def _score_career_keywords(text: str, career_key: str) -> dict:
    text_lower = text.lower()
    keywords = CAREER_KEYWORDS.get(career_key, [])
    found   = [kw for kw in keywords if kw.lower() in text_lower]
    missing = [kw for kw in keywords if kw.lower() not in text_lower]
    ratio   = len(found) / max(len(keywords), 1)
    return {"ratio": ratio, "found": found, "missing": missing[:10]}


# ---------------------------------------------------------------------------
# ENCOURAGEMENT MESSAGES — positive, student-friendly
# ---------------------------------------------------------------------------

def _build_highlights(av, qi, acc, fw, bw, pp, act, sec, kw, career_key) -> list:
    """
    Returns a list of actionable, encouraging tips.
    Phrased as 'quick wins' rather than failures.
    """
    tips = []

    if av["score"] < 6:
        tips.append("💡 Quick win: swap a few weak verbs like 'worked on' or 'helped' for power verbs like 'led', 'built' or 'delivered' — it makes a big difference!")
    elif av["score"] < 9:
        tips.append("✅ Good use of action verbs! Try replacing one or two remaining weak verbs to push this even higher.")

    if qi["quantified_lines"] == 0:
        tips.append("💡 Quick win: add at least one number to your CV — e.g. team size, % improvement or event attendance. Recruiters love specifics!")
    elif qi["quantified_lines"] < 3:
        tips.append(f"✅ Good — you already have {qi['quantified_lines']} line(s) with numbers. Adding one or two more will really strengthen your impact.")

    if acc["score"] < 5:
        tips.append("💡 Try rewriting one bullet point to show a result, not just a task. For example: 'Organised weekly meetings' → 'Organised weekly meetings for a 12-person team, improving coordination'.")

    if fw["score"] < 7:
        tips.append(f"💡 Remove a few filler words to make your writing sharper: {', '.join(fw['filler_found'][:4])}.")

    if bw["score"] < 7 and bw["buzzwords_found"]:
        tips.append(f"💡 Consider cutting these overused words — recruiters see them too often: {', '.join(bw['buzzwords_found'][:4])}.")

    if pp["score"] < 7:
        tips.append("💡 Remove personal pronouns (I, my, we) — CVs are written without them. Just start with the verb: 'Led a team of 5' instead of 'I led a team of 5'.")

    if act["score"] < 6:
        tips.append("💡 Try using active voice — instead of 'was responsible for organising', write 'organised'.")

    if sec["sections_missing"]:
        tips.append(f"💡 Consider adding these sections to make your CV more complete: {', '.join(sec['sections_missing'])}.")

    if len(kw["missing"]) > 6:
        tips.append(f"💡 Add a few {career_key}-relevant keywords naturally into your CV: {', '.join(kw['missing'][:4])}.")

    if not tips:
        tips.append("🌟 Your CV is looking really strong — you're well on your way to standing out!")

    return tips


# ---------------------------------------------------------------------------
# MAIN SCORING FUNCTION
# ---------------------------------------------------------------------------

def score_cv(pdf_file, career_key: str) -> dict:
    """
    Score a CV PDF with student-friendly, multi-dimensional analysis.

    Returns
    -------
    overall_pct    : int 0–100
    grade          : str  (A+ / A / B / C / D)
    percentile     : str  e.g. "top 25% of student CVs"
    encouragement  : str  motivational top-line message
    impact         : dict (score 0–40 + sub-scores)
    brevity        : dict (score 0–30 + sub-scores)
    style          : dict (score 0–30 + sub-scores)
    keywords       : dict (found / missing / ratio)
    highlights     : list[str]
    word_count     : int
    raw_text       : str
    """
    text       = extract_text(pdf_file)
    word_count = len(text.split())
    with pdfplumber.open(pdf_file) as _pdf:
        page_count = len(_pdf.pages)

    # ── IMPACT (40 pts) ──────────────────────────────────────────────────
    qi  = _score_quantifying_impact(text)
    av  = _score_action_verbs(text)
    acc = _score_accomplishments(text)
    rep = _score_repetition(text)

    impact_raw   = (qi["score"] + av["score"] + acc["score"] + rep["score"]) / 40
    impact_score = round(impact_raw * 40)

    # ── BREVITY (30 pts) ─────────────────────────────────────────────────
    ln  = _score_length(word_count)
    fw  = _score_filler_words(text)
    bc  = _score_bullet_count(text)
    bl  = _score_bullet_length(text)

    brevity_raw   = (ln["score"] + fw["score"] + bc["score"] + bl["score"]) / 40
    brevity_score = round(brevity_raw * 30)

    # ── STYLE (30 pts) ───────────────────────────────────────────────────
    sec = _score_sections(text)
    pp  = _score_personal_pronouns(text)
    bw  = _score_buzzwords(text)
    act = _score_active_voice(text)
    dat = _score_date_consistency(text)

    style_raw   = (sec["score"] + pp["score"] + bw["score"] + act["score"] + dat["score"]) / 50
    style_score = round(style_raw * 30)

    # ── CAREER KEYWORDS (display only — not included in score) ──────────
    kw = _score_career_keywords(text, career_key)

    # ── OVERALL ──────────────────────────────────────────────────────────
    overall_pct = max(0, min(100, impact_score + brevity_score + style_score))

    # Grade
    if overall_pct >= 85:
        grade = "A+"
    elif overall_pct >= 72:
        grade = "A"
    elif overall_pct >= 58:
        grade = "B"
    elif overall_pct >= 42:
        grade = "C"
    else:
        grade = "D"

    # Percentile label
    percentile = _get_percentile_label(overall_pct)

    # Encouragement message
    if overall_pct >= 80:
        encouragement = "🌟 Excellent CV! You're standing out from the crowd — a few small tweaks and this is recruiter-ready."
    elif overall_pct >= 65:
        encouragement = "👍 Solid CV! You have a great foundation — a couple of improvements will make it shine."
    elif overall_pct >= 50:
        encouragement = "💪 Good start! You're already doing a lot right. Focus on the quick wins below to level up."
    else:
        encouragement = "🚀 You're on the right track! Every CV is a work in progress — follow the tips below and you'll see a big improvement."

    # Highlights
    highlights = _build_highlights(av, qi, acc, fw, bw, pp, act, sec, kw, career_key)

    return {
        "overall_pct"  : overall_pct,
        "grade"        : grade,
        "percentile"   : percentile,
        "encouragement": encouragement,
        "impact": {
            "score"              : impact_score,
            "max"                : 40,
            "quantifying_impact" : qi,
            "action_verbs"       : av,
            "accomplishments"    : acc,
            "repetition"         : rep,
        },
        "brevity": {
            "score"        : brevity_score,
            "max"          : 30,
            "length"       : ln,
            "filler_words" : fw,
            "bullet_count" : bc,
            "bullet_length": bl,
        },
        "style": {
            "score"            : style_score,
            "max"              : 30,
            "sections"         : sec,
            "personal_pronouns": pp,
            "buzzwords"        : bw,
            "active_voice"     : act,
            "date_consistency" : dat,
        },
        "keywords"  : kw,
        "highlights": highlights,
        "word_count": word_count,
        "page_count": page_count,
        "raw_text"  : text,
    }