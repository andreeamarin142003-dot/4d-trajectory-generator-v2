# ─────────────────────────────────────────────────────────────────────────────
# app.py  —  Entry point & page router
# Run with:  streamlit run app.py
# ─────────────────────────────────────────────────────────────────────────────

import sys
import os

# Make sure sub-packages are importable
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st

# ── Page config (must be the very first Streamlit call) ──────────────────────
st.set_page_config(
    page_title="4D Trajectory Generator",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Load CSS ─────────────────────────────────────────────────────────────────
_css_path = os.path.join(os.path.dirname(__file__), "styles", "main.css")
with open(_css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Import pages ─────────────────────────────────────────────────────────────
from pages.home             import show as home
from pages.route            import show as route
from pages.preview          import show as preview
from pages.trajectory_page  import show as trajectory
from pages.vertical         import show as vertical

# ── Router ───────────────────────────────────────────────────────────────────
PAGE_MAP = {
    "home":       home,
    "route":      route,
    "preview":    preview,
    "trajectory": trajectory,
    "vertical":   vertical,
}

if "page" not in st.session_state:
    st.session_state["page"] = "home"

PAGE_MAP[st.session_state["page"]]()
