import streamlit as st
import streamlit.components.v1 as components

# =============================================================================
# LANDING PAGE — Nova CareerPath
# Pure-HTML navbar (no column splits), query_param CTA, scroll animations
# =============================================================================

LANDING_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }

/* ── Reset Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
.stApp { background: #ffffff !important; }
section.main > div { background: #ffffff !important; padding: 0 !important; }

/* Remove ALL blue outlines and borders */
button:focus, button:focus-visible, *:focus, *:focus-visible {
    outline: none !important;
    box-shadow: none !important;
    border-color: transparent !important;
}
div[data-testid="stButton"] > button {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}

/* ── NAVBAR ── */
.lp-nav {
    position: sticky; top: 0; z-index: 999;
    background: rgba(255,255,255,0.96);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid #EAEFF6;
    padding: 0 48px;
    height: 64px;
    display: flex; align-items: center; justify-content: space-between;
}
.lp-nav-brand,
.lp-nav-brand:hover,
.lp-nav-brand *,
.lp-nav-brand:hover * { text-decoration: none !important; }
.lp-nav-brand { display: flex; align-items: center; gap: 10px; }
.lp-nav-logo-mark {
    width: 34px; height: 34px; background: #0A1628; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 15px; font-weight: 900; color: white; letter-spacing: -1px;
    font-family: Arial Black, sans-serif;
}
.lp-nav-brand-text { font-size: 16px; font-weight: 700; color: #0A1628; letter-spacing: -0.3px; }
.lp-nav-brand-sub { font-size: 10px; color: #8A9BB0; font-weight: 400; }
.lp-nav-links { display: flex; align-items: center; gap: 6px; }
.lp-nav-link {
    font-size: 13.5px; font-weight: 500; color: #445566;
    text-decoration: none; padding: 8px 14px; border-radius: 8px;
    transition: color 0.15s, background 0.15s;
}
.lp-nav-link:hover { color: #0A1628; background: #F4F7FA; }
.lp-nav-cta {
    background: #0A1628 !important; color: white !important; font-size: 13.5px; font-weight: 600;
    text-decoration: none !important; padding: 9px 20px; border-radius: 8px;
    transition: background 0.15s, transform 0.1s;
    margin-left: 8px; border: none; cursor: pointer;
}
.lp-nav-cta:hover { background: #1A2E48 !important; transform: translateY(-1px); color: white !important; }

/* ── HERO ── */
.lp-hero {
    background: linear-gradient(170deg, #06101F 0%, #0D2952 60%, #0A1E3C 100%);
    padding: 100px 48px 80px;
    text-align: center;
    position: relative; overflow: hidden;
}
.lp-hero::before {
    content: '';
    position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
    background: radial-gradient(circle at 50% 40%, rgba(26,86,219,0.12) 0%, transparent 60%);
    pointer-events: none;
}
.lp-badge {
    display: inline-flex; align-items: center; gap: 7px;
    background: rgba(26,86,219,0.18); border: 1px solid rgba(26,86,219,0.3);
    border-radius: 20px; padding: 5px 14px; margin-bottom: 28px;
    font-size: 11px; font-weight: 700; color: #7BB8F0 !important;
    letter-spacing: 1px; text-transform: uppercase;
}
.lp-h1 {
    font-size: 54px; font-weight: 800; color: white !important;
    line-height: 1.1; letter-spacing: -2px; margin-bottom: 20px;
}
.lp-accent { color: #4B9FFF !important; }
.lp-sub {
    font-size: 17px; color: #8BBDE0 !important; line-height: 1.7;
    max-width: 500px !important;
    margin-top: 0 !important; margin-bottom: 40px !important;
    margin-left: auto !important; margin-right: auto !important;
    text-align: center !important; display: block !important;
}
.lp-hero-cta {
    display: inline-block;
    background: #1A56DB !important; color: white !important;
    font-size: 15px; font-weight: 700; text-decoration: none !important;
    padding: 16px 40px; border-radius: 12px;
    box-shadow: 0 8px 28px rgba(26,86,219,0.4);
    transition: transform 0.15s, box-shadow 0.15s;
    border: none; cursor: pointer;
}
.lp-hero-cta:hover { transform: translateY(-2px); box-shadow: 0 12px 36px rgba(26,86,219,0.5); color: white !important; }
.lp-hero-note { font-size: 12px; color: #8AAABF !important; margin-top: 14px; }
.lp-stats {
    display: flex; justify-content: center; gap: 0;
    border-top: 1px solid rgba(255,255,255,0.07);
    margin-top: 60px; padding-top: 40px;
}
.lp-stat { text-align: center; padding: 0 44px; border-right: 1px solid rgba(255,255,255,0.07); }
.lp-stat:last-child { border-right: none; }
.lp-stat-n { font-size: 38px; font-weight: 800; color: white !important; letter-spacing: -1.5px; }
.lp-stat-l { font-size: 11px; color: #4A7898; margin-top: 5px; text-transform: uppercase; letter-spacing: 0.5px; }

/* ── SECTIONS ── */
.lp-sec { padding: 80px 48px; }
.lp-sec-alt { background: #F7F9FC; }
.lp-eyebrow { font-size: 11px; font-weight: 700; color: #1A56DB; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 12px; }
.lp-sec-h2 { font-size: 34px; font-weight: 800; color: #0A1628; letter-spacing: -1px; margin-bottom: 12px; line-height: 1.2; }
.lp-sec-p { font-size: 15px; color: #667788; line-height: 1.7; max-width: 540px; margin-bottom: 48px; }

/* ── MOCKUP ── */
.lp-mockup { background: #0A1628; border-radius: 16px; overflow: hidden; box-shadow: 0 48px 96px rgba(10,22,40,0.28); max-width: 840px; margin: 0 auto; }
.lp-mockup-bar { background: #0D1F38; padding: 12px 18px; display: flex; align-items: center; gap: 7px; border-bottom: 1px solid #1E3A5F; }
.lp-dot { width: 11px; height: 11px; border-radius: 50%; display: inline-block; }
.lp-mockup-url { font-size: 10px; color: #3A6A9A; margin-left: 8px; }
.lp-mockup-body { display: flex; height: 340px; }
.lp-msb { width: 170px; min-width: 170px; background: #06101E; border-right: 1px solid #1A3050; padding: 12px 0; }
.lp-msb-logo { font-size: 13px; font-weight: 800; color: white; padding: 0 14px 12px; border-bottom: 1px solid #1A3050; margin-bottom: 8px; }
.lp-msec { font-size: 8px; color: #1E5070; letter-spacing: 1.2px; text-transform: uppercase; padding: 8px 14px 3px; }
.lp-mi { font-size: 11px; color: #4A80A8; padding: 5px 14px; display: flex; justify-content: space-between; align-items: center; }
.lp-mi-on { color: #60B0F0 !important; background: #0D1F38; border-left: 2px solid #60B0F0; font-weight: 600; }
.lp-mb { font-size: 9px; font-weight: 800; padding: 1px 5px; border-radius: 8px; }
.lp-mb-g { color: #4ADE80; background: rgba(74,222,128,0.12); }
.lp-mb-y { color: #FBBF24; background: rgba(251,191,36,0.12); }
.lp-mb-r { color: #F87171; background: rgba(248,113,113,0.12); }
.lp-mcon { flex: 1; background: #F7F9FC; padding: 18px; }
.lp-mcon-t { font-size: 17px; font-weight: 800; color: #0A1628; }
.lp-mcon-s { font-size: 10px; color: #8899AA; margin-bottom: 14px; }
.lp-msrow { display: flex; gap: 10px; margin-bottom: 12px; }
.lp-msbox { background: white; border-radius: 10px; padding: 14px 12px; text-align: center; border: 1px solid #E8EEF4; min-width: 90px; }
.lp-msnum { font-size: 34px; font-weight: 800; color: #1A56DB; line-height: 1; }
.lp-mslbl { font-size: 8px; color: #8899AA; margin-top: 2px; text-transform: uppercase; }
.lp-mbars { flex: 1; background: white; border-radius: 10px; padding: 12px; border: 1px solid #E8EEF4; }
.lp-mbar { margin-bottom: 9px; }
.lp-mbar-hd { display: flex; justify-content: space-between; font-size: 9px; color: #556677; margin-bottom: 3px; }
.lp-mbar-tr { height: 5px; background: #EEF2F8; border-radius: 3px; }
.lp-mbar-fi { height: 5px; border-radius: 3px; }
.lp-mtips { background: white; border-radius: 10px; padding: 12px; border: 1px solid #E8EEF4; }
.lp-mtip { font-size: 9px; color: #334455; background: #EFF6FF; border-left: 2px solid #3B82F6; border-radius: 0 5px 5px 0; padding: 6px 8px; margin-bottom: 5px; }

/* ── BEFORE/AFTER ── */
.lp-ba-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; max-width: 860px; margin: 0 auto; }
.lp-ba-card { border-radius: 16px; padding: 28px; border: 1px solid; }
.lp-ba-before { background: #FFF8F8; border-color: #FED7D7; }
.lp-ba-after  { background: #F0FDF4; border-color: #BBF7D0; }
.lp-ba-lbl { font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 16px; }
.lp-ba-before .lp-ba-lbl { color: #DC2626; }
.lp-ba-after  .lp-ba-lbl { color: #16A34A; }
.lp-ba-bullet { font-size: 13px; line-height: 1.6; margin-bottom: 12px; color: #334455; padding: 10px 14px; border-radius: 10px; }
.lp-ba-before .lp-ba-bullet { background: rgba(239,68,68,0.05); }
.lp-ba-after  .lp-ba-bullet { background: rgba(34,197,94,0.07); }
.lp-tag { display: inline-block; font-size: 10px; font-weight: 600; padding: 2px 8px; border-radius: 10px; margin: 3px 2px 0 0; }
.lp-tag-bad  { background: #FEE2E2; color: #DC2626; }
.lp-tag-good { background: #DCFCE7; color: #16A34A; }

/* ── HOW IT WORKS ── */
.lp-steps { display: grid; grid-template-columns: repeat(3,1fr); gap: 24px; max-width: 860px; margin: 0 auto; }
.lp-step { background: white; border-radius: 16px; padding: 30px; border: 1px solid #E8EEF4; box-shadow: 0 2px 12px rgba(10,22,40,0.05); }
.lp-step-n { width: 40px; height: 40px; border-radius: 10px; background: #EBF2FF; color: #1A56DB; font-size: 18px; font-weight: 800; display: flex; align-items: center; justify-content: center; margin-bottom: 18px; }
.lp-step-t { font-size: 16px; font-weight: 700; color: #0A1628; margin-bottom: 10px; }
.lp-step-d { font-size: 13.5px; color: #667788; line-height: 1.65; }

/* ── TRUST ── */
.lp-trust { background: white; padding: 40px 48px; text-align: center; border-top: 1px solid #EAEFF6; border-bottom: 1px solid #EAEFF6; }
.lp-trust-lbl { font-size: 11px; color: #99AABB; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 24px; }
.lp-trust-logos { display: flex; justify-content: center; align-items: center; gap: 44px; flex-wrap: wrap; }
.lp-trust-logo { font-size: 15px; font-weight: 700; color: #B0C4D8; }
.lp-logo-link {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 64px; height: 64px;
    text-decoration: none;
    transition: transform 0.2s;
}
.lp-logo-link:hover { transform: scale(1.1); }
.lp-logo-img {
    max-width: 48px; max-height: 48px;
    width: auto; height: auto;
    object-fit: contain;
}

/* ── FEATURES ── */
.lp-feat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; max-width: 860px; margin: 0 auto; }
.lp-feat { background: white; border-radius: 16px; padding: 28px; border: 1px solid #E8EEF4; display: flex; gap: 20px; align-items: flex-start; box-shadow: 0 2px 10px rgba(10,22,40,0.04); }
.lp-feat-ic { width: 46px; height: 46px; border-radius: 12px; font-size: 22px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.lp-feat-t { font-size: 15px; font-weight: 700; color: #0A1628; margin-bottom: 7px; }
.lp-feat-d { font-size: 13px; color: #667788; line-height: 1.65; }

/* ── FAQ ── */
.lp-faq-wrap { max-width: 860px; margin: 0 auto; padding: 0 48px 64px; }
.faq-item {
    background: white;
    border: 1px solid #EAEFF6;
    border-radius: 12px;
    margin-bottom: 10px;
    box-shadow: 0 1px 6px rgba(10,22,40,0.04);
    overflow: hidden;
}
.faq-item summary {
    padding: 18px 20px;
    font-size: 15px; font-weight: 600;
    color: #0A1628;
    cursor: pointer;
    list-style: none;
    display: flex; justify-content: space-between; align-items: center;
    user-select: none;
}
.faq-item summary::-webkit-details-marker { display: none; }
.faq-item summary::after {
    content: '+';
    font-size: 20px; font-weight: 300;
    color: #8A9BB0;
    transition: transform 0.2s;
    flex-shrink: 0;
}
.faq-item[open] summary::after { transform: rotate(45deg); }
.faq-body {
    padding: 6px 20px 18px;
    font-size: 14px; color: #334455;
    line-height: 1.75;
    border-top: 1px solid #F0F4F9;
}

/* ── QUOTE ── */
.lp-quote { background: linear-gradient(135deg, #06101F, #0D2952); padding: 72px 48px; text-align: center; }
.lp-quote-t { font-size: 26px; font-weight: 600; color: white !important; max-width: 620px; margin: 0 auto 18px; line-height: 1.55; }
.lp-quote-t em { color: #4B9FFF !important; font-style: normal; }
.lp-quote-a { font-size: 13px; color: #3A6888; }

/* ── FINAL CTA ── */
.lp-cta-sec { background: white; padding: 80px 48px; text-align: center; }
.lp-cta-box { background: linear-gradient(145deg, #06101F, #0D2952); border-radius: 20px; padding: 56px 48px; max-width: 640px; margin: 0 auto; }
.lp-cta-h2 { font-size: 32px; font-weight: 800; color: white !important; margin-bottom: 12px; letter-spacing: -0.8px; }
.lp-cta-p { font-size: 15px; color: #C0D8EE !important; line-height: 1.7; margin-bottom: 32px; }
.lp-cta-btn {
    display: inline-block; background: #1A56DB !important; color: white !important;
    font-size: 15px; font-weight: 700; text-decoration: none !important;
    padding: 16px 40px; border-radius: 12px;
    box-shadow: 0 8px 28px rgba(26,86,219,0.4);
    transition: transform 0.15s, box-shadow 0.15s;
    border: none; cursor: pointer;
}
.lp-cta-btn:hover { transform: translateY(-2px); box-shadow: 0 12px 36px rgba(26,86,219,0.5); color: white !important; }

/* ── FOOTER ── */
.lp-footer { background: #F7F9FC; padding: 24px 48px; display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #EAEFF6; }
.lp-footer-l { font-size: 12px; color: #6A8AA8; display: flex; align-items: center; gap: 10px; }
.lp-footer-r { font-size: 12px; color: #99AABB; }

/* ── SCROLL ANIMATIONS ── */
.reveal {
    opacity: 0;
    transform: translateY(36px);
    transition: opacity 0.65s cubic-bezier(0.22,1,0.36,1), transform 0.65s cubic-bezier(0.22,1,0.36,1);
}
.reveal.active { opacity: 1; transform: translateY(0); }
.reveal-delay-1 { transition-delay: 0.1s; }
.reveal-delay-2 { transition-delay: 0.2s; }
.reveal-delay-3 { transition-delay: 0.3s; }

/* ── MOBILE RESPONSIVE ── */
@media (max-width: 768px) {
    /* Hide entire navbar on mobile — go straight to hero with the badge */
    .lp-nav { display: none !important; }
}
/* Kill ALL Streamlit top spacing on mobile (outside @media because of selector specificity) */
@media (max-width: 768px) {
    html, body, #root, .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"],
    [data-testid="stAppViewBlockContainer"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stSidebar"],
    section.main, .main, .appview-container,
    .block-container, .block-container > div,
    section.main > div, section.main > div > div {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    header { display: none !important; height: 0 !important; min-height: 0 !important; }

    /* Kill element-container and vertical block gaps on landing */
    [data-testid="element-container"],
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdown"] {
        margin: 0 !important;
        padding: 0 !important;
        min-height: 0 !important;
    }
    [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        gap: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Hero */
    .lp-hero { padding: 60px 20px 50px; }
    .lp-h1 { font-size: 32px; letter-spacing: -1px; }
    .lp-sub { font-size: 14px; }
    .lp-hero-cta { padding: 13px 28px; font-size: 14px; }
    .lp-stats { flex-wrap: wrap; gap: 0; margin-top: 40px; }
    .lp-stat { padding: 14px 20px; border-right: none; border-bottom: 1px solid rgba(255,255,255,0.07); width: 50%; }
    .lp-stat:nth-child(odd) { border-right: 1px solid rgba(255,255,255,0.07); }
    .lp-stat:nth-last-child(-n+2) { border-bottom: none; }
    .lp-stat-n { font-size: 28px; }

    /* Sections */
    .lp-sec { padding: 50px 20px; }
    .lp-sec-h2 { font-size: 24px; }
    .lp-sec-p { font-size: 14px; }

    /* Platform mockup — hide sidebar, stack content */
    .lp-mockup { border-radius: 10px; }
    .lp-mockup-body { flex-direction: column; height: auto; }
    .lp-msb { display: none; }
    .lp-mcon { padding: 14px; }
    .lp-msrow { flex-direction: column; }
    .lp-msbox { min-width: 0; }

    /* Before/After grid — single column */
    .lp-ba-grid { grid-template-columns: 1fr; gap: 16px; }

    /* Steps — single column */
    .lp-steps { grid-template-columns: 1fr; gap: 16px; }

    /* Trust logos */
    .lp-trust { padding: 32px 20px; }
    .lp-trust-logos { gap: 20px; }

    /* Features — single column */
    .lp-feat-grid { grid-template-columns: 1fr; gap: 14px; }

    /* FAQ */
    .faq-item summary { font-size: 14px; padding: 15px 16px; }
    .faq-body { font-size: 13px; }

    /* Quote */
    .lp-quote { padding: 50px 20px; }
    .lp-quote-t { font-size: 20px; }

    /* Final CTA */
    .lp-cta-sec { padding: 50px 20px; }
    .lp-cta-box { padding: 36px 24px; }
    .lp-cta-h2 { font-size: 24px; }
    .lp-cta-btn { padding: 13px 28px; font-size: 14px; }

    /* Footer */
    .lp-footer { flex-direction: column; gap: 10px; padding: 20px 18px; text-align: center; }
    .lp-footer-l { flex-direction: column; gap: 6px; }

    /* FAQ wrapper */
    .lp-faq-wrap { padding: 0 16px 40px; }
}
</style>
"""


def landing_page():
    st.markdown(LANDING_CSS, unsafe_allow_html=True)

    # ── NAVBAR (pure HTML — no column split) ──
    st.markdown("""
    <nav class="lp-nav">
      <a class="lp-nav-brand" href="#">
        <div style="display:flex;flex-direction:column;align-items:flex-start;">
          <div style="display:flex;align-items:center;line-height:1;">
            <span style="font-size:22px;font-weight:900;color:#0A1628;letter-spacing:-1px;font-family:Arial Black,sans-serif;line-height:1;">N</span>
            <div style="width:17px;height:17px;border:5px solid #0A1628;border-radius:50%;margin:0 2px;flex-shrink:0;margin-top:-3px;"></div>
            <span style="font-size:22px;font-weight:900;color:#0A1628;letter-spacing:-1px;font-family:Arial Black,sans-serif;line-height:1;">VA</span>
          </div>
          <div style="width:22px;height:3px;background:#0A1628;margin-left:17px;margin-top:2px;"></div>
        </div>
        <div style="width:1px;height:30px;background:#D8E4F0;margin:0 4px;"></div>
        <div>
          <div class="lp-nav-brand-text">CareerPath</div>
          <div class="lp-nav-brand-sub">Nova School of Business &amp; Economics</div>
        </div>
      </a>
      <div class="lp-nav-links">
        <a class="lp-nav-link" href="#section-steps">How it works</a>
        <a class="lp-nav-link" href="#section-features">Features</a>
        <a class="lp-nav-link" href="#section-faq">FAQ</a>
        <a class="lp-nav-cta" href="?go=cv" target="_top">Analyse my CV &rarr;</a>
      </div>
    </nav>
    """, unsafe_allow_html=True)

    # ── HERO ──
    st.markdown("""
    <div class="lp-hero">
      <div class="lp-badge">&#9733;&nbsp; Built for Nova SBE Students</div>
      <h1 class="lp-h1">Your CV, <span class="lp-accent">recruiter-ready</span><br>in 60 seconds.</h1>
      <p class="lp-sub">Upload your PDF and get expert-level feedback across 13 dimensions — then discover your exact path to your dream career.</p>
      <a class="lp-hero-cta" href="?go=cv" target="_top">Analyse my CV &rarr;</a>
      <p class="lp-hero-note">Free &nbsp;·&nbsp; No sign-up &nbsp;·&nbsp; PDF only</p>
      <div class="lp-stats">
        <div class="lp-stat"><div class="lp-stat-n">13</div><div class="lp-stat-l">Scoring dimensions</div></div>
        <div class="lp-stat"><div class="lp-stat-n">60s</div><div class="lp-stat-l">Analysis time</div></div>
        <div class="lp-stat"><div class="lp-stat-n">6</div><div class="lp-stat-l">Career paths</div></div>
        <div class="lp-stat"><div class="lp-stat-n">Free</div><div class="lp-stat-l">No sign-up</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── PLATFORM MOCKUP ──
    st.markdown("""
    <div class="lp-sec lp-sec-alt" id="section-platform">
      <p class="lp-eyebrow" style="text-align:center" >The Platform</p>
      <h2 class="lp-sec-h2 reveal" style="text-align:center;max-width:100%">See your CV the way recruiters do.</h2>
      <p class="lp-sec-p reveal" style="text-align:center;margin:0 auto 40px">Every line scored, every weak verb flagged, every improvement explained.</p>
      <div class="lp-mockup reveal">
        <div class="lp-mockup-bar">
          <div class="lp-dot" style="background:#EF4444"></div>
          <div class="lp-dot" style="background:#F59E0B"></div>
          <div class="lp-dot" style="background:#22C55E"></div>
          <span class="lp-mockup-url">careerpath.novasbe.pt</span>
        </div>
        <div class="lp-mockup-body">
          <div class="lp-msb">
            <div class="lp-msb-logo">&#127891; CareerPath</div>
            <div class="lp-msec">Results</div>
            <div class="lp-mi lp-mi-on">Overview</div>
            <div class="lp-mi">Breakdown</div>
            <div class="lp-mi">Line-by-Line</div>
            <div class="lp-msec">Impact</div>
            <div class="lp-mi">Quantifying Impact <span class="lp-mb lp-mb-g">9</span></div>
            <div class="lp-mi">Action Verbs <span class="lp-mb lp-mb-y">5</span></div>
            <div class="lp-mi">Accomplishments <span class="lp-mb lp-mb-r">3</span></div>
            <div class="lp-msec">Brevity</div>
            <div class="lp-mi">Length <span class="lp-mb lp-mb-g">10</span></div>
            <div class="lp-mi">Filler Words <span class="lp-mb lp-mb-y">7</span></div>
          </div>
          <div class="lp-mcon">
            <div class="lp-mcon-t">Your CV Score</div>
            <div class="lp-mcon-s">Consulting · Grade B · Top 30% of student CVs</div>
            <div class="lp-msrow">
              <div class="lp-msbox"><div class="lp-msnum">72</div><div class="lp-mslbl">Overall</div></div>
              <div class="lp-mbars">
                <div class="lp-mbar"><div class="lp-mbar-hd"><span>Impact</span><span>28/40</span></div><div class="lp-mbar-tr"><div class="lp-mbar-fi" style="width:70%;background:#3B82F6"></div></div></div>
                <div class="lp-mbar"><div class="lp-mbar-hd"><span>Brevity</span><span>28/30</span></div><div class="lp-mbar-tr"><div class="lp-mbar-fi" style="width:93%;background:#22C55E"></div></div></div>
                <div class="lp-mbar"><div class="lp-mbar-hd"><span>Style</span><span>24/30</span></div><div class="lp-mbar-tr"><div class="lp-mbar-fi" style="width:80%;background:#8B5CF6"></div></div></div>
              </div>
            </div>
            <div class="lp-mtips">
              <div class="lp-mtip">&#128161; Replace "worked on" with "Led" or "Delivered"</div>
              <div class="lp-mtip">&#128161; Line 7: add a number — "Grew Instagram followers by 40%"</div>
              <div class="lp-mtip">&#128161; 2 personal pronouns found — remove "I" and "my"</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── BEFORE / AFTER ──
    st.markdown("""
    <div class="lp-sec">
      <p class="lp-eyebrow" style="text-align:center">Before &amp; After</p>
      <h2 class="lp-sec-h2 reveal" style="text-align:center;max-width:100%">See exactly what changes.</h2>
      <p class="lp-sec-p reveal" style="text-align:center;margin:0 auto 40px">Real examples of CV lines — before and after CareerPath feedback.</p>
      <div class="lp-ba-grid">
        <div class="lp-ba-card lp-ba-before reveal">
          <div class="lp-ba-lbl">&#10005; Before CareerPath</div>
          <div class="lp-ba-bullet">Helped with various marketing campaigns<br><span class="lp-tag lp-tag-bad">weak verb</span><span class="lp-tag lp-tag-bad">filler word</span><span class="lp-tag lp-tag-bad">no numbers</span></div>
          <div class="lp-ba-bullet">I was responsible for managing social media<br><span class="lp-tag lp-tag-bad">personal pronoun</span><span class="lp-tag lp-tag-bad">passive tone</span></div>
          <div class="lp-ba-bullet">Worked on a team project about sustainability<br><span class="lp-tag lp-tag-bad">weak verb</span><span class="lp-tag lp-tag-bad">vague</span></div>
        </div>
        <div class="lp-ba-card lp-ba-after reveal reveal-delay-1">
          <div class="lp-ba-lbl">&#10003; After CareerPath</div>
          <div class="lp-ba-bullet">Delivered 3 digital campaigns, growing Instagram engagement by 40%<br><span class="lp-tag lp-tag-good">strong verb</span><span class="lp-tag lp-tag-good">quantified</span></div>
          <div class="lp-ba-bullet">Managed social media across 4 platforms, reaching 12,000 followers<br><span class="lp-tag lp-tag-good">active voice</span><span class="lp-tag lp-tag-good">numbers</span></div>
          <div class="lp-ba-bullet">Led a 5-person team developing a carbon model adopted by 2 NGOs<br><span class="lp-tag lp-tag-good">leadership</span><span class="lp-tag lp-tag-good">impact</span></div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── HOW IT WORKS ──
    st.markdown("""
    <div class="lp-sec lp-sec-alt" id="section-steps">
      <p class="lp-eyebrow" style="text-align:center">How it works</p>
      <h2 class="lp-sec-h2 reveal" style="text-align:center;max-width:100%">Three steps to a recruiter-ready CV.</h2>
      <div class="lp-steps" style="margin-top:40px">
        <div class="lp-step reveal">
          <div class="lp-step-n">1</div>
          <div class="lp-step-t">Upload your CV</div>
          <div class="lp-step-d">Drop your PDF. We extract every line and run it through our 13-dimension analysis engine built specifically for student CVs.</div>
        </div>
        <div class="lp-step reveal reveal-delay-1">
          <div class="lp-step-n">2</div>
          <div class="lp-step-t">Get your score</div>
          <div class="lp-step-d">See your Impact, Brevity and Style scores — with specific rewrites for every weak line and keyword gaps for your target career.</div>
        </div>
        <div class="lp-step reveal reveal-delay-2">
          <div class="lp-step-n">3</div>
          <div class="lp-step-t">Build your path</div>
          <div class="lp-step-d">Get a personalised 30/60/90-day plan with courses, activities and alumni trajectories that prove the path works.</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── TRUSTED BY ──
    st.markdown("""
    <div class="lp-trust">
      <div class="lp-trust-lbl">Nova SBE alumni work at</div>
      <div class="lp-trust-logos">
        <a class="lp-logo-link" href="https://www.mckinsey.com" target="_blank" rel="noopener" title="McKinsey & Company"><img src="https://www.google.com/s2/favicons?domain=mckinsey.de&sz=128" alt="McKinsey" class="lp-logo-img"></a>
        <a class="lp-logo-link" href="https://www.goldmansachs.com" target="_blank" rel="noopener" title="Goldman Sachs"><img src="https://www.google.com/s2/favicons?domain=goldmansachs.com&sz=128" alt="Goldman Sachs" class="lp-logo-img"></a>
        <a class="lp-logo-link" href="https://www.bcg.com" target="_blank" rel="noopener" title="Boston Consulting Group"><img src="https://www.google.com/s2/favicons?domain=bcg.com&sz=128" alt="BCG" class="lp-logo-img"></a>
        <a class="lp-logo-link" href="https://www.google.com" target="_blank" rel="noopener" title="Google"><img src="https://www.google.com/s2/favicons?domain=google.com&sz=128" alt="Google" class="lp-logo-img"></a>
        <a class="lp-logo-link" href="https://www.jpmorgan.com" target="_blank" rel="noopener" title="J.P. Morgan"><img src="https://www.google.com/s2/favicons?domain=jpmorgan.com&sz=128" alt="J.P. Morgan" class="lp-logo-img"></a>
        <a class="lp-logo-link" href="https://www.deloitte.com" target="_blank" rel="noopener" title="Deloitte"><img src="https://www.google.com/s2/favicons?domain=deloitte.com&sz=128" alt="Deloitte" class="lp-logo-img"></a>
        <a class="lp-logo-link" href="https://www.bain.com" target="_blank" rel="noopener" title="Bain & Company"><img src="https://www.google.com/s2/favicons?domain=bain.com&sz=128" alt="Bain" class="lp-logo-img"></a>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── FEATURES ──
    st.markdown("""
    <div class="lp-sec" id="section-features">
      <p class="lp-eyebrow" style="text-align:center">What you get</p>
      <h2 class="lp-sec-h2 reveal" style="text-align:center;max-width:100%">Everything a career coach would tell you.</h2>
      <div class="lp-feat-grid reveal" style="margin-top:40px">
        <div class="lp-feat">
          <div class="lp-feat-ic" style="background:#EBF2FF">&#128202;</div>
          <div><div class="lp-feat-t">13-Dimension Scorecard</div><div class="lp-feat-d">From action verb strength to date consistency — every element recruiters actually check, scored and explained.</div></div>
        </div>
        <div class="lp-feat">
          <div class="lp-feat-ic" style="background:#ECFDF5">&#128269;</div>
          <div><div class="lp-feat-t">Line-by-Line Rewrites</div><div class="lp-feat-d">Every bullet point flagged with a specific rewrite suggestion. Your exact lines, improved.</div></div>
        </div>
        <div class="lp-feat">
          <div class="lp-feat-ic" style="background:#F3EFFF">&#128170;</div>
          <div><div class="lp-feat-t">Power Verb Library</div><div class="lp-feat-d">Replace weak verbs instantly. Categorised by skill — leadership, analysis, results, collaboration.</div></div>
        </div>
        <div class="lp-feat">
          <div class="lp-feat-ic" style="background:#FFFBEB">&#127919;</div>
          <div><div class="lp-feat-t">Career Path Matching</div><div class="lp-feat-d">Consulting, IB, Tech, Marketing, Sustainability and more. Keyword gaps, courses and alumni paths included.</div></div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── FAQ ──
    st.markdown("""
    <div class="lp-sec lp-sec-alt" id="section-faq">
      <p class="lp-eyebrow" style="text-align:center">FAQ</p>
      <h2 class="lp-sec-h2 reveal" style="text-align:center;max-width:100%;margin-bottom:32px">Frequently asked questions.</h2>
    </div>
    """, unsafe_allow_html=True)

    faqs = [
        ("How do I use CareerPath?",
         "It takes three steps: (1) Upload your CV as a PDF. (2) Select your target career path (e.g. Consulting, Investment Banking). (3) Read your score, quick wins, and Career Readiness report. The whole process takes under 2 minutes."),
        ("What file formats are supported?",
         "PDF only. Make sure it's a real PDF — not a scanned image or a photo of your CV. Export directly from Word or Google Docs as PDF for the best results."),
        ("Is CareerPath free?",
         "Yes — completely free. No sign-up, no account, no credit card. Just upload and go."),
        ("Is my CV stored or shared?",
         "No. Your CV is analysed in real time and immediately discarded. Nothing is saved to any server or database. Your data stays private."),
        ("How is the CV score calculated?",
         "Your score (0–100) is split across three dimensions: Impact (40 pts) — how well you quantify and frame your achievements; Brevity (30 pts) — length, filler words, and bullet structure; Style (30 pts) — sections, active voice, buzzwords, and date consistency. Each dimension has sub-scores you can drill into."),
        ("I'm actively searching for internships — how do I use this?",
         "Start with CV Check: upload your CV, select the career path matching your target internship (e.g. Consulting for McKinsey, Finance for Goldman Sachs), and read your Quick Wins. Fix the top 2–3 issues flagged. Then switch to Career Readiness to see exactly which employers recruit Nova SBE students, when to apply, and what they look for. Re-upload your improved CV to see your score go up."),
        ("What does 'Quantifying Impact' mean?",
         "Recruiters want to see numbers, not just tasks. Instead of 'Managed social media', write 'Grew Instagram following by 40% in 3 months'. Even rough estimates count — team size, number of events, budget managed, ranking achieved. The tool scans every line of your CV for numbers and flags the ones that are missing them."),
        ("What is the Quick Win?",
         "The single most impactful change you can make to your CV right now, based on your results. Focus on this first before anything else — it's the change that will move your score the most."),
        ("How does Career Readiness work?",
         "Career Readiness goes beyond the CV score. It checks your CV against 6 criteria that employers in your chosen field actually use to screen candidates: internship experience, leadership roles, international exposure, case/competition experience, extracurricular involvement, and GPA signals. You also get recommended Nova SBE courses, real alumni contacts, and target employer info."),
        ("How do I reach out to the alumni shown in Career Readiness?",
         "Search their name on LinkedIn, send a short connection request mentioning you're also a Nova SBE student, and ask for a 20-minute virtual coffee chat. Keep it simple: 'Hi [Name], I'm a Nova SBE student interested in [field]. I came across your profile and would love to hear about your path to [Company] — would you be open to a quick call?' Most alumni are happy to help. One conversation is worth more than 10 cold applications."),
        ("Which career paths are available?",
         "Consulting, Investment Banking, Tech & Product, Entrepreneurship, Marketing & Brand, and Sustainability & Impact. Each path has its own set of employer criteria, keyword matching, course recommendations, and alumni data."),
        ("When should I apply to internships?",
         "Most top firms recruit 6–12 months before the internship start date. For summer internships starting in June/July, applications typically open in September–November. Check the Target Employers section in Career Readiness for firm-specific timing."),
        ("Can I upload my CV more than once?",
         "Yes — upload as many times as you like. We recommend: (1) upload your current CV to get a baseline score, (2) make improvements based on the feedback, (3) re-upload to check your new score. Iterate until you reach at least 75/100."),
        ("I'm an international student — does that affect my score?",
         "Yes, positively. The Career Readiness check automatically detects if you are a non-Portuguese national studying at Nova SBE, or if you have exchange/abroad experience. Being an international student IS a form of international exposure that employers value — it will show as a green check in your Career Readiness report."),
    ]

    faq_html = '<div class="lp-faq-wrap">'
    for q, a in faqs:
        faq_html += f'<details class="faq-item"><summary>{q}</summary><div class="faq-body">{a}</div></details>'
    faq_html += '</div>'
    st.markdown(faq_html, unsafe_allow_html=True)

    # ── QUOTE ──
    st.markdown("""
    <div class="lp-quote">
      <div class="lp-quote-t">"Most CVs fail in the first 6 seconds.<br><em>CareerPath</em> shows you exactly why — and how to fix it before you ever hit send."</div>
      <div class="lp-quote-a">Built by Nova SBE students &nbsp;·&nbsp; Introduction to Programming &nbsp;·&nbsp; 2026</div>
    </div>
    """, unsafe_allow_html=True)

    # ── FINAL CTA ──
    st.markdown("""
    <div class="lp-cta-sec">
      <div class="lp-cta-box reveal">
        <h2 class="lp-cta-h2">Ready to stand out?</h2>
        <p class="lp-cta-p">Upload your CV now and get your full score in under 60 seconds.<br>Free. No sign-up. No jargon.</p>
        <a class="lp-cta-btn" href="?go=cv" target="_top">Analyse my CV &rarr;</a>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── FOOTER ──
    st.markdown("""
    <div class="lp-footer">
      <div class="lp-footer-l">
        <div style="width:28px;height:28px;background:#0A1628;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:900;color:white;font-family:Arial Black,sans-serif;">N</div>
        CareerPath &nbsp;·&nbsp; Nova School of Business &amp; Economics &nbsp;·&nbsp; 2026
      </div>
      <div class="lp-footer-r">Introduction to Programming</div>
    </div>
    """, unsafe_allow_html=True)

    # ── SCROLL ANIMATION JS (via components.html — accesses parent doc) ──
    components.html("""
    <script>
    (function() {
        function init() {
            try {
                var doc = window.parent.document;

                // ── CTA navigation — find hidden native button and click it ──
                var navBtn = null;
                var allBtns = doc.querySelectorAll('button');
                for (var i = 0; i < allBtns.length; i++) {
                    if (allBtns[i].textContent.trim() === '▶') {
                        navBtn = allBtns[i]; break;
                    }
                }
                doc.querySelectorAll('.lp-hero-cta, .lp-nav-cta, .lp-cta-btn').forEach(function(cta) {
                    cta.addEventListener('click', function(e) {
                        e.preventDefault();
                        if (navBtn) navBtn.click();
                    });
                });

                // ── Smooth scroll for all anchor links ──
                doc.querySelectorAll('a[href^="#"]').forEach(function(a) {
                    a.addEventListener('click', function(e) {
                        var id = a.getAttribute('href').slice(1);
                        var target = doc.getElementById(id);
                        if (target) {
                            e.preventDefault();
                            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        }
                    });
                });

                // ── Scroll-reveal animations ──
                var els = doc.querySelectorAll('.reveal');
                if (!els.length) { setTimeout(init, 200); return; }

                var obs = new IntersectionObserver(function(entries) {
                    entries.forEach(function(e) {
                        if (e.isIntersecting) {
                            e.target.classList.add('active');
                            obs.unobserve(e.target);
                        }
                    });
                }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

                els.forEach(function(el) { obs.observe(el); });
            } catch(e) {}
        }
        setTimeout(init, 400);
    })();
    </script>
    """, height=0)
