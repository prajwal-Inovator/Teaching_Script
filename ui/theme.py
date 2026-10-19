"""
Centralized visual theme for the TeachingScript Streamlit application.

Dark-first palette inspired by modern developer tools (charcoal surfaces,
indigo/violet accents). Injected once per page via ``inject_theme()``.
"""
from __future__ import annotations

import streamlit as st

APP_VERSION = "1.0.0"
APP_NAME = "TeachingScript"

# Design tokens
_COLORS = {
    "bg_base": "#0d1117",
    "bg_surface": "#161b22",
    "bg_elevated": "#1c2128",
    "border": "#30363d",
    "text_primary": "#e6edf3",
    "text_muted": "#8b949e",
    "accent": "#7c6cf0",
    "accent_soft": "rgba(124, 108, 240, 0.15)",
    "cyan": "#58a6ff",
    "success": "#3fb950",
    "warning": "#d29922",
    "error": "#f85149",
}

_CSS = f"""
<style>
    /* App shell */
    .stApp {{
        background: {_COLORS["bg_base"]};
        color: {_COLORS["text_primary"]};
    }}
    [data-testid="stHeader"] {{
        background: transparent;
    }}
    [data-testid="stSidebar"] {{
        background: {_COLORS["bg_surface"]};
        border-right: 1px solid {_COLORS["border"]};
    }}
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {{
        color: {_COLORS["text_primary"]};
    }}

    /* Typography */
    .ts-mark {{
        font-family: "Segoe UI", system-ui, sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
        font-size: 1.35rem;
        color: {_COLORS["text_primary"]};
    }}
    .ts-mark span {{
        color: {_COLORS["accent"]};
    }}
    .ts-tagline {{
        color: {_COLORS["text_muted"]};
        font-size: 0.9rem;
        margin-top: 0.15rem;
    }}
    .ts-status-pill {{
        display: inline-block;
        padding: 0.2rem 0.65rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid {_COLORS["border"]};
        background: {_COLORS["bg_elevated"]};
        color: {_COLORS["success"]};
    }}

    /* Cards */
    .ts-panel {{
        background: {_COLORS["bg_surface"]};
        border: 1px solid {_COLORS["border"]};
        border-radius: 10px;
        padding: 1rem 1.15rem;
        margin-bottom: 0.75rem;
    }}
    .ts-panel-title {{
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: {_COLORS["text_muted"]};
        margin-bottom: 0.5rem;
    }}

    /* Stage pipeline */
    .ts-stage {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.35rem 0;
        font-size: 0.85rem;
        color: {_COLORS["text_muted"]};
    }}
    .ts-stage.done {{ color: {_COLORS["text_primary"]}; }}
    .ts-stage.fail {{ color: {_COLORS["error"]}; }}
    .ts-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: {_COLORS["border"]};
        flex-shrink: 0;
    }}
    .ts-stage.done .ts-dot {{ background: {_COLORS["success"]}; }}
    .ts-stage.fail .ts-dot {{ background: {_COLORS["error"]}; }}
    .ts-stage.pending .ts-dot {{ background: {_COLORS["accent"]}; opacity: 0.5; }}

    /* Code editor area */
    textarea {{
        font-family: "Cascadia Code", "Consolas", "SF Mono", monospace !important;
        font-size: 0.88rem !important;
        line-height: 1.45 !important;
        background: {_COLORS["bg_elevated"]} !important;
        color: {_COLORS["text_primary"]} !important;
        border: 1px solid {_COLORS["border"]} !important;
        border-radius: 8px !important;
    }}

    /* Primary button emphasis */
    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, {_COLORS["accent"]}, #5b4fd6);
        border: none;
        font-weight: 600;
    }}
    .stButton > button[kind="primary"]:hover {{
        filter: brightness(1.08);
    }}

    /* Metrics */
    [data-testid="stMetricValue"] {{
        color: {_COLORS["cyan"]};
    }}

    /* Dataframes */
    [data-testid="stDataFrame"] {{
        border: 1px solid {_COLORS["border"]};
        border-radius: 8px;
        overflow: hidden;
    }}

    /* Hide default Streamlit footer clutter */
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
</style>
"""


def inject_theme() -> None:
    """Apply global CSS. Safe to call on every rerun."""
    st.markdown(_CSS, unsafe_allow_html=True)


def header_block(*, status: str = "Ready") -> None:
    """Render the application header."""
    inject_theme()
    st.markdown(
        f"""
        <div style="padding: 0.25rem 0 1rem 0; border-bottom: 1px solid {_COLORS["border"]}; margin-bottom: 1rem;">
            <div class="ts-mark">Teach<span>Script</span></div>
            <div class="ts-tagline">ANTLR-based DSL for machine-learning training and evaluation</div>
            <div style="margin-top: 0.65rem;">
                <span class="ts-status-pill">{status}</span>
                <span style="color: {_COLORS["text_muted"]}; font-size: 0.75rem; margin-left: 0.75rem;">
                    v{APP_VERSION} · ANTLR 4.13.2 · scikit-learn
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
