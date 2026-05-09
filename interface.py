import streamlit as st
import re
from logic import get_recommendations
from data import CAREER_PATHS
from cv_score import score_cv
from landing import landing_page, LANDING_CSS
from career_readiness_ai import analyze_career_readiness
from gemini_ai import enhance_cv_feedback

st.set_page_config(
    page_title="Nova · CV Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# McKINSEY-STYLE CSS — clean white, navy, sky blue
# =============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif !important; }

/* Restore Streamlit's icon font (Material Symbols Rounded) — prevents icon names showing as text */
details > summary > p,
details > summary > p:first-child,
details > summary span[data-testid],
[data-testid="stExpanderToggleIcon"],
.material-icons, [class*="material-icon"], [class*="MaterialIcon"],
[class*="symbol"], [class*="Symbol"] {
    font-family: 'Material Symbols Rounded', 'Material Icons',
                 'Material Icons Outlined' !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 3rem 2.5rem !important; max-width: 100% !important; }

/* ── Global white background for ALL pages ── */
.stApp { background: #F0F4F8 !important; }
section.main > div { background: #F0F4F8 !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0A1628 !important;
    border-right: 1px solid #1E3A5F;
}
/* Sidebar toggle button — always visible, even when collapsed */
button[data-testid="collapsedControl"],
div[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    background: #0A1628 !important;
    border: 1px solid #1E3A5F !important;
    border-radius: 0 8px 8px 0 !important;
    color: #A8C4E0 !important;
}
section[data-testid="stSidebar"] * { color: #A8C4E0 !important; }
section[data-testid="stSidebar"] .stMarkdown h2 {
    color: #FFFFFF !important; font-size: 18px !important;
    font-weight: 800 !important; letter-spacing: -0.3px;
}
section[data-testid="stSidebar"] .stMarkdown p { font-size: 11px !important; }
section[data-testid="stSidebar"] hr { border-color: #1E3A5F !important; }

/* Nav items — styled as plain text links */
.nav-section {
    font-size: 9px; font-weight: 700; letter-spacing: 1.5px;
    text-transform: uppercase; color: #3A6A9A;
    padding: 14px 0 4px 0; margin: 0;
}
.nav-item {
    display: flex; justify-content: space-between; align-items: center;
    padding: 7px 12px; margin: 1px 0; border-radius: 6px;
    cursor: pointer; transition: background 0.15s;
    font-size: 13px; color: #8AB0CC;
    border-left: 3px solid transparent;
}
.nav-item:hover { background: #112240; color: #E0F0FF; }
.nav-item.active {
    background: #112240; color: #60B0F0 !important;
    border-left-color: #60B0F0; font-weight: 600;
}
.nav-badge {
    font-size: 11px; font-weight: 700; padding: 2px 7px;
    border-radius: 10px; min-width: 24px; text-align: center;
}
.nb-green  { background: #0A3020; color: #4ADE80; }
.nb-yellow { background: #2A2010; color: #FBBF24; }
.nb-red    { background: #300A0A; color: #F87171; }

/* ── Main area ── */
.main-bg { background: #F7F9FC; }

/* ── Page header ── */
.page-header {
    background: linear-gradient(135deg, #0A1628 0%, #0E2A4A 100%);
    border-radius: 16px; padding: 32px 36px; margin-bottom: 28px;
    color: white;
}
.page-header h1 { font-size: 28px; font-weight: 800; margin: 0 0 6px 0; color: white; }
.page-header p  { font-size: 14px; color: #7AA8CC; margin: 0; }

/* ── Score ring card ── */
.score-ring-card {
    background: white; border-radius: 16px; padding: 32px 24px;
    text-align: center; box-shadow: 0 2px 20px rgba(10,22,40,0.08);
    border: 1px solid #E8EFF8;
}
.score-number { font-size: 72px; font-weight: 800; line-height: 1; }
.score-sub    { font-size: 12px; color: #8899AA; margin-top: 6px; }
.grade-badge  {
    display: inline-block; font-size: 15px; font-weight: 700;
    padding: 5px 18px; border-radius: 20px; margin-top: 12px;
}

/* ── White card ── */
.white-card {
    background: white; border-radius: 14px; padding: 24px;
    box-shadow: 0 2px 16px rgba(10,22,40,0.06); border: 1px solid #E8EFF8;
    margin-bottom: 20px;
}
.card-title { font-size: 13px; font-weight: 600; color: #445566; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 16px; }

/* ── Metric card ── */
.metric-card {
    background: white; border-radius: 12px; padding: 20px;
    box-shadow: 0 2px 12px rgba(10,22,40,0.06); border: 1px solid #E8EFF8;
    text-align: center;
}
.metric-val { font-size: 32px; font-weight: 800; color: #0A1628; }
.metric-lbl { font-size: 11px; color: #889AAA; margin-top: 4px; font-weight: 500; letter-spacing: 0.5px; }

/* ── Progress bar ── */
.prog-wrap { margin-bottom: 16px; }
.prog-header { display: flex; justify-content: space-between; margin-bottom: 5px; }
.prog-label  { font-size: 13px; font-weight: 500; color: #334455; }
.prog-score  { font-size: 13px; color: #7788AA; }
.prog-track  { height: 7px; background: #EEF2F8; border-radius: 4px; overflow: hidden; }
.prog-fill   { height: 7px; border-radius: 4px; transition: width 0.4s; }

/* ── Tip card ── */
.tip-card {
    background: #F0F6FF; border-left: 4px solid #2D7DD2;
    border-radius: 8px; padding: 14px 16px; margin-bottom: 10px;
    font-size: 13.5px; color: #223344; line-height: 1.6;
}
.tip-card strong { color: #0A1628; }

/* ── Line item (line-by-line) ── */
.cv-line-good    { background: #F0FDF4; border-left: 3px solid #22C55E; border-radius: 8px; padding: 10px 14px; margin-bottom: 6px; font-size: 13px; color: #223344; }
.cv-line-warn    { background: #FFFBEB; border-left: 3px solid #F59E0B; border-radius: 8px; padding: 10px 14px; margin-bottom: 6px; font-size: 13px; color: #223344; }
.cv-line-bad     { background: #FEF2F2; border-left: 3px solid #EF4444; border-radius: 8px; padding: 10px 14px; margin-bottom: 6px; font-size: 13px; color: #223344; }
.cv-line-great   { background: #EFF6FF; border-left: 3px solid #3B82F6; border-radius: 8px; padding: 10px 14px; margin-bottom: 6px; font-size: 13px; color: #223344; }
.cv-line-tip     { font-size: 12px; color: #2D7DD2; margin-top: 5px; font-style: italic; }
.cv-line-rewrite { font-size: 12px; color: #059669; margin-top: 5px; font-weight: 500; }

/* ── Pills ── */
.pill-green  { background:#DCFCE7; color:#16A34A; padding:4px 12px; border-radius:20px; margin:3px; display:inline-block; font-size:12px; font-weight:500; }
.pill-red    { background:#FEE2E2; color:#DC2626; padding:4px 12px; border-radius:20px; margin:3px; display:inline-block; font-size:12px; font-weight:500; }
.pill-orange { background:#FEF3C7; color:#D97706; padding:4px 12px; border-radius:20px; margin:3px; display:inline-block; font-size:12px; font-weight:500; }
.pill-blue   { background:#DBEAFE; color:#2563EB; padding:4px 12px; border-radius:20px; margin:3px; display:inline-block; font-size:12px; font-weight:500; }
.pill-navy   { background:#E0E7FF; color:#3730A3; padding:4px 12px; border-radius:20px; margin:3px; display:inline-block; font-size:12px; font-weight:500; }

/* ── Divider ── */
.section-divider { border: none; border-top: 1px solid #E8EFF8; margin: 24px 0; }

/* ── Feature tiles (landing) ── */
.feature-tile {
    background: white; border: 1px solid #E8EFF8;
    border-radius: 14px; padding: 28px 24px; text-align: center;
    box-shadow: 0 2px 12px rgba(10,22,40,0.05);
    transition: box-shadow 0.2s;
}
.feature-icon  { font-size: 36px; margin-bottom: 12px; }
.feature-title { font-size: 15px; font-weight: 700; color: #0A1628; margin-bottom: 8px; }
.feature-desc  { font-size: 13px; color: #667788; line-height: 1.5; }

/* ── CTA button (main area only) ── */
section.main div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #1A56DB, #0A3EB0) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; padding: 22px 36px !important;
    font-size: 15px !important; font-weight: 600 !important;
    width: 100% !important; letter-spacing: 0.2px !important;
    box-shadow: 0 4px 16px rgba(26,86,219,0.3) !important;
    margin: 28px 0 !important;
}
section.main div[data-testid="stButton"] > button[kind="secondary"] {
    padding: 22px 36px !important;
    border-radius: 12px !important;
    font-size: 15px !important; font-weight: 600 !important;
    width: 100% !important;
    margin: 28px 0 !important;
}

/* ── Sidebar mode buttons ── */
section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"] {
    background: #1A3A5C !important;
    color: #7DD3FC !important;
    border: 1px solid #2A5A8C !important;
    border-radius: 10px !important;
    font-size: 13px !important; font-weight: 700 !important;
    padding: 10px 14px !important;
    box-shadow: none !important; margin: 0 0 6px 0 !important;
    width: 100% !important; text-align: left !important;
    letter-spacing: 0 !important;
}
section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="secondary"] {
    background: transparent !important;
    color: #4A7898 !important;
    border: 1px solid #1E3A5F !important;
    border-radius: 10px !important;
    font-size: 13px !important; font-weight: 500 !important;
    padding: 10px 14px !important;
    box-shadow: none !important; margin: 0 0 6px 0 !important;
    width: 100% !important; text-align: left !important;
    letter-spacing: 0 !important;
}
section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="secondary"]:hover {
    background: #112240 !important; color: #A8C4E0 !important;
}

/* hide streamlit radio circles, style as nav links */
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    display: flex !important; justify-content: space-between !important;
    align-items: center !important; padding: 7px 12px !important;
    margin: 1px 0 !important; border-radius: 6px !important;
    cursor: pointer !important; font-size: 13px !important;
    color: #8AB0CC !important; border-left: 3px solid transparent !important;
    transition: background 0.15s !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: #112240 !important; color: #E0F0FF !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {
    background: #112240 !important; color: #60B0F0 !important;
    border-left-color: #60B0F0 !important; font-weight: 600 !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] div[data-testid="stMarkdownContainer"] p {
    font-size: 13px !important;
}
/* hide the actual radio circle */
section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child { display: none !important; }

/* ── Expander titles — force dark text on light background ── */
div[data-testid="stExpander"] summary p,
div[data-testid="stExpander"] summary span,
div[data-testid="stExpander"] details summary {
    color: #0A1628 !important;
}

/* ── Tabs — dark text so labels are readable on light background ── */
button[data-baseweb="tab"] {
    color: #445566 !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    background: transparent !important;
}
button[data-baseweb="tab"]:hover { color: #0A1628 !important; }
button[data-baseweb="tab"][aria-selected="true"] {
    color: #0A1628 !important;
    font-weight: 700 !important;
}

/* ── Sidebar mode selector buttons ── */
section[data-testid="stSidebar"] .mode-btn {
    display: block; width: 100%; padding: 11px 14px; margin-bottom: 6px;
    border-radius: 10px; font-size: 13px; font-weight: 600; cursor: pointer;
    border: 1px solid #1E3A5F; text-align: left; transition: all 0.15s;
}
section[data-testid="stSidebar"] .mode-btn-active {
    background: #1A3A5C; color: #60B8FF !important;
    border-color: #2A5A8C; box-shadow: inset 0 0 0 1px #2A5A8C;
}
section[data-testid="stSidebar"] .mode-btn-inactive {
    background: transparent; color: #4A7898 !important;
}
section[data-testid="stSidebar"] .mode-btn-active::before { content: "▶  "; font-size: 9px; }

/* ── Mobile dropdown menu (hidden on desktop, shown on mobile) ── */
.mobile-menu-anchor { display: none; }
/* Hide the expander right after the anchor on desktop */
[data-testid="element-container"]:has(.mobile-menu-anchor) + [data-testid="element-container"] {
    display: none !important;
}

/* ── MOBILE RESPONSIVE ── */
@media (max-width: 768px) {
    .block-container { padding: 1rem 1rem 2rem 1rem !important; }
    .page-header { padding: 22px 20px; margin-bottom: 18px; }
    .page-header h1 { font-size: 20px; }
    .score-number { font-size: 52px; }
    .white-card { padding: 16px; }
    .tip-card { font-size: 12.5px; padding: 12px 13px; }

    /* Show mobile menu, hide desktop sidebar */
    .mobile-menu-anchor { display: block; }
    [data-testid="element-container"]:has(.mobile-menu-anchor) + [data-testid="element-container"] {
        display: block !important;
    }
    section[data-testid="stSidebar"] { display: none !important; }
    button[data-testid="collapsedControl"],
    div[data-testid="collapsedControl"] { display: none !important; }

    /* Mobile menu expander — compact floating dropdown */
    [data-testid="element-container"]:has(.mobile-menu-anchor) + [data-testid="element-container"] {
        max-width: 65% !important;
        margin-left: auto !important;
        margin-right: 0 !important;
    }
    [data-testid="element-container"]:has(.mobile-menu-anchor) + [data-testid="element-container"] div[data-testid="stExpander"] {
        background: white !important;
        border: 1px solid #E4ECF4 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 16px rgba(10,22,40,0.1) !important;
        margin-bottom: 12px !important;
        overflow: hidden !important;
    }
    [data-testid="element-container"]:has(.mobile-menu-anchor) + [data-testid="element-container"] div[data-testid="stExpander"] summary {
        padding: 7px 12px !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        color: #0A1628 !important;
    }
    [data-testid="element-container"]:has(.mobile-menu-anchor) + [data-testid="element-container"] div[data-testid="stExpander"] details > div {
        padding: 4px 8px 8px !important;
    }
    /* Smaller, denser buttons inside the mobile menu */
    [data-testid="element-container"]:has(.mobile-menu-anchor) ~ [data-testid="element-container"] div[data-testid="stExpander"] div[data-testid="stButton"] button {
        padding: 4px 8px !important;
        font-size: 11px !important;
        min-height: 0 !important;
        height: auto !important;
        margin: 0 !important;
        line-height: 1.3 !important;
    }
    [data-testid="element-container"]:has(.mobile-menu-anchor) ~ [data-testid="element-container"] div[data-testid="stExpander"] div[data-testid="stButton"] {
        margin-bottom: 2px !important;
    }
    .nav-section-mobile {
        font-size: 8px !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        color: #8AA0B8 !important;
        padding: 6px 2px 2px !important;
        margin: 0 !important;
    }
}

</style>
""", unsafe_allow_html=True)

# =============================================================================
# QUERY PARAM NAVIGATION (must run before session state defaults)
# =============================================================================
if st.query_params.get("go") == "cv":
    st.query_params.clear()
    st.session_state["step"] = "upload"
    st.rerun()

# =============================================================================
# SESSION STATE
# =============================================================================
for k, v in {
    "step":       "landing",
    "cv_result":  None,
    "career_key": "consulting",
    "cv_tab":     "overview",
    "main_tab":   "cv",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def go_to(step):
    st.session_state.step = step

# =============================================================================
# HELPERS
# =============================================================================
def _overall_color(s):
    if s >= 72: return "#22C55E"
    if s >= 50: return "#F59E0B"
    return "#EF4444"

# =============================================================================
# SIDEBAR
# =============================================================================
def _sidebar(result):
    # ── Branding ──────────────────────────────────────────────────────────────
    st.sidebar.markdown("""
    <div style="padding:20px 4px 12px;">
      <div style="font-size:18px;font-weight:800;color:white;letter-spacing:-0.4px;">
        &#127891; CareerPath
      </div>
      <div style="font-size:11px;color:#3A6888;margin-top:2px;">Nova SBE · CV Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Main mode selector — stacked, clearly differentiated ──────────────────
    is_cv     = st.session_state.main_tab == "cv"
    is_career = st.session_state.main_tab == "career"

    st.sidebar.markdown(
        '<div style="padding:0 4px 10px;font-size:9px;font-weight:700;color:#2A5070;'
        'letter-spacing:1.5px;text-transform:uppercase;">Mode</div>',
        unsafe_allow_html=True
    )

    if st.sidebar.button(
        "📄  CV Check",
        use_container_width=True,
        type="primary" if is_cv else "secondary",
        key="sb_cv"
    ):
        st.session_state.main_tab = "cv"
        st.session_state.cv_tab   = "overview"
        st.rerun()

    if st.sidebar.button(
        "🎯  Career Readiness",
        use_container_width=True,
        type="primary" if is_career else "secondary",
        key="sb_career"
    ):
        st.session_state.main_tab = "career"
        st.rerun()

    st.sidebar.markdown('<hr style="border-color:#1E3A5F;margin:12px 0;">', unsafe_allow_html=True)

    # ── Career Readiness sidebar ───────────────────────────────────────────────
    if st.session_state.main_tab == "career":
        cdata = st.session_state.get("career_data")
        if cdata:
            score = cdata["score"]
            crit  = cdata["criteria_met"]
            sc    = "#22C55E" if score >= 72 else "#F59E0B" if score >= 50 else "#EF4444"
            st.sidebar.markdown(
                f'<div style="padding:4px 0 10px;">'
                f'<div style="font-size:9px;font-weight:700;color:#2A5070;letter-spacing:1.5px;'
                f'text-transform:uppercase;margin-bottom:8px;">Readiness Score</div>'
                f'<div style="font-size:42px;font-weight:800;color:{sc};line-height:1;">{score}</div>'
                f'<div style="font-size:10px;color:#3A6888;margin-top:2px;">out of 100</div></div>',
                unsafe_allow_html=True
            )
            CRIT_LABELS = [
                ("internship",     "Internship"),
                ("leadership",     "Leadership"),
                ("international",  "International"),
                ("case_prep",      "Case / Competition"),
                ("extracurricular","Extracurricular"),
                ("gpa",            "GPA 16+"),
            ]
            rows = "".join(
                f'<div style="display:flex;justify-content:space-between;align-items:center;'
                f'padding:6px 0;border-bottom:1px solid #1A3050;">'
                f'<span style="font-size:12px;color:#8AB0CC;">{lbl}</span>'
                f'<span style="font-size:13px;">{"✅" if crit.get(k) else "❌"}</span></div>'
                for k, lbl in CRIT_LABELS
            )
            st.sidebar.markdown(
                '<div style="font-size:9px;font-weight:700;color:#2A5070;letter-spacing:1.5px;'
                'text-transform:uppercase;margin-bottom:8px;">Employer Criteria</div>'
                + rows,
                unsafe_allow_html=True
            )
            st.sidebar.markdown('<hr style="border-color:#1E3A5F;margin:14px 0;">', unsafe_allow_html=True)

    # ── CV Check sub-navigation ────────────────────────────────────────────────
    if st.session_state.main_tab == "cv" and result:
        imp  = result.get("impact",  {})
        brev = result.get("brevity", {})
        sty  = result.get("style",   {})
        def s(d, k): return d.get(k, {}).get("score", 0)

        qi =s(imp,"quantifying_impact"); av=s(imp,"action_verbs")
        acc=s(imp,"accomplishments");    rep=s(imp,"repetition")
        ln =s(brev,"length");            fw=s(brev,"filler_words")
        bc =s(brev,"bullet_count");      bl=s(brev,"bullet_length")
        sec=s(sty,"sections");           pp=s(sty,"personal_pronouns")
        bw =s(sty,"buzzwords");          act=s(sty,"active_voice")
        dat=s(sty,"date_consistency")

        def _nav(label, tab_key):
            active = st.session_state.cv_tab == tab_key
            if st.sidebar.button(label, use_container_width=True,
                                  type="primary" if active else "secondary",
                                  key=f"nb_{tab_key}"):
                st.session_state.cv_tab = tab_key

        st.sidebar.markdown('<p class="nav-section">Results & Feedback</p>', unsafe_allow_html=True)
        _nav("📊  Overview",       "overview")
        _nav("💪  Action Verbs",   "actions")

        st.sidebar.markdown('<p class="nav-section">Impact</p>', unsafe_allow_html=True)
        _nav(f"Quantifying Impact  {qi}/10",  "qi")
        _nav(f"Action Verb Use  {av}/10",     "av")
        _nav(f"Accomplishments  {acc}/10",    "acc")
        _nav(f"Repetition  {rep}/10",         "rep")

        st.sidebar.markdown('<p class="nav-section">Brevity</p>', unsafe_allow_html=True)
        _nav(f"Length  {ln}/10",              "ln")
        _nav(f"Filler Words  {fw}/10",        "fw")
        _nav(f"Total Bullets  {bc}/10",       "bc")
        _nav(f"Bullet Length  {bl}/10",       "bl")

        st.sidebar.markdown('<p class="nav-section">Style</p>', unsafe_allow_html=True)
        _nav(f"Sections  {sec}/10",           "sec")
        _nav(f"Personal Pronouns  {pp}/10",   "pp")
        _nav(f"Buzzwords  {bw}/10",           "bw")
        _nav(f"Active Voice  {act}/10",       "act")
        _nav(f"Date Consistency  {dat}/10",   "dat")

    st.sidebar.markdown('<hr style="border-color:#1E3A5F;margin:12px 0;">', unsafe_allow_html=True)
    if st.sidebar.button("← Start over", use_container_width=True):
        go_to("landing"); st.rerun()


def _mobile_menu(result):
    """Inline dropdown menu for mobile — mirrors the desktop sidebar."""
    st.markdown('<div class="mobile-menu-anchor"></div>', unsafe_allow_html=True)
    is_cv     = st.session_state.main_tab == "cv"
    is_career = st.session_state.main_tab == "career"

    with st.expander("Menu", expanded=False):
        is_overview = is_cv and st.session_state.cv_tab == "overview"
        is_actions  = is_cv and st.session_state.cv_tab == "actions"

        if st.button("📄 CV Check", key="m_mode_cv",
                     type="primary" if is_cv else "secondary",
                     use_container_width=True):
            st.session_state.main_tab = "cv"
            st.session_state.cv_tab   = "overview"
            st.rerun()
        if st.button("🎯 Career Readiness", key="m_mode_cr",
                     type="primary" if is_career else "secondary",
                     use_container_width=True):
            st.session_state.main_tab = "career"
            st.rerun()

        if is_cv and result:
            if st.button("📊 Overview", key="m_nav_overview",
                         type="primary" if is_overview else "secondary",
                         use_container_width=True):
                st.session_state.cv_tab = "overview"
                st.rerun()
            if st.button("💪 Action Verbs", key="m_nav_actions",
                         type="primary" if is_actions else "secondary",
                         use_container_width=True):
                st.session_state.cv_tab = "actions"
                st.rerun()

        if st.button("↻ Start over", key="m_restart", use_container_width=True):
            for k in ("cv_result", "gemini_result", "career_data"):
                st.session_state.pop(k, None)
            go_to("landing"); st.rerun()


# =============================================================================
# OVERVIEW PAGE
# =============================================================================
def _overview(result):
    score      = result["overall_pct"]
    grade      = result.get("grade", "B")
    enc        = result.get("encouragement", "")
    pct_lb     = result.get("percentile", "top 50%")
    oc         = _overall_color(score)
    imp        = result.get("impact",  {})
    brev       = result.get("brevity", {})
    sty        = result.get("style",   {})
    highlights = result.get("highlights", [])
    _gr = st.session_state.get("gemini_result") or {}
    if _gr.get("highlights"):
        highlights = _gr["highlights"]
    grade_color = "#22C55E" if grade in ("A+","A") else "#F59E0B" if grade=="B" else "#EF4444"

    def gs(d, k): return d.get(k, {}).get("score", 0)

    # ── Global white background for results page ─────────────────────────────
    st.markdown("""
    <style>
    .stApp, section.main, .block-container { background: #F0F4F8 !important; }
    section[data-testid="stSidebar"] { background: #0A1628 !important; }
    div[data-testid="stMetric"] { background: transparent !important; }
    div[data-testid="metric-container"] { background: transparent !important; }
    </style>
    """, unsafe_allow_html=True)

    # ── Header ───────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0A1628,#0E2A4A);border-radius:16px;
                padding:32px 40px;margin-bottom:24px;
                box-shadow:0 4px 24px rgba(10,22,40,0.15);">
        <h1 style="color:white;font-size:28px;font-weight:800;margin:0 0 8px;
                   letter-spacing:-0.5px;">Your CV Score</h1>
        <p style="color:#7AA8CC;font-size:14px;margin:0;line-height:1.6;">
            {enc} &nbsp;·&nbsp;
            You're in the <strong style="color:#60B8FF">{pct_lb}</strong> of student CVs.
        </p>
    </div>""", unsafe_allow_html=True)

    # ── Row 1: Score card + Scorecard ────────────────────────────────────────
    c_score, c_card = st.columns([1, 2], gap="large")

    with c_score:
        # Build progress ring-like display entirely in HTML
        ring_pct = score  # 0-100
        circumference = 2 * 3.14159 * 54
        dash_offset = circumference * (1 - ring_pct / 100)
        st.markdown(f"""
        <div style="background:white;border-radius:16px;padding:32px 20px;
                    text-align:center;border:1px solid #E4ECF4;
                    box-shadow:0 2px 16px rgba(10,22,40,0.06);">
            <div style="font-size:10px;font-weight:700;color:#AAB8C8;letter-spacing:1.2px;
                        text-transform:uppercase;margin-bottom:16px;">Overall Score</div>
            <svg width="140" height="140" viewBox="0 0 140 140" style="margin:0 auto;display:block;">
              <circle cx="70" cy="70" r="54" fill="none" stroke="#EEF2F8" stroke-width="10"/>
              <circle cx="70" cy="70" r="54" fill="none" stroke="{oc}" stroke-width="10"
                stroke-dasharray="{circumference:.1f}"
                stroke-dashoffset="{dash_offset:.1f}"
                stroke-linecap="round"
                transform="rotate(-90 70 70)"/>
              <text x="70" y="65" text-anchor="middle" dominant-baseline="middle"
                font-size="32" font-weight="800" fill="{oc}" font-family="Inter,sans-serif">{score}</text>
              <text x="70" y="88" text-anchor="middle" dominant-baseline="middle"
                font-size="11" fill="#AAB8C8" font-family="Inter,sans-serif">out of 100</text>
            </svg>
            <div style="margin-top:16px;">
                <div style="display:inline-block;font-size:15px;font-weight:700;
                            padding:6px 24px;border-radius:20px;
                            background:{grade_color}18;color:{grade_color};">Grade {grade}</div>
            </div>
            <div style="margin-top:16px;padding-top:16px;border-top:1px solid #F0F4F8;
                        display:flex;justify-content:space-around;">
                <div>
                    <div style="font-size:10px;color:#AAB8C8;text-transform:uppercase;
                                letter-spacing:0.8px;">Words</div>
                    <div style="font-size:20px;font-weight:700;color:#0A1628;">
                        {result["word_count"]}</div>
                </div>
                <div>
                    <div style="font-size:10px;color:#AAB8C8;text-transform:uppercase;
                                letter-spacing:0.8px;">Grade</div>
                    <div style="font-size:20px;font-weight:700;color:{grade_color};">{grade}</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

    with c_card:
        imp_pct  = int(imp.get("score", 0) / 40 * 100)
        brev_pct = int(brev.get("score", 0) / 30 * 100)
        sty_pct  = int(sty.get("score", 0) / 30 * 100)

        def sub_row(label, val):
            c = "#22C55E" if val >= 8 else "#F59E0B" if val >= 5 else "#EF4444"
            return (
                '<div style="display:flex;justify-content:space-between;'
                'align-items:center;padding:5px 0;border-bottom:1px solid #F5F7FA;">'
                '<span style="font-size:12px;color:#667788;">' + label + '</span>'
                '<span style="font-size:12px;font-weight:700;color:' + c + ';">'
                + str(val) + '/10</span></div>'
            )

        left_rows  = (sub_row("Quantifying Impact", gs(imp,  "quantifying_impact"))
                    + sub_row("Action Verbs",        gs(imp,  "action_verbs"))
                    + sub_row("Accomplishments",     gs(imp,  "accomplishments"))
                    + sub_row("Repetition",          gs(imp,  "repetition"))
                    + sub_row("Length",              gs(brev, "length"))
                    + sub_row("Filler Words",        gs(brev, "filler_words")))
        right_rows = (sub_row("Bullet Points",  gs(brev, "bullet_count"))
                    + sub_row("Bullet Length",  gs(brev, "bullet_length"))
                    + sub_row("Sections",       gs(sty,  "sections"))
                    + sub_row("Pronouns",       gs(sty,  "personal_pronouns"))
                    + sub_row("Buzzwords",      gs(sty,  "buzzwords"))
                    + sub_row("Active Voice",   gs(sty,  "active_voice")))

        st.markdown(
            '<div style="background:white;border-radius:16px;padding:28px 32px;'
            'border:1px solid #E4ECF4;box-shadow:0 2px 16px rgba(10,22,40,0.06);">'

            '<div style="font-size:10px;font-weight:700;color:#AAB8C8;letter-spacing:1.2px;'
            'text-transform:uppercase;margin-bottom:20px;">Scorecard</div>'

            '<div style="margin-bottom:6px;display:flex;justify-content:space-between;">'
            '<span style="font-size:13px;font-weight:600;color:#0A1628;">Impact</span>'
            '<span style="font-size:13px;font-weight:700;color:#3B82F6;">'
            + str(imp.get("score", 0)) + '/40</span></div>'
            '<div style="height:7px;background:#EEF2F8;border-radius:4px;margin-bottom:16px;">'
            '<div style="height:7px;width:' + str(imp_pct) + '%;background:#3B82F6;border-radius:4px;"></div></div>'

            '<div style="margin-bottom:6px;display:flex;justify-content:space-between;">'
            '<span style="font-size:13px;font-weight:600;color:#0A1628;">Brevity</span>'
            '<span style="font-size:13px;font-weight:700;color:#22C55E;">'
            + str(brev.get("score", 0)) + '/30</span></div>'
            '<div style="height:7px;background:#EEF2F8;border-radius:4px;margin-bottom:16px;">'
            '<div style="height:7px;width:' + str(brev_pct) + '%;background:#22C55E;border-radius:4px;"></div></div>'

            '<div style="margin-bottom:6px;display:flex;justify-content:space-between;">'
            '<span style="font-size:13px;font-weight:600;color:#0A1628;">Style</span>'
            '<span style="font-size:13px;font-weight:700;color:#8B5CF6;">'
            + str(sty.get("score", 0)) + '/30</span></div>'
            '<div style="height:7px;background:#EEF2F8;border-radius:4px;margin-bottom:20px;">'
            '<div style="height:7px;width:' + str(sty_pct) + '%;background:#8B5CF6;border-radius:4px;"></div></div>'

            '<div style="border-top:1px solid #F0F4F8;padding-top:16px;">'
            '<div style="font-size:10px;font-weight:700;color:#AAB8C8;letter-spacing:1px;'
            'text-transform:uppercase;margin-bottom:12px;">Sub-scores</div>'
            '<div style="display:flex;gap:24px;">'
            '<div style="flex:1;">' + left_rows + '</div>'
            '<div style="flex:1;">' + right_rows + '</div>'
            '</div></div></div>',
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── Quick Wins ────────────────────────────────────────────────────────────
    if st.session_state.get("gemini_result"):
        st.markdown(
            '<div style="text-align:right;margin-bottom:6px;">'
            '<span style="background:#EFF6FF;color:#1A56DB;font-size:11px;font-weight:600;'
            'padding:3px 12px;border-radius:20px;border:1px solid #BFDBFE;">'
            '✨ Powered by Gemini</span></div>',
            unsafe_allow_html=True
        )

    tips_html = ""
    for tip in highlights:
        tips_html += (
            '<div style="display:flex;gap:12px;align-items:flex-start;padding:14px 16px;'
            'background:#F8FAFF;border-left:4px solid #3B82F6;border-radius:8px;margin-bottom:10px;">'
            '<span style="font-size:13.5px;color:#223344;line-height:1.6;">' + tip + '</span>'
            '</div>'
        )

    st.markdown(
        '<div style="background:white;border-radius:16px;padding:28px 32px;'
        'border:1px solid #E4ECF4;box-shadow:0 2px 16px rgba(10,22,40,0.06);">'
        '<div style="font-size:10px;font-weight:700;color:#AAB8C8;letter-spacing:1.2px;'
        'text-transform:uppercase;margin-bottom:20px;">&#128640; Quick Wins — Your top priorities</div>'
        + tips_html + '</div>',
        unsafe_allow_html=True
    )

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    page_count = result.get("page_count", 1)
    pc_icon  = "✅" if page_count <= 2 else "⚠️"
    pc_color = "#16A34A" if page_count <= 2 else "#D97706"
    pc_msg   = (f"Your CV is <strong>{page_count} page{'s' if page_count > 1 else ''}</strong> — "
                + ("within the 1–2 page limit." if page_count <= 2
                   else "try to reduce it to a maximum of 2 pages."))

    st.markdown(
        '<div style="background:white;border-radius:16px;padding:28px 32px;'
        'border:1px solid #E4ECF4;box-shadow:0 2px 16px rgba(10,22,40,0.06);">'
        '<div style="font-size:10px;font-weight:700;color:#AAB8C8;letter-spacing:1.2px;'
        'text-transform:uppercase;margin-bottom:16px;">&#9989; Before you send</div>'
        f'<div style="display:flex;align-items:flex-start;gap:10px;padding:10px 0;border-bottom:1px solid #F0F4F8;">'
        f'<span style="font-size:16px;">{pc_icon}</span>'
        f'<span style="font-size:13px;color:{pc_color};">{pc_msg}</span></div>'
        '<div style="display:flex;align-items:flex-start;gap:10px;padding:10px 0;border-bottom:1px solid #F0F4F8;">'
        '<span style="font-size:16px;">📝</span>'
        '<span style="font-size:13px;color:#4A5568;">Run a <strong>spellcheck</strong> before sending — typos are the fastest way to get rejected.</span></div>'
        '<div style="display:flex;align-items:flex-start;gap:10px;padding:10px 0;border-bottom:1px solid #F0F4F8;">'
        '<span style="font-size:16px;">👀</span>'
        '<span style="font-size:13px;color:#4A5568;">Have a <strong>friend or mentor review</strong> your CV — a fresh pair of eyes catches what you miss.</span></div>'
        '<div style="display:flex;align-items:flex-start;gap:10px;padding:10px 0;border-bottom:1px solid #F0F4F8;">'
        '<span style="font-size:16px;">🔗</span>'
        '<span style="font-size:13px;color:#4A5568;"><strong>Email address not as a hyperlink</strong> — remove the blue underline from your email in the header (right-click → Remove Hyperlink in Word).</span></div>'
        '<div style="display:flex;align-items:flex-start;gap:10px;padding:10px 0;border-bottom:1px solid #F0F4F8;">'
        '<span style="font-size:16px;">✍️</span>'
        '<span style="font-size:13px;color:#4A5568;">Use <strong>"independently"</strong> at most 1–2 times — using it more often makes you sound like you don\'t work well in a team.</span></div>'
        '<div style="display:flex;align-items:flex-start;gap:10px;padding:10px 0;">'
        '<span style="font-size:16px;">💾</span>'
        '<span style="font-size:13px;color:#4A5568;">Save as a <strong>clear PDF filename</strong>: e.g. <em>CV_Firstname_Lastname.pdf</em></span></div>'
        '</div>',
        unsafe_allow_html=True
    )


# =============================================================================
# ACTION VERBS PAGE
# =============================================================================
def _action_verbs(result):
    from cv_score import STRONG_ACTION_VERBS, WEAK_ACTION_VERBS, ACTION_VERB_CATEGORIES, _strip_bullet
    raw   = result.get("raw_text","")
    lines = [l.strip().lower() for l in raw.split("\n") if len(l.strip())>15]
    found_weak   = [v for v in WEAK_ACTION_VERBS   if any(v in l[:60]     for l in lines)]

    replacements = {
        "worked":          "Led / Built / Delivered",
        "helped":          "Facilitated / Enabled / Supported",
        "assisted":        "Coordinated / Contributed",
        "supported":       "Strengthened / Enabled / Reinforced",
        "responsible for": "Managed / Oversaw / Led",
        "participated in": "Collaborated on / Contributed to",
        "involved in":     "Spearheaded / Championed",
        "handled":         "Managed / Executed",
        "carried out":     "Implemented / Delivered",
        "worked on":       "Developed / Built / Designed",
        "contributed to":  "Drove / Accelerated / Enhanced",
        "dealt with":      "Resolved / Managed / Navigated",
        "tasked with":     "Led / Owned / Directed",
        "duties included": "Managed / Oversaw / Delivered",
    }

    # ── All strong verbs found at start of any bullet ────────────────────────
    verb_counts = {}
    for line in lines:
        cleaned = _strip_bullet(line)
        for v in STRONG_ACTION_VERBS:
            if cleaned.startswith(v):
                verb_counts[v] = verb_counts.get(v, 0) + 1

    # Suggested verbs not yet used (career-aligned top picks)
    top_suggestions = [
        "spearheaded", "orchestrated", "streamlined", "transformed",
        "pioneered", "accelerated", "delivered", "generated",
        "optimised", "restructured", "launched", "negotiated",
    ]
    unused_suggestions = [v.capitalize() for v in top_suggestions if v not in verb_counts][:8]

    st.markdown(
        '<div class="page-header">'
        '<h1>Action Verbs</h1>'
        '<p>The words you start your bullet points with define how recruiters perceive you.</p>'
        '</div>',
        unsafe_allow_html=True
    )

    # ── Card 1: Strong verbs found ───────────────────────────────────────────
    if verb_counts:
        pills = "".join(
            '<span class="pill-green" style="font-size:13px;padding:5px 14px;margin:4px;">'
            + v.capitalize() + ' <span style="opacity:0.6;font-size:11px;">×' + str(cnt) + '</span>'
            + '</span>'
            for v, cnt in sorted(verb_counts.items(), key=lambda x: -x[1])
        )
        suggest_html = ""
        if unused_suggestions:
            suggest_html = (
                '<div style="margin-top:14px;padding-top:12px;border-top:1px solid #E8EFF8;">'
                '<div style="font-size:11px;font-weight:600;color:#889AAA;letter-spacing:0.8px;'
                'text-transform:uppercase;margin-bottom:8px;">Consider adding</div>'
                + "".join('<span class="pill-blue" style="margin:3px;">' + v + '</span>' for v in unused_suggestions)
                + '</div>'
            )
        strong_html = (
            '<div class="white-card">'
            '<p class="card-title">💪 Strong verbs you used</p>'
            + pills
            + '<div style="margin-top:10px;font-size:12px;color:#667788;">You used <b>'
            + str(len(verb_counts)) + '</b> distinct strong action verbs — keep it up!</div>'
            + suggest_html
            + '</div>'
        )
    else:
        strong_html = (
            '<div class="white-card">'
            '<p class="card-title">💪 Strong verbs you used</p>'
            '<div class="tip-card">No strong verbs detected at the start of your bullet points.'
            ' Try restructuring your bullets to begin with a strong action verb.</div>'
            '<div style="margin-top:10px;">'
            + "".join('<span class="pill-blue" style="margin:3px;">' + v + '</span>' for v in unused_suggestions)
            + '</div></div>'
        )

    # ── Card 2: Weak verbs ───────────────────────────────────────────────────
    if found_weak:
        found_pills = "".join('<span class="pill-orange" style="margin:3px;">' + v + '</span>' for v in found_weak)
        tips = "".join(
            '<div class="tip-card" style="margin-top:8px;">'
            '<strong>"' + w + '"</strong>'
            ' &rarr; Try: <span class="pill-blue">' + replacements[w] + '</span></div>'
            for w in found_weak if w in replacements
        )
        weak_html = (
            '<div class="white-card">'
            '<p class="card-title">⚠️ Weak verbs to replace</p>'
            + found_pills + tips
            + '</div>'
        )
    else:
        # Show the full replacement guide as reference even when CV is clean
        all_tips = "".join(
            '<div style="display:flex;justify-content:space-between;align-items:center;'
            'padding:7px 0;border-bottom:1px solid #F0F4F8;">'
            '<span style="font-size:13px;color:#667788;">' + w + '</span>'
            '<span style="font-size:12px;color:#2563EB;font-weight:500;">' + repl + '</span>'
            '</div>'
            for w, repl in replacements.items()
        )
        weak_html = (
            '<div class="white-card">'
            '<p class="card-title">✅ No weak verbs found</p>'
            '<div style="font-size:13px;color:#22C55E;font-weight:600;margin-bottom:14px;">'
            'Your CV avoids weak language — excellent!</div>'
            '<div style="font-size:11px;font-weight:700;color:#889AAA;letter-spacing:0.8px;'
            'text-transform:uppercase;margin-bottom:8px;">Common swaps for reference</div>'
            + all_tips
            + '</div>'
        )

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown(strong_html, unsafe_allow_html=True)
    with c2:
        st.markdown(weak_html, unsafe_allow_html=True)

    # ── Browse verb library ───────────────────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:20px;font-weight:700;color:#0A1628;margin-bottom:4px;">Browse Action Verbs</div>'
        '<div style="font-size:14px;color:#4A5568;margin-bottom:16px;">Make sure your CV stands out by starting every line with a strong action verb. Browse by skill you want to convey.</div>',
        unsafe_allow_html=True
    )

    categories = list(ACTION_VERB_CATEGORIES.keys())
    tabs       = st.tabs(["All"] + categories)

    def _verb_grid(verbs):
        rows = [verbs[i:i+4] for i in range(0, len(verbs), 4)]
        rows_html = ""
        for row in rows:
            cells = "".join(
                '<td style="padding:10px 20px;text-align:center;font-size:14px;'
                'color:#334455;font-weight:400;">' + v + '</td>'
                for v in row
            )
            cells += '<td style="padding:10px 20px;"></td>' * (4 - len(row))
            rows_html += '<tr>' + cells + '</tr>'
        st.markdown(
            '<div class="white-card" style="padding:8px 0;">'
            '<table style="width:100%;border-collapse:collapse;">'
            + rows_html +
            '</table></div>',
            unsafe_allow_html=True
        )

    with tabs[0]:
        all_verbs, seen = [], set()
        for vlist in ACTION_VERB_CATEGORIES.values():
            for v in vlist:
                if v.lower() not in seen:
                    all_verbs.append(v)
                    seen.add(v.lower())
        _verb_grid(sorted(all_verbs))

    for tab, cat in zip(tabs[1:], categories):
        with tab:
            st.markdown(
                '<div style="font-size:11px;font-weight:700;color:#0A1628;letter-spacing:1.2px;'
                'text-transform:uppercase;padding:8px 0 10px;">' + cat.upper() + '</div>',
                unsafe_allow_html=True
            )
            _verb_grid(ACTION_VERB_CATEGORIES[cat])


# =============================================================================
# DIMENSION DETAIL PAGE — CareerSet-style layout
# =============================================================================
def _dimension(key, result):
    from cv_score import (STRONG_ACTION_VERBS, WEAK_ACTION_VERBS,
                          QUANTIFICATION_PATTERNS, PERSONAL_PRONOUNS,
                          PASSIVE_INDICATORS, FILLER_WORDS,
                          ACCOMPLISHMENT_SIGNALS, _strip_bullet)

    imp  = result.get("impact",  {})
    brev = result.get("brevity", {})
    sty  = result.get("style",   {})
    raw  = result.get("raw_text","")
    lines = [l.strip() for l in raw.split("\n") if len(l.strip()) > 20]

    dim_map = {
        "qi": (imp,"quantifying_impact"),  "av":  (imp,"action_verbs"),
        "acc":(imp,"accomplishments"),     "rep": (imp,"repetition"),
        "ln": (brev,"length"),             "fw":  (brev,"filler_words"),
        "bc": (brev,"bullet_count"),       "bl":  (brev,"bullet_length"),
        "sec":(sty,"sections"),            "pp":  (sty,"personal_pronouns"),
        "bw": (sty,"buzzwords"),           "act": (sty,"active_voice"),
        "dat":(sty,"date_consistency"),
    }
    dim_info = {
        "qi":  ("Quantifying Impact",   "Increase the impact of your achievements by adding numbers and metrics"),
        "av":  ("Action Verb Use",       "Start every bullet with a strong, specific action verb"),
        "acc": ("Accomplishments",       "Show concrete outcomes and results, not just responsibilities"),
        "rep": ("Repetition",            "Vary the verbs at the start of your bullet points"),
        "ln":  ("CV Length",             "Keep your CV focused — one tight page beats two loose ones"),
        "fw":  ("Filler Words",          "Every word should earn its place — cut vague phrases that add length without meaning"),
        "bc":  ("Bullet Points",         "Use the right number of bullet points for your level of experience"),
        "bl":  ("Bullet Point Length",   "Each bullet should be one punchy line, not a paragraph"),
        "sec": ("CV Sections",           "Ensure all key sections recruiters look for are clearly labelled"),
        "pp":  ("Personal Pronouns",     "CV writing convention: never use 'I', 'my' or 'we'"),
        "bw":  ("Buzzwords & Clichés",   "Replace overused phrases with specific, evidenced claims"),
        "act": ("Active Voice",          "Active voice is direct and confident — passive constructions sound weak"),
        "dat": ("Date Consistency",      "Use one date format throughout — inconsistency signals poor attention to detail"),
    }

    cat_d, sub_k = dim_map.get(key, (imp,"quantifying_impact"))
    data  = cat_d.get(sub_k, {})
    score = data.get("score", 0)
    sc    = "#22C55E" if score >= 8 else "#F59E0B" if score >= 5 else "#EF4444"
    title, subtitle = dim_info.get(key, ("Detail", ""))

    # ── Helper: section block (header bar + white card) ──────────────────────
    def section(hdr, body):
        st.markdown(
            '<div style="background:#E8EDF5;padding:10px 16px;border-radius:8px 8px 0 0;'
            'font-size:11px;font-weight:700;color:#0A1628;letter-spacing:1.2px;text-transform:uppercase;">'
            + hdr + '</div>'
            '<div style="background:white;border:1px solid #DDE5F0;border-top:none;'
            'border-radius:0 0 12px 12px;padding:24px;margin-bottom:20px;">'
            + body + '</div>',
            unsafe_allow_html=True
        )

    def analysis_card(icon, icon_label, desc):
        return (
            '<div style="display:flex;align-items:flex-start;gap:32px;">'
            '<div style="text-align:center;min-width:96px;padding-top:8px;">'
            '<div style="font-size:52px;line-height:1;">' + icon + '</div>'
            '<div style="font-size:12px;color:#667788;margin-top:8px;line-height:1.4;">' + icon_label + '</div>'
            '</div>'
            '<div style="font-size:14px;color:#4A5568;line-height:1.75;padding-top:6px;">' + desc + '</div>'
            '</div>'
        )

    def lines_card(count, count_label, count_color, intro, rows_html):
        return (
            '<div style="display:flex;align-items:flex-start;gap:32px;">'
            '<div style="text-align:center;min-width:96px;">'
            '<div style="font-size:52px;font-weight:800;color:' + count_color + ';line-height:1;">' + str(count) + '</div>'
            '<div style="font-size:12px;color:#889AAA;margin-top:6px;line-height:1.4;">' + count_label + '</div>'
            '</div>'
            '<div style="flex:1;">'
            '<div style="font-size:13px;color:#667788;margin-bottom:10px;">' + intro + '</div>'
            + rows_html +
            '</div></div>'
        )

    def line_rows(line_list, color="#4A5568"):
        return "".join(
            '<div style="padding:11px 0;border-bottom:1px solid #F0F4F8;font-size:13px;color:' + color + ';">'
            + l + '</div>'
            for l in line_list
        )

    def example_table(pairs):
        rows = "".join(
            '<tr>'
            '<td style="padding:12px 10px;font-size:13px;color:#889AAA;border-bottom:1px solid #F0F4F8;vertical-align:top;width:46%;">' + bad + '</td>'
            '<td style="padding:12px 6px;text-align:center;color:#CBD5E1;font-size:18px;border-bottom:1px solid #F0F4F8;vertical-align:middle;">&raquo;</td>'
            '<td style="padding:12px 10px;font-size:13px;color:#1E3A5C;border-bottom:1px solid #F0F4F8;vertical-align:top;width:46%;">' + good + '</td>'
            '</tr>'
            for bad, good in pairs
        )
        return (
            '<div style="display:flex;gap:10px;padding:0 10px 10px;font-size:11px;font-weight:700;">'
            '<div style="flex:1;color:#EF4444;">✗ &nbsp;Responsibility-oriented</div>'
            '<div style="width:28px;"></div>'
            '<div style="flex:1;color:#22C55E;">✓ &nbsp;Accomplishment-oriented</div>'
            '</div>'
            '<table style="width:100%;border-collapse:collapse;">' + rows + '</table>'
        )

    # ── Score header ──────────────────────────────────────────────────────────
    st.markdown(
        '<div style="display:flex;align-items:flex-start;gap:28px;margin-bottom:32px;">'
        '<div style="width:88px;height:88px;border-radius:50%;border:3px solid ' + sc + ';'
        'display:flex;align-items:center;justify-content:center;flex-shrink:0;">'
        '<span style="font-size:34px;font-weight:800;color:' + sc + ';">' + str(score) + '</span></div>'
        '<div><h2 style="font-size:26px;font-weight:800;color:#0A1628;margin:0 0 8px 0;">' + title + '</h2>'
        '<p style="font-size:15px;color:#667788;margin:0;line-height:1.5;">' + subtitle + '</p></div>'
        '</div>',
        unsafe_allow_html=True
    )

    # ── Per-dimension CareerSet-style content ────────────────────────────────

    if key == "qi":
        qi_data = data
        def _has_number(l):
            if any(re.search(p, l) for p in QUANTIFICATION_PATTERNS):
                return True
            # catch plain numbers (e.g. "11 brokerages", ">50 companies", "3 months")
            if re.search(r'[>≥<≤]\s*\d+', l):
                return True
            if re.search(r'\b\d+\b', l):
                return True
            return False

        def _needs_number(l):
            ll = l.lower()
            # skip contact info
            if '@' in l or re.search(r'\+\d[\d\s\-]{7,}', l):
                return False
            # skip lines that already have any number
            if _has_number(l):
                return False
            # only show actual bullet/achievement lines
            starts_with_bullet = l.startswith(('•', '-', '–', '▪', '·', '▸'))
            starts_with_verb   = any(_strip_bullet(ll).startswith(v) for v in STRONG_ACTION_VERBS + WEAK_ACTION_VERBS)
            if not starts_with_bullet and not starts_with_verb:
                return False
            return True

        q_lines    = [l for l in lines if _has_number(l)]
        no_q_lines = [l for l in lines if _needs_number(l)]
        q_count   = qi_data.get("quantified_lines", len(q_lines))

        if q_count == 0:
            icon, icon_lbl = "📉", "0 quantified\nlines found"
            desc = ("Your CV currently has <strong>no lines with numbers or metrics</strong>. "
                    "Recruiters at top firms are trained to look for quantified achievements — a bullet with a number "
                    "is up to 40% more likely to be remembered. Even rough estimates ('team of ~10', '3 events') "
                    "are far stronger than no number at all.")
        elif q_count < 3:
            icon, icon_lbl = "📊", f"{q_count} quantified\nline{'s' if q_count>1 else ''} found"
            desc = (f"You have <strong>{q_count} line{'s' if q_count>1 else ''} with numbers</strong> — a good start. "
                    "Most strong student CVs have 4–8 quantified bullets. Adding 2–3 more metrics "
                    "will significantly boost how recruiters perceive your impact.")
        else:
            icon, icon_lbl = "✅", f"{q_count} quantified\nlines found"
            desc = (f"<strong>Great — {q_count} of your lines include numbers or metrics.</strong> "
                    "You're clearly thinking about impact. Review the remaining lines below and see if any "
                    "could be strengthened with a figure, percentage or scale.")

        section("Analysis", analysis_card(icon, icon_lbl, desc))

        section("Recruiter's Insight",
            '<p style="font-size:14px;color:#4A5568;line-height:1.75;margin:0;">'
            "Numbers make achievements concrete and memorable. When a recruiter reads "
            "<em>'Organised events'</em> they have no reference point. When they read "
            "<em>'Organised 4 events for 200+ attendees'</em>, the scale is instantly clear. "
            "You don't need perfect data — estimates, team sizes, timeframes and rankings all count."
            "</p>"
        )

        affected = no_q_lines[:6]
        rows_html = line_rows(
            [f'<span style="color:#F59E0B;">🟡</span> {l} '
             f'<span style="font-size:11px;color:#2D7DD2;font-style:italic;">→ Can you add a number here?</span>'
             for l in affected],
        ) if affected else '<div style="color:#22C55E;font-size:13px;">All content lines are quantified — excellent!</div>'

        section("Lines that need a number",
            lines_card(len(affected), "lines without\nmetrics", "#F59E0B",
                       "These lines from your CV have no numbers. Try adding team size, %, timeframe or ranking:",
                       rows_html)
        )

        with st.expander("How to add numbers — practical guide"):
            st.markdown("""
**Ask yourself these 4 questions for each bullet:**

| Question | Example answer |
|----------|---------------|
| How many people? | "team of 8", "200 attendees" |
| By how much? | "increased by 30%", "reduced from 2h to 45min" |
| At what scale? | "5 clients", "3 countries", "12 projects" |
| How fast? | "delivered in 2 weeks", "within a 48h deadline" |

Estimates are fine — "~50 participants" is better than nothing.
            """)

        section("Before & After Examples", example_table([
            ("Organised weekly team meetings", "Organised weekly meetings for a 12-person cross-functional team"),
            ("Managed social media accounts", "Grew Instagram following by 40% over 3 months"),
            ("Helped with event planning", "Co-organised 3 faculty events with 150+ attendees each"),
            ("Contributed to research project", "Analysed dataset of 2,000+ entries, identifying 4 key trends"),
        ]))

    elif key == "av":
        av_data = data
        strong_c = av_data.get("strong", 0)
        weak_c   = av_data.get("weak", 0)
        weak_lines_found = [(l, [v for v in WEAK_ACTION_VERBS if v in l.lower()[:60]])
                            for l in lines if any(v in l.lower()[:60] for v in WEAK_ACTION_VERBS)]
        verb_replacements = {
            "worked": "Led / Delivered / Built",
            "helped": "Facilitated / Enabled / Supported",
            "assisted": "Coordinated / Contributed",
            "supported": "Strengthened / Enabled",
            "responsible for": "Managed / Oversaw / Led",
            "participated in": "Collaborated on / Contributed to",
            "involved in": "Spearheaded / Championed",
            "handled": "Managed / Executed",
            "worked on": "Developed / Built",
            "contributed to": "Drove / Accelerated",
        }

        if weak_c == 0:
            icon, icon_lbl = "💪", "No weak verbs\ndetected"
            desc = (f"<strong>Excellent — your CV uses {strong_c} strong action verb lines</strong> "
                    "with no weak verbs detected. Every bullet starts with a direct, confident verb "
                    "that signals ownership and impact. Keep this standard.")
        elif weak_c <= 2:
            icon, icon_lbl = "⚠️", f"{weak_c} weak verb line{'s' if weak_c>1 else ''}"
            desc = (f"You have <strong>{weak_c} line{'s' if weak_c>1 else ''} with weak verbs</strong> "
                    f"and {strong_c} with strong verbs — mostly good. "
                    "Swapping those {weak_c} weak verbs will lift your overall impression significantly.")
        else:
            icon, icon_lbl = "🔴", f"{weak_c} weak verb lines"
            desc = (f"<strong>{weak_c} lines use weak, passive verbs</strong> like 'worked', 'helped' or 'assisted'. "
                    "Recruiters spend 6 seconds scanning a CV — the first word of each bullet "
                    "shapes their entire impression. Strong verbs like 'Led', 'Built' and 'Delivered' "
                    "signal ownership; weak verbs signal passivity.")

        section("Analysis", analysis_card(icon, icon_lbl, desc))

        section("Recruiter's Insight",
            '<p style="font-size:14px;color:#4A5568;line-height:1.75;margin:0;">'
            "The first word of each bullet is the single most-read word in your CV. "
            "Verbs like <strong>Led, Spearheaded, Delivered</strong> instantly frame you as someone who takes initiative. "
            "Verbs like <strong>helped, worked on, was involved in</strong> frame you as a bystander. "
            "The tasks may be identical — the verb alone changes the recruiter's perception."
            "</p>"
        )

        if weak_lines_found:
            rows_html = line_rows([
                f'<span style="color:#EF4444;">{l}</span>'
                f'<span style="font-size:11px;color:#2D7DD2;font-style:italic;display:block;margin-top:3px;">'
                f'→ Try: {verb_replacements.get(verbs[0], "a stronger verb")}</span>'
                for l, verbs in weak_lines_found[:5]
            ])
            section("Lines to fix",
                lines_card(len(weak_lines_found), "lines with\nweak verbs", "#EF4444",
                           "Replace the opening verb on each of these lines:",
                           rows_html)
            )
        else:
            section("Lines to fix",
                '<div style="color:#22C55E;font-size:13px;padding:8px 0;">'
                "No lines with weak verbs found — great job!</div>"
            )

        with st.expander("Verb swaps — quick reference"):
            st.markdown("\n".join(f"- **{w}** → {r}" for w, r in verb_replacements.items()))

        section("Before & After Examples", example_table([
            ("Was responsible for managing the project timeline", "Managed project timeline across 3 workstreams"),
            ("Helped the team prepare client presentations", "Co-developed 5 client presentations for McKinsey engagement"),
            ("Worked on data analysis for the strategy report", "Analysed market data to support €2M strategy recommendation"),
            ("Participated in the consulting club competitions", "Competed in 2 national case competitions, reaching semi-finals"),
        ]))

    elif key == "acc":
        acc_data = data
        signals  = acc_data.get("signals_found", 0)
        task_lines = [l for l in lines
                      if not any(re.search(p, l, re.IGNORECASE) for p in ACCOMPLISHMENT_SIGNALS)
                      and len(l) > 30
                      and any(l.lower().startswith(v) for v in STRONG_ACTION_VERBS)][:5]

        if signals >= 4:
            icon, icon_lbl = "🏆", f"{signals} result\nsignals found"
            desc = (f"<strong>Strong — {signals} lines signal concrete results or achievements.</strong> "
                    "You're clearly showing outcomes, not just tasks. Review the remaining bullets "
                    "to see if any can be pushed further with a 'resulting in' or specific outcome.")
        elif signals >= 2:
            icon, icon_lbl = "📋", f"{signals} result\nsignals found"
            desc = (f"<strong>{signals} lines show results</strong>, but most of your bullets still read as responsibilities. "
                    "Recruiters want to know what changed because of you, not just what you did. "
                    "Adding outcomes to 3–4 more bullets will significantly lift this score.")
        else:
            icon, icon_lbl = "📋", "Task-oriented CV"
            desc = ("<strong>Your CV currently reads mostly as a list of responsibilities.</strong> "
                    "There is a key difference: a task says what you did; an accomplishment says what changed. "
                    "For each bullet, ask yourself: 'so what?' — what was the outcome, result or impact?")

        section("Analysis", analysis_card(icon, icon_lbl, desc))

        section("Recruiter's Insight",
            '<p style="font-size:14px;color:#4A5568;line-height:1.75;margin:0;">'
            "Any two candidates may have the same role title — what separates them is results. "
            "When a recruiter reads <em>'Managed client relationships'</em>, they learn nothing unique about you. "
            "When they read <em>'Managed 8 client accounts, achieving 95% satisfaction score'</em>, "
            "you become memorable. Even small results — a positive piece of feedback, a process you improved — "
            "are worth including."
            "</p>"
        )

        if task_lines:
            rows_html = line_rows([
                f"{l} "
                f'<span style="font-size:11px;color:#2D7DD2;font-style:italic;">→ Add: "resulting in..." or a metric</span>'
                for l in task_lines
            ])
            section("Task-oriented lines to upgrade",
                lines_card(len(task_lines), "bullets without\na clear result", "#F59E0B",
                           "These lines have strong verbs but no stated outcome — add a result:",
                           rows_html)
            )

        section("The 'Amazing Test' — is your bullet good enough?",
            '<p style="font-size:13px;color:#4A5568;line-height:1.7;margin:0 0 14px;">'
            '<strong>Imagine a 14-year-old doing a 1-week internship.</strong> If they could write the same bullet — rewrite it immediately. '
            'Ask yourself these 5 questions for every bullet:</p>'
            '<div style="display:flex;flex-direction:column;gap:8px;">'
            + "".join(
                '<div style="display:flex;gap:10px;align-items:flex-start;padding:10px 12px;'
                'background:#F8FAFF;border-radius:8px;font-size:13px;color:#1E3A5C;">'
                '<span style="font-size:16px;flex-shrink:0;">' + icon + '</span>'
                '<span>' + q + '</span></div>'
                for icon, q in [
                    ("👥", "Did you <strong>lead a team</strong>? → State the team size."),
                    ("📊", "Did you <strong>present to management or C-level</strong>? → Say so explicitly."),
                    ("💡", "Did you <strong>proactively identify a problem</strong> and develop a solution? → Make it visible."),
                    ("📈", "Are there <strong>measurable results</strong>? (%, €, time saved, people reached) → Add the number."),
                    ("🎯", "Could this bullet have been written by anyone in any role? → If yes, make it more specific."),
                ]
            )
            + '</div>'
        )

        with st.expander("How to turn tasks into accomplishments"):
            st.markdown("""
**The 'So What?' test:** After each bullet, ask: *"So what happened as a result?"*

**Formula:** `[Strong verb] + [what you did] + [the result/impact]`

**Signal words to add:**
- *resulting in, achieving, delivering, leading to, reducing, increasing*
- *recognised for, awarded, selected for*

**Quantification ideas:**
- How many people did you lead or impact?
- How much time / cost / revenue did you save or generate?
- What was the project volume (€)?
- How many clients, brands or markets did you manage?
            """)

        section("Before & After Examples", example_table([
            ("Managed social media for the finance society", "Managed social media, growing followers by 35% in one semester"),
            ("Organised team meetings and took meeting notes", "Facilitated weekly team stand-ups, improving delivery speed by 20%"),
            ("Completed financial modelling tasks", "Built 3-statement financial model used in €500k investment decision"),
            ("Represented university at external events", "Represented Nova SBE at 2 international conferences, pitching to 50+ firms"),
        ]))

        strong_examples = [
            "Independently developed a strategy with a major vendor, enabling the client to exceed market share targets by 15% for a newly introduced product line",
            "Managed the sales process of 3 brands, maintaining national exclusivity by overachieving management-set sales targets",
            "Put together and led a team of 4, developing processes that reduced aircraft turnaround time by up to 20%",
            "Analysed the supply chain of non-EU import parts, identified a €350,000 savings potential and presented findings to the plant leader",
            "Managed a team of 10 engineers and completed 6 projects (avg. volume €1M), exceeding predefined ROI for all clients by at least 40%",
        ]
        rows_ex = "".join(
            '<div style="padding:10px 12px;border-bottom:1px solid #F0F4F8;font-size:13px;color:#1E3A5C;">'
            '<span style="color:#22C55E;font-weight:700;">→ </span>' + ex + '</div>'
            for ex in strong_examples
        )
        section("Strong bullet examples",
            '<p style="font-size:13px;color:#667788;margin:0 0 12px;">These real-world examples all pass the Amazing Test — strong verb, specific action, measurable result:</p>'
            + rows_ex
        )

    elif key == "rep":
        rep_data  = data
        repeats   = rep_data.get("repeated_starts", 0)
        all_starts = [re.split(r"[\s,;]", l.strip().lower())[0] for l in lines if l.strip()]
        from collections import Counter
        freq = Counter(all_starts)
        repeated_words = {w: c for w, c in freq.items() if c >= 3 and len(w) > 2}

        if repeats == 0:
            icon, icon_lbl = "✅", "No excessive\nrepetition"
            desc = ("<strong>Good variety — no single opening verb appears more than twice in a row.</strong> "
                    "Varied verbs signal breadth of skills and keep the recruiter engaged as they scan down the page.")
        else:
            icon, icon_lbl = "🔁", f"{repeats} repeated\nverb start{'s' if repeats>1 else ''}"
            desc = (f"<strong>{repeats} verb{'s appear' if repeats>1 else ' appears'} too frequently</strong> "
                    "at the start of your bullets. Repetition makes a CV feel lazy and one-dimensional. "
                    "Recruiters notice — variety in opening verbs signals breadth of experience and skills.")

        section("Analysis", analysis_card(icon, icon_lbl, desc))

        section("Recruiter's Insight",
            '<p style="font-size:14px;color:#4A5568;line-height:1.75;margin:0;">'
            "When every other bullet starts with 'Led' or 'Managed', the recruiter's eye stops registering the content. "
            "Each verb is a signal: <strong>Led</strong> = management, <strong>Analysed</strong> = analytical thinking, "
            "<strong>Built</strong> = delivery, <strong>Negotiated</strong> = influence. "
            "Variety in verbs tells a richer story about who you are."
            "</p>"
        )

        if repeated_words:
            rows_html = line_rows([
                f'<strong style="color:#EF4444;">{w.capitalize()}</strong> — used {c}× '
                f'<span style="font-size:11px;color:#2D7DD2;">(aim for max 2×)</span>'
                for w, c in sorted(repeated_words.items(), key=lambda x: -x[1])[:6]
            ])
            section("Overused opening words",
                lines_card(len(repeated_words), "verbs used\n3+ times", "#EF4444",
                           "Replace some of these repeated openers with alternatives from the verb library:",
                           rows_html)
            )

        with st.expander("Alternatives for the most common verbs"):
            st.markdown("""
| Overused | Alternatives |
|----------|-------------|
| Led | Spearheaded, Directed, Championed, Orchestrated |
| Managed | Oversaw, Administered, Coordinated, Supervised |
| Developed | Built, Created, Designed, Launched, Established |
| Worked on | Executed, Delivered, Implemented, Drove |
| Analysed | Evaluated, Assessed, Researched, Investigated |

→ Check the **Action Verbs** page for the full library by category.
            """)

        section("Before & After Examples", example_table([
            ("Led the project, led the team, led the presentation", "Led the project, Directed the team, Presented findings to stakeholders"),
            ("Managed events, managed the budget, managed communications", "Organised events, Budgeted €5k across 3 activities, Liaised with external partners"),
        ]))

    elif key == "ln":
        wc         = data.get("word_count", result.get("word_count", 0))
        page_count = result.get("page_count", 1)
        if wc < 200:
            icon, icon_lbl = "📄", f"{wc} words\n(too short)"
            desc = (f"<strong>Your CV has only {wc} words — this is quite short.</strong> "
                    "A student CV should demonstrate your experience, education and skills clearly. "
                    "Aim to expand your bullet points with more detail and quantification.")
        elif wc <= 800:
            icon, icon_lbl = "✅", f"{wc} words\n(ideal range)"
            desc = (f"<strong>Your CV is {wc} words — well within the ideal range of 300–800.</strong> "
                    "This signals focus and the ability to prioritise. Keep it concise as you add more experience.")
        elif wc <= 1100:
            icon, icon_lbl = "⚠️", f"{wc} words\n(slightly long)"
            desc = (f"<strong>At {wc} words, your CV is slightly long for a student.</strong> "
                    "Recruiters at top firms often spend under 30 seconds per CV. "
                    "Cutting to under 800 words will make every line feel more intentional.")
        else:
            icon, icon_lbl = "📚", f"{wc} words\n(too long)"
            desc = (f"<strong>Your CV is {wc} words — significantly over the recommended limit.</strong> "
                    "For a student, 1 clean, focused page is always better than 2 padded ones. "
                    "Cut old or irrelevant experience and tighten every bullet to its essential message.")

        pc_ok    = page_count <= 2
        pc_color = "#16A34A" if pc_ok else "#D97706"
        pc_note  = (f'<div style="margin-top:14px;padding:10px 14px;border-radius:8px;'
                    f'background:{"#F0FDF4" if pc_ok else "#FFFBEB"};'
                    f'font-size:13px;color:{pc_color};">'
                    f'{"✅" if pc_ok else "⚠️"} &nbsp;'
                    f'<strong>Page count:</strong> your CV is '
                    f'<strong>{page_count} page{"s" if page_count > 1 else ""}</strong>'
                    + (" — within the 1–2 page limit." if pc_ok else " — aim for a maximum of 2 pages.")
                    + '</div>')
        section("Analysis", analysis_card(icon, icon_lbl, desc) + pc_note)

        section("Recruiter's Insight",
            '<p style="font-size:14px;color:#4A5568;line-height:1.75;margin:0;">'
            "A student CV should be <strong>one page</strong>. Recruiters at McKinsey, Goldman and the Big 4 "
            "receive hundreds of CVs per role. The ability to distil your experience into one focused page "
            "is itself a signal of communication skills. Every extra line risks diluting your strongest points."
            "</p>"
        )

        long_lines = sorted([l for l in lines if len(l.split()) > 25], key=lambda x: -len(x.split()))[:5]
        if long_lines:
            rows_html = line_rows([
                f'{l[:120]}{"..." if len(l)>120 else ""} '
                f'<span style="font-size:11px;color:#2D7DD2;">({len(l.split())} words)</span>'
                for l in long_lines
            ])
            section("Longest lines — candidates to trim",
                lines_card(len(long_lines), "verbose\nlines", "#F59E0B",
                           "These lines are the wordiest — see if any can be shortened without losing meaning:",
                           rows_html)
            )

        with st.expander("How to cut word count without losing impact"):
            st.markdown("""
- **Remove the context, keep the action:** "As part of my role in the marketing team, I helped to organise..." → "Organised..."
- **Cut adverbs:** "successfully delivered", "efficiently managed" → just "Delivered", "Managed"
- **One idea per bullet:** Split long bullets into two shorter ones, or merge redundant ones
- **Remove old experience:** Pre-university roles rarely add value for student CVs
- **Cut the objective/summary section:** Recruiters skip it — use the space for an extra achievement
            """)

        section("Before & After Examples", example_table([
            ("As part of my responsibilities, I was in charge of making sure all the team members were updated on the project status on a weekly basis",
             "Managed weekly project status updates for a 6-person team"),
            ("I have been involved in various different activities both inside and outside the university setting",
             "Active in 3 extracurriculars: consulting club, finance society, debate team"),
        ]))

    elif key == "fw":
        fw_data    = data
        fill_found = fw_data.get("filler_found", [])
        fill_lines = [l for l in lines if any(f in l.lower() for f in fill_found)]

        if not fill_found:
            icon, icon_lbl = "✅", "No filler words\ndetected"
            desc = ("<strong>No filler words found — your writing is clean and direct.</strong> "
                    "Every word in your CV earns its place. This is a hallmark of clear, professional writing.")
        elif len(fill_found) <= 2:
            icon, icon_lbl = "⚠️", f"{len(fill_found)} filler phrase{'s' if len(fill_found)>1 else ''}"
            desc = (f"<strong>{len(fill_found)} filler phrase{'s' if len(fill_found)>1 else ''} found: "
                    f"{', '.join(fill_found)}.</strong> "
                    "These add length without adding meaning. Simply deleting them makes each sentence sharper.")
        else:
            icon, icon_lbl = "🗑️", f"{len(fill_found)} filler phrases"
            desc = (f"<strong>{len(fill_found)} filler phrases detected.</strong> "
                    "Phrases like 'various', 'in order to', 'a number of' dilute your writing. "
                    "Each one removed makes your CV more direct and confident.")

        section("Analysis", analysis_card(icon, icon_lbl, desc))

        section("Recruiter's Insight",
            '<p style="font-size:14px;color:#4A5568;line-height:1.75;margin:0;">'
            "Filler words are a sign of uncertainty — they soften statements that should be direct. "
            "<em>'Worked on various projects'</em> tells a recruiter nothing. "
            "<em>'Delivered 3 client projects in consulting and fintech'</em> is specific and confident. "
            "The rule: if removing a word doesn't change the meaning, remove it."
            "</p>"
        )

        if fill_lines:
            rows_html = line_rows([
                f'{l} <span style="font-size:11px;color:#2D7DD2;font-style:italic;">→ remove the filler, be specific</span>'
                for l in fill_lines[:5]
            ])
            section("Lines containing filler words",
                lines_card(len(fill_lines), "affected\nlines", "#F59E0B",
                           "Remove or replace the highlighted filler words in these lines:",
                           rows_html)
            )
        elif fill_found:
            section("Filler words found",
                '<div style="font-size:13px;color:#667788;padding:8px 0;">'
                + "".join(f'<span class="pill-orange" style="margin:3px;">{f}</span>' for f in fill_found)
                + '</div>'
            )

        with st.expander("Common fillers and what to write instead"):
            st.markdown("""
| Filler | Better alternative |
|--------|--------------------|
| various / several | Specify a number: "3 projects", "5 clients" |
| in order to | just "to" |
| a number of | give the number |
| due to the fact that | "because" |
| on a daily basis | "daily" |
| with regard to | "on" / "for" |
| and so on / etc. | list the items specifically |
            """)

        section("Before & After Examples", example_table([
            ("Worked on various projects in order to develop my skills", "Delivered 3 client projects in strategy and operations"),
            ("Responsible for a number of different tasks related to communications", "Managed social media, newsletters and press releases"),
        ]))

    elif key == "bc":
        bc_data = data
        count   = bc_data.get("bullet_count", 0)

        if 8 <= count <= 25:
            icon, icon_lbl = "✅", f"{count} bullet\npoints"
            desc = (f"<strong>{count} bullet points — right in the sweet spot.</strong> "
                    "This signals that you have real experience to talk about and can prioritise: "
                    "not so many that it looks padded, not so few that it looks thin.")
        elif count < 5:
            icon, icon_lbl = "📋", f"Only {count} bullet\npoints"
            desc = (f"<strong>Your CV has only {count} bullet point{'s' if count!=1 else ''}.</strong> "
                    "This may suggest limited experience — but more likely you're under-representing what you've done. "
                    "Add 2–4 bullets per role or activity, focusing on what you delivered.")
        elif count < 8:
            icon, icon_lbl = "⚠️", f"{count} bullet points\n(slightly low)"
            desc = (f"<strong>{count} bullets is slightly below the ideal range of 8–25.</strong> "
                    "Try to add 1–2 more bullets across your most relevant roles, focusing on specific outcomes.")
        else:
            icon, icon_lbl = "⚠️", f"{count} bullet points\n(too many)"
            desc = (f"<strong>{count} bullets is above the recommended maximum of 25.</strong> "
                    "Too many bullets dilutes each individual achievement. Aim to cut the weakest ones "
                    "and consolidate similar points.")

        section("Analysis", analysis_card(icon, icon_lbl, desc))

        section("Recruiter's Insight",
            '<p style="font-size:14px;color:#4A5568;line-height:1.75;margin:0;">'
            "The right number of bullets signals judgement. Too few implies a thin CV; too many implies "
            "an inability to edit. A strong student CV typically has <strong>2–4 bullets per role</strong>, "
            "with more bullets for significant positions and fewer for minor ones. "
            "Quality always beats quantity — one strong quantified bullet is worth three vague ones."
            "</p>"
        )

        with st.expander("How to decide which bullets to keep or cut"):
            st.markdown("""
**Rule per role:** minimum 2 bullets (1 looks odd), maximum 3–5 bullets per position.

**Keep a bullet if it:**
- Starts with a strong action verb
- Shows a concrete result or scale
- Is unique to this role (not generic)

**Cut a bullet if it:**
- Sounds like a job description, not an achievement
- Repeats something already covered
- Is more than 30 words (split or trim instead)

**Rule of thumb:** Major internship / full-time role = 3–5 bullets. Minor or short role = 2–3 bullets.
            """)

        section("Before & After Examples", example_table([
            ("(5 bullets for a minor student society role)", "(2 bullets: the most impactful achievements only)"),
            ("(1 bullet for a 6-month internship)", "(3–4 bullets: break down into specific projects and results)"),
        ]))

    elif key == "bl":
        bl_data = data
        avg_w   = bl_data.get("avg_bullet_words", 0)
        bullet_lines = [l.strip() for l in raw.split("\n") if l.strip().startswith(("•", "-", "–", "▪"))]
        long_bullets = [l for l in bullet_lines if len(l.split()) > 28]

        if 8 <= avg_w <= 28:
            icon, icon_lbl = "✅", f"Avg {avg_w} words\nper bullet"
            desc = (f"<strong>Your average bullet length is {avg_w} words — ideal.</strong> "
                    "Short enough to scan in one pass, long enough to convey substance. Keep this up.")
        elif avg_w > 28:
            icon, icon_lbl = "📖", f"Avg {avg_w} words\nper bullet (long)"
            desc = (f"<strong>Your bullets average {avg_w} words — too long.</strong> "
                    "Long bullets lose the reader mid-way. Each bullet should communicate one clear idea "
                    "in a single scannable line.")
        else:
            icon, icon_lbl = "📝", f"Avg {avg_w} words\nper bullet (short)"
            desc = (f"<strong>Your bullets average only {avg_w} words — too brief.</strong> "
                    "Very short bullets often lack context or quantification. Try adding the scale or result.")

        section("Analysis", analysis_card(icon, icon_lbl, desc))

        section("Recruiter's Insight",
            '<p style="font-size:14px;color:#4A5568;line-height:1.75;margin:0;">'
            "Recruiters scan, they don't read. A bullet that's too long forces them to slow down — "
            "and they won't. The sweet spot is <strong>12–20 words</strong>: enough to include "
            "a verb, an action and a result. If a bullet needs more, split it into two. "
            "If it needs less, it probably isn't strong enough to include."
            "</p>"
        )

        if long_bullets:
            rows_html = line_rows([
                f'{l[:130]}{"..." if len(l)>130 else ""} '
                f'<span style="font-size:11px;color:#EF4444;">({len(l.split())} words — aim for ≤20)</span>'
                for l in long_bullets[:5]
            ])
            section("Long bullets to trim",
                lines_card(len(long_bullets), "bullets over\n25 words", "#EF4444",
                           "Each of these can be shortened without losing the key information:",
                           rows_html)
            )

        with st.expander("How to trim a long bullet"):
            st.markdown("""
**Step 1:** Cut the context/background — start with the action
**Step 2:** Remove adverbs ("effectively", "successfully", "proactively")
**Step 3:** Replace phrases with single words: "in order to" → "to", "was responsible for" → the verb itself
**Step 4:** If there are two distinct ideas, split into two bullets

**Target format:** `[Verb] + [what] + [result/scale]` in under 20 words
            """)

        section("Before & After Examples", example_table([
            ("As the treasurer of the finance society, I was responsible for making sure that all the income and expenditure of the society was properly tracked and recorded throughout the year",
             "Managed €8,000 annual budget for 200-member finance society, maintaining full audit trail"),
            ("Led", "Led 4-person team to deliver consulting project for local NGO"),
        ]))

    elif key == "sec":
        sec_data = data
        found   = sec_data.get("sections_found", [])
        missing = sec_data.get("sections_missing", [])

        if not missing:
            icon, icon_lbl = "✅", f"{len(found)} sections\ndetected"
            desc = ("<strong>All key sections are present.</strong> "
                    "Your CV has a clear, complete structure that recruiters can navigate instantly. "
                    "Make sure each section is clearly and consistently labelled.")
        elif len(missing) <= 2:
            icon, icon_lbl = "⚠️", f"{len(missing)} section{'s' if len(missing)>1 else ''}\nmissing"
            desc = (f"<strong>Most key sections are present, but {len(missing)} "
                    f"section{'s are' if len(missing)>1 else ' is'} missing: "
                    f"{', '.join(missing)}.</strong> "
                    "Adding these will make your CV easier for recruiters to read quickly.")
        else:
            icon, icon_lbl = "📋", f"{len(missing)} sections\nmissing"
            desc = (f"<strong>{len(missing)} key sections are missing from your CV.</strong> "
                    "Recruiters have a mental map of a CV — they look for specific sections in specific places. "
                    "Missing sections slow them down and may suggest a less experienced candidate.")

        section("Analysis", analysis_card(icon, icon_lbl, desc))

        section("Recruiter's Insight",
            '<p style="font-size:14px;color:#4A5568;line-height:1.75;margin:0;">'
            "A clear section structure helps recruiters find information in under 3 seconds. "
            "The standard order for a <strong>student CV</strong> is: "
            "<strong>Education → Experience → Activities/Extracurriculars → Skills</strong>. "
            "Use clear, bold headers. Avoid creative section names ('My Journey') — stick to conventional labels."
            "</p>"
        )

        found_pills  = "".join(f'<span class="pill-green" style="margin:3px;">{s.title()}</span>' for s in found)
        missing_pills= "".join(f'<span class="pill-red" style="margin:3px;">{s.title()}</span>' for s in missing)

        body = (
            '<div style="display:flex;gap:32px;flex-wrap:wrap;">'
            '<div><div style="font-size:11px;font-weight:700;color:#22C55E;letter-spacing:0.8px;margin-bottom:8px;">DETECTED</div>'
            + (found_pills or '<span style="color:#889AAA;font-size:13px;">None</span>') + '</div>'
            '<div><div style="font-size:11px;font-weight:700;color:#EF4444;letter-spacing:0.8px;margin-bottom:8px;">MISSING</div>'
            + (missing_pills or '<span style="color:#22C55E;font-size:13px;">All present ✓</span>') + '</div>'
            '</div>'
        )
        section("Section Checklist", body)

        with st.expander("Recommended CV section structure"):
            st.markdown("""
**Standard section order:**
1. **Experience** (or Work Experience) — once you have internships/jobs
2. **Education** — degree type (M.Sc., B.Sc., etc.), university, GPA if strong, class rank if available
3. **Extracurricular & Awards** — societies, scholarships, competitions, leadership roles
4. **Additional Information & Skills** — languages, software, interests

*Still in your first year with no internships yet? Put Education first, then move Experience up once you have roles to show.*

**Education — what to include:**
- State the degree type explicitly: M.Sc., B.Sc., B.A., etc.
- Include your GPA / grade with a local scale (e.g. "GPA: 17/20" or "1.8 (German scale)")
- Add class rank if possible: "Top 10% of cohort", "Top 5% in Finance courses"
- Always include Abitur / High School — skip primary school

**Skills — how to write it:**
- **Languages:** always state the proficiency level — e.g. *German (Native), English (C1), French (B2)*
- **Computer Skills:** be specific, not generic. Instead of "Microsoft Office": *"PowerPoint (C-Level decks), Excel (financial modelling)"*
- **Interests:** include at least one specific interest that invites a follow-up question — e.g. *"Piano (performed for 1,000+ people at Christmas concerts)"* not just *"Music"*

**Avoid:** photos, date of birth, marital status (in most Western countries)
            """)

    elif key == "pp":
        pp_data    = data
        pron_count = pp_data.get("pronouns_found", 0)
        pron_lines = [l for l in lines if any(re.search(p, l, re.IGNORECASE) for p in PERSONAL_PRONOUNS)]

        if pron_count == 0:
            icon, icon_lbl = "✅", "No personal\npronouns"
            desc = ("<strong>No personal pronouns detected — perfect.</strong> "
                    "Your CV follows the professional convention correctly. "
                    "Every bullet is written in the implied first-person without using 'I', 'my' or 'we'.")
        elif pron_count == 1:
            icon, icon_lbl = "⚠️", "1 pronoun\nfound"
            desc = ("<strong>1 personal pronoun found.</strong> "
                    "This is a minor issue — a quick fix. Simply delete the pronoun and the sentence "
                    "reads more professionally immediately.")
        else:
            icon, icon_lbl = "🔴", f"{pron_count} pronouns\nfound"
            desc = (f"<strong>{pron_count} personal pronouns detected.</strong> "
                    "Using 'I', 'my' or 'we' in a CV breaks a universal professional convention. "
                    "Any recruiter will notice — it signals unfamiliarity with CV writing standards.")

        section("Analysis", analysis_card(icon, icon_lbl, desc))

        section("Recruiter's Insight",
            '<p style="font-size:14px;color:#4A5568;line-height:1.75;margin:0;">'
            "CV writing uses an implied first person — the reader understands every bullet is about you. "
            "Writing <em>'I led a team'</em> is redundant and looks amateurish. "
            "Writing <em>'Led a team'</em> is direct, professional and 3 words shorter. "
            "This rule is universal across all industries and every recruiter knows it."
            "</p>"
        )

        if pron_lines:
            rows_html = line_rows([
                f'<span style="color:#EF4444;">{l}</span>'
                f'<span style="font-size:11px;color:#059669;display:block;margin-top:3px;">→ Fix: '
                + re.sub(r'\b(I|me|my|mine|myself|we|our|ours|ourselves)\b', '<del>\\g<0></del>', l, flags=re.IGNORECASE)
                + '</span>'
                for l in pron_lines[:5]
            ])
            section("Lines to fix",
                lines_card(len(pron_lines), "lines with\npronouns", "#EF4444",
                           "Remove the pronoun from each of these lines — the fix takes seconds:",
                           rows_html)
            )

        with st.expander("Common pronoun fixes"):
            st.markdown("""
| ❌ With pronoun | ✅ Fixed |
|----------------|---------|
| I led a team of 5 | Led a team of 5 |
| My role was to manage client relationships | Managed client relationships |
| I was responsible for data analysis | Conducted data analysis |
| We developed a new process | Developed a new process |
| In my spare time, I volunteer at... | Volunteer at... (in Activities section) |
            """)

        section("Before & After Examples", example_table([
            ("I led the project and managed a team of 6 people", "Led the project and managed a team of 6"),
            ("My responsibilities included managing client communications", "Managed client communications across 8 accounts"),
            ("We successfully delivered the final presentation to the board", "Delivered final board presentation to 12 senior stakeholders"),
        ]))

    elif key == "bw":
        bw_data  = data
        bw_found = bw_data.get("buzzwords_found", [])

        if not bw_found:
            icon, icon_lbl = "✅", "No buzzwords\ndetected"
            desc = ("<strong>No buzzwords or clichés found — excellent.</strong> "
                    "Your CV makes specific claims rather than relying on empty adjectives. "
                    "This is a strong signal of a well-written, evidence-based CV.")
        elif len(bw_found) <= 2:
            icon, icon_lbl = "⚠️", f"{len(bw_found)} buzzword{'s' if len(bw_found)>1 else ''}"
            desc = (f"<strong>{len(bw_found)} buzzword{'s' if len(bw_found)>1 else ''} found: "
                    f"{', '.join(bw_found)}.</strong> "
                    "Minor issue — replace with a specific, evidenced claim and this score jumps immediately.")
        else:
            icon, icon_lbl = "🗑️", f"{len(bw_found)} buzzwords"
            desc = (f"<strong>{len(bw_found)} overused buzzwords detected.</strong> "
                    "Phrases like 'passionate', 'hardworking' and 'results-driven' appear in over 70% of CVs. "
                    "Recruiters have learned to ignore them — they add no information. "
                    "Replace each one with specific evidence of the trait.")

        section("Analysis", analysis_card(icon, icon_lbl, desc))

        section("Recruiter's Insight",
            '<p style="font-size:14px;color:#4A5568;line-height:1.75;margin:0;">'
            "Buzzwords are a signal of insecurity — candidates use them when they don't have specific evidence. "
            "Every recruiter has read 'passionate about finance' hundreds of times. "
            "Instead, <em>prove</em> the passion: <em>'Completed CFA Level 1 while studying full-time'</em>. "
            "The same applies to every adjective — show the evidence, cut the label."
            "</p>"
        )

        if bw_found:
            evidence = {
                "passionate":    "Show it: 'Completed [course/certification] in X'",
                "hardworking":   "Show it: 'Delivered X under Y-week deadline'",
                "team player":   "Show it: 'Collaborated with 5-person team to deliver Z'",
                "motivated":     "Remove entirely — or replace with a concrete achievement",
                "results-driven":"Show a result: 'Grew X by Y%, delivered Z ahead of schedule'",
                "innovative":    "Show it: 'Designed a new process that reduced time by 30%'",
                "proactive":     "Show it: 'Identified gap in X and proposed solution adopted by team'",
                "dynamic":       "Remove — replace with a specific skill or achievement",
                "synergy":       "Remove entirely",
                "go-getter":     "Remove — show ambition through achievements instead",
            }
            rows_html = line_rows([
                f'<strong style="color:#EF4444;">"{bw}"</strong> — '
                + evidence.get(bw.lower(), f"Replace with specific evidence of this trait")
                for bw in bw_found[:6]
            ])
            section("Buzzwords to replace",
                lines_card(len(bw_found), "buzzwords\nto remove", "#EF4444",
                           "Each buzzword should be replaced with a specific, evidenced claim:",
                           rows_html)
            )

        with st.expander("Show don't tell — replacement guide"):
            st.markdown("""
| ❌ Buzzword | ✅ Evidence-based replacement |
|------------|------------------------------|
| Passionate about X | Completed [course] in X / Founded [project] in X |
| Hardworking | Delivered [project] under [tight deadline] |
| Team player | Collaborated with [N]-person team to deliver [outcome] |
| Results-driven | [Specific result with number] |
| Strong communicator | Presented to [audience of N] / Published [article] |
| Leadership skills | Led a team of [N] to [outcome] |
            """)

        section("Before & After Examples", example_table([
            ("Passionate about finance and investment", "Completed Bloomberg Market Concepts; managing personal investment portfolio since 2022"),
            ("A hardworking team player with strong communication skills", "Delivered 3 team projects under 2-week deadlines; presented findings to 40+ faculty members"),
            ("Results-driven individual looking to add value", "Increased event attendance by 35% as VP of Marketing for the Finance Society"),
        ]))

    elif key == "act":
        act_data   = data
        pass_count = act_data.get("passive_constructions", 0)
        pass_lines = [l for l in lines if any(re.search(p, l, re.IGNORECASE) for p in PASSIVE_INDICATORS)]

        if pass_count == 0:
            icon, icon_lbl = "✅", "No passive\nconstructions"
            desc = ("<strong>No passive voice detected — your CV is written in active, confident language.</strong> "
                    "Active voice is a hallmark of strong professional writing. Every bullet starts with a direct action.")
        elif pass_count <= 2:
            icon, icon_lbl = "⚠️", f"{pass_count} passive\nconstruction{'s' if pass_count>1 else ''}"
            desc = (f"<strong>{pass_count} passive construction{'s' if pass_count>1 else ''} found.</strong> "
                    "This is a minor fix — flipping a passive to active takes 5 seconds per line "
                    "and immediately makes the bullet sound more confident.")
        else:
            icon, icon_lbl = "🔴", f"{pass_count} passive\nconstructions"
            desc = (f"<strong>{pass_count} passive voice constructions detected.</strong> "
                    "Active voice is direct: 'Led a team.' Passive voice is indirect: 'A team was led.' "
                    "Passive constructions make you sound like a bystander in your own achievements.")

        section("Analysis", analysis_card(icon, icon_lbl, desc))

        section("Recruiter's Insight",
            '<p style="font-size:14px;color:#4A5568;line-height:1.75;margin:0;">'
            "Active voice puts you at the centre of the action. "
            "<em>'Reports were written'</em> could be written by anyone. "
            "<em>'Wrote monthly performance reports'</em> is yours. "
            "Top CVs are written almost entirely in active voice — it signals confidence, clarity and ownership."
            "</p>"
        )

        if pass_lines:
            rows_html = line_rows([
                f'<span style="color:#EF4444;">{l}</span>'
                f'<span style="font-size:11px;color:#2D7DD2;font-style:italic;display:block;margin-top:3px;">→ Flip: remove "was/were", use the direct verb</span>'
                for l in pass_lines[:5]
            ])
            section("Passive constructions to flip",
                lines_card(len(pass_lines), "passive voice\nlines", "#EF4444",
                           "Each of these can be flipped to active voice in seconds:",
                           rows_html)
            )

        with st.expander("How to spot and fix passive voice"):
            st.markdown("""
**Passive pattern:** `was/were + [past participle]`
**Active fix:** delete "was/were", make the subject the actor

| ❌ Passive | ✅ Active |
|-----------|---------|
| Reports were written by me | Wrote monthly performance reports |
| The project was managed by our team | Managed the project with a 4-person team |
| I was tasked with analysing the data | Analysed dataset of 5,000 rows |
| Events were organised and run | Organised and ran 6 annual events |

**'Was responsible for'** is always passive → just use the verb:
*'Was responsible for managing clients'* → *'Managed 8 client accounts'*
            """)

        section("Before & After Examples", example_table([
            ("Was tasked with researching new market opportunities", "Researched 5 new market opportunities for €10M expansion plan"),
            ("Reports were written and distributed to the management team", "Wrote and distributed weekly performance reports to 12 senior managers"),
            ("Was involved in the organisation of the annual conference", "Co-organised annual conference for 300+ participants"),
        ]))

    elif key == "dat":
        dat_data = data
        formats  = dat_data.get("formats_detected", [])
        fmt_map  = {
            "month_year_long":  "Full month name (January 2024)",
            "month_year_short": "Abbreviated month (Jan 2024)",
            "mm_yyyy":          "Numeric month (01/2024)",
            "yyyy":             "Year only (2024)",
        }

        if len(formats) <= 1:
            icon, icon_lbl = "✅", "Consistent\ndate format"
            desc = ("<strong>Dates are formatted consistently throughout your CV.</strong> "
                    "This signals attention to detail — exactly what top employers screen for.")
        elif len(formats) == 2:
            icon, icon_lbl = "⚠️", "2 date formats\ndetected"
            desc = ("<strong>2 different date formats found.</strong> "
                    "Pick one and apply it consistently. The recommended format is: <em>Jan 2024 – Jun 2024</em>.")
        else:
            icon, icon_lbl = "🔴", f"{len(formats)} date formats\ndetected"
            desc = (f"<strong>{len(formats)} different date formats used across your CV.</strong> "
                    "Inconsistent dates are a classic attention-to-detail red flag. "
                    "A recruiter notices this immediately — it signals careless proofreading.")

        section("Analysis", analysis_card(icon, icon_lbl, desc))

        section("Recruiter's Insight",
            '<p style="font-size:14px;color:#4A5568;line-height:1.75;margin:0;">'
            "Date formatting is a proxy for attention to detail. "
            "Recruiters — especially at consulting, finance and law firms — use these signals to filter. "
            "If you mix <em>Jan 2024</em> and <em>January 2024</em> and <em>01/2024</em> in the same CV, "
            "it tells the reader you haven't proofread carefully. The fix takes 5 minutes."
            "</p>"
        )

        if len(formats) > 1:
            rows_html = line_rows([
                f'<strong>{fmt_map.get(f, f)}</strong> — detected in your CV'
                for f in formats
            ])
            section("Date formats found",
                lines_card(len(formats), "formats\ndetected", "#F59E0B" if len(formats)==2 else "#EF4444",
                           "These date formats were found — standardise to one:",
                           rows_html)
            )

        with st.expander("Recommended date format and rules"):
            st.markdown("""
**Recommended format:** `Jan 2024 – Jun 2024`

**Rules:**
1. Use the same format for every single date in your CV
2. For ongoing roles: `Jan 2024 – Present`
3. For education: `Sep 2022 – Jun 2025 (expected)`
4. If year-only: just `2023 – 2024` (consistent throughout)

**Most common mistake:** mixing "January 2024" and "Jan 2024" — pick one.
            """)

        section("Before & After Examples", example_table([
            ("Goldman Sachs — June 2024 to Aug 2024 / McKinsey — 01/2024–03/2024", "Goldman Sachs — Jun 2024 – Aug 2024 / McKinsey — Jan 2024 – Mar 2024"),
            ("2023 — 2024 (Finance Society) / September 2022 – Present (Volunteer)", "Sep 2022 – Present (Volunteer) / Sep 2023 – Jun 2024 (Finance Society)"),
        ]))


# =============================================================================
# CAREER READINESS
# =============================================================================
def _career_readiness(career_key):
    career = CAREER_PATHS[career_key]
    result = st.session_state.cv_result

    st.markdown(f"""
    <div class="page-header">
        <h1>🎯 Career Readiness — {career['name']}</h1>
        <p>Your personalised overview based on real Nova SBE alumni, courses and employers.</p>
    </div>""", unsafe_allow_html=True)

    if not result or not result.get("raw_text"):
        st.markdown("""
        <div style="background:white;border-radius:14px;padding:28px 32px;
                    border:1px solid #E8EFF8;box-shadow:0 2px 12px rgba(10,22,40,0.06);">
          <div style="font-size:15px;font-weight:600;color:#0A1628;margin-bottom:8px;">Upload your CV first</div>
          <div style="font-size:13px;color:#667788;">Career Readiness matches your CV against real alumni, courses and employers.</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        if st.button("← Upload CV", type="primary"):
            go_to("upload"); st.rerun()
        return

    data         = analyze_career_readiness(cv_text=result["raw_text"], career_key=career_key, cv_result=result)
    score        = data["score"]
    strengths    = data["strengths"]
    gaps         = data["gaps"]
    courses      = data["courses"]
    clubs        = data.get("clubs", [])
    alumni            = data["alumni"]
    alumni_ai         = data.get("alumni_ai", False)
    employers         = data["employers"]
    employers_ai      = data.get("employers_ai", False)
    score_ai          = data.get("score_ai", False)
    score_explanation = data.get("score_explanation", "")
    quick_win         = data["quick_win"]
    criteria_met      = data["criteria_met"]
    _gr = st.session_state.get("gemini_result") or {}
    if _gr.get("strengths"): strengths = _gr["strengths"]
    if _gr.get("gaps"):      gaps      = _gr["gaps"]
    if _gr.get("quick_win"): quick_win = _gr["quick_win"]

    score_color   = "#22C55E" if score >= 72 else "#F59E0B" if score >= 50 else "#EF4444"
    circumference = 2 * 3.14159 * 54
    dash_offset   = circumference * (1 - score / 100)

    # ── Row 1: Score + Criteria ───────────────────────────────────────────────
    c_ring, c_crit = st.columns([1, 2], gap="large")

    with c_ring:
        st.markdown(f"""
        <div style="background:white;border-radius:16px;padding:28px 20px;text-align:center;
                    border:1px solid #E4ECF4;box-shadow:0 2px 16px rgba(10,22,40,0.06);">
          <div style="font-size:10px;font-weight:700;color:#AAB8C8;letter-spacing:1.2px;
                      text-transform:uppercase;margin-bottom:14px;">Career Readiness Score</div>
          <svg width="140" height="140" viewBox="0 0 140 140" style="display:block;margin:0 auto;">
            <circle cx="70" cy="70" r="54" fill="none" stroke="#EEF2F8" stroke-width="10"/>
            <circle cx="70" cy="70" r="54" fill="none" stroke="{score_color}" stroke-width="10"
              stroke-dasharray="{circumference:.1f}" stroke-dashoffset="{dash_offset:.1f}"
              stroke-linecap="round" transform="rotate(-90 70 70)"/>
            <text x="70" y="65" text-anchor="middle" dominant-baseline="middle"
              font-size="32" font-weight="800" fill="{score_color}" font-family="Inter,sans-serif">{score}</text>
            <text x="70" y="88" text-anchor="middle" dominant-baseline="middle"
              font-size="11" fill="#AAB8C8" font-family="Inter,sans-serif">out of 100</text>
          </svg>
          <div style="font-size:11px;color:#AAB8C8;margin-top:12px;">{"✨ AI-assessed for this career path" if score_ai else "Based on CV quality + employer criteria"}</div>
          {('<div style="font-size:11px;color:#445566;margin-top:10px;line-height:1.5;text-align:left;'
            'background:#F8FAFF;border-radius:8px;padding:10px 12px;">'
            + score_explanation + '</div>') if score_ai and score_explanation else ""}
        </div>""", unsafe_allow_html=True)

    with c_crit:
        _CRIT_BY_PATH = {
            "consulting": {
                "relevant_experience": ("Consulting experience",        "Direct consulting or strategy experience is the #1 screening criterion at MBB and top-tier firms."),
                "case_prep":           ("Case competition / club",       "MBB and tier-2 firms look directly for Nova Case Team, SBE Social Consulting, or case competition experience."),
                "leadership":          ("Leadership role",               "Employers screen for leadership — team lead, club president, or event organiser all count."),
                "gpa":                 ("GPA (16/20 or above)",          "Most consulting firms have a GPA threshold around 16/20 as a first screening filter."),
                "international":       ("International experience",      "An exchange semester or international internship is a strong differentiator for globally recruiting firms."),
                "extracurricular":     ("Extracurricular activity",      "Club membership, volunteering, or societies show engagement beyond academics."),
            },
            "investment_banking": {
                "relevant_experience": ("Finance / IB internship",       "A finance or IB internship is the single most critical signal — without it, most applications are filtered out."),
                "internship":          ("Any internship experience",      "Even non-finance internships show professional exposure and work ethic."),
                "leadership":          ("Leadership role",                "IB firms value initiative — club treasurer, team lead, or any role managing others counts."),
                "gpa":                 ("GPA (17/20+ preferred)",         "Most bulge-bracket banks set a high GPA bar. A 17/20 or above puts you in a competitive range."),
                "international":       ("International experience",       "IB is a global industry — international exposure, languages, or exchange programmes are a real advantage."),
                "extracurricular":     ("Finance club / extracurricular", "Nova Finance Club or Investment Group membership is a direct signal of genuine interest in finance."),
            },
            "tech": {
                "relevant_experience": ("Tech internship / project",     "A tech internship or hands-on technical project is the strongest signal for tech employers."),
                "internship":          ("Any internship experience",      "Any professional experience demonstrates initiative and a working understanding of business environments."),
                "leadership":          ("Leadership or product ownership","Leading a project, team, or product — even in a club context — shows the ownership mindset tech firms value."),
                "gpa":                 ("GPA (signal of rigour)",         "GPA matters less in tech than in banking, but a strong grade still signals the ability to learn fast."),
                "international":       ("International exposure",         "Cross-cultural experience is valued at global tech companies and helps in collaborative team environments."),
                "extracurricular":     ("Hackathons / tech clubs",        "Hackathon participation, coding clubs, or data science competitions show passion beyond the classroom."),
            },
            "entrepreneurship": {
                "relevant_experience": ("Own venture or startup",         "Having started or co-founded something — even a small project — is the strongest signal in entrepreneurship."),
                "internship":          ("Startup or business internship", "Working at a startup or in a business role shows you understand how companies operate under pressure."),
                "leadership":          ("Leadership & ownership",         "Taking ownership of initiatives — whether a club, event, or project — is the core entrepreneurial signal."),
                "extracurricular":     ("Entrepreneurship club / society","Nova Entrepreneurs Club or similar involvement shows genuine drive and access to a startup network."),
                "international":       ("International exposure",         "Exposure to different markets and cultures broadens the commercial thinking that entrepreneurs need."),
                "gpa":                 ("GPA (less critical here)",       "GPA matters less for entrepreneurship than execution and initiative — but a decent grade still helps."),
            },
            "marketing": {
                "relevant_experience": ("Marketing / brand internship",  "A marketing or brand internship is the clearest signal for FMCG, agency, and brand management roles."),
                "internship":          ("Any internship experience",      "Any internship shows professional exposure and the ability to work in a structured business environment."),
                "leadership":          ("Leadership or event organisation","Running a campaign, organising an event, or leading a team shows the coordination skills marketers need."),
                "extracurricular":     ("Marketing club / creative work", "Nova Marketing Club, brand competitions, or content creation projects all demonstrate genuine passion."),
                "international":       ("International experience",       "Global brands value international exposure — an exchange or international internship sets you apart."),
                "gpa":                 ("GPA (16/20 signal)",             "A strong GPA signals analytical ability, which matters increasingly in data-driven marketing roles."),
            },
            "sustainability": {
                "relevant_experience": ("Sustainability / ESG experience","Direct experience in sustainability, ESG, impact investing, or NGO work is the primary screening signal."),
                "internship":          ("Any internship experience",      "Internships in any sector show professional exposure, but sustainability-adjacent roles carry extra weight."),
                "leadership":          ("Leadership / project ownership", "Leading an impact initiative, social project, or sustainability committee demonstrates real commitment."),
                "extracurricular":     ("Values-aligned extracurricular", "Nova Sustainability Club, social consulting, or environmental volunteering are strong differentiators."),
                "international":       ("International or cross-cultural exposure", "Many sustainability roles are global in scope — international experience and language skills help significantly."),
                "gpa":                 ("GPA (academic rigour signal)",   "A strong GPA signals the analytical and research ability needed in ESG analysis and sustainability consulting."),
            },
        }
        CRIT_INFO = _CRIT_BY_PATH.get(career_key, _CRIT_BY_PATH["consulting"])
        rows_html = ""
        for key, (label, explanation) in CRIT_INFO.items():
            ok   = criteria_met.get(key, False)
            icon = "✅" if ok else "❌"
            rows_html += (
                f'<div style="display:flex;justify-content:space-between;align-items:flex-start;'
                f'padding:9px 0;border-bottom:1px solid #F5F7FA;gap:12px;">'
                f'<div>'
                f'<div style="font-size:13px;color:#334455;font-weight:500;">{label}</div>'
                f'<div style="font-size:11px;color:#889AAA;margin-top:2px;">{explanation}</div>'
                f'</div>'
                f'<span style="font-size:16px;flex-shrink:0;margin-top:2px;">{icon}</span></div>'
            )
        st.markdown(
            '<div style="background:white;border-radius:16px;padding:24px 28px;'
            'border:1px solid #E4ECF4;box-shadow:0 2px 16px rgba(10,22,40,0.06);">'
            '<div style="font-size:10px;font-weight:700;color:#AAB8C8;letter-spacing:1.2px;'
            'text-transform:uppercase;margin-bottom:14px;">What employers check</div>'
            + rows_html + '</div>',
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Quick Win banner ──────────────────────────────────────────────────────
    if st.session_state.get("gemini_result"):
        st.markdown(
            '<div style="text-align:right;margin-bottom:6px;">'
            '<span style="background:#EFF6FF;color:#1A56DB;font-size:11px;font-weight:600;'
            'padding:3px 12px;border-radius:20px;border:1px solid #BFDBFE;">'
            '✨ Powered by Gemini</span></div>',
            unsafe_allow_html=True
        )
    st.markdown(
        f'<div style="background:#EFF6FF;border-left:4px solid #1A56DB;border-radius:10px;'
        f'padding:16px 20px;margin-bottom:4px;">'
        f'<div style="font-size:10px;font-weight:700;color:#1A56DB;letter-spacing:1px;'
        f'text-transform:uppercase;margin-bottom:5px;">⚡ Your #1 action right now</div>'
        f'<div style="font-size:14px;color:#0A1628;line-height:1.6;">{quick_win}</div></div>',
        unsafe_allow_html=True
    )

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Strengths + Gaps (always visible, side by side) ──────────────────────
    c_str, c_gap = st.columns(2, gap="large")

    with c_str:
        items_html = "".join(
            f'<div style="display:flex;gap:10px;align-items:flex-start;padding:8px 0;'
            f'border-bottom:1px solid #F0F4F8;">'
            f'<span style="color:#16A34A;font-size:15px;flex-shrink:0;margin-top:1px;">✓</span>'
            f'<span style="font-size:13px;color:#334455;line-height:1.5;">{s}</span></div>'
            for s in strengths
        )
        st.markdown(
            '<div style="background:white;border-radius:14px;padding:22px 24px;'
            'border:1px solid #E8EFF8;box-shadow:0 2px 12px rgba(10,22,40,0.06);">'
            '<div style="font-size:10px;font-weight:700;color:#16A34A;letter-spacing:1.2px;'
            'text-transform:uppercase;margin-bottom:14px;">✅ Your Strengths</div>'
            + items_html + '</div>',
            unsafe_allow_html=True
        )

    with c_gap:
        items_html = "".join(
            f'<div style="display:flex;gap:10px;align-items:flex-start;padding:8px 0;'
            f'border-bottom:1px solid #F0F4F8;">'
            f'<span style="color:#EF4444;font-size:15px;flex-shrink:0;margin-top:1px;">→</span>'
            f'<span style="font-size:13px;color:#334455;line-height:1.5;">{g}</span></div>'
            for g in gaps
        )
        st.markdown(
            '<div style="background:white;border-radius:14px;padding:22px 24px;'
            'border:1px solid #E8EFF8;box-shadow:0 2px 12px rgba(10,22,40,0.06);">'
            '<div style="font-size:10px;font-weight:700;color:#EF4444;letter-spacing:1.2px;'
            'text-transform:uppercase;margin-bottom:14px;">⚠️ Gaps to Close</div>'
            + items_html + '</div>',
            unsafe_allow_html=True
        )

    # ── Database section ──────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin:28px 0 16px;">
      <div style="font-size:10px;font-weight:700;color:#AAB8C8;letter-spacing:1.5px;
                  text-transform:uppercase;margin-bottom:4px;">Nova SBE Resources</div>
      <div style="font-size:20px;font-weight:700;color:#0A1628;">Your personalised path to this career</div>
    </div>
    """, unsafe_allow_html=True)

    # Row 1: Courses + Clubs
    c_courses, c_clubs = st.columns(2, gap="large")

    with c_courses:
        if courses:
            course_html = "".join(
                f'<div style="padding:10px 0;border-bottom:1px solid #F0F4F8;">'
                f'<div style="font-size:13px;font-weight:600;color:#0A1628;line-height:1.4;">'
                f'{c.get("Course Name","")}</div>'
                f'<div style="font-size:11px;color:#889AAA;margin-top:3px;">'
                f'{c.get("Period","")}{"  ·  " + c.get("Type","") if c.get("Type") else ""}</div>'
                f'</div>'
                for c in courses
            )
        else:
            course_html = '<div style="font-size:13px;color:#889AAA;">No matching courses found.</div>'
        st.markdown(
            '<div style="background:white;border-radius:14px;padding:22px 24px;'
            'border:1px solid #E8EFF8;box-shadow:0 2px 12px rgba(10,22,40,0.06);">'
            '<div style="font-size:10px;font-weight:700;color:#1A56DB;letter-spacing:1.2px;'
            'text-transform:uppercase;margin-bottom:4px;">📚 Recommended Courses</div>'
            '<div style="font-size:12px;color:#667788;margin-bottom:14px;">'
            'Nova SBE courses most relevant for your target career</div>'
            + course_html + '</div>',
            unsafe_allow_html=True
        )

    with c_clubs:
        if clubs:
            clubs_html = "".join(
                f'<div style="padding:10px 0;border-bottom:1px solid #F0F4F8;">'
                f'<div style="font-size:13px;font-weight:600;color:#0A1628;">{cl["name"]}</div>'
                f'<div style="font-size:11px;color:#1A56DB;margin-top:2px;font-weight:500;">{cl["focus"]}</div>'
                f'<div style="font-size:11px;color:#667788;margin-top:3px;line-height:1.5;">{cl["why"]}</div>'
                f'</div>'
                for cl in clubs
            )
        else:
            clubs_html = '<div style="font-size:13px;color:#889AAA;">No club data for this path.</div>'
        st.markdown(
            '<div style="background:white;border-radius:14px;padding:22px 24px;'
            'border:1px solid #E8EFF8;box-shadow:0 2px 12px rgba(10,22,40,0.06);">'
            '<div style="font-size:10px;font-weight:700;color:#1A56DB;letter-spacing:1.2px;'
            'text-transform:uppercase;margin-bottom:4px;">🏛️ Clubs to Join</div>'
            '<div style="font-size:12px;color:#667788;margin-bottom:14px;">'
            'Nova SBE clubs that directly strengthen your profile</div>'
            + clubs_html + '</div>',
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Row 2: Alumni + Employers
    c_alumni, c_emp = st.columns(2, gap="large")

    with c_alumni:
        if alumni:
            alumni_html = ""
            for a in alumni:
                name     = a.get("Full Name", "").strip()
                role     = a.get("Job Title", "").strip()
                company  = a.get("Company", "").strip()
                prog     = a.get("Master's Program Name", "").strip()
                linkedin = a.get("LinkedIn Profile URL", "").strip()
                link = (f'<a href="{linkedin}" target="_blank" '
                        f'style="font-size:11px;color:#1A56DB;font-weight:600;text-decoration:none;">'
                        f'LinkedIn →</a>' if linkedin else "")
                alumni_html += (
                    f'<div style="padding:10px 0;border-bottom:1px solid #F0F4F8;">'
                    f'<div style="display:flex;justify-content:space-between;align-items:flex-start;">'
                    f'<div style="font-size:13px;font-weight:600;color:#0A1628;">{name}</div>'
                    f'{link}</div>'
                    f'<div style="font-size:11px;color:#445566;margin-top:2px;">'
                    f'{role}{" @ " + company if company else ""}</div>'
                    f'<div style="font-size:10px;color:#889AAA;margin-top:1px;">{prog}</div>'
                    f'</div>'
                )
        else:
            alumni_html = '<div style="font-size:13px;color:#889AAA;">No alumni data yet.</div>'
        st.markdown(
            '<div style="background:white;border-radius:14px;padding:22px 24px;'
            'border:1px solid #E8EFF8;box-shadow:0 2px 12px rgba(10,22,40,0.06);">'
            '<div style="font-size:10px;font-weight:700;color:#1A56DB;letter-spacing:1.2px;'
            'text-transform:uppercase;margin-bottom:4px;">🎓 Nova SBE Alumni'
            + (' &nbsp;<span style="background:#EFF6FF;color:#1A56DB;font-size:9px;font-weight:600;'
               'padding:2px 8px;border-radius:20px;border:1px solid #BFDBFE;vertical-align:middle;">'
               '✨ AI</span>' if alumni_ai else '') + '</div>'
            '<div style="font-size:12px;color:#667788;margin-bottom:14px;">'
            'Reach out on LinkedIn — one coffee chat beats 10 cold applications</div>'
            + alumni_html + '</div>',
            unsafe_allow_html=True
        )

    with c_emp:
        if employers:
            emp_html = ""
            for e in employers:
                company  = e.get("Company", "")
                criteria = e.get("Key Evaluation Criteria", "")
                timing   = e.get("Application Timing", "")
                reqs     = e.get("Typical Requirements", "")
                emp_html += (
                    f'<div style="padding:10px 0;border-bottom:1px solid #F0F4F8;">'
                    f'<div style="font-size:13px;font-weight:600;color:#0A1628;">{company}</div>'
                    f'<div style="font-size:11px;color:#667788;margin-top:2px;">{criteria}</div>'
                    f'<div style="font-size:11px;color:#889AAA;margin-top:1px;">{reqs}</div>'
                    f'<div style="font-size:11px;color:#1A56DB;font-weight:600;margin-top:3px;">'
                    f'📅 Apply: {timing}</div></div>'
                )
        else:
            emp_html = '<div style="font-size:13px;color:#889AAA;">No employer data yet.</div>'
        st.markdown(
            '<div style="background:white;border-radius:14px;padding:22px 24px;'
            'border:1px solid #E8EFF8;box-shadow:0 2px 12px rgba(10,22,40,0.06);">'
            '<div style="font-size:10px;font-weight:700;color:#1A56DB;letter-spacing:1.2px;'
            'text-transform:uppercase;margin-bottom:4px;">🏢 Target Employers'
            + (' &nbsp;<span style="background:#EFF6FF;color:#1A56DB;font-size:9px;font-weight:600;'
               'padding:2px 8px;border-radius:20px;border:1px solid #BFDBFE;vertical-align:middle;">'
               '✨ AI</span>' if employers_ai else '') + '</div>'
            '<div style="font-size:12px;color:#667788;margin-bottom:14px;">'
            'Who recruits Nova SBE students + when to apply</div>'
            + emp_html + '</div>',
            unsafe_allow_html=True
        )


# =============================================================================
# RESULTS ROUTER
# =============================================================================
def _results():
    result     = st.session_state.cv_result
    career_key = st.session_state.career_key

    # Re-show sidebar — upload page hides it via CSS that persists in session
    st.markdown("""
    <style>
    section[data-testid="stSidebar"]         { display: flex  !important; visibility: visible !important; }
    button[data-testid="collapsedControl"],
    div[data-testid="collapsedControl"]      { display: flex  !important; visibility: visible !important; }
    </style>
    """, unsafe_allow_html=True)
    import streamlit.components.v1 as _c
    _c.html("""<script>
    (function(){
        var doc = window.parent.document;
        var sb  = doc.querySelector('section[data-testid="stSidebar"]');
        if (sb) { sb.style.setProperty('display','flex','important');
                  sb.style.setProperty('visibility','visible','important'); }
        var btn = doc.querySelector('button[data-testid="collapsedControl"]')
               || doc.querySelector('div[data-testid="collapsedControl"]');
        if (btn){ btn.style.setProperty('display','flex','important'); }
    })();
    </script>""", height=0)

    # Cache career readiness data in session state (recompute if career path changed)
    if result and result.get("raw_text"):
        if (st.session_state.get("career_data_key") != career_key
                or "career_data" not in st.session_state):
            st.session_state["career_data"] = analyze_career_readiness(
                cv_text=result["raw_text"], career_key=career_key, cv_result=result
            )
            st.session_state["career_data_key"] = career_key
    else:
        st.session_state["career_data"] = None

    import streamlit.components.v1 as components
    components.html("""
    <script>
    (function() {
        const KEY = 'sidebarScroll';
        const doc = window.parent.document;
        function getSidebar() {
            return doc.querySelector('section[data-testid="stSidebar"] > div:first-child');
        }
        const sb = getSidebar();
        if (!sb) return;
        const saved = sessionStorage.getItem(KEY);
        if (saved) sb.scrollTop = parseInt(saved);
        sb.addEventListener('scroll', () => sessionStorage.setItem(KEY, sb.scrollTop), { passive: true });
        sb.addEventListener('click',  () => sessionStorage.setItem(KEY, sb.scrollTop), { passive: true });
    })();
    </script>
    """, height=0)

    _sidebar(result)
    _mobile_menu(result)

    if st.session_state.main_tab == "career":
        _career_readiness(career_key)
        return

    if not result:
        st.warning("No CV uploaded.")
        if st.button("← Upload CV"): go_to("upload"); st.rerun()
        return

    tab = st.session_state.cv_tab
    pages = {
        "overview": _overview,
        "actions":  _action_verbs,
    }
    dim_keys = ["qi","av","acc","rep","ln","fw","bc","bl","sec","pp","bw","act","dat"]

    if tab in pages:
        pages[tab](result)
    elif tab in dim_keys:
        _dimension(tab, result)


# =============================================================================
# LANDING
# =============================================================================
if st.session_state.step == "landing":
    # Invisible native button — JS will click this when user clicks any CTA
    # Also hide sidebar on landing page (empty, not needed there)
    st.markdown("""<style>
    div[data-testid="stButton"]:first-of-type button {
        position:fixed!important;left:-9999px!important;top:-9999px!important;
        width:1px!important;height:1px!important;opacity:0!important;
    }
    section[data-testid="stSidebar"] { display: none !important; }
    button[data-testid="collapsedControl"],
    div[data-testid="collapsedControl"] { display: none !important; }
    </style>""", unsafe_allow_html=True)
    if st.button("▶", key="_nav_trigger"):
        st.session_state.step = "upload"
        st.rerun()
    st.markdown(LANDING_CSS, unsafe_allow_html=True)
    landing_page()


# =============================================================================
# UPLOAD
# =============================================================================
elif st.session_state.step == "upload":

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    details > summary > p, details > summary > p:first-child,
    details > summary span[data-testid], [data-testid="stExpanderToggleIcon"],
    .material-icons, [class*="material-icon"], [class*="MaterialIcon"], [class*="symbol"] {
        font-family: 'Material Symbols Rounded', 'Material Icons' !important; }
    /* Full white page */
    .stApp, .stApp > div, section.main, .block-container {
        background: #F5F7FA !important;
    }
    /* White selectbox — target all layers */
    div[data-testid="stSelectbox"] * { color: #0A1628 !important; }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:first-child {
        background: white !important;
        border: 1.5px solid #D0DCE8 !important;
        border-radius: 10px !important;
    }
    /* Dropdown popover/menu — force white */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="popover"] ul,
    div[data-baseweb="menu"],
    div[data-baseweb="menu"] > div,
    div[data-baseweb="menu"] ul {
        background: white !important;
        background-color: white !important;
        border: 1px solid #E0EAF4 !important;
        border-radius: 10px !important;
        box-shadow: 0 8px 24px rgba(10,22,40,0.12) !important;
    }
    div[data-baseweb="option"] {
        background: white !important;
        color: #0A1628 !important;
        font-size: 14px !important;
        padding: 10px 14px !important;
    }
    div[data-baseweb="option"]:hover,
    div[data-baseweb="option"][aria-selected="true"] {
        background: #EFF6FF !important;
        color: #1A56DB !important;
    }
    li[role="option"] {
        background: white !important;
        color: #0A1628 !important;
    }
    li[role="option"]:hover {
        background: #EFF6FF !important;
    }
    /* File uploader */
    div[data-testid="stFileUploader"],
    div[data-testid="stFileUploader"] > div,
    div[data-testid="stFileUploaderDropzone"] { background: white !important; }
    div[data-testid="stFileUploaderDropzone"] {
        border: 2px dashed #BFDBFE !important;
        border-radius: 14px !important; padding: 24px 20px !important;
    }
    div[data-testid="stFileUploaderDropzone"]:hover {
        border-color: #1A56DB !important; background: #F0F6FF !important;
    }
    div[data-testid="stFileUploader"] button {
        background: #1A56DB !important;
        border-radius: 8px !important; border: none !important;
        padding: 8px 20px !important; position: relative !important;
        cursor: pointer !important;
    }
    /* Make all internal text invisible — Streamlit renders duplicate spans */
    div[data-testid="stFileUploader"] button,
    div[data-testid="stFileUploader"] button * {
        color: transparent !important; font-size: 0 !important;
    }
    /* Inject our own clean label */
    div[data-testid="stFileUploader"] button::after {
        content: "Browse files";
        color: white !important; font-size: 14px !important;
        font-weight: 700 !important; font-family: 'Inter', sans-serif !important;
    }
    div[data-testid="stFileUploader"] small { color: #889AAA !important; }
    div[data-testid="stFileUploaderDropzone"] svg { stroke: #1A56DB !important; fill: none !important; }
    /* Buttons */
    div[data-testid="stButton"] > button:not([kind="primary"]) {
        background: white !important;
        color: #0A1628 !important;
        border: 1.5px solid #D0DCE8 !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 14px 24px !important;
        margin: 0 !important;
    }
    div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(135deg, #1A56DB, #0A3EB0) !important;
        color: white !important; border: none !important;
        border-radius: 12px !important;
        font-size: 14px !important; font-weight: 700 !important;
        padding: 14px 24px !important;
        box-shadow: 0 4px 16px rgba(26,86,219,0.3) !important;
        margin: 0 !important;
    }
    /* Remove gap between columns so buttons align */
    div[data-testid="stHorizontalBlock"] {
        gap: 12px !important;
        align-items: stretch !important;
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    div[data-testid="stColumn"] {
        background: transparent !important;
        padding: 0 !important;
    }
    div[data-testid="stButton"] {
        height: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    div[data-testid="stButton"] > button {
        width: 100% !important;
        height: 52px !important;
        margin: 0 !important;
    }
    /* Hide sidebar and toggle completely on upload page */
    section[data-testid="stSidebar"] { display: none !important; }
    button[data-testid="collapsedControl"],
    div[data-testid="collapsedControl"] { display: none !important; }
    /* Hide the instruction text inside the dropzone — keeps only the button */
    div[data-testid="stFileUploaderDropzoneInstructions"] > div:first-child { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    _, c, _ = st.columns([1, 2, 1])
    with c:

        # ── Header ──────────────────────────────────────────────────────────
        st.markdown("""
        <div style="background:linear-gradient(135deg,#0A1628 0%,#0E2A4A 100%);
                    border-radius:16px;padding:40px 44px;margin-bottom:28px;
                    box-shadow:0 8px 32px rgba(10,22,40,0.2);">
            <div style="font-size:11px;font-weight:700;color:#3A7ABF;letter-spacing:1.5px;
                        text-transform:uppercase;margin-bottom:12px;">Step 1 of 2</div>
            <h1 style="color:white;font-size:34px;font-weight:800;margin:0 0 10px 0;
                       letter-spacing:-0.8px;line-height:1.1;">Upload your CV</h1>
            <p style="color:#7AA8CC;font-size:15px;margin:0;line-height:1.6;">
                We analyse it across 13 dimensions and give you<br>
                personalised, expert-level feedback in under 60 seconds.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # ── Form fields ─────────────────────────────────────────────────────
        st.markdown("""
        <p style="font-size:13px;font-weight:600;color:#6A8AA8;margin:0 0 6px 0;">
            Which career are you targeting?
        </p>
        """, unsafe_allow_html=True)

        career_key = st.selectbox(
            "",
            options=list(CAREER_PATHS.keys()),
            format_func=lambda k: CAREER_PATHS[k]["name"],
            label_visibility="collapsed",
        )
        st.session_state.career_key = career_key

        st.markdown("""
        <div style="height:1px;background:#E8EEF4;margin:22px 0 18px 0;"></div>
        <p style="font-size:13px;font-weight:600;color:#6A8AA8;margin:0 0 10px 0;">
            Your CV (PDF only)
        </p>
        """, unsafe_allow_html=True)

        uploaded = st.file_uploader("", type=["pdf"], label_visibility="collapsed")

        # Status badge
        if uploaded:
            st.markdown(f"""
            <div style="background:#ECFDF5;border:1px solid #BBF7D0;border-radius:10px;
                        padding:14px 18px;margin-top:16px;display:flex;align-items:center;gap:12px;">
                <span style="font-size:22px;">✅</span>
                <div>
                    <div style="font-size:13px;font-weight:700;color:#16A34A;margin-bottom:2px;">{uploaded.name}</div>
                    <div style="font-size:12px;color:#4ADE80;">Ready to analyse — click the button below</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Buttons always at the same position ─────────────────────────────
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        cb, cn = st.columns([1, 1])
        with cb:
            if st.button("← Back", use_container_width=True, key="upload_back"):
                go_to("landing"); st.rerun()
        with cn:
            if uploaded:
                if st.button("Analyse CV →", type="primary", use_container_width=True, key="upload_go"):
                    with st.spinner("Analysing your CV..."):
                        st.session_state.cv_result = score_cv(uploaded, career_key)
                        st.session_state.gemini_result = enhance_cv_feedback(
                            st.session_state.cv_result["raw_text"],
                            career_key,
                            st.session_state.cv_result,
                        )
                    st.session_state.main_tab = "cv"
                    st.session_state.cv_tab   = "overview"
                    go_to("results"); st.rerun()
            else:
                st.button("Analyse CV →", type="primary", use_container_width=True,
                          key="upload_go_dis", disabled=True)

        st.markdown("""
        <p style="text-align:center;font-size:12px;color:#AAB8C8;margin-top:16px;">
            🔒 Your CV is never stored — analysed in real time and immediately discarded.
        </p>
        """, unsafe_allow_html=True)


# =============================================================================
# RESULTS
# =============================================================================
elif st.session_state.step == "results":
    _results()