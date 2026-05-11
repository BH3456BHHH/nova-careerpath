"""CV history — save/load/diff a scan as a portable JSON file.

The user keeps their own data: after a scan they can download a tiny JSON
file, and on a future visit re-upload it to see a side-by-side comparison.
Nothing is stored server-side.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone

import streamlit as st

SCHEMA_VERSION = 1
APP_TAG = "nova-careerpath"


# ── serialize ────────────────────────────────────────────────────────────────

def build_save_payload(cv_result: dict, career_key: str) -> dict:
    """Pick a small, stable subset of the scan result for export."""
    if not cv_result:
        return {}

    def pick(d, *keys):
        return {k: d.get(k) for k in keys if k in d}

    impact  = cv_result.get("impact",  {}) or {}
    brevity = cv_result.get("brevity", {}) or {}
    style   = cv_result.get("style",   {}) or {}
    kw      = cv_result.get("keywords", {}) or {}

    return {
        "app"           : APP_TAG,
        "schema_version": SCHEMA_VERSION,
        "saved_at"      : datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "career_key"    : career_key,
        "overall_pct"   : cv_result.get("overall_pct"),
        "grade"         : cv_result.get("grade"),
        "word_count"    : cv_result.get("word_count"),
        "page_count"    : cv_result.get("page_count"),
        "impact"        : pick(impact, "score", "max"),
        "brevity"       : pick(brevity, "score", "max"),
        "style"         : pick(style, "score", "max"),
        "keywords"      : {
            "ratio"  : kw.get("ratio"),
            "found"  : kw.get("found")   or [],
            "missing": kw.get("missing") or [],
        },
        "raw_text"      : cv_result.get("raw_text", "") or "",
    }


def payload_to_json_bytes(payload: dict) -> bytes:
    return json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")


def default_filename(payload: dict) -> str:
    date = (payload.get("saved_at") or datetime.now(timezone.utc).isoformat())[:10]
    career = payload.get("career_key") or "scan"
    return f"nova-cv-{career}-{date}.json"


# ── parse / validate ─────────────────────────────────────────────────────────

def parse_uploaded_save(file) -> tuple[dict | None, str | None]:
    """Return (payload, error). Either payload is a dict or error is a str."""
    if file is None:
        return None, None
    try:
        raw = file.read()
        file.seek(0)
        data = json.loads(raw.decode("utf-8"))
    except Exception:
        return None, "This file is not a valid Nova CV save (couldn't read JSON)."

    if not isinstance(data, dict) or data.get("app") != APP_TAG:
        return None, "This file wasn't created by Nova CareerPath."

    if data.get("schema_version") != SCHEMA_VERSION:
        return None, "This save was created by a different version of the app."

    if "overall_pct" not in data:
        return None, "This save looks incomplete (missing scores)."

    return data, None


# ── diff helpers ─────────────────────────────────────────────────────────────

def _delta(new, old):
    if new is None or old is None:
        return None
    try:
        return round(float(new) - float(old), 1)
    except (TypeError, ValueError):
        return None


def _arrow(delta):
    if delta is None:
        return "·", "#94A3B8"
    if delta > 0:
        return f"▲ +{delta:g}", "#16A34A"
    if delta < 0:
        return f"▼ {delta:g}", "#EF4444"
    return "= 0", "#94A3B8"


def _tokenize_lines(text: str) -> list[str]:
    """Split CV text into bullet-ish lines for diffing."""
    if not text:
        return []
    lines = []
    for ln in text.splitlines():
        ln = re.sub(r"^[\s•·◦▪●○\-*]+", "", ln).strip()
        if len(ln) >= 3:
            lines.append(ln)
    return lines


def _line_diff(old_text: str, new_text: str, limit: int = 8):
    old_lines = _tokenize_lines(old_text)
    new_lines = _tokenize_lines(new_text)
    old_set, new_set = set(old_lines), set(new_lines)
    added   = [ln for ln in new_lines if ln not in old_set][:limit]
    removed = [ln for ln in old_lines if ln not in new_set][:limit]
    return added, removed


def compute_diff(old: dict, new_payload: dict) -> dict:
    return {
        "saved_at_old": old.get("saved_at", ""),
        "saved_at_new": new_payload.get("saved_at", ""),
        "career_old"  : old.get("career_key"),
        "career_new"  : new_payload.get("career_key"),
        "overall"     : _delta(new_payload.get("overall_pct"), old.get("overall_pct")),
        "impact"      : _delta(new_payload.get("impact",  {}).get("score"),
                               old.get("impact",  {}).get("score")),
        "brevity"     : _delta(new_payload.get("brevity", {}).get("score"),
                               old.get("brevity", {}).get("score")),
        "style"       : _delta(new_payload.get("style",   {}).get("score"),
                               old.get("style",   {}).get("score")),
        "kw_ratio"    : _delta(new_payload.get("keywords", {}).get("ratio"),
                               old.get("keywords", {}).get("ratio")),
        "new_keywords": sorted(set(new_payload.get("keywords", {}).get("found")   or [])
                               - set(old.get("keywords", {}).get("found") or [])),
        "lost_keywords": sorted(set(old.get("keywords", {}).get("found") or [])
                               - set(new_payload.get("keywords", {}).get("found") or [])),
        "added_lines"  : None,
        "removed_lines": None,
    }


# ── rendering ────────────────────────────────────────────────────────────────

def _fmt_date(iso: str) -> str:
    if not iso:
        return "—"
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%d %b %Y")
    except Exception:
        return iso[:10]


def render_comparison_panel(old: dict, new_cv_result: dict, new_career_key: str):
    """Render a side-by-side comparison card on the results page."""
    new_payload = build_save_payload(new_cv_result, new_career_key)
    diff = compute_diff(old, new_payload)
    added, removed = _line_diff(old.get("raw_text", ""), new_cv_result.get("raw_text", ""))

    overall_arrow, overall_color = _arrow(diff["overall"])
    imp_arrow,     imp_color     = _arrow(diff["impact"])
    brv_arrow,     brv_color     = _arrow(diff["brevity"])
    sty_arrow,     sty_color     = _arrow(diff["style"])

    career_note = ""
    if diff["career_old"] and diff["career_old"] != diff["career_new"]:
        career_note = (f'<div style="font-size:12px;color:#B45309;background:#FFFBEB;'
                       f'border:1px solid #FDE68A;border-radius:8px;padding:8px 12px;'
                       f'margin-top:8px;">'
                       f'Note: you were targeting <b>{diff["career_old"]}</b> last time, '
                       f'now <b>{diff["career_new"]}</b> — score differences may reflect '
                       f'that change.</div>')

    st.markdown(f"""
    <style>
    .nova-diff-card {{
      background:white;border-radius:16px;padding:24px 28px;
      border:1px solid #E4ECF4;box-shadow:0 2px 16px rgba(10,22,40,0.06);
      margin-bottom:20px;
    }}
    .nova-diff-head {{
      display:flex;align-items:center;justify-content:space-between;
      gap:12px;margin-bottom:14px;flex-wrap:wrap;
    }}
    .nova-diff-grid {{
      display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:12px;
    }}
    @media (max-width:640px) {{
      .nova-diff-card {{ padding:18px 18px; }}
      .nova-diff-grid {{ grid-template-columns:1fr; }}
      .nova-diff-head {{ flex-direction:column;align-items:flex-start;gap:6px; }}
    }}
    </style>
    <div class="nova-diff-card">
      <div class="nova-diff-head">
        <div>
          <div style="font-size:11px;font-weight:700;color:#1A56DB;letter-spacing:1.2px;
                      text-transform:uppercase;">Progress since last scan</div>
          <div style="font-size:13px;color:#6A8AA8;margin-top:4px;">
            {_fmt_date(diff['saved_at_old'])} &nbsp;→&nbsp; {_fmt_date(diff['saved_at_new'])}
          </div>
        </div>
        <div style="font-size:36px;font-weight:800;color:{overall_color};">{overall_arrow}</div>
      </div>

      <div class="nova-diff-grid">
        <div style="background:#F8FAFC;border-radius:10px;padding:12px 14px;">
          <div style="font-size:11px;color:#94A3B8;text-transform:uppercase;letter-spacing:0.8px;">Impact</div>
          <div style="font-size:20px;font-weight:800;color:{imp_color};margin-top:4px;">{imp_arrow}</div>
        </div>
        <div style="background:#F8FAFC;border-radius:10px;padding:12px 14px;">
          <div style="font-size:11px;color:#94A3B8;text-transform:uppercase;letter-spacing:0.8px;">Brevity</div>
          <div style="font-size:20px;font-weight:800;color:{brv_color};margin-top:4px;">{brv_arrow}</div>
        </div>
        <div style="background:#F8FAFC;border-radius:10px;padding:12px 14px;">
          <div style="font-size:11px;color:#94A3B8;text-transform:uppercase;letter-spacing:0.8px;">Style</div>
          <div style="font-size:20px;font-weight:800;color:{sty_color};margin-top:4px;">{sty_arrow}</div>
        </div>
      </div>
      {career_note}
    </div>
    """, unsafe_allow_html=True)

    new_kw  = diff["new_keywords"][:12]
    lost_kw = diff["lost_keywords"][:12]
    if new_kw or lost_kw:
        def _chips(words, color_bg, color_fg):
            return "".join(
                f'<span style="display:inline-block;background:{color_bg};color:{color_fg};'
                f'border-radius:999px;padding:4px 10px;font-size:12px;font-weight:600;'
                f'margin:2px 4px 2px 0;">{w}</span>' for w in words
            ) or '<span style="color:#94A3B8;font-size:12px;">—</span>'

        st.markdown(f"""
        <div style="background:white;border-radius:16px;padding:20px 24px;
                    border:1px solid #E4ECF4;box-shadow:0 2px 16px rgba(10,22,40,0.06);
                    margin-bottom:20px;">
          <div style="font-size:12px;font-weight:700;color:#0A1628;
                      text-transform:uppercase;letter-spacing:1px;margin-bottom:12px;">
            Keywords
          </div>
          <div style="font-size:12px;color:#16A34A;font-weight:700;margin:8px 0 6px;">NEW</div>
          <div>{_chips(new_kw, "#ECFDF5", "#16A34A")}</div>
          <div style="font-size:12px;color:#EF4444;font-weight:700;margin:14px 0 6px;">LOST</div>
          <div>{_chips(lost_kw, "#FEF2F2", "#B91C1C")}</div>
        </div>
        """, unsafe_allow_html=True)

    if added or removed:
        with st.expander("What changed in your CV text", expanded=False):
            cA, cR = st.columns(2)
            with cA:
                st.markdown('**New bullets / lines**')
                if added:
                    for ln in added:
                        st.markdown(f'- {ln}')
                else:
                    st.caption("—")
            with cR:
                st.markdown('**Removed lines**')
                if removed:
                    for ln in removed:
                        st.markdown(f'- {ln}')
                else:
                    st.caption("—")


def render_save_button(cv_result: dict, career_key: str, key: str = "save_scan"):
    """Render a download button that exports the current scan as JSON."""
    payload = build_save_payload(cv_result, career_key)
    if not payload:
        return
    st.download_button(
        label="💾 Save these results (for future comparison)",
        data=payload_to_json_bytes(payload),
        file_name=default_filename(payload),
        mime="application/json",
        use_container_width=True,
        key=key,
    )
